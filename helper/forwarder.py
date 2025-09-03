from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import MessageHandler , ContextTypes , filters 
from telegram.constants import ParseMode
import os
from dotenv import load_dotenv
from mssgStorage.msgstorageHandler import add_messages

load_dotenv()

dest_chat_id = int(os.getenv('DEST_CHAT_ID'))
HASHTAG = os.getenv("HASHTAG")
lastMsgId = 2105

async def forward_hashtag(update : Update , context : ContextTypes.DEFAULT_TYPE) :
    msg = update.message
    # sender details
    sender = msg.from_user

    sender_id = sender.id
    sender_name = f'{sender.first_name} {sender.last_name}'.replace('None','')
    # sender_username = {sender.username}

    # create formatted text to send
    formatted_mssg = (
                f'<b>{msg.text}\n\n</b>'
                f"<b>Sent By : \n</b>"
                f"<b>Name : <a href=\"tg://user?id={sender.id}\">{sender_name}</a></b>\n"
                f"<b>user_id : {sender_id}\n</b>" 
            )
    # create inline buttons to attach with formatted text
    keyboard = [
        [
            InlineKeyboardButton(
            text= "✅ Accept" ,
            callback_data=f"accept:{msg.id}"
            ),
            InlineKeyboardButton(
            text= "🚫 Reject",
            callback_data=f"reject:{msg.id}"
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if not msg or not msg.text : 
        return
    if HASHTAG in msg.text : 
        print("Hashtag found")
        if msg.id > lastMsgId : 
            await context.bot.send_message(
                chat_id= dest_chat_id ,
                text= formatted_mssg ,
                reply_markup=reply_markup,
                parse_mode= ParseMode.HTML
            )
            add_messages(msg.id , msg.text , sender_id , sender_name)
            print("Bot sent hashtag triggered message successfully")
        else : 
            print(f"{msg.id} is older than last message id {lastMsgId}")
    else : 
        print("No hashtag found")
    # print(f'update : {update}\nmsg : {msg}\n msg_id : {msg.id}')



forward_hashtag_handler = MessageHandler(filters.TEXT & ~filters.COMMAND , forward_hashtag)
