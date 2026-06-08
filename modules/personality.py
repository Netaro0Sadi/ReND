import random


PERSONALITY = "normal"


VALID_PERSONALITIES = [
    "normal",
    "friendly",
    "professional",
    "dramatic"
]


def set_personality(style):

    global PERSONALITY

    if style not in VALID_PERSONALITIES:
        return False

    PERSONALITY = style

    return True


def get_personality():

    return PERSONALITY


def personality_info():

    return (
        f"Current personality: {PERSONALITY}"
    )


def list_personalities():

    result = "Available personalities:\n\n"

    for style in VALID_PERSONALITIES:

        if style == PERSONALITY:

            result += f"- {style} (current)\n"

        else:

            result += f"- {style}\n"

    return result


def should_skip_personality(response):

    if response is None:
        return True

    response = str(
        response
    ).strip()

    if not response:
        return True

    if response.startswith(
        "/"
    ):
        return True

    if response.startswith(
        "Memory Status"
    ):
        return True
    
    if response.startswith(
        "ReND Statistics"
    ):
        return True

    if response.startswith(
        "Questions learned"
    ):
        return True
    
    if response.startswith(
        "Available Commands"
    ):
        return True
    
    if response.startswith(
        "System reloaded."
    ):
        return True

    if response.startswith(
        "Debug Status"
    ):
        return True

    if response.startswith(
        "Learned questions"
    ):
        return True
    
    if response.startswith(
        "ReND 0."
    ):
        return True
    
    if response.startswith(
        "Available personalities"
    ):
        return True
    
    if response.startswith(
        "Last Match Information"
    ):
        return True
    
    if response.startswith(
    "Personality changed to:"
    ):
        return True

    if len(
        response.split()
    ) <= 3:
        return True

    protected_responses = [
        "ReD",
        "ReND",
        "Hello!",
        "Olá!",
        "Memory cleared.",
        "Knowledge saved.",
        "Answer updated.",
        "Question removed.",
        "Question not found.",
        "Unknown command."
    ]

    if response in protected_responses:
        return True

    protected_starts = [
        "Responsive Network Development",
        "The weather in",
        "It is",
        "Today is"
    ]

    for start in protected_starts:

        if response.startswith(
            start
        ):
            return True

    return False


def lowercase_first_letter(text):

    if not text:
        return text

    return (
        text[0].lower()
        + text[1:]
    )


def apply_personality(response):

    if should_skip_personality(
        response
    ):
        return response

    response = str(
        response
    )

    if PERSONALITY == "normal":

        return response

    if PERSONALITY == "friendly":

        prefixes = [
            "Claro! ",
            "Sem problemas! ",
            "Boa pergunta! ",
            "Posso explicar. "
        ]

        return (
            random.choice(
                prefixes
            )
            + response
        )

    if PERSONALITY == "professional":

        prefixes = [
            "De acordo com meu conhecimento, ",
            "Com base nas informações disponíveis, ",
            "Em termos técnicos, ",
            "Pelo que sei, "
        ]

        return (
            random.choice(
                prefixes
            )
            + lowercase_first_letter(
                response
            )
        )

    if PERSONALITY == "dramatic":

        prefixes = [
            "Entre os registros do conhecimento, ",
            "Como os dados revelam, ",
            "Nas profundezas da informação, ",
            "Observando os fatos conhecidos, "
        ]

        return (
            random.choice(
                prefixes
            )
            + lowercase_first_letter(
                response
            )
        )

    return response