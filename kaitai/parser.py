from packet import Packet
from pprint import pp, pprint

def recurse_vars(obj):
    out = vars(obj).copy()
    for key, val in vars(obj).items():
        if key.startswith('_'):
            del out[key]
            continue
        if not type(val).__module__ == 'builtins':
            out[key] = recurse_vars(val)
    return out

# Basic Info
d = Packet.from_bytes(b"\xdd\x03\x00\x1b\x118\x00b\x00\xa4\x04\xb0\x00\x00'n\x02\x82\x00\x00" + b'\x00\x00!\x0e\x03\x0b\x02\x0b"\x0b\x10\xfcBw')

pp(recurse_vars(d))

pp(d.data.total_v)
pp(d.data.current_a)
pp(d.data.remain_cap_ah)

# Cells
d2 = Packet.from_bytes(b'\xdd\x04\x00\x16\x0f\xa7\x0f\xa5\x0f\xa1\x0f\x98\x0f\x9e\x0f\xa0\x0f\xb1\x0f\xbb' + b'\x0f\xb1\x0f\xa6\x0f\xa7\xf8\x18w',)
pp(recurse_vars(d2))

# HW
d2 = Packet.from_bytes(b'\xdd\x05\x00\x11SP15S001-P13S-30' + b'A\xfb\xfdw')
pp(recurse_vars(d2))