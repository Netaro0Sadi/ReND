import re


def detect_intent(message):

    message = (
        message.lower()
        .strip()
    )

    if message.startswith("/"):
        return "command"

    greetings = [
        "hi",
        "hello",
        "hey",
        "oi",
        "ola",
        "olá",
        "hola"
    ]

    if message in greetings:
        return "greeting"

    if (
        "my name is" in message
        or "what is my name" in message
        or "whats my name" in message
        or "what's my name" in message
    ):
        return "memory"

    small_talk_phrases = [
        "how are you",
        "how are you doing",
        "how do you feel",
        "como vai",
        "como voce esta",
        "como você está",
        "como se sente",
        "tudo bem",
        "tudo bom",
        "voce sente algo",
        "você sente algo"
    ]

    for phrase in small_talk_phrases:

        if phrase in message:
            return "small_talk"

    weather_words = [
        "weather",
        "temperature",
        "climate",
        "clima",
        "tempo",
        "temperatura",
        "graus",
        "chover",
        "chuva"
    ]

    for word in weather_words:

        if word in message:
            return "weather"

    time_date_words = [
        "what time",
        "current time",
        "today's date",
        "what date",
        "que horas",
        "horas",
        "horario",
        "horário",
        "data de hoje",
        "que dia é hoje",
        "que dia e hoje"
    ]

    for word in time_date_words:

        if word in message:
            return "time_date"

    if re.fullmatch(
        r"[0-9+\-*/().\s]+",
        message
    ):
        return "math"

    return "knowledge"