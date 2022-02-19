from py.parser import BmsPacket

def get_cells():
    incoming = 'dd0400160fa70fa50fa10f980f9e0fa00fb10fbb0fb10fa60fa7f81877'
    pkt = BmsPacket.from_bytes(bytes.fromhex(incoming))
    cells = [c.volt for c in pkt.body.data.cells]
    return cells

def get_info():
    incoming = 'dd03001b1138006200a404b00000276e028200000000210e030b020b220b10fc4277'
    pkt = BmsPacket.from_bytes(bytes.fromhex(incoming))
    # print(pktToString(pkt), '\n')
    i: BmsPacket.BasicInfo = pkt.body.data 
    table = [
        ('Pack Voltage', f'{i.pack_voltage.volt:.2f}', 'V'),
        ('Pack Current', f'{i.pack_current.amp:.2f}', 'A'),
        ('Typ Cap', f'{i.typ_cap.amp_hour:.3f}', 'Ah'),
        ('Remain Cap', f'{i.remain_cap.amp_hour:.3f}', 'Ah'),
        ('Remain Percent', f'{i.remain_cap_percent:.0f}', '%'),
        ('Cycle', f'{i.cycles:.0f}', 'Count'),
        # ('Balance', f'{i.balance_status.is_balancing}', 'bit'),
        # ('FET', f'CHG={i.fet_status.is_charge_enabled} DIS={i.fet_status.is_discharge_enabled}', 'bit'),
    ] + [
        ('Temp', f'{t.celsius:.2f}', '°C') 
        for t in i.temps
    ]
    balance = i.balance_status.is_balancing
    fet = {'chg': i.fet_status.is_charge_enabled, 'dis': i.fet_status.is_discharge_enabled}
    return (table, balance, fet)