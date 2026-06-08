import re


SPECIAL_ENTITIES = {
    "red": "ReD",
    "rend": "ReND",
    "json": "JSON",
    "python": "Python",
    "html": "HTML",
    "css": "CSS",
    "api": "API",
    "ram": "RAM",
    "cpu": "CPU",
    "gpu": "GPU",
    "ssd": "SSD",
    "hdd": "HDD",
    "dns": "DNS",
    "http": "HTTP",
    "url": "URL",
    "sql": "SQL",
    "ide": "IDE",
    "gui": "GUI",
    "os": "OS"
}


ENTITY_QUESTION_PATTERNS = [
    r"^who is (.+)$",
    r"^who was (.+)$",
    r"^who created (.+)$",
    r"^who invented (.+)$",
    r"^who discovered (.+)$",
    r"^who wrote (.+)$",
    r"^who painted (.+)$",
    r"^who co-founded (.+)$",
    r"^where was (.+) born$",
    r"^when was (.+) born$",
    r"^what did (.+) do$"
]


SUBJECT_QUESTION_PATTERNS = [
    r"^what is (.+)$",
    r"^what are (.+)$",
    r"^what does (.+) mean$",
    r"^what does (.+) stand for$",
    r"^what is the meaning of (.+)$",
    r"^explain (.+)$",
    r"^define (.+)$",
    r"^what is (.+) used for$",
    r"^who created (.+)$",
    r"^when was (.+) created$"
]


def clean_text(text):

    return (
        text.lower()
        .strip()
        .replace("?", "")
        .replace(".", "")
        .replace(",", "")
    )


def smart_title(text):

    words = text.split()
    fixed_words = []

    for word in words:

        clean_word = word.lower()

        if clean_word in SPECIAL_ENTITIES:

            fixed_words.append(
                SPECIAL_ENTITIES[clean_word]
            )

        else:

            fixed_words.append(
                word.capitalize()
            )

    return " ".join(
        fixed_words
    )


def remove_articles(text):

    for article in [
        "the ",
        "a ",
        "an "
    ]:

        if text.startswith(article):

            return text[
                len(article):
            ]

    return text


def remember_subject(
    context,
    subject
):

    subject = remove_articles(
        subject.strip()
    )

    subject = smart_title(
        subject
    )

    context.remember(
        "last_subject",
        subject
    )


def remember_entity(
    context,
    entity
):

    entity = remove_articles(
        entity.strip()
    )

    entity = smart_title(
        entity
    )

    context.remember(
        "last_entity",
        entity
    )


def clear_entity(context):

    context.remember(
        "last_entity",
        None
    )


def update_context(
    question,
    response,
    context
):

    if not question:
        return

    question_clean = clean_text(
        question
    )

    response_clean = (
        response.strip()
        if response
        else ""
    )

    if response_clean == "ReD":

        context.remember(
            "last_entity",
            "ReD"
        )

        context.remember(
            "last_subject",
            None
        )

        context.remember(
            "last_topic",
            None
        )

        return

    if response_clean == "I am ReND":

        context.remember(
            "last_subject",
            "ReND"
        )

        context.remember(
            "last_entity",
            "ReND"
        )

        context.remember(
            "last_topic",
            None
        )

        return

    capital_patterns = [
        r"^what is the capital of (.+)$",
        r"^what is (.+)'s capital$"
    ]

    for pattern in capital_patterns:

        match = re.match(
            pattern,
            question_clean
        )

        if match:

            country = match.group(
                1
            )

            context.remember(
                "last_topic",
                "capital"
            )

            context.remember(
                "last_subject",
                f"Capital of {smart_title(country)}"
            )

            clear_entity(
                context
            )

            return

    continent_patterns = [
        r"^what continent is (.+) in$",
        r"^which continent is (.+) in$"
    ]

    for pattern in continent_patterns:

        match = re.match(
            pattern,
            question_clean
        )

        if match:

            place = match.group(
                1
            )

            context.remember(
                "last_topic",
                "continent"
            )

            context.remember(
                "last_subject",
                f"Continent of {smart_title(place)}"
            )

            clear_entity(
                context
            )

            return

    if (
        "weather" in question_clean
        or "climate" in question_clean
        or "clima" in question_clean
    ):

        context.remember(
            "last_subject",
            "weather"
        )

        context.remember(
            "last_topic",
            "weather"
        )

        clear_entity(
            context
        )

        return

    for pattern in ENTITY_QUESTION_PATTERNS:

        match = re.match(
            pattern,
            question_clean
        )

        if match:

            entity = match.group(
                1
            )

            remember_entity(
                context,
                entity
            )

            context.remember(
                "last_subject",
                None
            )

            context.remember(
                "last_topic",
                None
            )

            return

    for pattern in SUBJECT_QUESTION_PATTERNS:

        match = re.match(
            pattern,
            question_clean
        )

        if match:

            subject = match.group(
                1
            )

            remember_subject(
                context,
                subject
            )

            context.remember(
                "last_topic",
                None
            )

            clear_entity(
                context
            )

            return

    clear_entity(
        context
    )