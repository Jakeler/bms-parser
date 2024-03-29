from py.protocol.parser import BmsPacket as bms
import inspect

def isBasicType(obj: object):
    return type(obj) in (int, float, bool, str)

def serialize(obj: object) -> dict:
    """ Recursive from object to dict"""
    if isBasicType(obj):
        return obj

    out = {}
    for key, val in inspect.getmembers(obj):
        # Filter first
        if key.startswith('_'):
            continue
        if inspect.ismethod(val) or inspect.isclass(val):
            continue
        
        # Dump basic types
        if isBasicType(val):
            out[key] = val
        if type(val) == bytes:
            out[key] = val.hex()
        elif type(val) == list:
            out[key] = [serialize(i) for i in val]
        else:
            out[key] = serialize(val)
    return out

def pktToString(pkt: bms):
    state = 'Valid' if pkt.is_checksum_valid else 'INVALID!'
    res = f'{state} packet with command code {pkt.cmd}\n'

    if isinstance(pkt.body, bms.ReadReq):
        res += f'Read request, ID {pkt.body.req_cmd}'
    elif isinstance(pkt.body, bms.WriteReq):
        res += f'Write request, ID {pkt.body.req_cmd}'
    elif isinstance(pkt.body, bms.Response):
        data = pkt.body.data
        res += f'Response {pkt.body.status.name}, Type {data.__class__.__name__}: '
        if isinstance(data, bms.BasicInfo):
            res += f'{data.pack_voltage.volt} V, {data.pack_current.amp} A, '
            res += f'{data.cell_count} Cells, {data.cycles} Cycles, T {[(str(t.celsius)+" °C") for t in data.temps]}\n'
            res += f"BAL {['B' if c else '-' for c in data.balance_status.is_balancing[:]]} \n"
            res += f'{data.remain_cap_percent} %, {data.remain_cap.amp_hour} / {data.typ_cap.amp_hour} Ah\t'
            res += f'FET: CHG={data.fet_status.is_charge_enabled} DIS={data.fet_status.is_discharge_enabled}'
        elif isinstance(data, bms.CellVoltages):
            res += ', '.join([(f"{c.volt:.3f} V") for c in data.cells])
        elif isinstance(data, bms.Hardware):
            res += data.version
        elif isinstance(data, bytes):
            res += f'{data} ({int.from_bytes(data, byteorder="big")} = 0x{data.hex()})'
    
    return res
