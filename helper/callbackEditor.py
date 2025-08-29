from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import MessageHandler , ContextTypes , filters,CallbackQueryHandler
from telegram.constants import ParseMode
import os
from dotenv import load_dotenv
from db_gen import mssg_collection

async def button_callback(update : Update , context : ContextTypes.DEFAULT_TYPE) : 
    query = update.callback_query

    [action , msg_id] = query.data.split(':')
    # convert id to a int 
    org_msg_id = int(msg_id)
    print(org_msg_id)
    org_sent_msg = mssg_collection.find_one({'sent_msg_id' : org_msg_id})

    #Gather the info to edit message

    org_sent_text = org_sent_msg["original_text"]
    sender_id = org_sent_msg["sender_id"]
    sender_name = org_sent_msg["sender_name"]
    user_credits = (
                        f"<b>Sent By :</b>\n"
                        f"<b>Name : <a href=\"tg://user?id={sender_id}\">{sender_name}</a></b>\n"
                        f"<b>user_id : {sender_id}</b>\n" 
                    )
    
    # bot editing logics
    if not org_msg_id : 
        return
    if action == 'accept' : 
        new_text = f'✅ {org_sent_text}\n\n{user_credits}'

        # edit the callback triggered message
        await query.edit_message_text(
            text= new_text ,
            reply_markup= InlineKeyboardMarkup(
                [[ InlineKeyboardButton(text='✅ Accepted',callback_data='accepted') ]]
            ),    
            parse_mode= ParseMode.HTML
        )
        await query.answer('✅ Request Accepted', show_alert=True)
    elif action == 'reject' : 
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