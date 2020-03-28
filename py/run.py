import os, select, time, argparse
from kai import packet
from kai.packet import Packet
from converter import DB, pktToString

parser = argparse.ArgumentParser(description='Basic BMS readout')
parser.add_argument('dev', help='Serial Port')
parser.add_argument('-l', '--log', dest='logfile', help='Log to file')
parser.add_argument('-m', '--mongo', dest='mongo', help='Log to mongodb instance')
args = parser.parse_args()

intervall = 0.5

class Requests:
    basic = b'\xdd\xa5\x03\x00\xff\xfdw'
    cells = b'\xdd\xa5\x04\x00\xff\xfcw'
    hw = b'\xdd\xa5\x05\x00\xff\xfbw'

def parse(data: bytes) -> str:
    try:
        pkt = Packet.from_bytes(data)
        pktToString(pkt)
    except Exception as e:
        return f'Failed: {e}'


fd = os.open(args.dev, os.O_RDWR)
while True:
    os.write(fd, Requests.basic)
    r, w, e = select.select([fd], [], [], intervall)
    if fd in r:
        data = os.read(fd, 255)
        time.sleep(intervall/2)

        # print(data)
        res = parse(data)
        
        print(res)
        time.sleep(intervall/2)

os.close(fd)

