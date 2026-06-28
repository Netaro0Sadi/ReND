import json
import os
import sys


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from backup import create_backup


ALIASES_FILE = "data/aliases.json"


PREFERRED_QUESTIONS = {
    "What is an API?":
        "What does API stand for?",

    "What is HTTP?":
        "What does HTTP stand for?",

    "What is RAM?":
        "What does RAM stand for?",

    "What is SQL?":
        "What does SQL stand for?",

    "What is DNS?":
        "What does DNS stand for?",

    "What is SSD?":
        "What does SSD stand for?",

    "What is HDD?":
        "What does HDD stand for?",

    "What is BIOS?":
        "What does BIOS stand for?"
}


def load_aliases():

    if not os.path.exists(
        ALIASES_FILE
    ):

        return {}

    with open(
        ALIASES_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_aliases(data):

    with open(
        ALIASES_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def normalize_alias(alias):

    return (
        alias.lower()
        .strip()
    )


def choose_owner(
    alias,
    questions
):

    for question in questions:

        if question in PREFERRED_QUESTIONS:

            preferred = PREFERRED_QUESTIONS[
                question
            ]

            if preferred in questions:

                return preferred

            return question

    return min(
        questions,
        key=len
    )


def build_alias_map(aliases):

    alias_map = {}

    for question, alias_list in aliases.items():

        for alias in alias_list:

            key = normalize_alias(
                alias
            )

            if key not in alias_map:

                alias_map[
                    key
                ] = []

            alias_map[
                key
            ].append(
                question
            )

    return alias_map


def find_duplicate_aliases(aliases):

    alias_map = build_alias_map(
        aliases
    )

    duplicates = []

    for alias, questions in alias_map.items():

        unique_questions = sorted(
            set(questions)
        )

        if len(unique_questions) <= 1:

            continue

        owner = choose_owner(
            alias,
            unique_questions
        )

        duplicates.append(
            (
                alias,
                owner,
                unique_questions
            )
        )

    return duplicates


def remove_duplicate_aliases(
    aliases,
    duplicates
):

    removed = 0

    for alias, owner, questions in duplicates:

        for question in questions:

            if question == owner:

                continue

            alias_list = aliases.get(
                question,
                []
            )

            for original_alias in alias_list[:]:

                if normalize_alias(
                    original_alias
                ) == alias:

                    aliases[
                        question
                    ].remove(
                        original_alias
                    )

                    removed += 1

    return removed


def main():

    print()
    print("=" * 70)
    print("ReND Duplicate Alias Fixer")
    print("=" * 70)
    print()

    aliases = load_aliases()

    if not aliases:

        print(
            "No aliases found."
        )

        return

    duplicates = find_duplicate_aliases(
        aliases
    )

    if not duplicates:

        print(
            "No duplicate aliases found."
        )

        return

    print(
        f"Duplicate groups found: "
        f"{len(duplicates)}"
    )

    print()
    print(
        "Creating backup before changes..."
    )

    create_backup()

    removed = remove_duplicate_aliases(
        aliases,
        duplicates
    )

    save_aliases(
        aliases
    )

    print()
    print(
        f"Duplicate groups fixed: "
        f"{len(duplicates)}"
    )

    print(
        f"Aliases removed: "
        f"{removed}"
    )

    print()

    for alias, owner, questions in duplicates[:20]:

        print(
            f"Alias: {alias}"
        )

        print(
            f"Owner: {owner}"
        )

        print(
            "Removed from:"
        )

        for question in questions:

            if question != owner:

                print(
                    f"  - {question}"
                )

        print()

    print("=" * 70)


if __name__ == "__main__":

    main()