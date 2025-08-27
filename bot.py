import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application , MessageHandler , filters , ContextTypes
from telethon import TelegramClient , events , Button
from mssgStorage.storageHandler import add_messages , clear_messages , load_messages
from helper.forwarder import mssgForwarder
from helper.callbackHandler import callbackHandler
from helper.msgStoreScheduler import schedule_cleanup
from helper.catchUpPending import catch_up
import asyncio

#load environmental variables
load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_Token = os.getenv("BOT_TOKEN")
admin_id = os.getenv("ADMIN_ID")
source_chat_id = int(os.getenv("SOURCE_CHAT_ID"))
dest_chat_id = int(os.getenv("DEST_CHAT_ID"))
HASHTAG = os.getenv("HASHTAG")




# Telethon client using only bot token (api_id=0, api_hash='0')
client = TelegramClient('bot_session' , api_id= int(api_id) , api_hash= api_hash).start(bot_token=bot_Token) 
print("🔄 Setting up bot...")


@client.on(events.NewMessage(chats=source_chat_id))
async def handler(event) : 
    await mssgForwarder(event.message,client,dest_entity=dest_chat_id ,source_entity=source_chat_id)

@client.on(events.CallbackQuery)
async def handler(event) : 
    await callbackHandler(event)


if __name__ == "__main__":
    # client.loop.create_task(init())
    client.loop.create_task(schedule_cleanup())
    print("🤖 Bot is running... waiting for messages.")
    client.run_until_disconnected()