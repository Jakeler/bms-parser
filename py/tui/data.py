from py.parser import BmsPacket
import os, select, time

class Serial:
    def __init__(self, path: str):
        self.fd = os.open(path, os.O_RDWR)

    def _request(self, req: bytes):
        os.write(self.fd, req)

        print(f'> Request: {req.hex()}')

        r, w, e = select.select([self.fd], [], [], 1.0)
        if self.fd in r:
            time.sleep(0.1)
            data = os.read(self.fd, 255)
            print(data)
            return data
        return None

    def request_info(self) -> bytes:
        return self._request(b'\xdd\xa5\x03\x00\xff\xfdw')

    def request_cells(self) -> bytes:
        return self._request(b'\xdd\xa5\x04\x00\xff\xfcw')

    def request_hw(self) -> bytes:
        return self._request(b'\xdd\xa5\x05\x00\xff\xfbw')


    def get_cells(self):
        raw = self.request_cells()
        pkt = BmsPacket.from_bytes(raw)
        # incoming = 'dd0400160fa70fa50fa10f980f9e0fa00fb10fbb0fb10fa60fa7f81877'
        # pkt = BmsPacket.from_bytes(bytes.fromhex(incoming))
        cells = [c.volt for c in pkt.body.data.cells]
        return cells

    def get_info(self):
        raw = self.request_info()
        pkt = BmsPacket.from_bytes(raw)
        # incoming = 'dd03001b1138006200a404b00000276e028200000000210e030b020b220b10fc4277'
        # pkt = BmsPacket.from_bytes(bytes.fromhex(incoming))
        # print(pktToString(pkt), '\n')
        i: BmsPacket.BasicInfo = pkt.body.data 
        table = [
            ('Pack Voltage', f'{i.pack_voltage.volt:.2f}', 'V'),
            ('Pack Current', f'{i.pack_current.amp:.2f}', 'A'),
            ('Typ Cap', f'{i.typ_cap.amp_hour:.3f}', 'Ah'),
            ('Remain Cap', f'{i.remain_cap.amp_hour:.3f}', 'Ah'),
            ('Remain Percent', f'{i.remain_cap_percent:.0f}', '%'),
            ('Cycle', f'{i.cycles:.0f}', 'Count'),
            # ('Balance', f'{i.balance_status.is_balancing}', 'bit'),
            # ('FET', f'CHG={i.fet_status.is_charge_enabled} DIS={i.fet_status.is_discharge_enabled}', 'bit'),
        ] + [
            ('Temp', f'{t.celsius:.2f}', '°C') 
            for t in i.temps
        ]
        balance = i.balance_status.is_balancing
        fet = {'chg': i.fet_status.is_charge_enabled, 'dis': i.fet_status.is_discharge_enabled}
        return (table, balance, fet)
