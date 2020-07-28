import os

approved = False
avaliableLanguages = ["es", "eng"]

selection = input("Are you sure you are running this in the root of the repository? [S/n] ")
if selection == "" or selection == "S" or selection == "s":
    print("[i] Perfect!")
else:
    print("[!] Exiting...")
    exit()

try:
    while not approved:
        token = input("Enter the token @BotFather gave you: ")
        botName = input("Enter a name for your bot: ")
        logChannelId = input("Id of the channel where all the events will be logged: ")
        keyChannelId = input("Id of the channel in which it's members should be able to use the bot: ")
        lang = input("Enter the language code you want [es/eng]: ")
        while not lang in avaliableLanguages:
            print("Language not avaliable")
            lang = input("Enter the language code you want [es/eng]: ")
        gpioPin = input("Enter the number of the GPIO pin you have your relay connected to. 17, for example. Be careful: ")
        btnPressTime = input("Enter the time(in seconds) the relay should be open when simulating a button pressing on your remote.(Recommended and default: 0.5): ")
        if btnPressTime == "":
            btnPressTime = 0.5
        else:
            try:
                btnPressTime = int(btnPressTime)
            except:
                try:
                    btnPressTime = float(btnPressTime)
                except:
                    pass
            while not isinstance(btnPressTime, int) and not isinstance(btnPressTime, float):
                print("Incorrect input. Be sure to use no spaces and for decimal numbers use \".\" instead of \",\"")
                btnPressTime = input("Enter the time(in seconds) the relay should be open when simulating a button pressing on your remote.(Recommended and default: 0.5): ")
                if btnPressTime == "":
                    btnPressTime = 0.5
                try:
                    btnPressTime = int(btnPressTime)
                except:
                    try:
                        btnPressTime = float(btnPressTime)
                    except:
                        pass
        btnPressTime = str(btnPressTime)
        waitToCloseTime = input("Enter the time(in seconds) the door should wait before closing itself when using /open command.(Recommended and default: 60): ")
        if waitToCloseTime == "":
            waitToCloseTime = 60
        else:
            try:
                waitToCloseTime = int(waitToCloseTime)
            except:
                try:
                    waitToCloseTime = float(waitToCloseTime)
                except:
                    pass
            while not isinstance(waitToCloseTime, int) and not isinstance(waitToCloseTime, float):
                print("Incorrect input. Be sure to use no spaces and for decimal numbers use \".\" instead of \",\"")
                waitToCloseTime = input("Enter the time(in seconds) the door should wait before closing itself when using /open command.(Recommended and default: 60): ")
                if waitToCloseTime == "":
                    waitToCloseTime = 60
                try:
                    waitToCloseTime = int(waitToCloseTime)
                except:
                    try:
                        waitToCloseTime = float(waitToCloseTime)
                    except:
                        pass
        waitToCloseTime = str(waitToCloseTime)
        lockFilePath = input("Enter the path where the lockFile should be created and checked for existance. Be sure to have the neccesary permissions: ")

        print("Ok. Check if this information is ok:")
        print("Token: [" + token + "]")
        print("Bot name: [" + botName + "]")
        print("Log channel id: [" + logChannelId + "]")
        print("Key channel id: [" + keyChannelId + "]")
        print("Language: [" + lang + "]")
        print("GPIO pin: [" + gpioPin + "]")
        print("Button press time: [" + btnPressTime + "]")
        print("Wait to close time: [" + waitToCloseTime + "]")
        print("Lock file path: [" + lockFilePath + "]")
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
    with open("config/variables.py", "w") as f:
        f.write('#The name of your bot. It\'ll be used for presenting itself\nbotName = ' + botName + '\n#Time(in seconds) the relay should be open when simulating a button pressing on your remote.(Recommended and default: 0.5).\nbtnPressTime = '+ btnPressTime +'\n#Time(in seconds) the door should wait before closing itself when using /open command.(Recommended and default: 60).\nwaitToCloseTime = '+ waitToCloseTime + '\n#Path where the lockFile should be created and checked for existance. Be sure to have the neccesary permissions.\nlockFilePath = "' + lockFilePath + '"')
        f.close()
    print("[i] Succesfull!")
    print("[i] Keep in mind that all this variables can be changed whenever you want at config/telegram.py and config/language.py.")
    print("[i] Bye!")

except Exception as e:
    print("[E] There was an error! vvv\n")
    print(e)
