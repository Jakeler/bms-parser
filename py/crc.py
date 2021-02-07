from battery_management_system_protocol import BatteryManagementSystemProtocol as bms
# from converter import pktToString

resp = [
        b'\xdd\xa5\x04\x00\xff\xfcw',
        b'\xdd\x04\x00\x16\x0f\xa7\x0f\xa5\x0f\xa1\x0f\x98\x0f\x9e\x0f\xa0\x0f\xb1\x0f\xbb' + b'\x0f\xb1\x0f\xa6\x0f\xa7\xf8\x18w',
        b'\xdd\xa5\x03\x00\xff\xfdw',
        b"\xdd\x03\x00\x1b\x118\x00b\x00\xa4\x04\xb0\x00\x00'n\x02\x82\x00\x00" + b'\x00\x00!\x0e\x03\x0b\x02\x0b"\x0b\x10\xfcBw',
        b'\xdd\xa5\x05\x00\xff\xfbw',
        b'\xdd\x05\x00\x11SP15S001-P13S-30' + b'A\xfb\xfdw'
    ]

def verify(packet):
    pkg = bms.from_bytes(packet)
    data =  pkg.checksum_input
    check = pkg.checksum

    print()
    # print(pktToString(pkg))

    crc=0x10000 - sum(data)

    print(f'Packet {packet.hex("_")} - CRC: {check} = {crc} -> {"OK" if check == crc else "FAIL"}')
    print('Checksum bytes:', crc.to_bytes(2, byteorder='big'))

for r in resp:
    verify(r)
