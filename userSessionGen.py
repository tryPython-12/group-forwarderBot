from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import os
from dotenv import load_dotenv

load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone = "+919477049214"
password = "Filmsys@123"

client = TelegramClient("user_session" , api_hash= api_hash , api_id=api_id)
async def main():
    print("Connecting...")
    await client.connect()

    if not await client.is_user_authorized():
        print("Sending code request...")
        await client.send_code_request(phone)

        try:
            code = input("Enter the code you received: ")
            await client.sign_in(phone=phone, code=code)
        except SessionPasswordNeededError:
            # This means 2FA password is enabled
            password = input("Enter your 2FA password: ")
            await client.sign_in(password=password)

    print("Authorization successful!")

    # Example: print your own info
    me = await client.get_me()
    print(me.stringify())

with client:
    client.loop.run_until_complete(main())