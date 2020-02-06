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
        ('data', 'BMS', (0,1,2,3,4)),
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
        self.state = 'WAIT FOR START'

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)

    '''
    OUTPUT_PYTHON format:

    Packet:
    [<ptype>, <rxtx>, <pdata>]

    This is the list of <ptype>s and their respective <pdata> values:
    - 'STARTBIT': The data is the (integer) value of the start bit (0/1).
    - 'DATA': This is always a tuple containing two items:
    - 1st item: the (integer) value of the UART data. Valid values
        range from 0 to 511 (as the data can be up to 9 bits in size).
    - 2nd item: the list of individual data bits and their ss/es numbers.
    - 'PARITYBIT': The data is the (integer) value of the parity bit (0/1).
    - 'STOPBIT': The data is the (integer) value of the stop bit (0 or 1).
    - 'INVALID STARTBIT': The data is the (integer) value of the start bit (0/1).
    - 'INVALID STOPBIT': The data is the (integer) value of the stop bit (0/1).
    - 'PARITY ERROR': The data is a tuple with two entries. The first one is
    the expected parity value, the second is the actual parity value.
    - 'BREAK': The data is always 0.
    - 'FRAME': The data is always a tuple containing two items: The (integer)
    value of the UART data, and a boolean which reflects the validity of the
    UART frame.
    '''
    def decode(self, ss, es, data):
        ptype, rxtx, pdata = data
        if ptype == 'FRAME':
            print(ptype, ss, es, pdata)
            value, valid = pdata
            if value == 0xdd:
                self.frame_start = es
                self.put(ss, es, self.out_ann, [0, ['Start Byte']])
            if value == 0x77:
               self.put(ss, es, self.out_ann, [4, ['Stop Byte']])
               self.frame_end = ss
               self.put(self.frame_start, self.frame_end, self.out_ann, [2, ['Content']])


