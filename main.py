import telegram
from telegram.ext import Updater  
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from config.telegram import *
from config.language import *
from config.gpio import *
from config.variables import *
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
    # print("Btn")
    GPIO.output(gpioPin, GPIO.LOW)
    sleep(btnPressTime)
    GPIO.output(gpioPin, GPIO.HIGH)

def openDoor():
    doorButton()
    sleep(waitToCloseTime)
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
        bot.sendMessage(chat_id=logChannelId, text=cmd + _(": First name: ")+ str(fromChat.first_name) +_(", Last name: ") + str(fromChat.last_name) +_(", chatId: ") + str(fromChat.id) + _(". ChatId is in the key channel"))  
    else:
        bot.sendMessage(chat_id=logChannelId, text=cmd + _(": Type: ")+ str(fromChat.type)+ _(", First name: ")+ str(fromChat.first_name) +_(", Last name: ") + str(fromChat.last_name) + _(", Username: ") + str(fromChat.username) + _(", Title: ") + str(fromChat.title) + _(", Description: ") + str(fromChat.description) + _(", chatId: ") + str(fromChat.id) + _(". ChatId isn't in the key channel"))
    return out

def sendMenu(destinationChatId):
    keyboard = [[KeyboardButton(_('Open'))],
                [KeyboardButton(_('Toggle'))]]
    keyboardObj = ReplyKeyboardMarkup(keyboard)
    bot.sendMessage(chat_id=destinationChatId, text=_("I'm giving you this beautiful menu without any additional cost, you can use it or you can go crazy and use commands; you decide."), reply_markup=keyboardObj)

def rmMenu(destinationChatId):
    bot.sendMessage(chat_id=destinationChatId, text=_("Ok, removing the keyboard menu. Use /sendmenu if you want it again"), reply_markup=ReplyKeyboardRemove())

def sendFuckOff(destinationChatId):
    bot.sendMessage(chat_id=destinationChatId, text=_("I said you this was a private bot, so don't use it!"))

def start(update, context):
    if logCommand(update.effective_chat, "/start"):
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("Hi, I'm Morfeo. Send /help to see avaliable commands"))
        sendMenu(update.effective_chat.id)

def help(update, context):
    if logCommand(update.effective_chat, "/help"):
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("This is a list of avaliable commands:\n/open - Opens the door and closes it automatically after ") + str(waitToCloseTime) + _(" seconds since you sent the command(It'll do the opposite thing if it's already open)\n/toggle - Just opens/closes the door depending on it's actual state(presses the button one time and forgets about everything).\n/sendmenu - Sends you a menu for the keyboard with the most useful commands for the door. Doesn't do anything if you already have one.\n/removemenu - Removes the actions menu from your keyboard. Doesn't do anything if already removed\n/start - The command executed the first time you use the bot.\n/help - This command"))

def open(update, context):
    if logCommand(update.effective_chat, "/open"): 
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("Opening door... It'll close in ") + str(waitToCloseTime) + _(" seconds"))
        openDoor()

def toggle(update, context):
    if logCommand(update.effective_chat, "/toggle"): 
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("Opening, or closing ;), door..."))
        doorButton()

def removemenu(update, context):
    if logCommand(update.effective_chat, "/removemenu"): 
        rmMenu(update.effective_chat.id)

def sendmenu(update, context):
    if logCommand(update.effective_chat, "/sendmenu"): 
        sendMenu(update.effective_chat.id)

startHandler = CommandHandler('start', start)  
helpHandler = CommandHandler('help', help)
openHandler = CommandHandler('open', open)  
toggleHandler = CommandHandler('toggle', toggle)
removemenuHandler = CommandHandler('removemenu', removemenu)
sendmenuHandler = CommandHandler('sendmenu', sendmenu)
btnOpenHandler = MessageHandler(Filters.regex(r"^"+_('Open')+"$"), open)
btnToggleHandler = MessageHandler(Filters.regex(r"^"+_('Toggle')+"$"), toggle)

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

dispatcher.add_handler(startHandler)
dispatcher.add_handler(helpHandler)  
dispatcher.add_handler(openHandler)  
dispatcher.add_handler(toggleHandler)
dispatcher.add_handler(removemenuHandler)  
dispatcher.add_handler(sendmenuHandler)    
dispatcher.add_handler(btnOpenHandler)
dispatcher.add_handler(btnToggleHandler)

updater.start_polling()
