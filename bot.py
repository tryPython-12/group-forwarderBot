import os
from dotenv import load_dotenv
from telethon import TelegramClient, events, Button
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio
from contextlib import asynccontextmanager
from mssgStorage.storageHandler import add_messages, clear_messages, load_messages

# Load environmental variables
load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_Token = os.getenv("BOT_TOKEN")
source_chat_id = int(os.getenv("SOURCE_CHAT_ID"))
dest_chat_id = int(os.getenv("DEST_CHAT_ID"))
HASHTAG = os.getenv("HASHTAG")

# Global client instance
client = None

async def start_telethon_client():
    """Initialize and start the Telethon client"""
    global client
    client = TelegramClient('bot_session', api_id=int(api_id), api_hash=api_hash)
    await client.start(bot_token=bot_Token)
    print("🔄 Telethon client started successfully!")
    return client

async def setup_telethon_handlers(client):
    """Setup all Telethon event handlers"""
    
    @client.on(events.NewMessage(chats=source_chat_id))
    async def handler(event):
        print("📩 New message received in source group!")

        if not event.message or not event.message.text:
            return

        print(f"➡️ Incoming Message Text: {event.message.text}")

        if HASHTAG in event.message.text:
            print(f"✅ Hashtag {HASHTAG} found! Forwarding...")
            try:
                buttons = [
                    [Button.inline("✅ Approve", b'approve'), Button.inline("❌ Reject", b'reject')]
                ]

                incoming_msg = event.message
                sender = await event.get_sender()

                sender_name = (f'{sender.first_name} {sender.last_name}').replace('None', '')
                sender_id = sender.id

                formatted_Text = (
                    f'<b>{incoming_msg.text}\n\n</b>'
                    f"<b>Sent By : \n</b>"
                    f"<b>Name : <a href=\"tg://user?id={sender.id}\">{sender_name}</a></b>\n"
                    f"<b>user_id : {sender_id}\n</b>"
                )

                bot_fwd_res = await client.forward_messages(
                    entity=dest_chat_id,
                    messages=incoming_msg.id,
                    from_peer=source_chat_id,
                )
                bot_sent_res = await client.send_message(
                    entity=dest_chat_id,
                    message=formatted_Text,
                    buttons=buttons,
                    parse_mode='html'
                )
                add_messages(bot_sent_res.id, incoming_msg.text, sender_id, sender_name)

            except Exception as e:
                print("❌ Forward failed:", str(e))
        else:
            print(f"🚫 No {HASHTAG} in this message, skipped.")

    @client.on(events.CallbackQuery)
    async def callbackHandler(event):
        callback_triggered_msg = await event.get_message()
        print(f"The Callback triggered msg id : {callback_triggered_msg.id}")
        stored_message = load_messages()
        
        if callback_triggered_msg.id in stored_message:
            original_target_message = stored_message[callback_triggered_msg.id]
            org_sent_text = original_target_message["original_text"]
            sender_id = original_target_message["sender_id"]
            sender_name = original_target_message["sender_name"]

            user_credits = (
                f"<b>Sent By :</b>\n"
                f"<b>Name : <a href=\"tg://user?id={sender_id}\">{sender_name}</a></b>\n"
                f"<b>user_id : {sender_id}</b>\n"
            )

            if event.data == b"approve":
                approved_text = f'<b>✅{org_sent_text}</b>\n\n{user_credits}'
                await callback_triggered_msg.edit(
                    text=approved_text,
                    parse_mode='html',
                    buttons=[
                        Button.inline("✅ Approved", b'approved')
                    ],
                )
            elif event.data == b"reject":
                rejected_text = f"❌<b><s>{org_sent_text}</s></b>\n\n{user_credits}"
                await callback_triggered_msg.edit(
                    text=rejected_text,
                    parse_mode='html',
                    buttons=[
                        [Button.inline("❌ Rejected", b'rejected')]
                    ],
                )
                await event.answer('📝Updated')

async def schedule_cleanup():
    """Background task for cleanup"""
    while True:
        clear_messages()
        await asyncio.sleep(120)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI"""
    # Startup
    print("🚀 Starting Telegram bot and web server...")
    telethon_client = await start_telethon_client()
    await setup_telethon_handlers(telethon_client)
    
    # Start background tasks
    asyncio.create_task(schedule_cleanup())
    
    yield
    
    # Shutdown
    print("🛑 Shutting down Telegram bot...")
    if client:
        await client.disconnect()

# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return f"""
    <html>
        <head>
            <title>Telegram Bot Server</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .status {{ color: green; font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1>🤖 Telegram Bot Server</h1>
            <p class="status">✅ Server is running</p>
            <p>Bot is actively listening for messages with hashtag: <strong>#{HASHTAG}</strong></p>
        </body>
    </html>
    """

@app.get("/health")
async def health_check():
    return {"status": "healthy", "bot_running": client is not None and client.is_connected()}

async def main():
    """Main async function to run both FastAPI and Telethon"""
    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8000,
        loop="asyncio"
    )
    server = uvicorn.Server(config)
    
    # Run the server
    await server.serve()

if __name__ == "__main__":
    # Use asyncio.run() to properly handle the event loop
    asyncio.run(main())
