import inspect
from pprint import pp
from pymongo import MongoClient
from pymongo.results import InsertOneResult
import kai.packet as packet
from bson.objectid import ObjectId


class DB:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['bms']
    
    def insert(self, pkt: packet.Packet):
        data = pkt.body.data
        if isinstance(data, packet.BasicInfo):
            col = 'info'
        if isinstance(data, packet.CellVoltages):
            col = 'cells'
        
        json = serialize(data)
        res: InsertOneResult = self.db[col].insert_one(json)
        id: ObjectId = res.inserted_id
        print(id.generation_time, 
            f'Mongo send {col} successful' if res.acknowledged else f'Mongo send {col} failed')


def isBasicType(obj: object):
    return type(obj) in (int, float, bool, str)

def serialize(obj: object) -> dict:
    """ Recursive from object to dict"""
    if isBasicType(obj):
        return obj

    out = {}
    for key, val in inspect.getmembers(obj):
        # Filter first
        if key.startswith('_'):
            continue
        if inspect.ismethod(val) or inspect.isclass(val):
            continue
        
        # Dump basic types
        if isBasicType(val):
            out[key] = val
        if type(val) == bytes:
            out[key] = val.hex()
        elif type(val) == list:
            out[key] = [serialize(i) for i in val]
        else:
            out[key] = serialize(val)
    return out