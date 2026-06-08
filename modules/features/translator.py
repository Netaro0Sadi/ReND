from deep_translator import GoogleTranslator
from langdetect import detect


PROTECTED_RESPONSES = [
    "ReD",
    "ReND",
    "Last Match Information",
    "Debug Status",
    "ReND Statistics",
    "ReND Version Information",
    "Available Commands",
    "Memory Status"
]


def detect_language(text):

    text_lower = text.lower().strip()

    portuguese_words = [
        "qual",
        "quem",
        "oque",
        "o que",
        "voce",
        "você",
        "meu",
        "minha",
        "nome",
        "criou",
        "clima",
        "tempo",
        "capital",
        "quanto",
        "quantos",
        "quantas",
        "graus",
        "tudo bem",
        "tudo bom",
        "como vai",
        "como se sente",
        "explique",
        "explica",
        "melhor",
        "significa",
        "significado",
        "quer dizer",
        "para que",
        "pra que",
        "serve",
        "onde",
        "quando",
        "por que",
        "porque",
        "cidade",
        "país",
        "continente",
        "futebol",
        "filme",
        "série",
        "jogo",
        "me fale",
        "fale sobre",
        "me diga",
        "sobre"
    ]

    english_words = [
        "what",
        "who",
        "where",
        "when",
        "why",
        "how",
        "tell",
        "about",
        "weather",
        "temperature",
        "capital",
        "country",
        "continent",
        "movie",
        "game",
        "football"
    ]

    for word in portuguese_words:

        if word in text_lower:

            return "pt"

    for word in english_words:

        if word in text_lower:

            return "en"

    try:

        detected = detect(text)

        if detected in [
            "pt",
            "en"
        ]:

            return detected

        return "en"

    except:

        return "en"


def translate_to_english(text):

    if detect_language(text) == "en":

        return text

    try:

        translated = GoogleTranslator(
            source="auto",
            target="en"
        ).translate(text)

        return translated

    except:

        return text


def translate_from_english(
    text,
    target_language
):

    if target_language == "en":

        return text

    if not text:

        return text

    for protected in PROTECTED_RESPONSES:

        if text.startswith(protected):

            return text

    if text.strip() in [
        "ReD",
        "ReND"
    ]:

        return text

    try:

        translated = GoogleTranslator(
            source="en",
            target=target_language
        ).translate(text)

        return translated

    except:

        return text