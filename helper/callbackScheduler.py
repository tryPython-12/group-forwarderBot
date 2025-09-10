from dotenv import load_dotenv
import os
from mssgStorage.storageHandler import load_messages
from telethon import Button
from db_gen import mssg_collection

load_dotenv()
admin_id = os.getenv("ADMIN_ID")

async def callbackHandler(event) : 
    callback_triggered_msg = await event.get_message()
    callback_sender = await event.get_sender()
    print('callback sent by id : ',callback_sender.id)
    print(f"The Callback triggered msg id : {callback_triggered_msg.id}")
    #fetch all messages from database
    target_org_mssg = mssg_collection.find_one({'sent_msg_to_id' : callback_triggered_msg.id})
    if callback_sender.id == int(admin_id) : 
        print("callback sent by admin")

        #Gather the info to edit message
        org_sent_text = target_org_mssg["original_text"]
        sender_id = target_org_mssg["sender_id"]
        sender_name = target_org_mssg["sender_name"]
        source_msg_link = target_org_mssg["source_msg_link"]

        #format the message
        user_credits = (
                    f"<b>Sent By :</b>\n"
                    f"<b>Name : <a href=\"tg://user?id={sender_id}\">{sender_name}</a></b>\n"
                    f"<b>user_id : {sender_id}</b\n" 
                )
        
        print(f"Event data : {event.data}") #<----Debugging
        if event.data == b"approve" : 
            approved_text = f'<b><i>🕑 Pending</i></b>\n\n<b>{org_sent_text}</b>\n\n{user_credits}'
            await callback_triggered_msg.edit(
                text= approved_text ,
                parse_mode = 'html',
                buttons = [
                    [Button.inline("✅ Upload",'upload'), Button.inline("❌ Cancel","cancel")],
                    [Button.url("🌐 Source Request Message", source_msg_link)]
                ]
            )
            await event.answer("✅ Request Approved",alert = True)
        elif event.data == b"reject" : 
            rejected_text = f"❌<b><s>{org_sent_text}</s></b>\n\n{user_credits}"
            await callback_triggered_msg.edit(
                text= rejected_text,
                parse_mode = 'html',
                buttons = [
                    [Button.inline("❌ Rejected",'rejected')],
                    [Button.inline("🌐 Source Request Message", source_msg_link)]
                ],
            )
            await event.answer('❌ Request Rejected',alert = True) 
        elif event.data == b'upload' : 
            approved_text = f'<b>✅ {org_sent_text}</b>\n\n{user_credits}'
            await callback_triggered_msg.edit(
                text= approved_text ,
                parse_mode = 'html',
                buttons = [
                    [Button.inline("✅ Uploaded",'uploaded')],
                    [Button.url("🌐 Source Request Message", source_msg_link)]
                ]
            )
            await event.answer("✅ Request Uploaded",alert = True)
        
        elif event.data == b'cancel' : 
            rejected_text = f"❌<b><s>{org_sent_text}</s></b>\n\n{user_credits}"
            await callback_triggered_msg.edit(
                text= rejected_text,
                parse_mode = 'html',
                buttons = [
                    [Button.inline("❌ Upload Cancelled",'cancelled')],
                    [Button.inline("🌐 Source Request Message", source_msg_link)]
                ],
            )
            await event.answer('❌ Uploaded Cancelled',alert = True)
        else : 
            return

    else : 
        print("callback sent by non-admin")
        await event.answer('🚫 You are a non-admin , Access Prohibited',alert = True)