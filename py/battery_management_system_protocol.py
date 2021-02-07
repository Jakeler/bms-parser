# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class BatteryManagementSystemProtocol(KaitaiStruct):
    """Many modern general purpose BMS include a UART/Bluetooth based communication interface.
    After sending read requests they respond with various information's about the battery state in
    a custom binary format.
    
    .. seealso::
       Source - https://www.lithiumbatterypcb.com/Protocol%20English%20Version.rar
    """

    class Commands(Enum):
        write = 90
        read = 165
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic_start = self._io.read_bytes(1)
        if not self.magic_start == b"\xDD":
            raise kaitaistruct.ValidationNotEqualError(b"\xDD", self.magic_start, self._io, u"/seq/0")
        self.cmd = self._io.read_u1()
        if self.ofs_body_start < 0:
            self._unnamed2 = self._io.read_bytes(0)

        _on = self.cmd
        if _on == BatteryManagementSystemProtocol.Commands.read.value:
            self.body = BatteryManagementSystemProtocol.ReadReq(self._io, self, self._root)
        elif _on == BatteryManagementSystemProtocol.Commands.write.value:
            self.body = BatteryManagementSystemProtocol.WriteReq(self._io, self, self._root)
        else:
            self.body = BatteryManagementSystemProtocol.Response(self.cmd, self._io, self, self._root)
        if self.ofs_body_end < 0:
            self._unnamed4 = self._io.read_bytes(0)

        self.checksum = self._io.read_u2be()
        self.magic_end = self._io.read_bytes(1)
        if not self.magic_end == b"\x77":
            raise kaitaistruct.ValidationNotEqualError(b"\x77", self.magic_end, self._io, u"/seq/6")

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
                self.cells.append(BatteryManagementSystemProtocol.CellVoltages.Voltage(self._io, self, self._root))
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
            self.data_len = self._io.read_bytes(1)
            if not self.data_len == b"\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x00", self.data_len, self._io, u"/types/read_req/seq/1")


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
            self.status = KaitaiStream.resolve_enum(BatteryManagementSystemProtocol.Response.Status, self._io.read_u1())
            self.data_len = self._io.read_u1()
            _on = self.cmd
            if _on == 3:
                self._raw_data = self._io.read_bytes(self.data_len)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = BatteryManagementSystemProtocol.BasicInfo(_io__raw_data, self, self._root)
            elif _on == 4:
                self._raw_data = self._io.read_bytes(self.data_len)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = BatteryManagementSystemProtocol.CellVoltages(_io__raw_data, self, self._root)
            elif _on == 5:
                self._raw_data = self._io.read_bytes(self.data_len)
                _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
                self.data = BatteryManagementSystemProtocol.Hardware(_io__raw_data, self, self._root)
            else:
                self.data = self._io.read_bytes(self.data_len)


    class BasicInfo(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.total = BatteryManagementSystemProtocol.BasicInfo.Voltage(self._io, self, self._root)
            self.current = BatteryManagementSystemProtocol.BasicInfo.Current(self._io, self, self._root)
            self.remain_cap = BatteryManagementSystemProtocol.BasicInfo.Capacity(self._io, self, self._root)
            self.typ_cap = BatteryManagementSystemProtocol.BasicInfo.Capacity(self._io, self, self._root)
            self.cycles = self._io.read_u2be()
            self.prod_date = self._io.read_u2be()
            self.balance_status = BatteryManagementSystemProtocol.BasicInfo.BalanceList(self._io, self, self._root)
            self.prot_status = BatteryManagementSystemProtocol.BasicInfo.ProtList(self._io, self, self._root)
            self.software_version = self._io.read_u1()
            self.remain_cap_percent = self._io.read_u1()
            self.fet_status = BatteryManagementSystemProtocol.BasicInfo.FetBits(self._io, self, self._root)
            self.cell_count = self._io.read_u1()
            self.ntc_count = self._io.read_u1()
            self._raw_temps = [None] * (self.ntc_count)
            self.temps = [None] * (self.ntc_count)
            for i in range(self.ntc_count):
                self._raw_temps[i] = self._io.read_bytes(2)
                _io__raw_temps = KaitaiStream(BytesIO(self._raw_temps[i]))
                self.temps[i] = BatteryManagementSystemProtocol.BasicInfo.Temp(_io__raw_temps, self, self._root)


        class FetBits(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.reserved = self._io.read_bits_int_be(6)
                self.is_discharge_enabled = self._io.read_bits_int_be(1) != 0
                self.is_charge_enabled = self._io.read_bits_int_be(1) != 0


        class ProtList(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.reserved = self._io.read_bits_int_be(3)
                self.is_fet_lock = self._io.read_bits_int_be(1) != 0
                self.is_ic_error = self._io.read_bits_int_be(1) != 0
                self.is_ocp_short = self._io.read_bits_int_be(1) != 0
                self.is_ocp_discharge = self._io.read_bits_int_be(1) != 0
                self.is_ocp_charge = self._io.read_bits_int_be(1) != 0
                self.is_utp_discharge = self._io.read_bits_int_be(1) != 0
                self.is_otp_discharge = self._io.read_bits_int_be(1) != 0
                self.is_utp_charge = self._io.read_bits_int_be(1) != 0
                self.is_otp_charge = self._io.read_bits_int_be(1) != 0
                self.is_uvp_pack = self._io.read_bits_int_be(1) != 0
                self.is_ovp_pack = self._io.read_bits_int_be(1) != 0
                self.is_uvp_cell = self._io.read_bits_int_be(1) != 0
                self.is_ovp_cell = self._io.read_bits_int_be(1) != 0


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
                self.is_balancing = [None] * (32)
                for i in range(32):
                    self.is_balancing[i] = self._io.read_bits_int_be(1) != 0



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


    @property
    def ofs_body_start(self):
        if hasattr(self, '_m_ofs_body_start'):
            return self._m_ofs_body_start if hasattr(self, '_m_ofs_body_start') else None

        self._m_ofs_body_start = self._io.pos()
        return self._m_ofs_body_start if hasattr(self, '_m_ofs_body_start') else None

    @property
    def ofs_body_end(self):
        if hasattr(self, '_m_ofs_body_end'):
            return self._m_ofs_body_end if hasattr(self, '_m_ofs_body_end') else None

        self._m_ofs_body_end = self._io.pos()
        return self._m_ofs_body_end if hasattr(self, '_m_ofs_body_end') else None

    @property
    def checksum_input(self):
        if hasattr(self, '_m_checksum_input'):
            return self._m_checksum_input if hasattr(self, '_m_checksum_input') else None

        _pos = self._io.pos()
        self._io.seek(self.ofs_body_start)
        self._m_checksum_input = self._io.read_bytes((self.ofs_body_end - self.ofs_body_start))
        self._io.seek(_pos)
        return self._m_checksum_input if hasattr(self, '_m_checksum_input') else None


