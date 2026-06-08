import json
import os


KNOWLEDGE_FILE = "data/knowledge.json"
PACKS_FOLDER = "data/knowledge_packs"


def load_json(file_path):

    if os.path.exists(file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    return {}


def save_json(file_path, data):

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def load_all_packs():

    merged = {}

    if not os.path.exists(
        PACKS_FOLDER
    ):
        return merged

    for filename in os.listdir(
        PACKS_FOLDER
    ):

        if not filename.endswith(
            ".json"
        ):
            continue

        path = os.path.join(
            PACKS_FOLDER,
            filename
        )

        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(
                    file
                )

                merged.update(
                    data
                )

                print(
                    f"Loaded pack: {filename}"
                )

        except Exception as error:

            print(
                f"Error loading {filename}: {error}"
            )

    return merged


def import_knowledge():

    knowledge = load_json(
        KNOWLEDGE_FILE
    )

    new_knowledge = load_all_packs()

    added = 0
    skipped = 0

    for question, answer in (
        new_knowledge.items()
    ):

        if question not in knowledge:

            knowledge[
                question
            ] = answer

            added += 1

        else:

            skipped += 1

    save_json(
        KNOWLEDGE_FILE,
        knowledge
    )

    print("\nImport completed.")
    print(
        f"Added: {added}"
    )
    print(
        f"Skipped: {skipped}"
    )
    print(
        f"Total knowledge: {len(knowledge)}"
    )


import_knowledge()