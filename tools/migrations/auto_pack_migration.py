import os
import json
import shutil
import sys

sys.path.append(".")

from modules.storage import load_data
from modules.router import suggest_pack
from modules.semantic_search import find_question_pack


PACKS_FOLDER = "data/knowledge_packs"
BACKUP_FOLDER = "data/knowledge_packs_backup"


def load_pack(pack_name):

    file_path = os.path.join(
        PACKS_FOLDER,
        f"{pack_name}.json"
    )

    if not os.path.exists(file_path):

        return {}

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_pack(
    pack_name,
    data
):

    file_path = os.path.join(
        PACKS_FOLDER,
        f"{pack_name}.json"
    )

    with open(
        file_path,
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


def main():

    print()
    print(
        "ReND Auto Pack Migration"
    )
    print()

    create_backup()

    knowledge = load_data()

    migrated = 0

    for question, answer in knowledge.items():

        current_pack = find_question_pack(
            question
        )

        if current_pack:

            continue

        suggested_pack = suggest_pack(
            question
        )

        pack_data = load_pack(
            suggested_pack
        )

        if question in pack_data:

            continue

        pack_data[
            question
        ] = answer

        save_pack(
            suggested_pack,
            pack_data
        )

        migrated += 1

        print(
            f"[{migrated}] "
            f"{question}"
        )

        print(
            f"    -> "
            f"{suggested_pack}"
        )

    print()
    print(
        "=" * 60
    )

    print(
        f"Migrated: {migrated}"
    )

    print(
        "Backup folder:"
    )

    print(
        BACKUP_FOLDER
    )

    print(
        "=" * 60
    )

    print()
    print(
        "Run /reload afterwards."
    )


if __name__ == "__main__":

    main()