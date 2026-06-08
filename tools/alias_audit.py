import json
import os


ALIASES_FILE = "data/aliases.json"
KNOWLEDGE_FILE = "data/knowledge.json"


def load_json(path):

    if not os.path.exists(path):

        return {}

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def main():

    aliases = load_json(
        ALIASES_FILE
    )

    knowledge = load_json(
        KNOWLEDGE_FILE
    )

    no_aliases = []
    low_aliases = []
    duplicate_aliases = []
    orphan_aliases = []

    all_aliases = {}

    for question in knowledge:

        if question not in aliases:

            no_aliases.append(
                question
            )

            continue

        alias_list = aliases[
            question
        ]

        if len(alias_list) < 3:

            low_aliases.append(
                (
                    question,
                    len(alias_list)
                )
            )

        for alias in alias_list:

            key = alias.lower()

            if key not in all_aliases:

                all_aliases[key] = []

            all_aliases[key].append(
                question
            )

    for alias, questions in all_aliases.items():

        unique_questions = set(
            questions
        )

        if len(unique_questions) > 1:

            duplicate_aliases.append(
                (
                    alias,
                    list(unique_questions)
                )
            )

    for question in aliases:

        if question not in knowledge:

            orphan_aliases.append(
                question
            )

    print()
    print("=" * 70)
    print("ReND Alias Audit")
    print("=" * 70)
    print()

    print("Summary")
    print("-" * 70)

    print(
        f"Knowledge questions: "
        f"{len(knowledge)}"
    )

    print(
        f"Questions with aliases: "
        f"{len(aliases)}"
    )

    print(
        f"Questions without aliases: "
        f"{len(no_aliases)}"
    )

    print(
        f"Questions with less than 3 aliases: "
        f"{len(low_aliases)}"
    )

    print(
        f"Duplicate aliases: "
        f"{len(duplicate_aliases)}"
    )

    print(
        f"Orphan aliases: "
        f"{len(orphan_aliases)}"
    )

    if no_aliases:

        print()
        print("-" * 70)
        print("Questions without aliases")
        print("-" * 70)

        for question in no_aliases[:30]:

            print(question)

        if len(no_aliases) > 30:

            print()
            print(
                f"...and {len(no_aliases)-30} more"
            )

    if low_aliases:

        print()
        print("-" * 70)
        print("Questions with less than 3 aliases")
        print("-" * 70)

        for question, count in low_aliases[:30]:

            print(
                f"{question} ({count})"
            )

        if len(low_aliases) > 30:

            print()
            print(
                f"...and {len(low_aliases)-30} more"
            )

    if duplicate_aliases:

        print()
        print("-" * 70)
        print("Duplicate aliases")
        print("-" * 70)

        for alias, questions in duplicate_aliases[:20]:

            print(
                f"Alias: {alias}"
            )

            for question in questions:

                print(
                    f"  - {question}"
                )

            print()

        if len(duplicate_aliases) > 20:

            print(
                f"...and {len(duplicate_aliases)-20} more"
            )

    if orphan_aliases:

        print()
        print("-" * 70)
        print("Orphan aliases")
        print("-" * 70)

        for question in orphan_aliases:

            print(question)

    print()
    print("=" * 70)
    print("End of audit")
    print("=" * 70)


if __name__ == "__main__":

    main()