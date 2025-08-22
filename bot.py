import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application , MessageHandler , filters , ContextTypes
from telethon import TelegramClient , events , Button
from mssgStorage.storageHandler import add_messages , clear_messages , load_messages
import asyncio

#load environmental variables
load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_Token = os.getenv("BOT_TOKEN")
source_chat_id = int(os.getenv("SOURCE_CHAT_ID"))
dest_chat_id = int(os.getenv("DEST_CHAT_ID"))
HASHTAG = os.getenv("HASHTAG")

# async def forward_hashtag_messages ( update : Update , context : ContextTypes.DEFAULT_TYPE ) :
#     message = update.message
#     print("Update received:", message)   # <--- DEBUG

#     if not message or not message.text :
#         return
#     # ✅ Check if message is from source group and contains hashtag
#     if message.chat.id == source_chat_id and "#request" in message.text.lower() :
#         print("hashtag got")
#         await context.bot.forward_message (
#             chat_id= dest_chat_id ,
#             from_chat_id= message.chat.id,
#             message_id= message.message_id
#         )





# Telethon client using only bot token (api_id=0, api_hash='0')
client = TelegramClient('bot_session' , api_id= int(api_id) , api_hash= api_hash).start(bot_token=bot_Token) 
print("🔄 Setting up bot...")
@client.on(events.NewMessage(chats=source_chat_id))
async def handler(event) :
    print("📩 New message received in source group!")

    if not event.message or not event.message.text : #if there is no user sent message stop the event
        return 
    
    print(f"➡️ Incoming Message Text: {event.message.text}")

    if HASHTAG in event.message.text : #take event action if incoming message has the HASHTAG
        print(f"✅ Hashtag {HASHTAG} found! Forwarding...")
        try :
            #creating inline buttons for future admin actions
            buttons = [
                [Button.inline("✅ Approve" , b'approve'),Button.inline("❌ Reject", b'reject')]
            ]

            # Gathering all useful sender data

            incoming_msg = event.message
            sender = await event.get_sender()

            sender_name = (f'{sender.first_name} {sender.last_name}').replace('None','')
            sender_id = sender.id

            # Keep ready the formatted text to send and forward
            formatted_Text = (
                f'<b>{incoming_msg.text}\n\n</b>'
                f"<b>Sent By : \n</b>"
                f"<b>Name : <a href=\"tg://user?id={sender.id}\">{sender_name}</a></b>\n"
                f"<b>user_id : {sender_id}\n</b>" 
            )

            # event actions [ forward & send ]
            bot_fwd_res = await client.forward_messages(
                entity=  dest_chat_id ,
                messages=incoming_msg.id ,
                from_peer= source_chat_id,
            )
            bot_sent_res = await client.send_message(
                entity= dest_chat_id ,
                message= formatted_Text ,
                buttons= buttons,
                parse_mode= 'html'
            )
            #storing all incoming message data to storage file
            add_messages(bot_sent_res.id , incoming_msg.text , sender_id , sender_name)

            # print(f"sent forwarded request successfully : {bot_sent_res}") # <-- bot sending reponse debugging

        #error response
        except Exception as e :
            print("❌ Forward failed:", str(e))
    else :
        print(f"🚫 No {HASHTAG} in this message, skipped.")

@client.on(events.CallbackQuery)
async def callbackHandler(event) : 
    callback_triggered_msg = await event.get_message()
    print(callback_triggered_msg)
    print(f"The Callback triggered msg id : {callback_triggered_msg.id}")
    stored_message = load_messages()
    if callback_triggered_msg.id in stored_message : 
        #Gather the info to edit message
        original_target_message = stored_message[callback_triggered_msg.id]

        org_sent_text = original_target_message["original_text"]
        sender_id = original_target_message["sender_id"]
        sender_name = original_target_message["sender_name"]

        #format the message
        user_credits = (
                    f"<b>Sent By :</b>\n"
                    f"<b>Name : <a href=\"tg://user?id={sender_id}\">{sender_name}</a></b>\n"
                    f"<b>user_id : {sender_id}</b\n" 
                )

        if event.data == b"approve" : 
            approved_text = f'<b>✅{org_sent_text}</b>\n\n{user_credits}'
            await callback_triggered_msg.edit(
                text= approved_text ,
                parse_mode = 'html',
                buttons = [
                    Button.inline("✅ Approved",b'approved')
                ],

            ) 
        elif event.data == b"reject" : 
            rejected_text = f"❌<b><s>{org_sent_text}</s></b>\n\n{user_credits}"
            await callback_triggered_msg.edit(
                text= rejected_text,
                parse_mode = 'html',
                buttons = [
                    [Button.inline("❌ Rejected",b'rejected')]
                ],
            )
            await event.answer('📝Updated') 
    else:
        print('if part didnt execute')


        
# async def main():
    # app = Application.builder().token(bot_token).build()

    # # Listen to all messages, but filter inside handler

    # app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND , forward_hashtag_messages))
    # print("Bot is running")
    # app.run_polling()
    
async def schedule_cleanup() : 
    while True : 
        clear_messages()
        await asyncio.sleep(120)

if __name__ == "__main__":
    client.loop.create_task(schedule_cleanup())
    print("🤖 Bot is running... waiting for messages.")
    client.run_until_disconnected()