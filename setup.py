import os

approved = False

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
        print("Ok. Check if this information is ok:")
        print("Token: [" + token + "]")
        print("Log channel id: [" + logChannelId + "]")
        print("Key channel id: [" + keyChannelId + "]")
        selection = input("Is this correct [S/n] ")
        if selection == "" or selection == "S" or selection == "s":
            approved = True
        else:
            approved = False
    print("[i] Creating config dir...")
    os.mkdir("config")
    print("[i] Creating config files...")
    #Writing content to the files
    with open("config/telegram.py", "w") as f:
        f.write('#The telegram bot token that you obtained from @BotFather\ntoken = "'+ token +'"\n\n#Channel where all the events will be logged\nlogChannelId = "'+ logChannelId +'"\n\n#Channel in which it\'s members should be able to use the bot\nkeyChannelId = "'+ keyChannelId +'"')
        f.close()
    print("[i] Succesfull!")
    print("[i] Keep in mind that all this variables can be changed whenever you want at config/telegram.py.")
    print("[i] Bye!")

except Exception as e:
    print("[E] There was an error! vvv\n")
    print(e)