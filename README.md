# BMS parser
Definitions for the generic smart battery managment system protocol. 
It is written [Kaitai Struct], which can used to export parsers in different langugages, some examples are in `py` for Python and `src` for Java/Kotlin. `py/main.py` allows logging to a file or MongoDB instance, see the parameters.

`dumps` contains DSView logic analyzer captures of the protocol. In `decoder/bms` includes a protocol decoder for DSView or sigrok Pulseview, you can try it out with the captures.

Read more about the protocol: https://blog.ja-ke.tech/2020/02/07/ltt-power-bms-chinese-protocol.html
