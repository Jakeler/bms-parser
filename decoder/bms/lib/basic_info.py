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
        self.total = self._io.read_u2be()
        self.current = self._io.read_u2be()
        self.remain_cap = self._io.read_u2be()
        self.typ_cap = self._io.read_u2be()
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
        self.temp_count = self._io.read_u1()
        self.temp_value = [None] * (self.temp_count)
        for i in range(self.temp_count):
            self.temp_value[i] = self._io.read_u2be()


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


    class FetBits(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.charge = self._root.FetBit(self._io.read_bits_int(1))
            self.discharge = self._root.FetBit(self._io.read_bits_int(1))


    @property
    def total_v(self):
        """Pack voltage (V)."""
        if hasattr(self, '_m_total_v'):
            return self._m_total_v if hasattr(self, '_m_total_v') else None

        self._m_total_v = (self.total * 0.01)
        return self._m_total_v if hasattr(self, '_m_total_v') else None

    @property
    def current_a(self):
        """Actual current (A)."""
        if hasattr(self, '_m_current_a'):
            return self._m_current_a if hasattr(self, '_m_current_a') else None

        self._m_current_a = (self.current * 0.01)
        return self._m_current_a if hasattr(self, '_m_current_a') else None

    @property
    def remain_cap_ah(self):
        """Capacity (Ah)."""
        if hasattr(self, '_m_remain_cap_ah'):
            return self._m_remain_cap_ah if hasattr(self, '_m_remain_cap_ah') else None

        self._m_remain_cap_ah = (self.remain_cap * 0.01)
        return self._m_remain_cap_ah if hasattr(self, '_m_remain_cap_ah') else None

    @property
    def typ_cap_ah(self):
        """Capacity (Ah)."""
        if hasattr(self, '_m_typ_cap_ah'):
            return self._m_typ_cap_ah if hasattr(self, '_m_typ_cap_ah') else None

        self._m_typ_cap_ah = (self.typ_cap * 0.01)
        return self._m_typ_cap_ah if hasattr(self, '_m_typ_cap_ah') else None


