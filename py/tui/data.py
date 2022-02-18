from parser import BmsPacket

def get_cells():
    incoming = 'dd0400160fa70fa50fa10f980f9e0fa00fb10fbb0fb10fa60fa7f81877'
    pkt = BmsPacket.from_bytes(bytes.fromhex(incoming))
    cells = [c.volt for c in pkt.body.data.cells]
    return cells
