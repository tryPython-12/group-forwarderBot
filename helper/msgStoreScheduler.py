from mssgStorage.storageHandler import clear_messages
import asyncio

async def schedule_cleanup() : 
    while True : 
        clear_messages()
        await asyncio.sleep(20)