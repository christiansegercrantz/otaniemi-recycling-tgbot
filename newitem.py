from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from classes import Item
from datetime import datetime
from db_manager import dbManager

import sqlite3
from sqlite3 import Error
import os

db_file_path = os.path.join(os.getcwd(), "db\pythonsqlite.db")

NAME, DESC, PRICE, PICTURE, DONE = range(5)
i = Item()
dibsKeyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Dibs", callback_data='dibs')]])


def newitem(update, context):
    dbMan = dbManager(db_file_path)
    dbMan.create_item_for_sale(update.message.from_user.id)
    update.message.reply_text("It seems you want to add a new item, great! Let's get started. First, give me the name of the item you want to give away. Type \"Quit\" at any point to stop quit the process.")
    return NAME

def name(update, context):
    dbMan = dbManager(db_file_path)
    dbMan.set_item_for_sale(update.message.text, NAME)
    update.message.reply_text("Next please me the description of the item(s).")
    return DESC

def description(update, context):
    dbMan = dbManager(db_file_path)
    dbMan.set_item_for_sale(update.message.text, DESC)
    update.message.reply_text("Now tell me the price of the item. If it's free, simple send the 'free'")
    i.desc(update.message.text)
    return PRICE

def price(update, context):
    dbMan = dbManager(db_file_path)
    dbMan.set_item_for_sale(update.message.text, PRICE)
    update.message.reply_text("Next please send me a picture of the item, you may include a caption in the picture. In case you don't want to include pictures, send \"/next\".")
    return PICTURE

def photo(update, context):
    dbMan = dbManager(db_file_path)
    dbMan.set_item_for_sale(update.message.text, PICTURE)
    update.message.reply_text("Continue sending pictures if you like, or send \"/next\" to move on.")
    i.photo(update.message.photo[-1].file_id, update.message.caption) #This needs to be transfered!!!
    return PICTURE

def need_pic(update, context): 
    update.message.reply_text("Please provide one or multiple pictures!")
    return PICTURE

def done(update, context):
    broadcast_channel = '@otaniemirecycles'
    sent_message = ""
    picture_message = ""
    picture_message_ids = ""
    update.message.reply_text("Thank you for your item, it will now be posted to the broadcasting channel! Once someone claims the item, I will notify you with a message!")
    if len(i.myphotos) == 0:
        sent_message = context.bot.send_message(chat_id = broadcast_channel, text = str(i), reply_markup = dibsKeyboard)
    elif len(i.myphotos) == 1:
        picture_message = context.bot.send_photo(chat_id = broadcast_channel, photo = i.myphotos[0][0], caption = i.myphotos[0][1])
        picture_message_ids = picture_message['message_id']
        sent_message = context.bot.send_message(chat_id = broadcast_channel, text= "The items related can be seen in the picture above.\n\n" + str(i), reply_markup = dibsKeyboard)
    else:
        mediagroup = []
        for j in  range(len(i.myphotos)):
            mediagroup.append(InputMediaPhoto(i.myphotos[j][0],i.myphotos[j][1]))
        picture_message = context.bot.send_media_group(chat_id = broadcast_channel, media = mediagroup)
        picture_message_ids = ",".join(map(lambda x: str(x['message_id']),picture_message))
        sent_message = context.bot.send_message(chat_id = broadcast_channel, text= "The items related can be seen in the album above.\n\n" + str(i), reply_markup = dibsKeyboard)
    print(picture_message_ids)
    item = (update.message.from_user.id, #seller_id
            "done",
            sent_message['message_id'],#channel_message_id
            datetime.date(datetime.now()),#posted_date
            i.myname,#name
            i.mydesc,#description
            i.myprice,#price
            picture_message_ids) #picture_message_id
    print(item)
    try: 
        dbMan = dbManager(db_file_path)
        dbMan.create_item_for_sale(item)
    except Error as e:
        print(e)

    for pic in i.myphotos:
        picture = ("","","")
        pass
        #The loop needs to create a db input for each picture and it's caption. The id for the specific item needs to be fetched first though
        #i.myphotos)#photos

    
    i.clear()
    return ConversationHandler.END

def quit(update, context):
	update.message.reply_text("Until next time!")
	return ConversationHandler.END
    