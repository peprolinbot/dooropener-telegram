import os

approved = False
avaliableLanguages = ["es", "eng"]
lang="777"

selection = input("Are you sure you are running this in the root of the repository? [S/n] ")
if selection == "" or selection == "S" or selection == "s":
    print("[i] Perfect!")
else:
    print("[!] Exiting...")
    exit()

try:
    while not approved:
        token = input("Enter the token @BotFather gave you: ")
        logChannelId = input("Id of the channel where all the events will be logged: ")
        keyChannelId = input("Id of the channel in which it's members should be able to use the bot: ")
        while not lang in avaliableLanguages:
            lang = input("Enter the language code you want [es/eng]: ")
            print("Language not avaliable")
        gpioPin = input("Enter the number of the GPIO pin you have your relay connected to. 17, for example. Be careful: ")

        print("Ok. Check if this information is ok:")
        print("Token: [" + token + "]")
        print("Log channel id: [" + logChannelId + "]")
        print("Key channel id: [" + keyChannelId + "]")
        print("Language: [" + lang + "]")
        print("GPIO pin: [" + gpioPin + "]")
        selection = input("Is this correct [S/n] ")
        if selection == "" or selection == "S" or selection == "s":
            approved = True
        else:
            approved = False
    print("[i] Creating config dir if it doesn't exist...")
    if not os.path.isdir('./config'):
        os.mkdir("config")
    print("[i] Creating config files...")
    #Writing content to the files
    with open("config/telegram.py", "w") as f:
        f.write('#The telegram bot token that you obtained from @BotFather\ntoken = "'+ token +'"\n\n#Channel where all the events will be logged\nlogChannelId = "'+ logChannelId +'"\n\n#Channel in which it\'s members should be able to use the bot\nkeyChannelId = "'+ keyChannelId +'"')
        f.close()
    with open("config/language.py", "w") as f:
        f.write('#Language selection. Can be "es" or "eng".\nlang = "'+ lang +'"')
        f.close()
    with open("config/gpio.py", "w") as f:
        f.write('#Number of the gpio where the relay is connected.\ngpioPin = '+ gpioPin)
        f.close()
    print("[i] Succesfull!")
    print("[i] Keep in mind that all this variables can be changed whenever you want at config/telegram.py and config/language.py.")
    print("[i] Bye!")

except Exception as e:
    print("[E] There was an error! vvv\n")
    print(e)