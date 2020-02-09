# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

from .hardware import Hardware
from .cell_voltages import CellVoltages
from .basic_info import BasicInfo
class Packet(KaitaiStruct):

    class Status(Enum):
        ok = 0
        fail = 128
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic_start = self._io.ensure_fixed_contents(b"\xDD")
        self.cmd = self._io.read_u1()
        _on = self.cmd
        if _on == 165:
            self.body = self._root.ReadReq(self._io, self, self._root)
        elif _on == 90:
            self.body = self._root.WriteReq(self._io, self, self._root)
        else:
            self.body = self._root.Response(self.cmd, self._io, self, self._root)
        self.checksum = self._io.read_bytes(2)
        self.magic_end = self._io.ensure_fixed_contents(b"\x77")

    class ReadReq(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.req_cmd = self._io.read_u1()
            self.data_len = self._io.ensure_fixed_contents(b"\x00")


    class WriteReq(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.req_cmd = self._io.read_u1()
            self.data_len = self._io.read_u1()
            self.write_data = self._io.read_bytes(self.data_len)


    class Response(KaitaiStruct):
        def __init__(self, cmd, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.cmd = cmd
            self._read()

        def _read(self):
            self.status = self._root.Status(self._io.read_u1())
            self.data_len = self._io.read_u1()
            _on = self.cmd
            if _on == 3:
                self._raw_data = self._io.read_bytes(self.data_len)
                io = KaitaiStream(BytesIO(self._raw_data))
                self.data = BasicInfo(io)
            elif _on == 4:
                self._raw_data = self._io.read_bytes(self.data_len)
                io = KaitaiStream(BytesIO(self._raw_data))
                self.data = CellVoltages(io)
            elif _on == 5:
                self._raw_data = self._io.read_bytes(self.data_len)
                io = KaitaiStream(BytesIO(self._raw_data))
                self.data = Hardware(io)
            else:
                self.data = self._io.read_bytes(self.data_len)



