from battery_management_system_protocol import BatteryManagementSystemProtocol as bms

class BmsPacket(bms):

    @property
    def is_checksum_valid(self):
        expected_checksum = 0x10000 - sum(self.checksum_input)
        return self.checksum == expected_checksum