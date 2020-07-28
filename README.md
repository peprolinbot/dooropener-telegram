# dooropener-telegram
Open your door with a telegram bot. This is programmed in python3. And it's avaliable in english and spanish.

## HW Setup
You need a Raspberry pi with a Picamera, a speaker, and a relay connected to the button in the remote of yor door. Just that. Write down the number of the GPIO pin where you put the relay.

## SW Setup
You need three things from telgram: A bot and two channels, one is used for logging the events and the other for adding the persons that should be able to use the bot, you need the chatId from both channels. Now clone this repo. Then run the setup.py script and answer it's questions. For executing the bot run main.py

## Using
You can change whatever you want if you have a little knowdeledge on python, but as default this is very simple: `/open` will open the door for 60s and close it, and the opposite if it's closed; `/toggle` will open or close it, depending on it's actual state, but just that, no automagically closing.

### This short documentation will be better in future. You can help if you want ;)