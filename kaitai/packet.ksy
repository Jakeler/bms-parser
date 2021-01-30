meta:
  id: packet
  imports:
    - basic_info
    - cell_voltages
    - hardware
  endian: be
seq:
  - id: magic_start
    contents: [0xdd]
  - id: cmd
    type: u1

  - id: body
    type:
      switch-on: cmd
      cases:
        0xa5: read_req
        0x5a: write_req
        _: response(cmd)
  
  - id: checksum
    size: 2
  - id: magic_end
    contents: [0x77]
  
enums:
  status:
    0x00: ok
    0x80: fail

types:
  read_req:
    seq:
      - id: req_cmd
        type: u1
        doc: Same value as cmd for response
      - id: data_len
        contents: [0x00]
  write_req:
    seq:
      - id: req_cmd
        type: u1
        doc: Same value as cmd for response
      - id: data_len
        type: u1
      - id: write_data
        size: data_len
  response:
    params:
      - id: cmd
        type: u1
    seq:
      - id: status
        type: u1
        enum: status
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
