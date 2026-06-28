import json
import os
import re


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


def add_common_subject_aliases(aliases, subject):

    aliases.extend([
        f"Explain {subject}.",
        f"Define {subject}.",
        f"Tell me about {subject}.",
        f"What does {subject} mean?",
        f"What is the meaning of {subject}?",
        f"O que é {subject}?",
        f"Explique {subject}.",
        f"Defina {subject}.",
        f"Me fale sobre {subject}.",
        f"O que significa {subject}?"
    ])


def generate_aliases_for_question(question):

    aliases = []

    question = question.strip()

    # hello / greetings
    if question.lower() == "hello":

        aliases.extend([
            "hi",
            "hey",
            "oi",
            "olá",
            "ola",
            "e aí",
            "bom dia",
            "boa tarde",
            "boa noite"
        ])

        return list(dict.fromkeys(aliases))

    # What is X?
    match = re.match(
        r"^What is (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        add_common_subject_aliases(
            aliases,
            subject
        )

        return list(dict.fromkeys(aliases))

    # What are X?
    match = re.match(
        r"^What are (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"Explain {subject}.",
            f"Tell me about {subject}.",
            f"O que são {subject}?",
            f"Explique {subject}.",
            f"Me fale sobre {subject}."
        ])

        return list(dict.fromkeys(aliases))

    # Who is X?
    match = re.match(
        r"^Who is (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"Tell me about {subject}.",
            f"Who exactly is {subject}?",
            f"Who is {subject} exactly?",
            f"Quem é {subject}?",
            f"Me fale sobre {subject}.",
            f"Explique quem é {subject}."
        ])

        return list(dict.fromkeys(aliases))

    # Who was X?
    match = re.match(
        r"^Who was (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"Tell me about {subject}.",
            f"Who exactly was {subject}?",
            f"Who was {subject} exactly?",
            f"Quem foi {subject}?",
            f"Me fale sobre {subject}.",
            f"Explique quem foi {subject}."
        ])

        return list(dict.fromkeys(aliases))

    # What does X stand for / mean?
    match = re.match(
        r"^What does (.+) (stand for|mean)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"What does {subject} mean?",
            f"What is the meaning of {subject}?",
            f"What is {subject}?",
            f"O que significa {subject}?",
            f"O que {subject} quer dizer?",
            f"Qual o significado de {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # Capital questions
    match = re.match(
        r"^What is the capital of (.+)\?$",
        question
    )

    if match:

        place = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"What city is the capital of {place}?",
            f"Capital of {place}?",
            f"What is {place}'s capital?",
            f"Qual é a capital de {place}?",
            f"Qual a capital de {place}?",
            f"Capital de {place}?"
        ])

        return list(dict.fromkeys(aliases))

    # Continent questions
    match = re.match(
        r"^What continent is (.+) in\?$",
        question
    )

    if match:

        place = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"Which continent is {place} in?",
            f"What is the continent of {place}?",
            f"{place} is in which continent?",
            f"Em qual continente fica {place}?",
            f"Qual continente fica {place}?",
            f"{place} fica em qual continente?"
        ])

        return list(dict.fromkeys(aliases))

    # Currency questions
    match = re.match(
        r"^What is the currency of (.+)\?$",
        question
    )

    if match:

        place = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"What currency is used in {place}?",
            f"What money is used in {place}?",
            f"Currency of {place}?",
            f"Qual é a moeda de {place}?",
            f"Qual moeda é usada em {place}?",
            f"Moeda de {place}?"
        ])

        return list(dict.fromkeys(aliases))

    # How many X?
    match = re.match(
        r"^How many (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"What is the number of {subject}?",
            f"How much {subject}?",
            f"Quantos {subject}?",
            f"Quantas {subject}?",
            f"Qual é a quantidade de {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # How long X?
    match = re.match(
        r"^How long (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"What is the duration of {subject}?",
            f"Quanto tempo {subject}?",
            f"Qual é a duração de {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # How fast X?
    match = re.match(
        r"^How fast (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"What is the speed of {subject}?",
            f"Quão rápido {subject}?",
            f"Qual é a velocidade de {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # How old X?
    match = re.match(
        r"^How old (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"What is the age of {subject}?",
            f"Quantos anos tem {subject}?",
            f"Qual é a idade de {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # Why X?
    match = re.match(
        r"^Why (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"What is the reason {subject}?",
            f"Explain why {subject}.",
            f"Por que {subject}?",
            f"Explique por que {subject}."
        ])

        return list(dict.fromkeys(aliases))

    # Which X?
    match = re.match(
        r"^Which (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"What {subject}?",
            f"Qual {subject}?",
            f"Quais {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # Who invented X?
    match = re.match(
        r"^Who invented (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"Who created {subject}?",
            f"Who was the inventor of {subject}?",
            f"Quem inventou {subject}?",
            f"Quem criou {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # Who discovered X?
    match = re.match(
        r"^Who discovered (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"Who found {subject}?",
            f"Who was the discoverer of {subject}?",
            f"Quem descobriu {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # Who wrote X?
    match = re.match(
        r"^Who wrote (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"Who is the author of {subject}?",
            f"Quem escreveu {subject}?",
            f"Quem é o autor de {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # Who painted X?
    match = re.match(
        r"^Who painted (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"Who created the painting {subject}?",
            f"Who is the painter of {subject}?",
            f"Quem pintou {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # In which year X?
    match = re.match(
        r"^In which year (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"What year did {subject}?",
            f"When did {subject}?",
            f"Em que ano {subject}?",
            f"Quando {subject}?"
        ])

        return list(dict.fromkeys(aliases))
    
        # What color is X?
    match = re.match(
        r"^What color (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"Which color {subject}?",
            f"What is the color {subject}?",
            f"Qual é a cor {subject}?",
            f"Que cor {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # What gas X?
    match = re.match(
        r"^What gas (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"Which gas {subject}?",
            f"What kind of gas {subject}?",
            f"Qual gás {subject}?",
            f"Que gás {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # Are you X?
    match = re.match(
        r"^Are you (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"Você é {subject}?",
            f"Tu é {subject}?",
            f"Are you really {subject}?",
            f"Are you a {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # Can you X?
    match = re.match(
        r"^Can you (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"Você consegue {subject}?",
            f"Você pode {subject}?",
            f"Are you able to {subject}?",
            f"Can ReND {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # What was X?
    match = re.match(
        r"^What was (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"Explain {subject}.",
            f"Tell me about {subject}.",
            f"O que foi {subject}?",
            f"Explique {subject}.",
            f"Me fale sobre {subject}."
        ])

        return list(dict.fromkeys(aliases))

    # What kind of X?
    match = re.match(
        r"^What kind of (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"What type of {subject}?",
            f"Que tipo de {subject}?",
            f"Qual tipo de {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # What causes X?
    match = re.match(
        r"^What causes (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"What is the cause of {subject}?",
            f"Why does {subject} happen?",
            f"O que causa {subject}?",
            f"Por que {subject} acontece?"
        ])

        return list(dict.fromkeys(aliases))

    # Where was X born?
    match = re.match(
        r"^Where was (.+) born\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"Where was {subject} born?",
            f"What is {subject}'s birthplace?",
            f"Onde {subject} nasceu?",
            f"Onde nasceu {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # When was X born?
    match = re.match(
        r"^When was (.+) born\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"When was {subject} born?",
            f"What is {subject}'s birth date?",
            f"Quando {subject} nasceu?",
            f"Quando nasceu {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # What did X do?
    match = re.match(
        r"^What did (.+) do\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"What was {subject} known for?",
            f"What is {subject} famous for?",
            f"O que {subject} fez?",
            f"Pelo que {subject} ficou conhecido?"
        ])

        return list(dict.fromkeys(aliases))

    # When did X?
    match = re.match(
        r"^When did (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(
            match.group(1)
        )

        aliases.extend([
            f"What year did {subject}?",
            f"At what time did {subject}?",
            f"Quando {subject}?",
            f"Em que ano {subject}?"
        ])

        return list(dict.fromkeys(aliases))
    match = re.match(
        r"^Who co-founded (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(match.group(1))

        aliases.extend([
            f"Who helped create {subject}?",
            f"Who was one of the founders of {subject}?",
            f"Quem cofundou {subject}?",
            f"Quem ajudou a fundar {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # Who created X?
    match = re.match(
        r"^Who created (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(match.group(1))

        aliases.extend([
            f"Who made {subject}?",
            f"Who was the creator of {subject}?",
            f"Quem criou {subject}?",
            f"Quem fez {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # What ancient civilization X?
    match = re.match(
        r"^What ancient civilization (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(match.group(1))

        aliases.extend([
            f"Which ancient civilization {subject}?",
            f"Que civilização antiga {subject}?",
            f"Qual civilização antiga {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # What instrument X?
    match = re.match(
        r"^What instrument (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(match.group(1))

        aliases.extend([
            f"Which instrument {subject}?",
            f"What tool {subject}?",
            f"Qual instrumento {subject}?",
            f"Que instrumento {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # What plant X?
    match = re.match(
        r"^What plant (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(match.group(1))

        aliases.extend([
            f"Which plant {subject}?",
            f"What plant does {subject} come from?",
            f"Qual planta {subject}?",
            f"De qual planta {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # In which country X?
    match = re.match(
        r"^In which country (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(match.group(1))

        aliases.extend([
            f"What country {subject}?",
            f"Which country {subject}?",
            f"Em qual país {subject}?",
            f"Que país {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # In which century X?
    match = re.match(
        r"^In which century (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(match.group(1))

        aliases.extend([
            f"What century {subject}?",
            f"Which century {subject}?",
            f"Em qual século {subject}?",
            f"Que século {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # What historical event X?
    match = re.match(
        r"^What historical event (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(match.group(1))

        aliases.extend([
            f"Which historical event {subject}?",
            f"What happened {subject}?",
            f"Qual evento histórico {subject}?",
            f"O que aconteceu {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # How often X?
    match = re.match(
        r"^How often (.+)\?$",
        question
    )

    if match:

        subject = clean_subject(match.group(1))

        aliases.extend([
            f"How frequently {subject}?",
            f"How many times {subject}?",
            f"Com que frequência {subject}?",
            f"De quanto em quanto tempo {subject}?"
        ])

        return list(dict.fromkeys(aliases))

    # What does X do?
    match = re.match(
        r"^What does (.+) do\?$",
        question
    )

    if match:

        subject = clean_subject(match.group(1))

        aliases.extend([
            f"What is the function of {subject}?",
            f"What is {subject} used for?",
            f"O que {subject} faz?",
            f"Para que serve {subject}?"
        ])

        return list(dict.fromkeys(aliases))

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