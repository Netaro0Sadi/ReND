import json
import os


KNOWLEDGE_FILE = "data/knowledge.json"
ALIASES_FILE = "data/aliases.json"


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


def clean_subject(text):

    return (
        text.replace("?", "")
        .replace(".", "")
        .strip()
    )


def generate_aliases_for_question(question):

    aliases = []

    question = question.strip()

    if (
        question.startswith("What is ")
        and question.count(" ") <= 4
    ):

        subject = clean_subject(
            question.replace(
                "What is ",
                ""
            )
        )

        aliases.extend([
            f"Explain {subject}.",
            f"Define {subject}.",
            f"What does {subject} mean?",
            f"O que é {subject}?",
            f"Explique {subject}.",
            f"O que significa {subject}?"
        ])

    elif question.startswith("Who is "):

        subject = clean_subject(
            question.replace(
                "Who is ",
                ""
            )
        )

        aliases.extend([
            f"Tell me about {subject}.",
            f"Who exactly is {subject}?",
            f"Quem é {subject}?",
            f"Me fale sobre {subject}."
        ])

    elif question.startswith("Who was "):

        subject = clean_subject(
            question.replace(
                "Who was ",
                ""
            )
        )

        aliases.extend([
            f"Tell me about {subject}.",
            f"Quem foi {subject}?",
            f"Me fale sobre {subject}."
        ])

    elif (
        question.startswith("What does ")
        and (
            "stand for" in question
            or "mean" in question
        )
    ):

        subject = (
            question.replace(
                "What does ",
                ""
            )
            .replace("stand for", "")
            .replace("mean", "")
        )

        subject = clean_subject(
            subject
        )

        aliases.extend([
            f"What does {subject} mean?",
            f"What is the meaning of {subject}?",
            f"O que significa {subject}?",
            f"O que {subject} quer dizer?",
            f"Qual o significado de {subject}?"
        ])

    return list(
        dict.fromkeys(
            aliases
        )
    )


def generate_aliases():

    knowledge = load_json(
        KNOWLEDGE_FILE
    )

    aliases = load_json(
        ALIASES_FILE
    )

    added = 0

    for question in knowledge.keys():

        generated = generate_aliases_for_question(
            question
        )

        if not generated:
            continue

        if question not in aliases:

            aliases[question] = []

        for alias in generated:

            if alias not in aliases[question]:

                aliases[question].append(
                    alias
                )

                added += 1

    save_json(
        ALIASES_FILE,
        aliases
    )

    print("Alias generation completed.")
    print(f"New aliases added: {added}")
    print(f"Questions with aliases: {len(aliases)}")


generate_aliases()