meta:
  id: battery_management_system_protocol
  title: Communication protocol of smart battery management systems from LLT power
  license: CC0-1.0
  ks-version: 0.8
  endian: be

doc: |
  Many modern general purpose BMS include a UART/Bluetooth based communication interface.
  After sending read requests they respond with various information's about the battery state in
  a custom binary format.

doc-ref: https://www.lithiumbatterypcb.com/Protocol%20English%20Version.rar

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

  basic_info:
    seq:
      - id: total
        type: voltage
      - id: current
        type: current
      - id: remain_cap
        type: capacity
      - id: typ_cap
        type: capacity
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
        size: 2
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
      - id: ntc_count
        type: u1
      - id: temps
        type: temp
        size: 2
        repeat: expr
        repeat-expr: ntc_count
    enums:
      fet_bit:
        0: off
        1: on
    types:
      balance_list:
        seq:
          - id: flag
            type: b1
            repeat: expr
            repeat-expr: 32
      prot_list:
        seq:
          - id: reserved
            type: b3
          - id: fet_lock
            type: b1
          - id: ic_error
            type: b1
          - id: ocp_short
            type: b1
          - id: ocp_discharge
            type: b1
          - id: ocp_charge
            type: b1
          - id: utp_discharge
            type: b1
          - id: otp_discharge
            type: b1
          - id: utp_charge
            type: b1
          - id: otp_charge
            type: b1
          - id: uvp_pack
            type: b1
          - id: ovp_pack
            type: b1
          - id: uvp_cell
            type: b1
          - id: ovp_cell
            type: b1
      fet_bits:
        seq:
          - id: reserved
            type: b6
          - id: discharge
            type: b1
            enum: fet_bit
          - id: charge
            type: b1
            enum: fet_bit
      voltage:
        seq:
          - id: raw
            type: u2
            doc: Pack voltage (raw)
        instances:
          volt:
            value: raw * 0.01
            doc: Pack voltage (V)
      capacity:
        seq:
          - id: raw
            type: u2
            doc: Capacity (raw)
        instances:
          amp_hour:
            value: raw * 0.01
            doc: Capacity (Ah)
      current:
        seq:
          - id: raw
            type: s2
            doc: Actual current (raw)
        instances:
          amp:
            value: raw * 0.01
            doc: Actual current (A)
      temp:
        seq:
          - id: raw
            type: u2
        instances:
          celsius:
            value: raw * 0.1 - 273.1

  cell_voltages:
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

  hardware:
    seq:
      - id: version
        type: str
        encoding: ascii
        size-eos: true
        doc: BMS model and version specification

  response:
    params:
      - id: cmd
        type: u1
    enums:
      status:
        0x00: ok
        0x80: fail
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
