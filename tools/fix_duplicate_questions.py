import os
import json
import shutil


PACKS_FOLDER = "data/knowledge_packs"
BACKUP_FOLDER = "data/knowledge_packs_duplicate_backup"


PACK_PRIORITY = [
    "rend_core",
    "programming",
    "technology",
    "science",
    "history",
    "geography",
    "sports",
    "pop_culture",
    "math",
    "general"
]


MANUAL_KEEP = {
    "How many players are on a basketball team?": "sports",
    "What is an API?": "programming",
    "What is an algorithm?": "programming",
    "What is cybersecurity?": "technology",
    "What is encryption?": "technology"
}


def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_json(path, data):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def create_backup():

    if os.path.exists(
        BACKUP_FOLDER
    ):

        shutil.rmtree(
            BACKUP_FOLDER
        )

    shutil.copytree(
        PACKS_FOLDER,
        BACKUP_FOLDER
    )

    print(
        "Backup created."
    )


def load_packs():

    packs = {}

    for file_name in os.listdir(
        PACKS_FOLDER
    ):

        if not file_name.endswith(
            ".json"
        ):

            continue

        pack_name = file_name.replace(
            ".json",
            ""
        )

        path = os.path.join(
            PACKS_FOLDER,
            file_name
        )

        packs[pack_name] = load_json(
            path
        )

    return packs


def save_packs(packs):

    for pack_name, data in packs.items():

        path = os.path.join(
            PACKS_FOLDER,
            f"{pack_name}.json"
        )

        save_json(
            path,
            data
        )


def choose_pack(
    question,
    locations
):

    if question in MANUAL_KEEP:

        preferred = MANUAL_KEEP[
            question
        ]

        if preferred in locations:

            return preferred

    for pack in PACK_PRIORITY:

        if pack in locations:

            return pack

    return locations[0]


def main():

    print()
    print(
        "ReND Duplicate Fixer"
    )
    print()

    create_backup()

    packs = load_packs()

    question_locations = {}

    for pack_name, data in packs.items():

        for question in data.keys():

            if question not in question_locations:

                question_locations[
                    question
                ] = []

            question_locations[
                question
            ].append(
                pack_name
            )

    fixed = 0

    for question, locations in question_locations.items():

        if len(locations) <= 1:

            continue

        keep_pack = choose_pack(
            question,
            locations
        )

        print(
            f"Duplicate: {question}"
        )

        print(
            f"Keeping in: {keep_pack}"
        )

        for pack_name in locations:

            if pack_name == keep_pack:

                continue

            if question in packs[pack_name]:

                del packs[pack_name][
                    question
                ]

                print(
                    f"Removed from: {pack_name}"
                )

        print()

        fixed += 1

    save_packs(
        packs
    )

    print(
        "=" * 60
    )

    print(
        f"Duplicates fixed: {fixed}"
    )

    print(
        f"Backup folder: {BACKUP_FOLDER}"
    )

    print(
        "=" * 60
    )


if __name__ == "__main__":

    main()