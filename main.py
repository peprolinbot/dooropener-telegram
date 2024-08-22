import logging
import gettext
import os
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove

# Loads config
from config import telegram_bot_token, log_channel_id, key_channel_id, language, bot_name

from door import open_door, toggle_door, DoorException

# Loads traductions
l = gettext.translation('base', localedir='locales', languages=[language])
l.install()
_ = l.gettext


# Sets up the telegram bot
bot = telegram.Bot(token=telegram_bot_token)
updater = Updater(bot.token, use_context=True)


'''
Telegram helpers
'''


# Checks if specified chatId is in the key channel, or other channel/group specified
def _check_key(check_for_user_id, check_in_chat_id=key_channel_id):
    try:
        user = bot.get_chat_member(check_in_chat_id, check_for_user_id)
        if user['status'] == 'left':
            return False
    except:
        return False
    return True


# Logs to the log channel the cmd argument and the details of the from_chat
def _log_command(from_chat, cmd, destination_chat_id=log_channel_id):
    allowed = _check_key(from_chat.id)
    bot.sendMessage(chat_id=destination_chat_id, text=cmd + _(": Type: ") + str(from_chat.type) + _(", First name: ") + str(from_chat.first_name) + _(", Last name: ") + str(from_chat.last_name) +
                    _(", Username: ") + str(from_chat.username) + _(", Title: ") + str(from_chat.title) + _(", Description: ") + str(from_chat.description) + _(", chatId: ") + str(from_chat.id) + (_("chatIdInChannel") if allowed else _("chatIdNotInChannel")))
    return allowed


# Sends an in-keyboard menu to the specified destination_chat_id
def _send_menu(destination_chat_id):
    keyboard = [[KeyboardButton(_("open"))],
                [KeyboardButton(_("toggle"))]]
    keyboard_obj = ReplyKeyboardMarkup(keyboard)
    bot.sendMessage(chat_id=destination_chat_id, text=_(
        "hereYouHaveMenu"), reply_markup=keyboard_obj)


# Removes the in-keyboard menu if existing in specified destination_chat_id
def _remove_menu(destination_chat_id):
    bot.sendMessage(chat_id=destination_chat_id, text=_(
        "removingMenu"), reply_markup=ReplyKeyboardRemove())


# Sends a message saying you shouldn't use this bot to the specified destination_chat_id
def _send_access_denied(destination_chat_id):
    bot.sendMessage(chat_id=destination_chat_id, text=_("thisIsPrivateBot"))


def _send_info(destination_chat_id):  # Send info about the bot and it's source-code
    bot.sendMessage(chat_id=destination_chat_id, text=_("botInfo"))


'''
Starts telegram commands section
'''


def start(update, context):  # Start command. Presents itself and sends an in-keyboard menu
    if _log_command(update.effective_chat, update.message.text):
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_(
            "hello") + bot_name + _("useHelp"))
        _send_menu(update.effective_chat.id)


def help(update, context):  # Help command. Tells what does each command
    if _log_command(update.effective_chat, update.message.text):
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_(
            "helpCmdList"))


def open_(update, context):  # Open command. Opens the door and closes after specified time
    if _log_command(update.effective_chat, update.message.text):
        try:
            wait_to_close_time = open_door().split()[-1][:-1]
            context.bot.sendMessage(
                chat_id=update.effective_chat.id, text=_("openingDoor")+wait_to_close_time+_("seconds"))
        except DoorException as e:
            if str(e) == "doorInUse":
                context.bot.sendMessage(
                    chat_id=update.effective_chat.id, text=_("doorAlreadyOpening"))
            else:
                context.bot.sendMessage(
                    chat_id=update.effective_chat.id, text=_("doorGenericError"))
                raise e


def toggle(update, context):  # Toggle command. Presses the button of the door only one time
    if _log_command(update.effective_chat, update.message.text):
        try:
            toggle_door()
            context.bot.sendMessage(
                chat_id=update.effective_chat.id, text=_("togglingDoor"))
        except DoorException as e:
            if str(e) == "doorInUse":
                context.bot.sendMessage(
                    chat_id=update.effective_chat.id, text=_("doorAlreadyOpening"))
            else:
                context.bot.sendMessage(
                    chat_id=update.effective_chat.id, text=_("doorGenericError"))
                raise e


# removemenu command. Removes the in-keyboard menu from the sender's chatId
def remove_menu(update, context):
    if _log_command(update.effective_chat, update.message.text):
        _remove_menu(update.effective_chat.id)


def send_menu(update, context):  # sendmenu command. Sends an in-keyboard menu to the sender's chatId
    if _log_command(update.effective_chat, update.message.text):
        _send_menu(update.effective_chat.id)


def info(update, context):  # /info command
    if _log_command(update.effective_chat, update.message.text):
        _send_info(update.effective_chat.id)


# Executed with any message. Checks if sender is allowed and else sends the this is private bot text and the info text
def check_and_send_access_denied(update, context):
    if not _log_command(update.effective_chat, update.message.text):
        _send_access_denied(update.effective_chat.id)
        context.bot.sendMessage(
            chat_id=update.effective_chat.id, text=_("anywaysCheckThisInfo"))
        _send_info(update.effective_chat.id)


# Defining handlers
start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
open_handler = CommandHandler('open', open_)
toggle_handler = CommandHandler('toggle', toggle)
info_handler = CommandHandler('info', info)
remove_menu_handler = CommandHandler('removemenu', remove_menu)
send_menu_handler = CommandHandler('sendmenu', send_menu)
btn_open_handler = MessageHandler(Filters.regex(r"^"+_('open')+"$"), open_)
btn_toggle_handler = MessageHandler(
    Filters.regex(r"^"+_('toggle')+"$"), toggle)
all_msg_handler = MessageHandler(Filters.all, check_and_send_access_denied)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Adding handlers
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(open_handler)
dispatcher.add_handler(toggle_handler)
dispatcher.add_handler(info_handler)
dispatcher.add_handler(remove_menu_handler)
dispatcher.add_handler(send_menu_handler)
dispatcher.add_handler(btn_open_handler)
dispatcher.add_handler(btn_toggle_handler)
dispatcher.add_handler(all_msg_handler)

updater.start_polling()
