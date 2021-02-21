import os, select, time, argparse
from parser import BmsPacket
from kaitaistruct import KaitaiStructError
from converter import DB, pktToString

parser = argparse.ArgumentParser(description='Basic BMS readout')
parser.add_argument('dev', help='Serial Port')
parser.add_argument('-v', '--verbose', action='store_true', help='Print complete raw data')
parser.add_argument('-m', '--mongo', dest='mongo', help='Log to mongodb instance')
args = parser.parse_args()

intervall = 1.0

class Requests:
    basic = b'\xdd\xa5\x03\x00\xff\xfdw'
    cells = b'\xdd\xa5\x04\x00\xff\xfcw'
    hw = b'\xdd\xa5\x05\x00\xff\xfbw'

def parse(data: bytes) -> str:
    try:
        pkt = BmsPacket.from_bytes(data)

        if args.mongo:
            db.insert(pkt)
        
        return pktToString(pkt)

    # kaitai uses BaseException, which is not included in Exception...
    except (Exception, KaitaiStructError) as e:
        return f'Failed: {e}'

def requestData(req: bytes):
    os.write(fd, req)

    if args.verbose:
        print(f'> Request: {req.hex()}')
    else:
        print('Sending request')

    r, w, e = select.select([fd], [], [], intervall)
    if fd in r:
        time.sleep(0.1)
        data = os.read(fd, 255)

        if args.verbose:
            print(f'< Response: {data.hex()}')

        res = parse(data)
        print(res)


if __name__ == "__main__":
    fd = os.open(args.dev, os.O_RDWR)
    if args.mongo:
        db = DB()
    while True:
        requestData(Requests.basic)
        requestData(Requests.cells)
        time.sleep(intervall)

    os.close(fd)

