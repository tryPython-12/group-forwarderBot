from mssgStorage.storageHandler import load_messages
from helper.forwarder import mssgForwarder
import os
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()
source_chat_id = int(os.getenv('SOURCE_CHAT_ID'))
dest_chat_id = int(os.getenv("DEST_CHAT_ID"))
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_Token = os.getenv("BOT_TOKEN")

async def catch_up(client) : 
    storedMsgDict = load_messages()
    lastMsgId = list(storedMsgDict.keys())[-1]
    print(f"🔎 Catching up messges from last message id : {lastMsgId}")
    source_entity = None
    dest_entity = None

    # fetch the entities through client dialogs
    dialogs = await client.get_dialogs()
    # find dest and source entity matching with the group ids of dialogs

    for dialog in dialogs : 
        if dialog.id == dest_chat_id : 
            dest_entity = dialog.entity
        elif dialog.id == source_chat_id : 
            source_entity = dialog.entity

    # get all pending messages
    if not source_entity or not dest_entity : 
        print(f"entity not found\ndest_enity : {dest_entity}\nsource_entity : {source_entity}")
        return
    
    botclient = TelegramClient('bot_session' , api_id= int(api_id) , api_hash= api_hash).start(bot_token=bot_Token) 
    async for msg in client.iter_messages(source_chat_id, min_id = lastMsgId , reverse = False,limit =2)  : 
        await mssgForwarder(msg,botclient,dest_entity=dest_entity , source_entity=source_entity)