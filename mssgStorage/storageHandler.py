import time
import os
import pickle

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
    messages = load_messages()
    messages[sent_msg_id] = {
        "original_text" : original_text ,
        "sender_id" : sender_id ,
        "sender_name" : sender_name ,
        "timestamp" : time.time()
    }
    save_messages(messages)

def clear_messages () : 
    print('entered the cleanup module')
    messages = load_messages()
    now = time.time()
    messages = { k : v for k,v in messages.items() if ( now - v["timestamp"]) <= expiryTime }
    save_messages(messages)