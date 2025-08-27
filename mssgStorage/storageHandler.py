import time
import os
import pickle
from pymongo import MongoClient
pickleFIleAddress = 'mssgStorage/msgStg.txt' 
expiryTime = 120
# Create mongo client setup

mongo_clilent = MongoClient("mongodb+srv://tanmoy576halder:zrfjrAO810XpIqLn@cluster0.i4iqow6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo_clilent['telegram_group_Data']
mssg_collection = db['message_info']
# mssg_collection.delete_one({'id' : 2})

def load_messages() : 
    if os.path.exists(pickleFIleAddress) : 
        with open(pickleFIleAddress,'rb') as f : 
            return pickle.load(f)
    return {}
def save_messages(messages) : 
    with open(pickleFIleAddress,'wb') as f :
        return pickle.dump(messages,f)

def add_messages(sent_msg_id , original_text, sender_id , sender_name) : 
    messages = load_messages()
    messages[sent_msg_id] = {
        "original_text" : original_text ,
        "sender_id" : sender_id ,
        "sender_name" : sender_name ,
        "timestamp" : time.time()
    }
    newData = {
        "sent_msg_d" : sent_msg_id,
        "original_text" : original_text ,
        "sender_id" : sender_id ,
        "sender_name" : sender_name ,
        "timestamp" : time.time()
    }
    mssg_collection.insert_one(newData)
    save_messages(messages)

def clear_messages () : 
    print('entered the cleanup module')
    messages = load_messages()
    now = time.time()
    messages = { k : v for k,v in messages.items() if ( now - v["timestamp"]) <= expiryTime }
    d2 = list(mssg_collection.find({}))
    for msgdict in d2 : 
        if(now - msgdict['timestamp']) >= expiryTime : 
            mssg_collection.delete_one({'timestamp' : msgdict['timestamp']})
            print(f"Message id {msgdict['sent_msg_d']} deleted")

    save_messages(messages)