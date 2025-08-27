from telethon import TelegramClient
import os 
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_Token = os.getenv("BOT_TOKEN")

async def start_telethon_client():
    """Initialize and start the Telethon client"""
    # global client
    client = TelegramClient('bot_session', api_id=int(api_id), api_hash=api_hash)
    await client.start(bot_token=bot_Token)
    print("🔄 Telethon client started successfully!")
    return client
