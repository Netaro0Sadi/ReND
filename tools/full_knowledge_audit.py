import os
import json


KNOWLEDGE_FILE = "data/knowledge.json"
ALIASES_FILE = "data/aliases.json"
PACKS_FOLDER = "data/knowledge_packs"


def load_json(path):

    if not os.path.exists(path):

        return {}

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def load_packs():

    packs = {}

    if not os.path.exists(PACKS_FOLDER):

        return packs

    for file_name in os.listdir(PACKS_FOLDER):

        if not file_name.endswith(".json"):

            continue

        path = os.path.join(
            PACKS_FOLDER,
            file_name
        )

        packs[
            file_name.replace(".json", "")
        ] = load_json(path)

    return packs


def main():

    knowledge = load_json(KNOWLEDGE_FILE)
    aliases = load_json(ALIASES_FILE)
    packs = load_packs()

    question_locations = {}
    empty_answers = []
    empty_packs = []
    pack_only_questions = []
    missing_aliases = []
    orphan_aliases = []

    for pack_name, data in packs.items():

        if len(data) == 0:

            empty_packs.append(pack_name)

        for question, answer in data.items():

            if question not in question_locations:

                question_locations[question] = []

            question_locations[question].append(pack_name)

            if not str(answer).strip():

                empty_answers.append(
                    (question, pack_name)
                )

            if question not in knowledge:

                pack_only_questions.append(
                    (question, pack_name)
                )

    duplicate_questions = [
        (question, locations)
        for question, locations in question_locations.items()
        if len(locations) > 1
    ]

    for question in knowledge.keys():

        if question not in aliases:

            missing_aliases.append(question)

    for question in aliases.keys():

        if question not in knowledge:

            orphan_aliases.append(question)

    total_pack_questions = sum(
        len(data)
        for data in packs.values()
    )

    print()
    print("=" * 70)
    print("ReND Full Knowledge Audit")
    print("=" * 70)
    print()

    print("Summary")
    print("-" * 70)
    print(f"Knowledge questions: {len(knowledge)}")
    print(f"Pack questions: {total_pack_questions}")
    print(f"Knowledge packs: {len(packs)}")
    print(f"Alias entries: {len(aliases)}")
    print(f"Duplicate questions: {len(duplicate_questions)}")
    print(f"Questions only in packs: {len(pack_only_questions)}")
    print(f"Questions without aliases: {len(missing_aliases)}")
    print(f"Orphan alias entries: {len(orphan_aliases)}")
    print(f"Empty answers: {len(empty_answers)}")
    print(f"Empty packs: {len(empty_packs)}")

    print()
    print("Pack sizes")
    print("-" * 70)

    for pack_name, data in sorted(packs.items()):

        print(f"{pack_name}: {len(data)}")

    if duplicate_questions:

        print()
        print("Duplicate questions")
        print("-" * 70)

        for index, (question, locations) in enumerate(
            duplicate_questions,
            start=1
        ):

            print(f"{index}. {question}")
            print("   Packs:")

            for location in locations:

                print(f"   - {location}")

            print()

    if pack_only_questions:

        print()
        print("Questions only in packs")
        print("-" * 70)

        for index, (question, pack_name) in enumerate(
            pack_only_questions,
            start=1
        ):

            print(f"{index}. {question}")
            print(f"   Pack: {pack_name}")
            print()

    if orphan_aliases:

        print()
        print("Orphan alias entries")
        print("-" * 70)

        for index, question in enumerate(
            orphan_aliases,
            start=1
        ):

            print(f"{index}. {question}")

    if empty_answers:

        print()
        print("Empty answers")
        print("-" * 70)

        for index, (question, pack_name) in enumerate(
            empty_answers,
            start=1
        ):

            print(f"{index}. {question}")
            print(f"   Pack: {pack_name}")
            print()

    if empty_packs:

        print()
        print("Empty packs")
        print("-" * 70)

        for index, pack_name in enumerate(
            empty_packs,
            start=1
        ):

            print(f"{index}. {pack_name}")

    print()
    print("=" * 70)
    print("End of audit")
    print("=" * 70)


if __name__ == "__main__":

    main()