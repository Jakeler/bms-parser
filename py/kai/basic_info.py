# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class BasicInfo(KaitaiStruct):

    class FetBit(Enum):
        false = 0
        true = 1
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.total = self._root.Voltage(self._io, self, self._root)
        self.current = self._root.Current(self._io, self, self._root)
        self.remain_cap = self._root.Capacity(self._io, self, self._root)
        self.typ_cap = self._root.Capacity(self._io, self, self._root)
        self.cycles = self._io.read_u2be()
        self.prod_date = self._io.read_u2be()
        self.balance_status = self._root.BalanceList(self._io, self, self._root)
        self._raw_prot_status = self._io.read_bytes(2)
        io = KaitaiStream(BytesIO(self._raw_prot_status))
        self.prot_status = self._root.ProtList(io, self, self._root)
        self.software_version = self._io.read_u1()
        self.remain_cap_percent = self._io.read_u1()
        self._raw_fet_status = self._io.read_bytes(1)
        io = KaitaiStream(BytesIO(self._raw_fet_status))
        self.fet_status = self._root.FetBits(io, self, self._root)
        self.cell_count = self._io.read_u1()
        self.ntc_count = self._io.read_u1()
        self._raw_temps = [None] * (self.ntc_count)
        self.temps = [None] * (self.ntc_count)
        for i in range(self.ntc_count):
            self._raw_temps[i] = self._io.read_bytes(2)
            io = KaitaiStream(BytesIO(self._raw_temps[i]))
            self.temps[i] = self._root.Temp(io, self, self._root)


    class FetBits(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.charge = self._root.FetBit(self._io.read_bits_int(1))
            self.discharge = self._root.FetBit(self._io.read_bits_int(1))


    class ProtList(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ovp_cell = self._io.read_bits_int(1) != 0
            self.uvp_cell = self._io.read_bits_int(1) != 0
            self.ovp_pack = self._io.read_bits_int(1) != 0
            self.uvp_pack = self._io.read_bits_int(1) != 0
            self.otp_charge = self._io.read_bits_int(1) != 0
            self.utp_charge = self._io.read_bits_int(1) != 0
            self.otp_discharge = self._io.read_bits_int(1) != 0
            self.utp_discharge = self._io.read_bits_int(1) != 0
            self.ocp_charge = self._io.read_bits_int(1) != 0
            self.ocp_discharge = self._io.read_bits_int(1) != 0
            self.ocp_short = self._io.read_bits_int(1) != 0
            self.ic_error = self._io.read_bits_int(1) != 0
            self.fet_lock = self._io.read_bits_int(1) != 0


    class Temp(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.raw = self._io.read_u2be()

        @property
        def celsius(self):
            if hasattr(self, '_m_celsius'):
                return self._m_celsius if hasattr(self, '_m_celsius') else None

            self._m_celsius = ((self.raw * 0.1) - 273.1)
            return self._m_celsius if hasattr(self, '_m_celsius') else None


    class Current(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.raw = self._io.read_s2be()

        @property
        def amp(self):
            """Actual current (A)."""
            if hasattr(self, '_m_amp'):
                return self._m_amp if hasattr(self, '_m_amp') else None

            self._m_amp = (self.raw * 0.01)
            return self._m_amp if hasattr(self, '_m_amp') else None


    class Voltage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.raw = self._io.read_u2be()

        @property
        def volt(self):
            """Pack voltage (V)."""
            if hasattr(self, '_m_volt'):
                return self._m_volt if hasattr(self, '_m_volt') else None

            self._m_volt = (self.raw * 0.01)
            return self._m_volt if hasattr(self, '_m_volt') else None


    class BalanceList(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.flag = [None] * (32)
            for i in range(32):
                self.flag[i] = self._io.read_bits_int(1) != 0



    class Capacity(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.raw = self._io.read_u2be()

        @property
        def amp_hour(self):
            """Capacity (Ah)."""
            if hasattr(self, '_m_amp_hour'):
                return self._m_amp_hour if hasattr(self, '_m_amp_hour') else None

            self._m_amp_hour = (self.raw * 0.01)
            return self._m_amp_hour if hasattr(self, '_m_amp_hour') else None



