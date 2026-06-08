import json
import os

PROFILE_FILE = "data/profile.json"


def load_profile():

    if os.path.exists(PROFILE_FILE):

        with open(
            PROFILE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    return {}


def save_profile(profile):

    with open(
        PROFILE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            profile,
            file,
            ensure_ascii=False,
            indent=4
        )


class UserProfile:

    def __init__(self):

        self.data = load_profile()

    def remember(self, key, value):

        self.data[key] = value

        save_profile(
            self.data
        )

    def recall(self, key):

        return self.data.get(key)

    def forget(self, key):

        if key in self.data:

            del self.data[key]

            save_profile(
                self.data
            )

            return True

        return False

    def all_data(self):

        return self.data