from basic_info import BasicInfo
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

d = BasicInfo.from_bytes(b"\xdd\x03\x00\x1b\x118\x00b\x00\xa4\x04\xb0\x00\x00'n\x02\x82\x00\x00" + b'\x00\x00!\x0e\x03\x0b\x02\x0b"\x0b\x10\xfcBw')
pp(recurse_vars(d))
pp(d._io._io)