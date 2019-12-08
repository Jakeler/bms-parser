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
  - id: data
    type: data_block
    size: data_len
  - id: checksum
    size: 2
  - id: magic_end
    contents: [0x77]


enums:
  status:
    0x00: ok
    0x80: fail
  fet_bit:
    0: off
    1: on

types:
  balance_list:
    seq:
      - id: flag
        type: b1
        repeat: expr
        repeat-expr: 4*8
  prot_list: # TODO: specify all bits...
    seq:
      - id: flag
        type: b1
        repeat: expr
        repeat-expr: 2*8
  fet_bits:
    seq:
      - id: charge
        type: b1
        enum: fet_bit
      - id: discharge
        type: b1
        enum: fet_bit
  data_block:
    seq:
      - id: total
        type: u2
        doc: Pack voltage (raw)
      - id: current
        type: u2
        doc: Actual current (raw)
      - id: remain_cap
        type: u2
        doc: Capacity (raw)
      - id: typ_cap
        type: u2
        doc: Capacity (raw)
      - id: cycles
        type: u2
        doc: Cycle times
      - id: prod_date
        type: u2
        doc: Production date
      - id: balance_status
        type: balance_list
        doc: List of balance bits
      - id: prot_status
        type: prot_list
        doc: List of protection bits
      - id: software_version
        type: u1
      - id: remain_cap_percent
        type: u1
        doc: Portion of remaining capacity
      - id: fet_status
        type: fet_bits
        size: 1
      - id: cell_count
        type: u1
      - id: temp_count
        type: u1
      - id: temp_value
        type: u2
        repeat: expr
        repeat-expr: temp_count
    

instances:
  total_v:
    value: data.total * 0.01
    doc: Pack voltage (V)
  current_a:
    value: data.current * 0.01
    doc: Actual current (A)
  remain_cap_ah:
    value: data.remain_cap * 0.01
    doc: Capacity (Ah)
  typ_cap_ah:
    value: data.typ_cap * 0.01
    doc: Capacity (Ah)
  # temp_celsius:
  #   value: temp_value * 0.1 - 273.1
  #   doc: Temperature of NTCs