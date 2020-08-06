import threading 
import os
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
from pydub import AudioSegment

#Loads traductions
import gettext
l = gettext.translation('base', localedir='locales', languages=[lang])
l.install()
_ = l.gettext

#Initializes pygame
import pygame
pygame.init()

#Sets up piCamera
from picamera import PiCamera
camera = PiCamera()

#Sets up gpio
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(gpioPin, GPIO.OUT)
GPIO.output(gpioPin, GPIO.HIGH)

#Removes the lockFile in case it already existed
if os.path.isfile(lockFilePath):
    os.remove(lockFilePath)

#Sets up the telegram bot
bot = telegram.Bot(token=token)  
updater = Updater(bot.token, use_context=True)

def doorButton(): #Presses the door button
    # print("Btn")
    GPIO.output(gpioPin, GPIO.LOW)
    sleep(btnPressTime)
    GPIO.output(gpioPin, GPIO.HIGH)

def doorButtonWithLocking(): #Presses the door button and locks and unlocks at start and end, respectively, the lockFile
    if not os.path.isfile(lockFilePath):
        with open(lockFilePath, 'w') as f: 
            pass
        doorButton()
        os.remove(lockFilePath)


def openDoor(): #Opens door and closes it after specified time
    if not os.path.isfile(lockFilePath):
        with open(lockFilePath, 'w') as f: 
            pass

        doorButton()
        sleep(waitToCloseTime)
        doorButton()
    
        os.remove(lockFilePath)

def playFile(file_path): #Plays the audio file specified
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(1.0) 
    pygame.mixer.music.play()
    pygame.event.wait()

def checkLockFile(path=lockFilePath): #Checks if the lock file exists
    if os.path.isfile(path):
        return True
    else:
        return False

def takePhoto(photoPath="doorPhoto.jpg"): #Takes a photo to the specified path
    # print("Photo")
    camera.capture(photoPath)

def sendPhoto(destinationChatId, photoPath="doorPhoto.jpg"): #Sends the phot specified to the chatId specified
    bot.send_photo(chat_id=destinationChatId, photo=open(photoPath, 'rb'))

def checkKey(checkForUserId, checkInchatId=keyChannelId): #Checks if specified chatId is in the key channel, or other channel/group specified
    try:
        bot.get_chat_member(checkInchatId, checkForUserId)
    except:
        return False
    return True

def logCommand(fromChat, cmd, destinationChatId=logChannelId): #Logs to the log channel the cmd argument and the details of the fromChat
    if not cmd == "/photo":
        takePhoto()
    out = checkKey(fromChat.id)
    if out:
        bot.send_photo(chat_id=destinationChatId, photo = open("doorPhoto.jpg", "rb"), caption=cmd + _(": First name: ")+ str(fromChat.first_name) +_(", Last name: ") + str(fromChat.last_name) +_(", chatId: ") + str(fromChat.id) + _("chatIdInChannel"))  
    else:
        bot.send_photo(chat_id=destinationChatId, photo = "doorPhoto.jpg", caption=cmd + _(": Type: ")+ str(fromChat.type)+ _(", First name: ")+ str(fromChat.first_name) +_(", Last name: ") + str(fromChat.last_name) + _(", Username: ") + str(fromChat.username) + _(", Title: ") + str(fromChat.title) + _(", Description: ") + str(fromChat.description) + _(", chatId: ") + str(fromChat.id) + _("chatIdNotInChannel"))
    return out

def sendMenu(destinationChatId): #Sends an in-keyboard menu to the specified destinationChatId
    keyboard = [[KeyboardButton(_("open"))],
                [KeyboardButton(_("toggle"))],
                [KeyboardButton(_("photo"))]]
    keyboardObj = ReplyKeyboardMarkup(keyboard)
    bot.sendMessage(chat_id=destinationChatId, text=_("hereYouHaveMenu"), reply_markup=keyboardObj)

def rmMenu(destinationChatId): #Removes the in-keyboard menu if existing in specified destinationChatId
    bot.sendMessage(chat_id=destinationChatId, text=_("removingMenu"), reply_markup=ReplyKeyboardRemove())

def sendFuckOff(destinationChatId): #Sends a message saying you shouldn't use this bot to the specified destinationChatId
    bot.sendMessage(chat_id=destinationChatId, text=_("thisIsPrivateBot"))

def sendInfo(destinationChatId): #Send info about the bot and it's source-code
    bot.sendMessage(chat_id=destinationChatId, text=_("botInfo"))

def start(update, context): #Start command. Presents itself and sends an in-keyboard menu
    if logCommand(update.effective_chat, update.message.text):
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("hello") + botName + _("useHelp"))
        sendMenu(update.effective_chat.id)

def help(update, context): #Help command. Tells what does each command
    if logCommand(update.effective_chat, update.message.text):
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("helpCmdListP1") + str(waitToCloseTime) + _("helpCmdListP2"))

def openCmd(update, context): #Open command. Opens the door and closes after specified time
    if logCommand(update.effective_chat, update.message.text): 
        if checkLockFile():
            context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("doorAlreadyOpening"))
        else:
            doorOpenThread = threading.Thread(target=openDoor)
            doorOpenThread.start()
            context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("openingDoor") + str(waitToCloseTime) + _("seconds") + _("."))

def toggle(update, context): #Toggle command. Presses the button of the door only one time
    if logCommand(update.effective_chat, update.message.text):
        if checkLockFile():
            context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("doorAlreadyOpening"))
        else:     
            doorButtonWithLockingThread = threading.Thread(target=doorButtonWithLocking)
            doorButtonWithLockingThread.start() 
            context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("togglingDoor"))


def photo(update, context): #Photo command. Takes a photo from the piCamera and sends it
    if logCommand(update.effective_chat, update.message.text): 
        takePhoto()
        sendPhoto(update.effective_chat.id)

def removemenu(update, context): #Removemenu command. Removes the in-keyboard menu from the sender's chatId
    if logCommand(update.effective_chat, update.message.text): 
        rmMenu(update.effective_chat.id)

def sendmenu(update, context): #Sendmenu command. Sends an in-keyboard menu to the sender's chatId
    if logCommand(update.effective_chat, update.message.text): 
        sendMenu(update.effective_chat.id)

def talk(update, context): #Executed when someone sends a Voice Note. Plays the voice note on the speakers
    if logCommand(update.effective_chat, _("voiceNote")):
        update.message.voice.get_file().download(custom_path="voice.mp3")
        sound = AudioSegment.from_file("voice.mp3")
        sound.export("voice.ogg", format="ogg") 
        playFile("voice.ogg")

def info(update, context): #/info command
    if logCommand(update.effective_chat, update.message.text):
        sendInfo(update.effective_chat.id)

def checkAndSendFuckOffAndInfo(update, context): #Executed with any message. Checks if sender is allowed and else sends the this is private bot text and the info text
    if not logCommand(update.effective_chat, update.message.text):
        sendFuckOff(update.effective_chat.id)
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("anywaysCheckThisInfo"))
        sendInfo(update.effective_chat.id)

#Defining handlers
startHandler = CommandHandler('start', start)  
helpHandler = CommandHandler('help', help)
openHandler = CommandHandler('open', openCmd)  
toggleHandler = CommandHandler('toggle', toggle)
photoHandler = CommandHandler('photo', photo)
infoHandler = CommandHandler('info', info)
removemenuHandler = CommandHandler('removemenu', removemenu)
sendmenuHandler = CommandHandler('sendmenu', sendmenu)
btnOpenHandler = MessageHandler(Filters.regex(r"^"+_('open')+"$"), openCmd)
btnToggleHandler = MessageHandler(Filters.regex(r"^"+_('toggle')+"$"), toggle)
btnPhotoHandler = MessageHandler(Filters.regex(r"^"+_('photo')+"$"), photo)
voiceNoteHandler = MessageHandler(Filters.voice, talk)
allMsgHandler = MessageHandler(Filters.all, checkAndSendFuckOffAndInfo)

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

#Adding handlers
dispatcher.add_handler(startHandler)
dispatcher.add_handler(helpHandler)  
dispatcher.add_handler(openHandler)  
dispatcher.add_handler(toggleHandler)
dispatcher.add_handler(photoHandler)
dispatcher.add_handler(infoHandler)
dispatcher.add_handler(removemenuHandler)  
dispatcher.add_handler(sendmenuHandler)    
dispatcher.add_handler(btnOpenHandler)
dispatcher.add_handler(btnToggleHandler)
dispatcher.add_handler(btnPhotoHandler)
dispatcher.add_handler(voiceNoteHandler)
dispatcher.add_handler(allMsgHandler)

updater.start_polling()
