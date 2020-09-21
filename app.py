import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
import requests
import re
import logging
from newitem import *
from db_manager import dbManager


# To-think:
# - How to deal with "I'll leave this here, please take"
# - How to deal with multiple of the same file

APItoken = os.getenv("APItoken")

db_file_path = os.path.join(os.getcwd(), "db\pythonsqlite.db")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def test(update, context):
    print(update.message.from_user.id)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
    print("Command failed")

def start(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "Hi there, welcome to the Otaniemi Recylic bot!")
    print("Bot started")

def example(update, context):
    print("Empty")

def update_to_queue(update, context):
    query = update.callback_query

    bot = context.bot
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=query.message.text,
        reply_markup= InlineKeyboardMarkup([[
            InlineKeyboardButton("Queue", callback_data='queue'),
            InlineKeyboardButton("Undibs", callback_data="undibs")
        ]])
    )

def dibs(update, context):
    query = update.callback_query
    seller_id = 55244162
    update_to_queue(update, context)
    context.bot.send_message(
        chat_id = seller_id,
        text = "Your item has been dibsed by {buyer.first_name} {buyer.last_name}, username: @{buyer.username}. \nCurrent queue:\n1. @{buyer.username}".format(buyer = query.from_user))

def main():
    # create a database connection
    dbMan = dbManager(db_file_path)
    dbMan.initiate_tables()

    updater = Updater(token = APItoken, use_context = True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('newitem', newitem)],
        states={
        NAME: [MessageHandler(Filters.text & (~Filters.regex('^Quit$')),name)],
        DESC: [MessageHandler(Filters.text & (~Filters.regex('^Quit$')),description)],
        PRICE: [MessageHandler(Filters.text & (~Filters.regex('^Quit$')),price)],
        PICTURE:[MessageHandler(Filters.photo, photo),
                CommandHandler('next', done),
                MessageHandler(Filters.text & (~Filters.regex('^Next$')) & (~Filters.regex('^Quit$')), need_pic)]
        },
        fallbacks=[MessageHandler(Filters.regex('^Quit$'), quit)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CallbackQueryHandler(dibs, pattern = '^dibs$'))
    dp.add_handler(CallbackQueryHandler(dibs, pattern = '^queue$'))

    dp.add_handler(CommandHandler('test', test))
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(MessageHandler(Filters.command, unknown))


    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()