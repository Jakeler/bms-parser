import time, argparse
from py.helper.data import Serial
from py.protocol.parser import BmsPacket
from py.helper.converter import pktToString

interval = 1.0

def parse_args():
    parser = argparse.ArgumentParser(description='Basic BMS readout')
    parser.add_argument('dev', help='Serial Port')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print complete raw data')
    parser.add_argument('-m', '--mongo', dest='mongo', help='Log to mongodb instance')
    return parser.parse_args()

def parse_packet(data: bytes, insert_db = False) -> str:
    try:
        pkt = BmsPacket.from_bytes(data)

        if insert_db:
            db.insert(pkt)

        return pktToString(pkt)

    except (Exception) as e:
        return f'Failed: {e}'


if __name__ == "__main__":
    args = parse_args()

    serial = Serial(args.dev, verbose=args.verbose)

    if args.mongo:
        from py.cli.db import DB
        db = DB()

    while True:
        res = parse_packet(serial.request_info())
        print(res)
        res = parse_packet(serial.request_cells())
        print(res)
        # parse_packet(serial.request_hw())
        time.sleep(interval)
