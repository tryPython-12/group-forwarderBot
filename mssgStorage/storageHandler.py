import time
import os
from dotenv import load_dotenv
import pickle
from db_gen import mssg_collection
load_dotenv()

pickleFIleAddress = 'mssgStorage/msgStg.txt' 
expiryTime = 24 * 60 * 60 


def load_messages() : 
    if os.path.exists(pickleFIleAddress) : 
        with open(pickleFIleAddress,'rb') as f : 
            return pickle.load(f)
    return {}
def save_messages(messages) : 
    with open(pickleFIleAddress,'wb') as f :
        return pickle.dump(messages,f)

def add_messages(sent_msg_id , original_text, sender_id , sender_name) : 
    # messages = load_messages()
    # messages[sent_msg_id] = {
    #     "original_text" : original_text ,
    #     "sender_id" : sender_id ,
    #     "sender_name" : sender_name ,
    #     "timestamp" : time.time()
    # }
    newData = {
        "sent_msg_id" : sent_msg_id,
        "original_text" : original_text ,
        "sender_id" : sender_id ,
        "sender_name" : sender_name ,
        "timestamp" : time.time()
    }
    mssg_collection.insert_one(newData)
    # save_messages(messages)

def clear_messages () : 
    print('entered the cleanup module')
    # messages = load_messages()
    now = time.time()
    # messages = { k : v for k,v in messages.items() if ( now - v["timestamp"]) <= expiryTime }
    msgList = list(mssg_collection.find({}))
    for msgBody in msgList : 
        if(now - msgBody['timestamp']) >= expiryTime : 
            mssg_collection.delete_one({'timestamp' : msgBody['timestamp']})
            print(f"Message id {msgBody['sent_msg_id']} deleted")
    # save_messages(messages)