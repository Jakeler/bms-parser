##
## This file is part of the libsigrokdecode project.
##
## Copyright (C) 2015 Bart de Waal <bart@waalamo.com>
## Copyright (C) 2019 DreamSourceLab <support@dreamsourcelab.com>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, see <http://www.gnu.org/licenses/>.
##

import sigrokdecode as srd

from .lib.packet import Packet
from .lib import packet

class Decoder(srd.Decoder):
    api_version = 3
    id = 'bms'
    name = 'BMS'
    longname = 'Battery Managment System'
    desc = 'Chinese de facto standard for smart BMS with uart/bluetooth'
    license = 'gplv3+'
    inputs = ['uart']
    outputs = ['bms']
    tags = ['Embedded/industrial']
    annotations = (
        ('start', 'Start Byte'),
        ('len', 'Packet Length'),
        ('msg', 'Message'),
        ('crc', 'CRC 2 Bytes'),
        ('stop', 'Stop Byte'),
    )
    annotation_rows = (
        ('data', 'Packets', (0,1,2,3,4)),
    )
    options = (
        {'id': 'dir', 'desc': 'Direction', 'default': 'TX', 'values': ('TX', 'RX')},
    )

    def __init__(self):
        self.reset()

    def reset(self):
        self.samplenum = 0
        self.frame_start = -1
        self.frame_end = -1
        self.packet = [0xdd]
        self.state = 'WAIT FOR START'

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)


    def parse(self) -> str:
        try:
            print('Parsing', self.packet)
            pkt = Packet.from_bytes(bytes(self.packet))
            res = f'Packet with {pkt.cmd}'

            if isinstance(pkt.body, Packet.ReadReq):
                res = f'Read request, ID {pkt.body.req_cmd}'
            elif isinstance(pkt.body, Packet.WriteReq):
                res = f'Write request, ID {pkt.body.req_cmd}'
            elif isinstance(pkt.body, Packet.Response):
                data = pkt.body.data
                res = f'Response {pkt.body.status.name}, Type {data.__class__.__name__}: '
                if isinstance(data, packet.BasicInfo):
                    res += f'{data.total.volt} V, {data.current.amp} A, {data.remain_cap_percent} %, '
                    res += f'{data.cell_count} Cells, {data.cycles} Cycles, T {[(str(t.celsius)+" °C") for t in data.temps]}'
                elif isinstance(data, packet.CellVoltages):
                    res += ', '.join([(str(c.volt)+" V") for c in data.cells])
                elif isinstance(data, packet.Hardware):
                    res += data.version
                elif isinstance(data, bytes):
                    res += data.hex(' ')
            return res
        except Exception as e:
            return f'Failed: {e}'


    def decode(self, ss, es, data):
        ptype, rxtx, pdata = data
        if ptype == 'FRAME': # FRAME contains start/stop bit samples, oyterwise use DATA
            # print(ptype, ss, es, pdata)
            value, valid = pdata
            self.packet.append(value)

            if value == 0xdd:
                self.reset()
                self.frame_start = es
                self.put(ss, es, self.out_ann, [0, ['Start Byte']])
            elif value == 0x77:
                self.put(ss, es, self.out_ann, [4, ['Stop Byte']])
                self.frame_end = ss

                result = self.parse()
                self.put(self.frame_start, self.frame_end, self.out_ann, [2, [result]])




