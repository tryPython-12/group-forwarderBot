from telegram import Update
from telegram.ext import Application,filters
import os
import asyncio
from dotenv import load_dotenv
from helper.forwarder import forward_hashtag_handler
from helper.callbackEditor import callBackHandler
from db_gen import mssg_collection

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")


def main() : 
    app =  Application.builder().token(bot_token).build()
    app.add_handler(forward_hashtag_handler)
    app.add_handler(callBackHandler)
    print("🤖 Bot running....")
    app.run_polling()

if __name__ == '__main__' : 
    asyncio.run(main())
