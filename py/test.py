from parser import BmsPacket
from pprint import pp
from converter import serialize, pktToString
import unittest

class TestBasicInfo(unittest.TestCase):

    def test_valid_pkt(self):
        incoming = 'dd03001b1138006200a404b00000276e028200000000210e030b020b220b10fc4277'
        pkt = BmsPacket.from_bytes(bytes.fromhex(incoming))
        print(pktToString(pkt), '\n')

        self.assertTrue(pkt.is_checksum_valid)
        self.assertEqual(pkt.cmd, 3)
        self.assertIsInstance(pkt.body.data, BmsPacket.BasicInfo)
        self.assertEqual(pkt.body.data.total.volt, 44.08)
        self.assertEqual(pkt.body.data.current.amp, 0.98)
        self.assertAlmostEqual(pkt.body.data.temps[0].celsius, 11.9)
        self.assertAlmostEqual(pkt.body.data.temps[1].celsius, 10.1)
        self.assertAlmostEqual(pkt.body.data.remain_cap.amp_hour, 1.64)
        self.assertEqual(pkt.body.data.balance_status.is_balancing, 
            [0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.assertEqual(pkt.body.data.fet_status.is_charge_enabled, True)
        self.assertEqual(pkt.body.data.fet_status.is_discharge_enabled, True)

    def test_valid_pkt_discharge(self):
        incoming = 'dd03001b103cfe0e02d704b00000276e000000000000213d030b020b370b47fb6977'
        pkt = BmsPacket.from_bytes(bytes.fromhex(incoming))
        print(pktToString(pkt), '\n')

        self.assertTrue(pkt.is_checksum_valid)
        self.assertEqual(pkt.cmd, 3)
        self.assertIsInstance(pkt.body.data, BmsPacket.BasicInfo)
        self.assertEqual(pkt.body.data.current.amp, -4.98)

    def test_wrong_checksum(self):
        incoming = 'dd03001b103cfe0e02d704b00000276e000000100000213d030b020b370b47fb6977'
        pkt = BmsPacket.from_bytes(bytes.fromhex(incoming))
        print(pktToString(pkt), '\n')

        self.assertFalse(pkt.is_checksum_valid)

class TestCells(unittest.TestCase):

    def test_valid_pkt(self):
        incoming = 'dd0400160fa70fa50fa10f980f9e0fa00fb10fbb0fb10fa60fa7f81877'
        pkt = BmsPacket.from_bytes(bytes.fromhex(incoming))
        cells = [c.volt for c in pkt.body.data.cells]
        print(pktToString(pkt), f'= SUM: {sum(cells):.2f} V', '\n')

        self.assertTrue(pkt.is_checksum_valid)
        self.assertEqual(pkt.cmd, 4)
        self.assertIsInstance(pkt.body.data, BmsPacket.CellVoltages)
        self.assertEqual(cells, [4.007, 4.005, 4.001, 3.992, 3.998, 4.000, 4.017, 4.027, 4.017, 4.006, 4.007])

class TestHardware(unittest.TestCase):

    def test_valid_pkt(self):
        incoming = 'dd05001153503135533030312d503133532d333041fbfd77'
        pkt = BmsPacket.from_bytes(bytes.fromhex(incoming))
        print(pktToString(pkt), '\n')

        self.assertTrue(pkt.is_checksum_valid)
        self.assertEqual(pkt.cmd, 5)
        self.assertIsInstance(pkt.body.data, BmsPacket.Hardware)
        self.assertEqual(pkt.body.data.version, 'SP15S001-P13S-30A')

class TestOtherSettings(unittest.TestCase):

    def test_cmd16(self):
        incoming = 'dd10000207d0ff2777'
        pkt = BmsPacket.from_bytes(bytes.fromhex(incoming))
        print(pktToString(pkt), '\n')

        self.assertTrue(pkt.is_checksum_valid)
        self.assertEqual(pkt.cmd, 16)
        self.assertIsInstance(pkt.body, BmsPacket.Response)
        self.assertEqual(pkt.body.data, bytes.fromhex('07d0'))

class TestRequests(unittest.TestCase):

    def test_read(self):
        incoming = 'dda50500fffb77'
        pkt = BmsPacket.from_bytes(bytes.fromhex(incoming))
        print(pktToString(pkt), '\n')

        self.assertTrue(pkt.is_checksum_valid)
        self.assertEqual(pkt.body.req_cmd, 5)
        self.assertIsInstance(pkt.body, BmsPacket.ReadReq)
        self.assertEqual(pkt.body.data_len, bytes.fromhex('00'))

    def test_write(self):
        incoming = 'dd5a10024e20ff8077'
        pkt = BmsPacket.from_bytes(bytes.fromhex(incoming))
        print(pktToString(pkt), '\n')

        self.assertTrue(pkt.is_checksum_valid)
        self.assertEqual(pkt.body.req_cmd, 16)
        self.assertIsInstance(pkt.body, BmsPacket.WriteReq)
        self.assertEqual(pkt.body.data_len, 2)
        self.assertEqual(pkt.body.write_data, bytes.fromhex('4e20'))


if __name__ == '__main__':
    unittest.main()
