meta:
  id: cell_voltages
  endian: be

seq:
  - id: cells
    type: voltage
    repeat: eos

types:
  voltage:
    seq:
      - id: raw
        type: u2
        doc: Cell voltage (raw)
    instances:
      volt:
        value: raw * 0.001
        doc: Cell voltage (V)
