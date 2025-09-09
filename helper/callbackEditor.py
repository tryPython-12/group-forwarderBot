from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import MessageHandler , ContextTypes , filters,CallbackQueryHandler
from telegram.constants import ParseMode
import os
from dotenv import load_dotenv
from db_gen import mssg_collection

async def button_callback(update : Update , context : ContextTypes.DEFAULT_TYPE) : 
    query = update.callback_query

    # <-------Degubgging------>
    print(f"callback coming from message id : {query.message.message_id}",type(query.message.message_id))
    print(f"Callback data: {query.data}")
    # [action , msg_id] = query.data.split(':')
    # # convert id to a int 
    query_msg_id= query.message.message_id
    # print(org_msg_id)
    org_sent_msg = mssg_collection.find_one({'sent_msg_to_id' : query_msg_id})
    # <----debugging---->
    print(f"Original sent message : {org_sent_msg}")


    # #Gather the info to edit message

    org_sent_text = org_sent_msg["original_text"]
    sender_id = org_sent_msg["sender_id"]
    sender_name = org_sent_msg["sender_name"]
    user_credits = (
                        f"<b>Sent By :</b>\n"
                        f"<b>Name : <a href=\"tg://user?id={sender_id}\">{sender_name}</a></b>\n"
                        f"<b>user_id : {sender_id}</b>\n" 
                    )
    
    # # bot editing logics
    # if not org_msg_id : 
    #     return
    if query.data == 'approve' : 
        new_text = f'✅ {org_sent_text}\n\n{user_credits}'

        # edit the callback triggered message
        await query.edit_message_text(
            text= new_text ,
            reply_markup= InlineKeyboardMarkup(
                [
                    [ 
                        InlineKeyboardButton(text='✅ Upload',callback_data='accepted'),
                        InlineKeyboardButton(text='❌ Reject', callback_data='Rejected')
                    ]
                ]
            ),    
            parse_mode= ParseMode.HTML
        )
        await query.answer('✅ Request Accepted', show_alert=True)
    elif query.data == 'reject' : 
        new_text = f'❌ <s>{org_sent_text}</s>\n\n{user_credits}'

        # edit the callback triggered message
        await query.edit_message_text(
        text= new_text ,
        reply_markup = InlineKeyboardMarkup(
            [[ InlineKeyboardButton(text='❌ Rejected',callback_data='rejected')]]
        ) ,
        parse_mode= ParseMode.HTML
        )
        await query.answer('❌ Request Denied', show_alert= True)

callBackHandler = CallbackQueryHandler(button_callback)