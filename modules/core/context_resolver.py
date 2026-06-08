import re
import unicodedata


COUNTRY_TRANSLATIONS = {
    "japao": "Japan",
    "japão": "Japan",
    "brasil": "Brazil",
    "argentina": "Argentina",
    "chile": "Chile",
    "franca": "France",
    "frança": "France",
    "alemanha": "Germany",
    "italia": "Italy",
    "itália": "Italy",
    "espanha": "Spain",
    "portugal": "Portugal",
    "china": "China",
    "india": "India",
    "índia": "India",
    "russia": "Russia",
    "rússia": "Russia",
    "mexico": "Mexico",
    "méxico": "Mexico",
    "canada": "Canada",
    "canadá": "Canada",
    "egito": "Egypt",
    "australia": "Australia",
    "austrália": "Australia"
}


def normalize_text(text):

    text = text.lower().strip()

    text = (
        text
        .replace("oque", "o que")
        .replace("vc", "você")
        .replace("pq", "porque")
    )

    return text


def normalize_place(place):

    place = (
        place.lower()
        .strip()
        .replace("?", "")
        .replace(".", "")
    )

    no_accents = "".join(
        char
        for char in unicodedata.normalize(
            "NFD",
            place
        )
        if unicodedata.category(char) != "Mn"
    )

    return COUNTRY_TRANSLATIONS.get(
        place,
        COUNTRY_TRANSLATIONS.get(
            no_accents,
            place
        )
    )


def resolve_context(
    message,
    context
):

    text = normalize_text(
        message
    )

    if text in [
        "como se chama",
        "como você se chama",
        "como voce se chama",
        "qual seu nome",
        "qual o seu nome",
        "quem é você",
        "quem e voce",
        "quem é voce",
        "quem e você"
    ]:

        return "What is your name?"

    last_entity = context.recall(
        "last_entity"
    )

    last_subject = context.recall(
        "last_subject"
    )

    last_topic = context.recall(
        "last_topic"
    )

    if last_entity:

        if text in [
            "quem é ele?",
            "quem e ele?",
            "quem é ele",
            "quem e ele",
            "quem é?",
            "quem e?",
            "quem é",
            "quem e",
            "who is he?",
            "who is he",
            "who is it?",
            "who is it"
        ]:

            return (
                f"Who is "
                f"{last_entity}?"
            )

        if text in [
            "onde nasceu?",
            "onde nasceu",
            "onde ele nasceu?",
            "onde ele nasceu",
            "onde ela nasceu?",
            "onde ela nasceu",
            "where was he born?",
            "where was he born",
            "where was she born?",
            "where was she born"
        ]:

            return (
                f"Where was "
                f"{last_entity} born?"
            )

        if text in [
            "quando nasceu?",
            "quando nasceu",
            "quando ele nasceu?",
            "quando ele nasceu",
            "quando ela nasceu?",
            "quando ela nasceu",
            "when was he born?",
            "when was he born",
            "when was she born?",
            "when was she born"
        ]:

            return (
                f"When was "
                f"{last_entity} born?"
            )

        if text in [
            "o que ele fez?",
            "o que ele fez",
            "o que ela fez?",
            "o que ela fez",
            "o que ele faz?",
            "o que ele faz",
            "o que ela faz?",
            "o que ela faz",
            "what did he do?",
            "what did he do",
            "what did she do?",
            "what did she do",
            "what does he do?",
            "what does he do",
            "what does she do?",
            "what does she do"
        ]:

            return (
                f"What did "
                f"{last_entity} do?"
            )

    if last_subject:

        if text in [
            "para que serve?",
            "para que serve",
            "pra que serve?",
            "pra que serve",
            "what is it used for?",
            "what is it used for"
        ]:

            return (
                f"What is "
                f"{last_subject} used for?"
            )

        if text in [
            "quem criou?",
            "quem criou",
            "quem criou isso?",
            "quem criou isso",
            "who created it?",
            "who created it",
            "who created this?",
            "who created this"
        ]:

            return (
                f"Who created "
                f"{last_subject}?"
            )

        if text in [
            "quando foi criado?",
            "quando foi criado",
            "when was it created?",
            "when was it created"
        ]:

            return (
                f"When was "
                f"{last_subject} created?"
            )

        if text in [
            "o que significa?",
            "o que significa",
            "o que quer dizer?",
            "o que quer dizer",
            "qual o significado?",
            "qual o significado",
            "what does it mean?",
            "what does it mean"
        ]:

            return (
                f"What does "
                f"{last_subject} stand for?"
            )

        if text in [
            "explique melhor",
            "explique melhor?",
            "me explique melhor",
            "fale mais",
            "tell me more",
            "explain better"
        ]:

            if last_entity:

                return (
                    f"Who is "
                    f"{last_entity}?"
                )

            if last_subject != "weather":

                return (
                    f"Explain "
                    f"{last_subject}."
                )

            return message

    if last_topic == "capital":

        patterns = [
            r"^e\s+(a\s+|o\s+)?(da|do)\s+(.+)$",
            r"^e\s+(a|o)\s+(.+)$",
            r"^e\s+(.+)$"
        ]

        for pattern in patterns:

            match = re.match(
                pattern,
                text
            )

            if match:

                country = normalize_place(
                    match.groups()[-1]
                )

                return (
                    f"What is the capital of "
                    f"{country}?"
                )

    if last_topic == "continent":

        patterns = [
            r"^e\s+(a\s+|o\s+)?(da|do)\s+(.+)$",
            r"^e\s+(a|o)\s+(.+)$",
            r"^e\s+(.+)$"
        ]

        for pattern in patterns:

            match = re.match(
                pattern,
                text
            )

            if match:

                place = normalize_place(
                    match.groups()[-1]
                )

                return (
                    f"What continent is "
                    f"{place} in?"
                )
            
    if last_topic == "weather":

        match = re.match(
            r"^e em (.+)$",
            text
        )

        if match:

            city = match.group(
                1
            )

            return (
                f"weather in "
                f"{city}"
            )

        match = re.match(
            r"^e de (.+)$",
            text
        )

        if match:

            city = match.group(
                1
            )

            return (
                f"weather in "
                f"{city}"
            )

        match = re.match(
            r"^and in (.+)$",
            text
        )

        if match:

            city = match.group(
                1
            )

            return (
                f"weather in "
                f"{city}"
            )

        match = re.match(
            r"^and of (.+)$",
            text
        )

        if match:

            city = match.group(
                1
            )

            return (
                f"weather in "
                f"{city}"
            )

    return message