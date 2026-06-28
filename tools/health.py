import json
import os


PACKS_FOLDER = "data/knowledge_packs"
ALIASES_FILE = "data/aliases.json"
BACKUP_FOLDER = "data/backups"


def check(message, success):

    status = "OK" if success else "FAIL"

    print(
        f"[{status}] {message}"
    )

    return success


def count_pack_questions():

    total = 0
    packs = 0

    if not os.path.exists(
        PACKS_FOLDER
    ):

        return 0, 0

    for file_name in os.listdir(
        PACKS_FOLDER
    ):

        if not file_name.endswith(
            ".json"
        ):

            continue

        packs += 1

        path = os.path.join(
            PACKS_FOLDER,
            file_name
        )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            total += len(
                json.load(file)
            )

    return total, packs


def count_aliases():

    if not os.path.exists(
        ALIASES_FILE
    ):

        return 0, 0

    with open(
        ALIASES_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        aliases = json.load(
            file
        )

    groups = len(
        aliases
    )

    total = sum(
        len(alias_list)
        for alias_list in aliases.values()
    )

    return groups, total


def latest_backup():

    if not os.path.exists(
        BACKUP_FOLDER
    ):

        return None

    files = os.listdir(
        BACKUP_FOLDER
    )

    if not files:

        return None

    return max(
        files,
        key=lambda file:
        os.path.getmtime(
            os.path.join(
                BACKUP_FOLDER,
                file
            )
        )
    )


def main():

    print("=" * 60)
    print("ReND Health Check")
    print("=" * 60)
    print()

    questions, packs = (
        count_pack_questions()
    )

    alias_groups, aliases = (
        count_aliases()
    )

    backup = latest_backup()

    checks = [

        check(
            "Knowledge Packs",
            packs > 0
        ),

        check(
            "Questions Loaded",
            questions > 0
        ),

        check(
            "Aliases Loaded",
            alias_groups > 0
        ),

        check(
            "Backup Folder",
            backup is not None
        )
    ]

    print()

    print("=" * 60)
    print("Statistics")
    print("=" * 60)

    print(
        f"Packs............... {packs}"
    )

    print(
        f"Questions........... {questions}"
    )

    print(
        f"Alias Groups........ {alias_groups}"
    )

    print(
        f"Aliases............. {aliases}"
    )

    if backup:

        print(
            f"Latest Backup....... {backup}"
        )

    else:

        print(
            "Latest Backup....... None"
        )

    print()

    print("=" * 60)

    health = (
        int(
            sum(checks)
            / len(checks)
            * 100
        )
    )

    print(
        f"System Health....... {health}%"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()