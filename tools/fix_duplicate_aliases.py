import json
import os


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


def choose_owner(
    alias,
    questions
):

    for question in questions:

        if question in PREFERRED_QUESTIONS:

            return question

    shortest = min(
        questions,
        key=len
    )

    return shortest


def main():

    aliases = load_aliases()

    alias_map = {}

    for question, alias_list in aliases.items():

        for alias in alias_list:

            key = alias.lower().strip()

            if key not in alias_map:

                alias_map[key] = []

            alias_map[key].append(
                question
            )

    duplicates = []

    removed = 0

    for alias, questions in alias_map.items():

        unique_questions = list(
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

        for question in unique_questions:

            if question == owner:

                continue

        alias_list = aliases.get(
            question,
            []
        )

        for original_alias in alias_list[:]:

            if original_alias.lower().strip() == alias:

                aliases[
                    question
                ].remove(
                    original_alias
                )

                removed += 1

    save_aliases(
        aliases
    )

    print()
    print("=" * 70)
    print("ReND Duplicate Alias Fixer")
    print("=" * 70)
    print()

    print(
        f"Duplicate groups: "
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