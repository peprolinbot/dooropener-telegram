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
from picamera import PiCamera

camera = PiCamera()

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

def takePhoto(photoPath="doorPhoto.jpg"):
    print("Photo")
    camera.capture(photoPath)

def sendPhoto(destinationChatId, photoPath="doorPhoto.jpg"):
    bot.send_photo(chat_id=destinationChatId, photo=open(photoPath, 'rb'))

def checkKey(checkForUserId, checkInchatId=keyChannelId):
    try:
        bot.get_chat_member(checkInchatId, checkForUserId)
    except:
        return False
    return True

def logCommand(fromChat, cmd, destinationChatId=logChannelId):
    out = checkKey(fromChat.id)
    if out:
        bot.sendMessage(chat_id=logChannelId, text=cmd + _(": First name: ")+ str(fromChat.first_name) +_(", Last name: ") + str(fromChat.last_name) +_(", chatId: ") + str(fromChat.id) + _("chatIdInChannel"))  
    else:
        bot.sendMessage(chat_id=logChannelId, text=cmd + _(": Type: ")+ str(fromChat.type)+ _(", First name: ")+ str(fromChat.first_name) +_(", Last name: ") + str(fromChat.last_name) + _(", Username: ") + str(fromChat.username) + _(", Title: ") + str(fromChat.title) + _(", Description: ") + str(fromChat.description) + _(", chatId: ") + str(fromChat.id) + _("chatIdNotInChannel"))
    return out

def sendMenu(destinationChatId):
    keyboard = [[KeyboardButton(_("open"))],
                [KeyboardButton(_("toggle"))],
                [KeyboardButton(_("photo"))]]
    keyboardObj = ReplyKeyboardMarkup(keyboard)
    bot.sendMessage(chat_id=destinationChatId, text=_("hereYouHaveMenu"), reply_markup=keyboardObj)

def rmMenu(destinationChatId):
    bot.sendMessage(chat_id=destinationChatId, text=_("removingMenu"), reply_markup=ReplyKeyboardRemove())

def sendFuckOff(destinationChatId):
    bot.sendMessage(chat_id=destinationChatId, text=_("thisIsPrivateBot"))

def start(update, context):
    if logCommand(update.effective_chat, "/start"):
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("hello") + botName + _("useHelp"))
        sendMenu(update.effective_chat.id)

def help(update, context):
    if logCommand(update.effective_chat, "/help"):
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("helpCmdListP1") + str(waitToCloseTime) + _("helpCmdListP2"))

def openDoor(update, context):
    if logCommand(update.effective_chat, "/open"): 
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("openingDoor") + str(waitToCloseTime) + _("seconds") + _("."))
        openDoor()

def toggle(update, context):
    if logCommand(update.effective_chat, "/toggle"): 
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("togglingDoor"))
        doorButton()

def photo(update, context):
    if logCommand(update.effective_chat, "/photo"): 
        takePhoto()
        sendPhoto(update.effective_chat.id)

def removemenu(update, context):
    if logCommand(update.effective_chat, "/removemenu"): 
        rmMenu(update.effective_chat.id)

def sendmenu(update, context):
    if logCommand(update.effective_chat, "/sendmenu"): 
        sendMenu(update.effective_chat.id)

startHandler = CommandHandler('start', start)  
helpHandler = CommandHandler('help', help)
openHandler = CommandHandler('open', openDoor)  
toggleHandler = CommandHandler('toggle', toggle)
photoHandler = CommandHandler('photo', photo)
removemenuHandler = CommandHandler('removemenu', removemenu)
sendmenuHandler = CommandHandler('sendmenu', sendmenu)
btnOpenHandler = MessageHandler(Filters.regex(r"^"+_('open')+"$"), openDoor)
btnToggleHandler = MessageHandler(Filters.regex(r"^"+_('toggle')+"$"), toggle)
btnPhotoHandler = MessageHandler(Filters.regex(r"^"+_('photo')+"$"), photo)

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

dispatcher.add_handler(startHandler)
dispatcher.add_handler(helpHandler)  
dispatcher.add_handler(openHandler)  
dispatcher.add_handler(toggleHandler)
dispatcher.add_handler(photoHandler)
dispatcher.add_handler(removemenuHandler)  
dispatcher.add_handler(sendmenuHandler)    
dispatcher.add_handler(btnOpenHandler)
dispatcher.add_handler(btnToggleHandler)
dispatcher.add_handler(btnPhotoHandler)

updater.start_polling()
