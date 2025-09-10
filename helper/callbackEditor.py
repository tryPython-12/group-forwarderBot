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
    source_msg_link = org_sent_msg['source_msg_link']
    user_credits = (
                        f"<b>Sent By :</b>\n"
                        f"<b>Name : <a href=\"tg://user?id={sender_id}\">{sender_name}</a></b>\n"
                        f"<b>user_id : {sender_id}</b>\n" 
                    )
    
    # # bot editing logics
    # if not org_msg_id : 
    #     return


    if query.data == 'approve' : 
        new_text = f'<b><i>🕑 Pending</i></b>\n\n<b>{org_sent_text}</b>\n\n{user_credits}'

        # edit the callback triggered message
        await query.edit_message_text(
            text= new_text ,
            reply_markup= InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text='✅ Upload',callback_data='upload'),
                        InlineKeyboardButton(text='❌ Cancel', callback_data='cancel')
                    ],
                    [
                        InlineKeyboardButton(text= '🌐 Source Request Message' , url=source_msg_link)
                    ]
                ]
            ),    
            parse_mode= ParseMode.HTML
        )
        await query.answer('✅ Request Approved', show_alert=True)
    elif query.data == 'reject' : 
        new_text = f'❌ <s><b>{org_sent_text}</b></s>\n\n{user_credits}'

        # edit the callback triggered message
        await query.edit_message_text(
        text= new_text ,
        reply_markup = InlineKeyboardMarkup(
            [
                [ InlineKeyboardButton(text='❌ Rejected',callback_data='rejected')],
                [InlineKeyboardButton(text='🌐 Source Request Message' , url=source_msg_link)]
            ]
        ) ,
        parse_mode= ParseMode.HTML
        )
        await query.answer('❌ Request Rejected', show_alert= True)
    
    elif query.data == 'upload' : 
        new_text = f'<b>✅ {org_sent_text}</b>\n\n{user_credits}'

        # edit the callback triggered message
        await query.edit_message_text(
            text= new_text ,
            reply_markup= InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text='✅ Uploaded',callback_data='uploaded'),
                    ],
                    [
                        InlineKeyboardButton(text= '🌐 Source Request Message' , url=source_msg_link)
                    ]
                ]
            ),    
            parse_mode= ParseMode.HTML
        )
        await query.answer('✅ Request Uploaded', show_alert=True)
    elif query.data == 'cancel' : 
        new_text = f'❌ <s><b>{org_sent_text}</b></s>\n\n{user_credits}'

        # edit the callback triggered message
        await query.edit_message_text(
        text= new_text ,
        reply_markup = InlineKeyboardMarkup(
            [
                [ InlineKeyboardButton(text='❌ Upload Cancelled',callback_data='cancelled')],
                [InlineKeyboardButton(text='🌐 Source Request Message' , url=source_msg_link)]
            ]
        ) ,
        parse_mode= ParseMode.HTML
        )
        await query.answer('❌ Upload Cancelled', show_alert= True)
    else:
        return

callBackHandler = CallbackQueryHandler(button_callback)