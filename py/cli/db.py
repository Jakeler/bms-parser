from py.protocol.parser import BmsPacket as bms

class DB:
    def __init__(self):
        from pymongo import MongoClient
        from pymongo.results import InsertOneResult
        from bson.objectid import ObjectId

        self.client = MongoClient('localhost', 27017)
        self.db = self.client['bms']
    
    def insert(self, pkt: bms):
        data = pkt.body.data
        if isinstance(data, bms.BasicInfo):
            col = 'info'
        if isinstance(data, bms.CellVoltages):
            col = 'cells'
        
        json = serialize(data)
        res: InsertOneResult = self.db[col].insert_one(json)
        id: ObjectId = res.inserted_id
        print(id.generation_time, 
            f'Mongo send {col} successful' if res.acknowledged else f'Mongo send {col} failed')
