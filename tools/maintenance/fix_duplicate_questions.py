import json
import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from backup import create_backup


PACKS_FOLDER = "data/knowledge_packs"


PACK_PRIORITY = [
    "rend_core",
    "programming",
    "technology",
    "science",
    "history",
    "geography",
    "sports",
    "fictional_characters",
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

    if not os.path.exists(path):
        return {}

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


def load_packs():

    packs = {}

    if not os.path.exists(
        PACKS_FOLDER
    ):

        return packs

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

        packs[
            pack_name
        ] = load_json(
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


def find_duplicate_questions(packs):

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

    return {
        question: locations
        for question, locations in question_locations.items()
        if len(locations) > 1
    }


def main():

    print()
    print(
        "ReND Duplicate Question Fixer"
    )
    print()

    packs = load_packs()

    if not packs:

        print(
            "No knowledge packs found."
        )

        return

    duplicates = find_duplicate_questions(
        packs
    )

    if not duplicates:

        print(
            "No duplicate questions found."
        )

        return

    print(
        f"Duplicate questions found: "
        f"{len(duplicates)}"
    )

    print()
    print(
        "Creating backup before changes..."
    )

    create_backup()

    fixed = 0
    removed = 0

    for question, locations in duplicates.items():

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

                removed += 1

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
        "Duplicate Fix Summary"
    )

    print(
        "=" * 60
    )

    print(
        f"Duplicate groups fixed: {fixed}"
    )

    print(
        f"Questions removed: {removed}"
    )

    print(
        "Backup: data/backups"
    )

    print(
        "=" * 60
    )


if __name__ == "__main__":

    main()