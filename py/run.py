import os, select, time, argparse
from kai import packet
from kai.packet import Packet

parser = argparse.ArgumentParser(description='Basic BMS readout')
parser.add_argument('dev', help='Serial Port')
args = parser.parse_args()

intervall = 1.0

class Requests:
    basic = b'\xdd\xa5\x03\x00\xff\xfdw'
    cells = b'\xdd\xa5\x04\x00\xff\xfcw'
    hw = b'\xdd\xa5\x05\x00\xff\xfbw'

def parse(data) -> str:
    try:
        pkt = Packet.from_bytes(data)
        res = f'Packet with {pkt.cmd}'

        if isinstance(pkt.body, Packet.ReadReq):
            res = f'Read request, ID {pkt.body.req_cmd}'
        elif isinstance(pkt.body, Packet.WriteReq):
            res = f'Write request, ID {pkt.body.req_cmd}'
        elif isinstance(pkt.body, Packet.Response):
            data = pkt.body.data
            res = f'Response {pkt.body.status.name}, Type {data.__class__.__name__}: '
            if isinstance(data, packet.BasicInfo):
                res += f'{data.total.volt} V, {data.current.amp} A, {data.remain_cap_percent} %, '
                res += f'{data.cell_count} Cells, {data.cycles} Cycles, T {[(str(t.celsius)+" °C") for t in data.temps]}'
            elif isinstance(data, packet.CellVoltages):
                res += ', '.join([(str(c.volt)+" V") for c in data.cells])
            elif isinstance(data, packet.Hardware):
                res += data.version
            elif isinstance(data, bytes):
                res += f'{data} ({int.from_bytes(data, byteorder="big")} = 0x{data.hex()})'
        
        
        return res
    except Exception as e:
        return f'Failed: {e}'


fd = os.open(args.dev, os.O_RDWR)
while True:
    os.write(fd, Requests.basic)
    r, w, e = select.select([fd], [], [], intervall)
    if fd in r:
        data = os.read(fd, 255)
        print(data)
        res = parse(data)
        print(res)
        time.sleep(intervall)

os.close(fd)

