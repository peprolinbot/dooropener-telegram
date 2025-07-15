# dooropener-telegram
A client for [door-dumb-api](https://codeberg.org/peprolinbot/door-dumb-api) that allows to use a Telegram bot to simply open the door. The bot used to do a few more things (check the `old` branch if interested), but if you want anything more advanced, you should check [Home assistant](https://www.home-assistant.io/) as this is meant to be extremly simple (I run it at my grandparents' country house, where there are limited resources).

## ⚠️ DEPRECATION NOTICE
I no longer used this (altough it should still work, but keep in mind this was developed when I was 13 and poorly patched over the years) and therefore i will not update it (I seriously doubt anyone would want to use this, but feel free to fork). My grandparents bought a new door opener and now there is  fiber at the house, so **we now use** Home Assistant and [tg-ha-door](https://github.com/peprolinbot/tg-ha-door). 

## 🔧 Deploy it 

###  🐳 With Docker (Recommended)

This is quick, easy and simple (if everything is going to be on a Pi, you should make yourself a `docker-compose.yml`):

1. First, you need a [door-dumb-api](https://codeberg.org/peprolinbot/door-dumb-api) instance. Check that README to learn how to spin one up

2. Then, you can setup the basic configuration (check `config.example.json`).

3. Then you can use this docker command:
```bash
docker run -d --name dooropener-telegram -v /tmp/config:/app/config ghcr.io/peprolinbot/dooropener-telegram
```

#### Environment Variables

| Name              | Description                                                                                                         |
|-------------------|-----------------------------------------------------------------------------|
| `CONFIG_FILE`     | Path to the json file with the basic config _(Default: "config/config.json")|

#### Configuration values
- `telegram`
    - `bot_token`: The token @BotFather gave you
    - `log_channel_id`: Id of the channel where all the events will be logged
    - `key_channel_id`: Id of the channel whose members should be able to use the bot
    - `bot_name`: A name for your bot
    - `language`: The language code you want the messages to be sent in (es/eng)
- `door-dumb-api`
    - `base_url`: The base url of the door-dumb-api instance
    - `token`: A token for door-dumb-api(check that README)
    - `door_id`: The door_id that will be controlled by the bot
    - `wait_to_close_time`: This is **optional**, if specified it will override the value specified for the door in door-dumb-api

#### Build the image
```bash
git clone https://github.com/peprolinbot/dooropener-telegram
cd dooropener-telegram
docker build -t dooropener-telegram .
```

### 💪🏻 Without Docker
Only use this for development unless you know what you're doing.

```bash
git clone https://github.com/peprolinbot/dooropener-telegram
cd dooropener-telegram
python3 main.py
```
