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
    "Memory Status",
    "Related Knowledge"
]


SUPPORTED_LANGUAGES = {
    "auto": "Auto detect",
    "pt": "Portuguese",
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh-cn": "Chinese Simplified",
    "ru": "Russian"
}

LANGUAGE_ALIASES = {
    "auto": "auto",
    "automatico": "auto",
    "automático": "auto",
    "detectar": "auto",

    "pt": "pt",
    "portugues": "pt",
    "português": "pt",
    "portuguese": "pt",

    "en": "en",
    "ingles": "en",
    "inglês": "en",
    "english": "en",

    "es": "es",
    "espanhol": "es",
    "spanish": "es",
    "español": "es",

    "fr": "fr",
    "frances": "fr",
    "francês": "fr",
    "french": "fr",

    "de": "de",
    "alemao": "de",
    "alemão": "de",
    "german": "de",

    "it": "it",
    "italiano": "it",
    "italian": "it",

    "ja": "ja",
    "japones": "ja",
    "japonês": "ja",
    "japanese": "ja",

    "ko": "ko",
    "coreano": "ko",
    "korean": "ko",

    "zh": "zh-cn",
    "zh-cn": "zh-cn",
    "chines": "zh-cn",
    "chinês": "zh-cn",
    "chinese": "zh-cn",

    "ru": "ru",
    "russo": "ru",
    "russian": "ru"
}

def normalize_language_code(language):

    if not language:
        return None

    language = (
        language.lower()
        .strip()
    )

    return LANGUAGE_ALIASES.get(
        language,
        language
    )

def detect_language(text):

    text_lower = text.lower().strip()

    portuguese_words = [
        "qual", "quem", "oque", "o que", "voce", "você",
        "meu", "minha", "nome", "criou", "clima", "tempo",
        "capital", "quanto", "quantos", "quantas", "graus",
        "tudo bem", "tudo bom", "como vai", "como se sente",
        "explique", "explica", "melhor", "significa",
        "significado", "quer dizer", "para que", "pra que",
        "serve", "onde", "quando", "por que", "porque",
        "cidade", "país", "continente", "futebol", "filme",
        "série", "jogo", "me fale", "fale sobre", "me diga",
        "sobre"
    ]

    english_words = [
        "what", "who", "where", "when", "why", "how",
        "tell", "about", "weather", "temperature", "capital",
        "country", "continent", "movie", "game", "football"
    ]

    for word in portuguese_words:

        if word in text_lower:
            return "pt"

    for word in english_words:

        if word in text_lower:
            return "en"

    try:

        detected = detect(text)

        if detected in SUPPORTED_LANGUAGES:
            return detected

        return "en"

    except:

        return "en"


def is_protected_response(text):

    if not text:
        return True

    for protected in PROTECTED_RESPONSES:

        if text.startswith(protected):
            return True

    if text.strip() in [
        "ReD",
        "ReND"
    ]:
        return True

    return False


def translate_text(
    text,
    source_language="auto",
    target_language="en"
):

    if not text:
        return text

    source_language = normalize_language_code(
        source_language
    )

    target_language = normalize_language_code(
        target_language
    )

    if source_language == target_language:
        return text

    if target_language not in SUPPORTED_LANGUAGES:
        return None

    if (
        source_language != "auto"
        and source_language not in SUPPORTED_LANGUAGES
    ):
        return None

    try:

        translated = GoogleTranslator(
            source=source_language,
            target=target_language
        ).translate(text)

        return translated

    except:

        return None


def translate_to_english(text):

    if detect_language(text) == "en":
        return text

    translated = translate_text(
        text,
        source_language="auto",
        target_language="en"
    )

    if translated:
        return translated

    return text


def translate_from_english(
    text,
    target_language
):

    if target_language == "en":
        return text

    if is_protected_response(text):
        return text

    translated = translate_text(
        text,
        source_language="en",
        target_language=target_language
    )

    if translated:
        return translated

    return text


def supported_languages():

    result = "Supported Languages\n\n"

    for code, name in SUPPORTED_LANGUAGES.items():

        result += (
            f"- {code}: {name}\n"
        )

    return result.strip()


def handle_translate_command(message):

    parts = message.split(
        maxsplit=3
    )

    if len(parts) < 4:

        return (
            "Use:\n"
            "/translate <source> <target> <text>\n\n"
            "Examples:\n"
            "/translate en pt Hello world\n"
            "/translate auto es Eu gosto de programar"
        )

    source_language = normalize_language_code(
        parts[1]
    )

    target_language = normalize_language_code(
        parts[2]
    )
    text = parts[3]

    translated = translate_text(
        text,
        source_language=source_language,
        target_language=target_language
    )

    if translated is None:

        return (
            "Translation failed.\n\n"
            "Use /languages to see supported languages."
        )

    return (
        "Translation\n\n"
        f"From: {source_language}\n"
        f"To: {target_language}\n\n"
        f"{translated}"
    )