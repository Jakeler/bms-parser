import inspect
from pprint import pp
from pymongo import MongoClient
from pymongo.results import InsertOneResult
import kai.packet as packet
from bson.objectid import ObjectId


class DB:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['bms']
    
    def insert(self, pkt: packet.Packet):
        data = pkt.body.data
        if isinstance(data, packet.BasicInfo):
            col = 'info'
        if isinstance(data, packet.CellVoltages):
            col = 'cells'
        
        json = serialize(data)
        res: InsertOneResult = self.db[col].insert_one(json)
        id: ObjectId = res.inserted_id
        print(id.generation_time, 
            f'Mongo send {col} successful' if res.acknowledged else f'Mongo send {col} failed')


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

def pktToString(pkt: packet.Packet):
    res = f'Packet with {pkt.cmd}'

    if isinstance(pkt.body, packet.Packet.ReadReq):
        res = f'Read request, ID {pkt.body.req_cmd}'
    elif isinstance(pkt.body, packet.Packet.WriteReq):
        res = f'Write request, ID {pkt.body.req_cmd}'
    elif isinstance(pkt.body, packet.Packet.Response):
        data = pkt.body.data
        res = f'Response {pkt.body.status.name}, Type {data.__class__.__name__}: '
        if isinstance(data, packet.BasicInfo):
            res += f'{data.total.volt} V, {data.current.amp} A, '
            res += f'{data.cell_count} Cells, {data.cycles} Cycles, T {[(str(t.celsius)+" °C") for t in data.temps]}\n'
            res += f"BAL {['B' if c else '-' for c in data.balance_status.flag[:]]} \n"
            res += f'{data.remain_cap_percent} %, {data.remain_cap.amp_hour} / {data.typ_cap.amp_hour} Ah\t'
            res += f'FET: CHG={data.fet_status.charge.name} DIS={data.fet_status.discharge.name}'
        elif isinstance(data, packet.CellVoltages):
            res += ', '.join([(str(c.volt)+" V") for c in data.cells])
        elif isinstance(data, packet.Hardware):
            res += data.version
        elif isinstance(data, bytes):
            res += f'{data} ({int.from_bytes(data, byteorder="big")} = 0x{data.hex()})'
    
    return res