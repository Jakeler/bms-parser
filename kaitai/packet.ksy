meta:
  id: packet
  endian: be
  imports:
    - basic_info
    - cell_voltages
    - hardware
seq:
  - id: magic_start
    contents: [0xdd]
  - id: cmd
    type: u1
  - id: magic_status
    contents: [0x00]
  - id: data_len
    type: u1
  - id: data
    type:
      switch-on: cmd
      cases:
        0x03: basic_info
        0x04: cell_voltages
        0x05: hardware
    size: data_len
  - id: checksum
    size: 2
  - id: magic_end
    contents: [0x77]