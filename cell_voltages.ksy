meta:
  id: cell_voltages
  endian: be
seq:
  - id: magic_start
    contents: [0xdd]
  - id: magic_cmd
    contents: [0x04]
  - id: magic_status
    contents: [0x00]
  - id: data_len
    type: u1
  - id: cells
    type: u2
    repeat: expr
    repeat-expr: count
    doc: Cell voltages in mV
  - id: checksum
    size: 2
  - id: magic_end
    contents: [0x77]

instances:
  count:
    value: data_len / 2