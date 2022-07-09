from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, Update
import os
import contants as key
import Backend as bb
import logging
from telegram.ext import *
import _json
import requests
import time

array = []
START_ROUTE,MID_ROUTE1,MID_ROUTE2, END_ROUTE,TIME,DATE,LOC,EXPNO, STORE,CALL = range(10)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    """Send a message when the command /start is issued."""
    """ user = update.message.from_user"""
    ###

    WhoRu = [
        [
            InlineKeyboardButton("Seeking for volunteers", callback_data="Seeking for volunteers"),
        ],
        [
            InlineKeyboardButton("Volunteering", callback_data="Volunteering"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(WhoRu)
    update.message.reply_text('Hi! \nWelcome to VolunteerFinds', reply_markup=reply_markup)
    return START_ROUTE

def PostVolunteers(update,contex):
    query = update.callback_query
    query.answer()
    TypesOfV = [
        [
            InlineKeyboardButton("Environmental", callback_data="Environmental"),
            InlineKeyboardButton("Animals", callback_data="Animals"),
        ],
        [
            InlineKeyboardButton("Social", callback_data="Social"),
            InlineKeyboardButton("Healthcare", callback_data="Healthcare"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(TypesOfV)
    query.edit_message_text(text="Hi! \nWelcome to VolunteerFinds, Please select the type of volunteer you are interested in.", reply_markup=reply_markup)
    return MID_ROUTE2


def PostOrganisation(update,context):
    query = update.callback_query
    ##query.answer
    TypesOfV = [
        [
            InlineKeyboardButton("Environmental", callback_data="Environmental"),
            InlineKeyboardButton("Animals", callback_data="Animals"),
        ],
        [
            InlineKeyboardButton("Social", callback_data="Social"),
            InlineKeyboardButton("Healthcare", callback_data="Healthcare"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(TypesOfV)
    query.edit_message_text('Hi! \nWelcome to VolunteerFinds, Please select the volunteer type that you are posting for.',
                         reply_markup=reply_markup)
    return MID_ROUTE1

def CollectionOfDetails(update,context):
    query = update.callback_query
    query.answer()
    name = array[0]
    type = array[1]
    expno = array[2]
    time = array[3]
    date = array[4]
    loc = array[5]
    context.bot.send_message(chat_id=update.effective_chat.id, text =f"Name: {name} \n type: {type}\n expected number: {expno} \n time: {str(time)} \n date: {str(date)}\n location: {str(loc)}")

def CollectionOfDetails1(update,context:CallbackContext):
    query = update.callback_query
    ##query.answer
    context.user_data["type"] = query.data
    context.bot.send_message(chat_id=update.effective_chat.id, text = "What's the name of your organisation?")
    return EXPNO

def CollectionOfDetails2(update,context:CallbackContext):
    context.user_data["orgname"] = update.message.text
    ##query.answer
    update.message.reply_text(text = "What is the number of people expected for volunteering?")
    return TIME

def CollectionOfDetails3(update,context:CallbackContext):
    context.user_data["expno"] = update.message.text
    update.message.reply_text(text= "What is the time required for the volunteers to help?")
    return DATE

def CollectionOfDetails4(update,context:CallbackContext):
    context.user_data["time"] = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text = "What is the date required for the volunteers to help?")
    return LOC

def CollectionOfDetails5(update,context:CallbackContext):
    context.user_data["Date"] = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Where is the volunteering location?")
    return STORE

def CollectionOfDetails6(update,context:CallbackContext):
    context.user_data["Loc"] = update.message.text
    user = update.message.from_user

    context.bot.send_message(chat_id=update.effective_chat.id, text = "Done")
    Template(update,context)


def Template(update, context):
    array.append(context.user_data["orgname"])
    array.append(context.user_data["type"])
    array.append(context.user_data["expno"])
    array.append(context.user_data["time"])
    array.append(context.user_data["Date"])
    array.append(context.user_data["Loc"])

    update.message.reply_text(f"Here are the information you have submitted\nName: {array[0]} \n type: {array[1]}\n expected number: {array[2]} \n time: {str(array[3])} \n date: {str(array[4])}\n location: {str(array[5])}")

def main():
    """Start the bot"""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(key.apn, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler=(ConversationHandler(
            entry_points= [CommandHandler("start",start)],
            states = {
                START_ROUTE: [
                    CallbackQueryHandler(PostVolunteers, pattern="^Volunteering$",pass_user_data=True),
                    CallbackQueryHandler(PostOrganisation, pattern="^Seeking for volunteers$",pass_user_data=True)
                ],
                MID_ROUTE1: [
                    CallbackQueryHandler(CollectionOfDetails1, pattern="^Environmental$", pass_user_data=True),
                    CallbackQueryHandler(CollectionOfDetails1, pattern="^Animals$", pass_user_data=True),
                    CallbackQueryHandler(CollectionOfDetails1, pattern="^Healthcare$", pass_user_data=True),
                    CallbackQueryHandler(CollectionOfDetails1, pattern="^Social$", pass_user_data=True),
                ],
                MID_ROUTE2: [
                    CallbackQueryHandler(CollectionOfDetails, pattern="^Environmental$", pass_user_data=True),
                    CallbackQueryHandler(CollectionOfDetails, pattern="^Animals$", pass_user_data=True),
                    CallbackQueryHandler(CollectionOfDetails, pattern="^Healthcare$", pass_user_data=True),
                    CallbackQueryHandler(CollectionOfDetails, pattern="^Social$", pass_user_data=True),
                ],
                EXPNO:[MessageHandler(Filters.text,CollectionOfDetails2)],
                TIME: [MessageHandler(Filters.text, CollectionOfDetails3)],
                DATE: [MessageHandler(Filters.text, CollectionOfDetails4)],
                LOC: [MessageHandler(Filters.text, CollectionOfDetails5)],
                STORE: [MessageHandler(Filters.text, CollectionOfDetails6)]


            },
            fallbacks= [CommandHandler("start",start)]

    ))
    dp.add_handler(conv_handler)




    # Start the Bot
    TOKEN = key.apn



    # add handlers
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()