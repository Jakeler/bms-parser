# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class BatteryManagementSystemProtocol(KaitaiStruct):
    """Many modern general purpose BMS include a UART/Bluetooth based communication interface.
    After sending read requests they respond with various information's about the battery state in
    a custom binary format.
    
    .. seealso::
       Source - https://www.lithiumbatterypcb.com/Protocol%20English%20Version.rar
    """
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

    class CellVoltages(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cells = []
            i = 0
            while not self._io.is_eof():
                self.cells.append(self._root.CellVoltages.Voltage(self._io, self, self._root))
                i += 1


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
                """Cell voltage (V)."""
                if hasattr(self, '_m_volt'):
                    return self._m_volt if hasattr(self, '_m_volt') else None

                self._m_volt = (self.raw * 0.001)
                return self._m_volt if hasattr(self, '_m_volt') else None



    class ReadReq(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.req_cmd = self._io.read_u1()
            self.data_len = self._io.ensure_fixed_contents(b"\x00")


    class Hardware(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.version = (self._io.read_bytes_full()).decode(u"ascii")


    class Response(KaitaiStruct):

        class Status(Enum):
            ok = 0
            fail = 128
        def __init__(self, cmd, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.cmd = cmd
            self._read()

        def _read(self):
            self.status = self._root.Response.Status(self._io.read_u1())
            self.data_len = self._io.read_u1()
            _on = self.cmd
            if _on == 3:
                self._raw_data = self._io.read_bytes(self.data_len)
                io = KaitaiStream(BytesIO(self._raw_data))
                self.data = self._root.BasicInfo(io, self, self._root)
            elif _on == 4:
                self._raw_data = self._io.read_bytes(self.data_len)
                io = KaitaiStream(BytesIO(self._raw_data))
                self.data = self._root.CellVoltages(io, self, self._root)
            elif _on == 5:
                self._raw_data = self._io.read_bytes(self.data_len)
                io = KaitaiStream(BytesIO(self._raw_data))
                self.data = self._root.Hardware(io, self, self._root)
            else:
                self.data = self._io.read_bytes(self.data_len)


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
            self.total = self._root.BasicInfo.Voltage(self._io, self, self._root)
            self.current = self._root.BasicInfo.Current(self._io, self, self._root)
            self.remain_cap = self._root.BasicInfo.Capacity(self._io, self, self._root)
            self.typ_cap = self._root.BasicInfo.Capacity(self._io, self, self._root)
            self.cycles = self._io.read_u2be()
            self.prod_date = self._io.read_u2be()
            self.balance_status = self._root.BasicInfo.BalanceList(self._io, self, self._root)
            self._raw_prot_status = self._io.read_bytes(2)
            io = KaitaiStream(BytesIO(self._raw_prot_status))
            self.prot_status = self._root.BasicInfo.ProtList(io, self, self._root)
            self.software_version = self._io.read_u1()
            self.remain_cap_percent = self._io.read_u1()
            self._raw_fet_status = self._io.read_bytes(1)
            io = KaitaiStream(BytesIO(self._raw_fet_status))
            self.fet_status = self._root.BasicInfo.FetBits(io, self, self._root)
            self.cell_count = self._io.read_u1()
            self.ntc_count = self._io.read_u1()
            self._raw_temps = [None] * (self.ntc_count)
            self.temps = [None] * (self.ntc_count)
            for i in range(self.ntc_count):
                self._raw_temps[i] = self._io.read_bytes(2)
                io = KaitaiStream(BytesIO(self._raw_temps[i]))
                self.temps[i] = self._root.BasicInfo.Temp(io, self, self._root)


        class FetBits(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.reserved = self._io.read_bits_int(6)
                self.discharge = self._root.BasicInfo.FetBit(self._io.read_bits_int(1))
                self.charge = self._root.BasicInfo.FetBit(self._io.read_bits_int(1))


        class ProtList(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.reserved = self._io.read_bits_int(3)
                self.fet_lock = self._io.read_bits_int(1) != 0
                self.ic_error = self._io.read_bits_int(1) != 0
                self.ocp_short = self._io.read_bits_int(1) != 0
                self.ocp_discharge = self._io.read_bits_int(1) != 0
                self.ocp_charge = self._io.read_bits_int(1) != 0
                self.utp_discharge = self._io.read_bits_int(1) != 0
                self.otp_discharge = self._io.read_bits_int(1) != 0
                self.utp_charge = self._io.read_bits_int(1) != 0
                self.otp_charge = self._io.read_bits_int(1) != 0
                self.uvp_pack = self._io.read_bits_int(1) != 0
                self.ovp_pack = self._io.read_bits_int(1) != 0
                self.uvp_cell = self._io.read_bits_int(1) != 0
                self.ovp_cell = self._io.read_bits_int(1) != 0


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



