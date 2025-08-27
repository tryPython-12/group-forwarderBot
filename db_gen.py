from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()


mongo_client = MongoClient(os.getenv('MONGO_URL'))

db = mongo_client['telegram_group_bot']
mssg_collection = db['message_info']

