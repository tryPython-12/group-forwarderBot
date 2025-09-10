from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import MessageHandler , ContextTypes , filters 
from telegram.constants import ParseMode
import os
from dotenv import load_dotenv
from mssgStorage.msgstorageHandler import add_messages
from db_gen import mssg_collection

load_dotenv()
source_chat_id = int(os.getenv('SOURCE_CHAT_ID'))
dest_chat_id = int(os.getenv('DEST_CHAT_ID'))
HASHTAG = os.getenv("HASHTAG")
# lastMsgId = 2105

async def forward_hashtag(update : Update , context : ContextTypes.DEFAULT_TYPE) :
    msgUpdate = update.message
    # <----debugging--->
    print(f"Update message body : {msgUpdate}")
    #update message's destination chat details
    msg_updated_from_id = msgUpdate.id 
    source_msg_link = f"https://t.me/c/{str(source_chat_id)[4:]}/{msg_updated_from_id}" 

    # sender details
    sender = msgUpdate.from_user
    sender_id = sender.id
    sender_name = f'{sender.first_name} {sender.last_name}'.replace('None','')
    # sender_username = {sender.username}

    # create formatted text to send
    formatted_mssg = (
                f'<b>{msgUpdate.text}\n\n</b>'
                f"<b>Sent By : \n</b>"
                f"<b>Name : <a href=\"tg://user?id={sender.id}\">{sender_name}</a></b>\n"
                f"<b>user_id : {sender_id}\n</b>" 
            )
    # create inline buttons to attach with formatted text
    keyboard = [
        [
            InlineKeyboardButton(
            text= "✅ Accept" ,
            callback_data='approve'
            ),
            InlineKeyboardButton(
            text= "🚫 Reject",
            callback_data='reject'
            )
        ],
        [
            InlineKeyboardButton(
                text= "🌐 Source Request Message",
                url= source_msg_link
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if not msgUpdate or not msgUpdate.text : 
        return
    if HASHTAG in msgUpdate.text.lower() : 
        print("Hashtag found")

        #grabbing last stored message id from database
        last_sent_msg = mssg_collection.find_one(sort=[("_id",-1)])
        last_sent_msg_from_id = last_sent_msg['sent_msg_from_id'] if last_sent_msg else 0
        # # <--debugging---->
        # print(f'all messages : {lastMsg}')

        if msg_updated_from_id > last_sent_msg_from_id : 
            print(f"Last message (id : {last_sent_msg_from_id}) is older than new message (id : {msg_updated_from_id})")
            bot_sent_res = await context.bot.send_message(
                chat_id= dest_chat_id ,
                text= formatted_mssg ,
                reply_markup=reply_markup,
                parse_mode= ParseMode.HTML
            )
            add_messages(msg_updated_from_id,bot_sent_res.id , msgUpdate.text , sender_id , sender_name,source_msg_link)
            print("Bot sent hashtag triggered message successfully")
        else : 
            print(f"new message id {msg_updated_from_id} is older than last message id {last_sent_msg_from_id}")
    else : 
        print("No hashtag found")
    # print(f'update : {update}\nmsg : {msg}\n msg_id : {msg.id}')



forward_hashtag_handler = MessageHandler(filters.TEXT & ~filters.COMMAND , forward_hashtag)
