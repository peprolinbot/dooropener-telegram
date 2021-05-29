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
from gtts import gTTS

#Instantiates a door
from door import Door
main_door = Door(gpio_pin, lock_file_path, wait_to_close_time, btn_press_time)

#Loads traductions
import gettext
l = gettext.translation('base', localedir='locales', languages=[lang])
l.install()
_ = l.gettext

#Sets the lang of the tts
tts_lang = lang
if tts_lang == "eng":
    tts_lang = "en"

#Initializes pygame
import pygame
pygame.init()

#Removes the lockFile in case it already existed
if os.path.isfile(lock_file_path):
    os.remove(lock_file_path)

#Sets up the telegram bot
bot = telegram.Bot(token=token)  
updater = Updater(bot.token, use_context=True)

def generate_tts(name):
    tts = gTTS(_("welcome") + ", " + name , lang=tts_lang)
    tts.save("tempTts.mp3")
    sound = AudioSegment.from_file("tempTts.mp3")
    os.remove("tempTts.mp3")
    sound.export("audios/" + name + ".ogg", format="ogg")

def check_lock_file(path=lock_file_path): #Checks if the lock file exists
    if os.path.isfile(path):
        return True
    else:
        return False

'''
Telegram helpers
'''
def _send_photo(destination_chat_id, photo_path="doorPhoto.jpg"): #Sends the phot specified to the chatId specified
    bot.send_photo(chat_id=destination_chat_id, photo=open(photo_path, 'rb'))

def _check_key(check_for_user_id, check_in_chat_id=key_channel_id): #Checks if specified chatId is in the key channel, or other channel/group specified
    try:
        user = bot.get_chat_member(check_in_chat_id, check_for_user_id)
        if user['status'] == 'left':
            return False
    except:
        return False
    return True

def _log_command(from_chat, cmd, destination_chat_id=log_channel_id): #Logs to the log channel the cmd argument and the details of the from_chat
    if not cmd == "/photo":
        main_door.take_photo()
    out = _check_key(from_chat.id)
    if out:
        bot.send_photo(chat_id=destination_chat_id, photo = open("doorPhoto.jpg", "rb"), caption=cmd + _(": First name: ")+ str(from_chat.first_name) +_(", Last name: ") + str(from_chat.last_name) +_(", chatId: ") + str(from_chat.id) + _("chatIdInChannel"))  
    else:
        bot.send_photo(chat_id=destination_chat_id, photo = "doorPhoto.jpg", caption=cmd + _(": Type: ")+ str(from_chat.type)+ _(", First name: ")+ str(from_chat.first_name) +_(", Last name: ") + str(from_chat.last_name) + _(", Username: ") + str(from_chat.username) + _(", Title: ") + str(from_chat.title) + _(", Description: ") + str(from_chat.description) + _(", chatId: ") + str(from_chat.id) + _("chatIdNotInChannel"))
    return out

def _send_menu(destination_chat_id): #Sends an in-keyboard menu to the specified destination_chat_id
    keyboard = [[KeyboardButton(_("open"))],
                [KeyboardButton(_("toggle"))],
                [KeyboardButton(_("photo"))]]
    keyboard_obj = ReplyKeyboardMarkup(keyboard)
    bot.sendMessage(chat_id=destination_chat_id, text=_("hereYouHaveMenu"), reply_markup=keyboard_obj)

def _remove_menu(destination_chat_id): #Removes the in-keyboard menu if existing in specified destination_chat_id
    bot.sendMessage(chat_id=destination_chat_id, text=_("removingMenu"), reply_markup=ReplyKeyboardRemove())

def _send_access_denied(destination_chat_id): #Sends a message saying you shouldn't use this bot to the specified destination_chat_id
    bot.sendMessage(chat_id=destination_chat_id, text=_("thisIsPrivateBot"))

def _send_info(destination_chat_id): #Send info about the bot and it's source-code
    bot.sendMessage(chat_id=destination_chat_id, text=_("botInfo")) 

'''
Starts telegram commands section
'''

def start(update, context): #Start command. Presents itself and sends an in-keyboard menu
    if _log_command(update.effective_chat, update.message.text):
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("hello") + bot_name + _("useHelp"))
        _send_menu(update.effective_chat.id)
        requester_name =  update.effective_chat.first_name.split(' ', 1)[0]
        generate_tts(requester_name)

def help(update, context): #Help command. Tells what does each command
    if _log_command(update.effective_chat, update.message.text):
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("helpCmdListP1") + str(wait_to_close_time) + _("helpCmdListP2"))

def open_(update, context): #Open command. Opens the door and closes after specified time
    if _log_command(update.effective_chat, update.message.text): 
        if check_lock_file():
            context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("doorAlreadyOpening"))
        else:
            door_open_thread = threading.Thread(target=main_door.open)
            door_open_thread.start()
            requester_name =  update.effective_chat.first_name.split(' ', 1)[0]
            main_door.play_audio_file("audios/" + requester_name + ".ogg")
            context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("openingDoor") + str(wait_to_close_time) + _("seconds") + _("."))

def toggle(update, context): #Toggle command. Presses the button of the door only one time
    if _log_command(update.effective_chat, update.message.text):
        if check_lock_file():
            context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("doorAlreadyOpening"))
        else:     
            door_button_with_locking_thread = threading.Thread(target=main_door.press_button_with_locking)
            door_button_with_locking_thread.start() 
            requester_name =  update.effective_chat.first_name.split(' ', 1)[0]
            main_door.play_audio_file("audios/" + requester_name + ".ogg")
            context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("togglingDoor"))


def photo(update, context): #Photo command. Takes a photo from the piCamera and sends it
    if _log_command(update.effective_chat, update.message.text): 
        main_door.take_photo()
        _send_photo(update.effective_chat.id)

def remove_menu(update, context): #removemenu command. Removes the in-keyboard menu from the sender's chatId
    if _log_command(update.effective_chat, update.message.text): 
        _remove_menu(update.effective_chat.id)

def send_menu(update, context): #sendmenu command. Sends an in-keyboard menu to the sender's chatId
    if _log_command(update.effective_chat, update.message.text): 
        _send_menu(update.effective_chat.id)

def gentts(update, context): #Gentts command. Generates the tts wlecome audio file for the user who requested it with it's name
    if _log_command(update.effective_chat, update.message.text):
        requester_name =  update.effective_chat.first_name.split(' ', 1)[0]
        generate_tts(requester_name)
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("ttsGenerated"))

def removetts(update, context): #Removetts command. Removes the welcome audio file
    if _log_command(update.effective_chat, update.message.text):
        requester_name =  update.effective_chat.first_name.split(' ', 1)[0]
        try:
            os.remove("audios/" + requester_name + ".ogg")
        except FileNotFoundError:
            pass
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("ttsRemoved"))
        

def talk(update, context): #Executed when someone sends a Voice Note. Plays the voice note on the speakers
    if _log_command(update.effective_chat, _("voiceNote")):
        update.message.voice.get_file().download(custom_path="voice.mp3")
        sound = AudioSegment.from_file("voice.mp3")
        sound.export("voice.ogg", format="ogg") 
        main_door.play_audio_file("voice.ogg")
        os.remove("voice.mp3")
        os.remove("voice.ogg")

def info(update, context): #/info command
    if _log_command(update.effective_chat, update.message.text):
        _send_info(update.effective_chat.id)

def check_and_send_access_denied(update, context): #Executed with any message. Checks if sender is allowed and else sends the this is private bot text and the info text
    if not _log_command(update.effective_chat, update.message.text):
        _send_access_denied(update.effective_chat.id)
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=_("anywaysCheckThisInfo"))
        _send_info(update.effective_chat.id)

#Defining handlers
start_handler = CommandHandler('start', start)  
help_handler = CommandHandler('help', help)
open_handler = CommandHandler('open', open_)  
toggle_handler = CommandHandler('toggle', toggle)
photo_handler = CommandHandler('photo', photo)
info_handler = CommandHandler('info', info)
remove_menu_handler = CommandHandler('removemenu', remove_menu)
send_menu_handler = CommandHandler('sendmenu', send_menu)
gentts_handler = CommandHandler('gentts', gentts)
removetts_handler = CommandHandler('removetts', removetts)
btn_open_handler = MessageHandler(Filters.regex(r"^"+_('open')+"$"), open_)
btn_toggle_handler = MessageHandler(Filters.regex(r"^"+_('toggle')+"$"), toggle)
btn_photo_handler = MessageHandler(Filters.regex(r"^"+_('photo')+"$"), photo)
voice_note_handler = MessageHandler(Filters.voice, talk)
all_msg_handler = MessageHandler(Filters.all, check_and_send_access_denied)

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

#Adding handlers
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)  
dispatcher.add_handler(open_handler)  
dispatcher.add_handler(toggle_handler)
dispatcher.add_handler(photo_handler)
dispatcher.add_handler(info_handler)
dispatcher.add_handler(remove_menu_handler)  
dispatcher.add_handler(send_menu_handler)  
dispatcher.add_handler(gentts_handler)
dispatcher.add_handler(removetts_handler)
dispatcher.add_handler(btn_open_handler)
dispatcher.add_handler(btn_toggle_handler)
dispatcher.add_handler(btn_photo_handler)
dispatcher.add_handler(voice_note_handler)
dispatcher.add_handler(all_msg_handler)

updater.start_polling()
