meta:
  id: cell_voltages
  endian: be

params:
  - id: data_len
    type: u1
    doc: Data size (used to determine cell count)

seq:
  - id: cells
    type: u2
    repeat: expr
    repeat-expr: count
    doc: Cell voltages in mV

instances:
  count:
    value: data_len / 2