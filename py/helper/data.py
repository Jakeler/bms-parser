import serial
from py.protocol.parser import BmsPacket
from py.protocol import mock_inputs

END_BYTE = b'\x77'

class Serial:
    def __init__(self, path: str, verbose: bool = False,
                 use_mock: bool = False, mock_fail_rate: float = 0.05):
        if not use_mock:
            self.pyserial = serial.Serial(path, timeout=1.0)
        self.verbose = verbose
        self.use_mock = use_mock
        self.mock_fail_rate = mock_fail_rate

    def _request(self, req: bytes):
        self.pyserial.write(req)
        if self.verbose:
            print(f'> Request: {req.hex()}')

        data = self.pyserial.read_until(expected=END_BYTE) # waits for a full packet with global timeout (1.0 sec)
        data += self.pyserial.read_all() # empty the buffer
        if self.verbose:
            print(f'< Response: {data.hex()}')
        return data

    def request_info(self) -> bytes:
        if self.use_mock:
            return mock_inputs.get_response('info', self.mock_fail_rate)
        return self._request(b'\xdd\xa5\x03\x00\xff\xfdw')

    def request_cells(self) -> bytes:
        if self.use_mock:
            return mock_inputs.get_response('cell', self.mock_fail_rate)
        return self._request(b'\xdd\xa5\x04\x00\xff\xfcw')

    def request_hw(self) -> bytes:
        return self._request(b'\xdd\xa5\x05\x00\xff\xfbw')


    def get_cells(self) -> list[float]:
        raw = self.request_cells()
        pkt = BmsPacket.from_bytes(raw)

        cells = [c.volt for c in pkt.body.data.cells]
        return cells

    def get_info(self) -> tuple[list[tuple[str, str, str]], list[bool], dict[str, bool]]:
        raw = self.request_info()
        pkt = BmsPacket.from_bytes(raw)

        i: BmsPacket.BasicInfo = pkt.body.data 
        table = [
            ('Pack Voltage', f'{i.pack_voltage.volt:.2f}', 'V'),
            ('Cell', f'{i.cell_count}', 'count'),
            ('Pack Current', f'{i.pack_current.amp:.2f}', 'A'),
            ('Typ Cap', f'{i.typ_cap.amp_hour:.3f}', 'Ah'),
            ('Remain Cap', f'{i.remain_cap.amp_hour:.3f}', 'Ah'),
            ('Remain Percent', f'{i.remain_cap_percent}', '%'),
            ('Cycle', f'{i.cycles:.0f}', 'count'),
            # ('Balance', f'{i.balance_status.is_balancing}', 'bit'),
            # ('FET', f'CHG={i.fet_status.is_charge_enabled} DIS={i.fet_status.is_discharge_enabled}', 'bit'),
        ] + [
            ('Temp', f'{t.celsius:.2f}', '°C') 
            for t in i.temps
        ]
        balance = i.balance_status.is_balancing
        fet = {
            'charge enabled': i.fet_status.is_charge_enabled, 
            'discharge enabled': i.fet_status.is_discharge_enabled,
        }
        prot_all = vars(i.prot_status)
        prot = {k: v for k, v in prot_all.items() if not k.startswith('_')}
        return (table, balance, fet, prot)
