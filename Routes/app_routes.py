from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from helper.clientSetup import start_telethon_client

router = APIRouter()
@router.get("/", response_class=HTMLResponse)
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
            <p>Bot is actively listening for messages with registered hashtag</p>
        </body>
    </html>
    """

@router.get("/health")
async def health_check():
    client = await start_telethon_client()
    return {"status": "healthy", "bot_running": client is not None and client.is_connected()}