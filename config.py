from os import getenv
from os.path import exists
import json


def _load_config(env_var: str, default: str):
    """
    Loads json from the file-path specified in the environment var provided
    """
    file_path = getenv(env_var, default)
    if not exists(file_path):
        raise FileNotFoundError(
            f"{file_path} was not found. Please create it and/or set the '{env_var}' environment variable."
        )

    with open(file_path) as f:
        data = json.load(f)

    return data


_config_data = _load_config("CONFIG_FILE", "config/config.json")
_config = _config_data["config"]
telegram_bot_token = _config["telegram"]["bot_token"]
log_channel_id = _config["telegram"]["log_channel_id"]
key_channel_id = _config["telegram"]["key_channel_id"]
bot_name = _config["telegram"]["bot_name"]
language = _config["telegram"]["language"]
dumbdoorapi_base_url = _config["dumb-door-api"]["base_url"]
dumbdoorapi_token = _config["dumb-door-api"]["token"]
door_id = _config["dumb-door-api"]["door_id"]
wait_to_close_time = _config["dumb-door-api"].get("wait_to_close_time")
