import os

approved = False
avaliable_languages = ["es", "eng"]

selection = input("Are you sure you are running this in the root of the repository? [Y/n] ")
if selection == "" or selection == "Y" or selection == "y":
    print("[i] Perfect!")
else:
    print("[!] Exiting...")
    exit()

try:
    while not approved:
        token = input("Enter the token @BotFather gave you: ")
        bot_name = input("Enter a name for your bot: ")
        log_channel_id = input("Id of the channel where all the events will be logged: ")
        key_channel_id = input("Id of the channel in which it's members should be able to use the bot: ")
        lang = input("Enter the language code you want [es/eng]: ")
        while not lang in avaliable_languages:
            print("Language not avaliable")
            lang = input("Enter the language code you want [es/eng]: ")
        gpio_pin = input("Enter the number of the GPIO pin you have your relay connected to. 17, for example. Be careful: ")
        btn_press_time = input("Enter the time(in seconds) the relay should be open when simulating a button pressing on your remote.(Recommended and default: 0.5): ")
        if btn_press_time == "":
            btn_press_time = 0.5
        else:
            try:
                btn_press_time = int(btn_press_time)
            except:
                try:
                    btn_press_time = float(btn_press_time)
                except:
                    pass
            while not isinstance(btn_press_time, int) and not isinstance(btn_press_time, float):
                print("Incorrect input. Be sure to use no spaces and for decimal numbers use \".\" instead of \",\"")
                btn_press_time = input("Enter the time(in seconds) the relay should be open when simulating a button pressing on your remote.(Recommended and default: 0.5): ")
                if btn_press_time == "":
                    btn_press_time = 0.5
                try:
                    btn_press_time = int(btn_press_time)
                except:
                    try:
                        btn_press_time = float(btn_press_time)
                    except:
                        pass
        btn_press_time = str(btn_press_time)
        wait_to_close_time = input("Enter the time(in seconds) the door should wait before closing itself when using /open command.(Recommended and default: 60): ")
        if wait_to_close_time == "":
            wait_to_close_time = 60
        else:
            try:
                wait_to_close_time = int(wait_to_close_time)
            except:
                try:
                    wait_to_close_time = float(wait_to_close_time)
                except:
                    pass
            while not isinstance(wait_to_close_time, int) and not isinstance(wait_to_close_time, float):
                print("Incorrect input. Be sure to use no spaces and for decimal numbers use \".\" instead of \",\"")
                wait_to_close_time = input("Enter the time(in seconds) the door should wait before closing itself when using /open command.(Recommended and default: 60): ")
                if wait_to_close_time == "":
                    wait_to_close_time = 60
                try:
                    wait_to_close_time = int(wait_to_close_time)
                except:
                    try:
                        wait_to_close_time = float(wait_to_close_time)
                    except:
                        pass
        wait_to_close_time = str(wait_to_close_time)
        lock_file_path = input("Enter the path where the lockFile should be created and checked for existance. Be sure to have the neccesary permissions: ")

        print("Ok. Check if this information is ok:")
        print("Token: [" + token + "]")
        print("Bot name: [" + bot_name + "]")
        print("Log channel id: [" + log_channel_id + "]")
        print("Key channel id: [" + key_channel_id + "]")
        print("Language: [" + lang + "]")
        print("GPIO pin: [" + gpio_pin + "]")
        print("Button press time: [" + btn_press_time + "]")
        print("Wait to close time: [" + wait_to_close_time + "]")
        print("Lock file path: [" + lock_file_path + "]")
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
        f.write('#The telegram bot token that you obtained from @BotFather\ntoken = "'+ token +'"\n\n#Channel where all the events will be logged\nlog_channel_id = "'+ log_channel_id +'"\n\n#Channel in which it\'s members should be able to use the bot\nkey_channel_id = "'+ key_channel_id +'"')
        f.close()
    with open("config/language.py", "w") as f:
        f.write('#Language selection. Can be "es" or "eng".\nlang = "'+ lang +'"')
        f.close()
    with open("config/gpio.py", "w") as f:
        f.write('#Number of the gpio where the relay is connected.\ngpio_pin = '+ gpio_pin)
        f.close()
    with open("config/variables.py", "w") as f:
        f.write('#The name of your bot. It\'ll be used for presenting itself\nbot_name = "' + bot_name + '"\n#Time(in seconds) the relay should be open when simulating a button pressing on your remote.(Recommended and default: 0.5).\nbtn_press_time = '+ btn_press_time +'\n#Time(in seconds) the door should wait before closing itself when using /open command.(Recommended and default: 60).\nwait_to_close_time = '+ wait_to_close_time + '\n#Path where the lockFile should be created and checked for existance. Be sure to have the neccesary permissions.\nlock_file_path = "' + lock_file_path + '"')
        f.close()
    print("[i] Creating audios dir if it doesn't exist...")
    if not os.path.isdir('./audios'):
        os.mkdir("audios")
    print("[i] Succesfull!")
    print("[i] Keep in mind that all this variables can be changed whenever you want at config/telegram.py and config/language.py.")
    print("[i] Bye!")

except Exception as e:
    print("[E] There was an error! vvv\n")
    print(e)
