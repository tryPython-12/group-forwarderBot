import os
from dotenv import load_dotenv
from telethon import  events
from fastapi import FastAPI
import uvicorn
import asyncio
from contextlib import asynccontextmanager
from mssgStorage.storageHandler import add_messages, clear_messages, load_messages
from helper.callbackScheduler import callbackHandler
from helper.msgStoreScheduler import schedule_cleanup
from helper.mssgSender import sender
from helper.clientSetup import start_telethon_client
from Routes import app_routes

# Load environmental variables
load_dotenv()

source_chat_id = int(os.getenv("SOURCE_CHAT_ID"))
dest_chat_id = int(os.getenv("DEST_CHAT_ID"))

# Global client instance
# client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI"""
    # Startup
    print("🚀 Starting Telegram bot and web server...")
    client = await start_telethon_client()

    """Setup all Telethon event handlers"""
    @client.on(events.NewMessage(chats=source_chat_id))
    async def handler(event):
        await sender(event.message , client , dest_entity = dest_chat_id)
    @client.on(events.CallbackQuery)
    async def handler(event) : 
        await callbackHandler(event)
    
    # Start background tasks
    asyncio.create_task(schedule_cleanup())
    
    yield
    
    # Shutdown
    print("🛑 Shutting down Telegram bot...")
    if client:
        await client.disconnect()

# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

#routes setup
app.include_router(app_routes.router)


async def main():
    """Main async function to run both FastAPI and Telethon"""
    
    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port = int(os.environ.get("PORT", 8000)),
        loop="asyncio"
    )
    server = uvicorn.Server(config)
    
    # Run the server
    await server.serve()

if __name__ == "__main__":
    # Use asyncio.run() to properly handle the event loop
    asyncio.run(main())
