from pymongo import MongoClient
from app.config import Config

client = MongoClient(Config.MONGO_URI)
db = client['vivanx_courier']

# Collections
admins_col = db['admins']
bookings_col = db['bookings']
tracking_col = db['tracking']
counter_col = db['awb_counter']

# Initialize AWB Counter if not exists
if counter_col.count_documents({"_id": "awb_sequence"}) == 0:
    counter_col.insert_one({"_id": "awb_sequence", "sequence_value": 0})
