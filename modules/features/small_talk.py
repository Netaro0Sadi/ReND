import re


def clean_message(message):

    message = message.lower().strip()

    message = re.sub(
        r"[^\w\sáéíóúãõâêîôûç]",
        "",
        message
    )

    return message


def handle_small_talk(message):

    message = clean_message(
        message
    )

    how_are_you = [
        "how are you",
        "how are you doing",
        "como vai",
        "como voce esta",
        "como você está",
        "tudo bem",
        "tudo bom"
    ]

    feelings = [
        "how do you feel",
        "como se sente",
        "voce sente algo",
        "você sente algo"
    ]

    if message in how_are_you:
        return (
            "I am functioning well. "
            "Thanks for asking."
        )

    if message in feelings:
        return (
            "I don't have feelings like a human, "
            "but I am here and ready to help."
        )

    return None