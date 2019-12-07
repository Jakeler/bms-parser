meta:
  id: basic_info
  endian: be
seq:
  - id: magic_start
    contents: [0xdd]
  - id: magic_cmd
    contents: [0x03]
  - id: magic_status
    contents: [0x00]
  - id: data_len
    type: u1

enums:
    status:
      0x00: ok
      0x80: fail

 
