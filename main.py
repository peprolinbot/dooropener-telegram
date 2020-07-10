import telegram
from telegram.ext import Updater  
from telegram.ext import CommandHandler
from config.telegram import *
from config.language import *
from config.gpio import *
from time import sleep
import gettext
l = gettext.translation('base', localedir='locales', languages=[lang])
l.install()
_ = l.gettext
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(gpioPin, GPIO.OUT)

bot = telegram.Bot(token=token)  
updater = Updater(bot.token, use_context=True)

def doorButton():
    GPIO.output(gpioPin, GPIO.LOW)
    sleep(0.5)
    GPIO.output(gpioPin, GPIO.HIGH)

def openDoor():
    doorButton()
    sleep(60)
    doorButton()

def checkKey(checkForUserId, checkInchatId=keyChannelId):
    try:
        bot.get_chat_member(checkInchatId, checkForUserId)
    except:
        return False
    return True

def logCommand(fromChat, cmd, destinationChatId=logChannelId):
    out = checkKey(fromChat.id)
    if out:
        bot.sendMessage(chat_id=logChannelId, text=cmd + _(": First name: ")+ str(fromChat.first_name) +_(", Last name: ") + str(fromChat.last_name) +_(", chatId: [") + str(fromChat.id) + _("]. ChatId is in the key channel"))  
    else:
        bot.sendMessage(chat_id=logChannelId, text=cmd + _(": Type: ")+ str(fromChat.type)+ _(", First name: ")+ str(fromChat.first_name) +_(", Last name: ") + str(fromChat.last_name) + _(", Username: ") + str(fromChat.username) + _(", Title: ") + str(fromChat.title) + _(", Description: ") + str(fromChat.description) + _(", chatId: ") + str(fromChat.id) + _(". ChatId isn't in the key channel"))
    return out

def start(update, context):
    if logCommand(update.effective_chat, "/start"):
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("Hi, I'm Morfeo. Send /help to see avaliable commands"))

def help(update, context):
    if logCommand(update.effective_chat, "/help"):
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("This is a list of avaliable commands:\n/open - Opens the door and closes it automatically after 1 minute since you sent the command(It'll do the opposite thing if it's already open)\n/toggle - Just opens/closes the door depending on it's actual state(presses the button one time and forgets about everything).\n/start - The command executed the first time you use the bot.\n/help - this command"))
def open(update, context):
    if logCommand(update.effective_chat, "/open"): 
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("Opening door... It'll close in 60s"))
        openDoor()

def toggle(update, context):
    if logCommand(update.effective_chat, "/toggle"): 
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("Opening, or closing ;), door..."))
        doorButton()

start_handler = CommandHandler('start', start)  
help_handler = CommandHandler('help', help)
open_handler = CommandHandler('open', open)  
toggle_handler = CommandHandler('toggle', toggle)

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)  
dispatcher.add_handler(open_handler)  
dispatcher.add_handler(toggle_handler)  

updater.start_polling()
