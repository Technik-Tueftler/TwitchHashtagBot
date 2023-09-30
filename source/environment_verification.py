#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path

from source.constants import (
    CONFIGURATION_FILE_PATH,
    LOG_FILE_PATH,
    HASHTAG_MAX_LENGTH,
    HASHTAG_MIN_LENGTH,
    TWEET_MAX_LENGTH,
    TWEET_START_STRING,
    TWEET_END_STRING,
)

client_id = os.getenv("TW_CLIENT_ID", None)
token = os.getenv("TW_TOKEN", None)
nickname = os.getenv("TW_NICKNAME", None)
init_channels = os.getenv("TW_INIT_CHANNELS", None)

discord_username = os.getenv("DC_USER_NAME", None)
webhook_url = os.getenv("DC_WEBHOOK_URL", None)

tweet_settings = {
    "hashtag_max_length": HASHTAG_MAX_LENGTH,
    "hashtag_min_length": HASHTAG_MIN_LENGTH,
    "tweet_max_length": TWEET_MAX_LENGTH,
    "tweet_start_string": TWEET_START_STRING,
    "tweet_end_string": TWEET_END_STRING
}

app_settings = {
    "ID": client_id,
    "token": token,
    "nickname": nickname,
    "channels": None,
    "discord_username": discord_username,
    "webhook_url": webhook_url,
    "dc_available": False,
}


def check_twitter_settings():
    if not Path(CONFIGURATION_FILE_PATH).exists(): return
    with open(CONFIGURATION_FILE_PATH, encoding="utf-8") as file:
        data = json.load(file)
        if not "twitch" in data: return
        if "hashtag_max_length" in data["twitter"]:
            tweet_settings["len_hash_max"] = int(data["twitter"]["hashtag_max_length"])
        if "hashtag_min_length" in data["twitter"]:
            tweet_settings["len_hash_min"] = int(data["twitter"]["hashtag_min_length"])
        if "tweet_max_length" in data["twitter"]:
            tweet_settings["tweet_max_length"] = int(data["twitter"]["tweet_max_length"])
        if "tweet_start_string" in data["twitter"]:
            tweet_settings["tweet_start_string"] = data["twitter"]["tweet_start_string"]
        if "tweet_end_string" in data["twitter"]:
            tweet_settings["tweet_end_string"] = data["twitter"]["tweet_end_string"]


def check_env_available() -> bool:
    if None not in (client_id, token, nickname, init_channels):
        return True
    return False


def check_config_available() -> bool:
    if not Path(CONFIGURATION_FILE_PATH).exists():
        return False
    with open(CONFIGURATION_FILE_PATH, encoding="utf-8") as file:
        data = json.load(file)
        if "twitch" not in data:
            return False
        return True


def twitch_setting_verification() -> bool:
    if check_env_available():
        app_settings["channels"] = init_channels.split(",")
        return True
    if check_config_available():
        with open(CONFIGURATION_FILE_PATH, encoding="utf-8") as file:
            data = json.load(file)
        app_settings["ID"] = data["twitch"]["client_id"]
        app_settings["token"] = data["twitch"]["token"]
        app_settings["nickname"] = data["twitch"]["nickname"]
        app_settings["channels"] = data["twitch"]["init_channels"].split(",")
        return True
    with open(LOG_FILE_PATH, "a") as file:
        file.write("The login data for twitch is missing or incomplete.")
    return False


def check_dc_env_available() -> bool:
    if None not in (discord_username, webhook_url):
        return True
    return False


def check_dc_config_available() -> bool:
    if not Path(CONFIGURATION_FILE_PATH).exists():
        return False
    with open(CONFIGURATION_FILE_PATH, encoding="utf-8") as file:
        data = json.load(file)
        if "discord" not in data:
            return False
        return True


def discord_setting_verification() -> None:
    if check_dc_env_available():
        app_settings["dc_available"] = True
        return
    if check_dc_config_available():
        with open(CONFIGURATION_FILE_PATH, encoding="utf-8") as file:
            data = json.load(file)
        app_settings["discord_username"] = data["discord"]["discord_username"]
        app_settings["webhook_url"] = data["discord"]["webhook_url"]
        app_settings["dc_available"] = True
        return
    with open(LOG_FILE_PATH, "a") as file:
        file.write("The login data for discord is missing or incomplete.")
    app_settings["dc_available"] = False
    return


def main() -> None:
    twitch_setting_verification()


if __name__ == "__main__":
    main()
