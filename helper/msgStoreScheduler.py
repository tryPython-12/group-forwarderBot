import asyncio
from mssgStorage.storageHandler import clear_messages

async def schedule_cleanup():
    """Background task for cleanup"""
    while True:
        clear_messages()
        await asyncio.sleep(120)