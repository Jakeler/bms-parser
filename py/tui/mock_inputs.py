import random

info_hex: list[str] = [
    'dd03001b1138006200a404b00000276e028200000000210e030b020b220b10fc4277',
    'dd03001b14c1000003fb03fc0029276e0000000000002164030d020b200b11fb7777',
    'dd03001b14c2000003fb03fc0029276e0000000000002164030d020b200b11fb7677',
    'dd03001b14c1000003fb03fc0029276e0000000000002164030d020b200b11fb7777',
    'dd03001b14c2000003fb03fc0029276e0000000000002164030d020b200b11fb7677',
]


cell_hex: list[str] = [
    # 'dd0400160fa70fa50fa10f980f9e0fa00fb10fbb0fb10fa60fa7f81877',
    'dd04001a0ffa0ff80ff80ff80ff80ff60ff60ff50ff70ff20ffb0ffb0ff8f29177',
    'dd04001a0ffa0ff90ff80ff80ff80ff50ff60ff50ff70ff20ffb0ffb0ff8f29177',
    'dd04001a0ffb0ff90ff90ff80ff90ff50ff70ff50ff70ff20ffb0ffb0ff8f28d77',
    'dd04001a0ffb0ff90ff80ff80ff80ff60ff60ff50ff70ff20ffb0ffb0ff8f28f77',
    'dd04001a0ffa0ff80ff80ff80ff80ff60ff60ff60ff70ff20ffb0ffb0ff8f29077',
    'dd04001a0ffa0ff80ff80ff80ff90ff60ff60ff50ff70ff20ffb0ffb0ff8f29077',
    'dd04001a0ffb0ff90ff80ff80ff80ff50ff60ff60ff70ff20ffb0ffb0ff8f28f77',
    'dd04001a0ffa0ff90ff90ff80ff80ff50ff70ff50ff70ff20ffb0ffb0ff7f29077',
    'dd04001a0ffb0ff90ff90ff80ff90ff50ff60ff50ff70ff20ffb0ffb0ff8f28e77',
    'dd04001a0ffa0ff90ff90ff80ff80ff60ff60ff50ff70ff20ffb0ffb0ff8f28f77',
    'dd04001a0ffb0ff90ff90ff80ff80ff60ff60ff50ff70ff20ffc0ffb0ff8f28d77',
    'dd04001a0ffa0ff80ff90ff80ff80ff60ff70ff50ff70ff20ffb0ffb0ff8f28f77',
    'dd04001a0ffa0ff80ff90ff80ff80ff50ff60ff50ff70ff20ffb0ffb0ff8f29177',
    'dd04001a0ffb0ff90ff80ff80ff80ff60ff70ff50ff70ff20ffb0ffb0ff8f28e77',
    'dd04001a0ffb0ff90ff90ff80ff90ff60ff60ff50ff70ff20ffb0ffb0ff8f28d77',
    'dd04001a0ffb0ff90ff80ff80ff90ff60ff70ff50ff80ff20ffb0ffb0ff8f28c77',
    'dd04001a0ffb0ff90ff80ff80ff90ff60ff60ff50ff70ff20ffb0ffb0ff8f28e77',
    'dd04001a0ffb0ff90ff90ff80ff80ff50ff60ff50ff80ff20ffb0ffb0ff7f28f77',
    'dd04001a0ffb0ff80ff90ff80ff80ff50ff60ff50ff70ff20ffb0ffb0ff8f29077',
    'dd04001a0ffa0ff80ff80ff80ff80ff60ff60ff50ff70ff20ffb0ffb0ff7f29277',
    'dd04001a0ffa0ff90ff90ff80ff90ff50ff60ff50ff70ff20ffb0ffb0ff8f28f77',
    'dd04001a0ffb0ff90ff90ff80ff90ff60ff70ff50ff70ff20ffb0ffb0ff8f28c77',
    'dd04001a0ffb0ff90ff80ff80ff80ff60ff60ff50ff70ff20ffb0ffb0ff7f29077',
    'dd04001a0ffb0ff90ff90ff80ff80ff50ff60ff50ff70ff20ffb0ffb0ff8f28f77',
    'dd04001a0ffb0ff90ff90ff80ff80ff50ff60ff60ff70ff20ffb0ffb0ff8f28e77',
    'dd04001a0ffa0ff90ff90ff80ff80ff50ff60ff50ff70ff20ffb0ffb0ff8f29077',
    'dd04001a0ffa0ff90ff90ff80ff90ff50ff60ff50ff70ff20ffb0ffb0ff7f29077',
    'dd04001a0ffb0ff90ff90ff80ff80ff50ff70ff60ff70ff20ffb0ffb0ff7f28e77',
    'dd04001a0ffa0ff90ff80ff80ff80ff60ff60ff50ff70ff20ffb0ffb0ff7f29177',
    'dd04001a0ffb0ff90ff80ff80ff80ff50ff60ff50ff70ff20ffb0ffb0ff8f29077',
    'dd04001a0ffa0ff90ff80ff80ff80ff60ff60ff50ff70ff20ffb0ffb0ff8f29077',
    'dd04001a0ffa0ff90ff90ff80ff80ff50ff70ff50ff70ff20ffb0ffb0ff8f28f77',
    'dd04001a0ffb0ff80ff80ff80ff80ff60ff60ff50ff70ff20ffb0ffb0ff8f29077',
    'dd04001a0ffb0ff90ff80ff80ff90ff50ff70ff50ff70ff20ffb0ffb0ff8f28e77',
    'dd04001a0ffb0ff90ff80ff80ff90ff50ff60ff50ff70ff20ffb0ffb0ff8f28f77',
    'dd04001a0ffa0ff80ff80ff80ff80ff50ff60ff50ff70ff20ffb0ffb0ff8f29277',
    'dd04001a0ffa0ff90ff90ff80ff90ff50ff60ff60ff70ff20ffb0ffb0ff8f28e77',
    'dd04001a0ffa0ff90ff90ff80ff90ff60ff60ff50ff70ff20ffb0ffb0ff8f28e77',
]

fails: list[bytes] = [
    b'',
    b'\x00'
]

def get_response(category: str, failure_rate: float):
    if random.random() <= failure_rate:
        print('Injecting failed response')
        return random.choice(fails)

    db = {'info': info_hex, 'cell': cell_hex}
    raws = tuple(bytes.fromhex(resp) for resp in db[category])

    return random.choice(raws)
