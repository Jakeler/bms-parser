meta:
  id: basic_info
  endian: be
seq:
  - id: uuid
    size: 16
  - id: name
    type: str
    size: 24
    encoding: UTF-8
  - id: birth_year
    type: u2
  - id: weight
    type: f8
  - id: rating
    type: s4

 
