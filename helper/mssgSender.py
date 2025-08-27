from mssgStorage.storageHandler import add_messages
from telethon import Button

from dotenv import load_dotenv
import os

load_dotenv()

HASHTAG = os.getenv("HASHTAG")

async def sender(msg,client,dest_entity) : 
    print("📩 New message received in source group!")

    if not  msg or not  msg.text : #if there is no user sent message stop the event
        return 
    
    print(f"➡️ Incoming Message Text: { msg.text}")

    if HASHTAG in  msg.text : #take event action if incoming message has the HASHTAG
        print(f"✅ Hashtag {HASHTAG} found! Forwarding...")
        try :
            #creating inline buttons for future admin actions
            buttons = [
                [Button.inline("✅ Approve" , b'approve'),Button.inline("❌ Reject", b'reject')]
            ]

            # Gathering all useful sender data

            incoming_msg =  msg
            sender = await  msg.get_sender()

            sender_name = (f'{sender.first_name} {sender.last_name}').replace('None','')
            sender_id = sender.id

            # Keep ready the formatted text to send and forward
            formatted_Text = (
                f'<b>{incoming_msg.text}\n\n</b>'
                f"<b>Sent By : \n</b>"
                f"<b>Name : <a href=\"tg://user?id={sender.id}\">{sender_name}</a></b>\n"
                f"<b>user_id : {sender_id}\n</b>" 
            )

            # # event actions [ forward & send ]
            # bot_fwd_res = await client.forward_messages(
            #     entity=  dest_entity ,
            #     messages=incoming_msg.id ,
            #     from_peer= source_entity,
            # )
            
            bot_sent_res = await client.send_message(
                entity= dest_entity ,
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