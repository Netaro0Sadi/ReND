import json
import os


SETTINGS_FILE = "data/settings.json"


def load_settings():

    if os.path.exists(
        SETTINGS_FILE
    ):

        with open(
            SETTINGS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    return {
        "personality": "normal"
    }


def save_settings(settings):

    with open(
        SETTINGS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            settings,
            file,
            ensure_ascii=False,
            indent=4
        )


def get_setting(
    key,
    default=None
):

    settings = load_settings()

    return settings.get(
        key,
        default
    )


def set_setting(
    key,
    value
):

    settings = load_settings()

    settings[key] = value

    save_settings(
        settings
    )