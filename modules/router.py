import json
import os
import re

from modules.core.context_updater import (
    update_context
)

from modules.settings import (
    get_setting,
    set_setting
)

from modules.commands import (
    list_questions,
    stats,
    remove_question,
    edit_question,
    memory_status,
    clear_memory,
    help_menu,
    version,
    about,
    packstats,
    find_knowledge,
    find_alias,
    related,
    languages,
    translate_command
)

from modules.core.context_resolver import (
    resolve_context
)

from modules.features.time_date import (
    handle_time_date
)

from modules.features.weather import (
    handle_weather
)

from modules.features.small_talk import (
    handle_small_talk
)

from modules.personality import (
    apply_personality,
    get_personality,
    set_personality,
    list_personalities
)

from modules.storage import (
    load_data,
    save_data
)

from modules.knowledge import (
    KnowledgeBase
)

from modules.features.calculator import (
    calculate
)

from modules.semantic_search import (
    SemanticSearch
)

from modules.core.context import (
    ConversationContext
)

from modules.core.memory_handler import (
    process_memory
)

from modules.core.user_profile import (
    UserProfile
)

from modules.features.translator import (
    detect_language,
    translate_to_english,
    translate_from_english
)

from modules.features.greetings import (
    handle_greeting
)

from modules.intent_detector import (
    detect_intent
)


PACKS_FOLDER = "data/knowledge_packs"


knowledge_base = KnowledgeBase(
    load_data()
)

search_engine = SemanticSearch(
    knowledge_base
)

context = ConversationContext()

profile = UserProfile()

saved_personality = get_setting(
    "personality",
    "normal"
)

set_personality(
    saved_personality
)


def save_to_pack(
    pack_name,
    question,
    answer
):

    if not os.path.exists(
        PACKS_FOLDER
    ):

        os.makedirs(
            PACKS_FOLDER
        )

    pack_name = (
        pack_name.lower()
        .strip()
        .replace(" ", "_")
    )

    if not pack_name.endswith(
        ".json"
    ):

        pack_name += ".json"

    pack_path = os.path.join(
        PACKS_FOLDER,
        pack_name
    )

    if os.path.exists(
        pack_path
    ):

        with open(
            pack_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )

    else:

        data = {}

    data[
        question
    ] = answer

    with open(
        pack_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def learn(question, answer):

    knowledge_base.add(
        question,
        answer
    )

    save_data(
        knowledge_base.all_data()
    )

    search_engine.update()


def learn_with_pack(
    pack_name,
    question,
    answer
):

    save_to_pack(
        pack_name,
        question,
        answer
    )

    learn(
        question,
        answer
    )


def reload_system():

    global knowledge_base
    global search_engine

    knowledge_base = KnowledgeBase(
        load_data()
    )

    search_engine = SemanticSearch(
        knowledge_base
    )

    return (
        "System reloaded.\n"
        f"Questions: {len(knowledge_base.all_questions())}"
    )


def debug_status():

    return (
        "Debug Status\n\n"
        f"Language: {context.recall('debug_language')}\n"
        f"Intent: {context.recall('debug_intent')}\n"
        f"Original Message: {context.recall('debug_original_message')}\n"
        f"English Message: {context.recall('debug_english_message')}\n"
        f"Last Intent: {context.recall('last_intent')}\n"
        f"Last Subject: {context.recall('last_subject')}\n"
        f"Last Entity: {context.recall('last_entity')}\n"
        f"Last Topic: {context.recall('last_topic')}\n"
        f"Personality: {get_personality()}"
    )

import re


def suggest_pack(question):

    text = (
        question.lower()
        .strip()
    )

    words = re.findall(
        r"\b\w+\b",
        text
    )

    phrase_rules = {
        "geography": [
            "capital of",
            "continent is",
            "located in",
            "largest country",
            "largest ocean",
            "smallest country",
            "population of",
            "currency of",
            "official language"
        ],

        "science": [
            "red planet",
            "solar system",
            "speed of light",
            "speed of sound",
            "boiling point",
            "freezing point",
            "chemical symbol",
            "periodic table",
            "black hole",
            "milky way",
            "human body",
            "blood cells",
            "universal donor",
            "universal recipient",
            "theory of relativity"
        ],

        "technology": [
            "binary system",
            "file path",
            "dynamic memory allocation",
            "operating system",
            "computer science",
            "artificial intelligence",
            "machine learning",
            "main function of a cpu",
            "android app development"
        ],

        "programming": [
            "programming language",
            "source code",
            "data structure",
            "for loop",
            "while loop",
            "object oriented",
            "machine code"
        ],

        "history": [
            "world war",
            "first president",
            "roman empire",
            "mongolian empire",
            "french revolution",
            "industrial revolution",
            "ancient civilization",
            "middle ages",
            "first emperor",
            "statue of liberty",
            "mona lisa",
            "romeo and juliet",
            "the odyssey"
        ],

        "math": [
            "square root",
            "prime number",
            "right angle",
            "straight line",
            "multiplication table",
            "quadratic equation",
            "value of pi"
        ],

        "pop_culture": [
            "star wars",
            "dragon ball",
            "one piece",
            "death note",
            "attack on titan",
            "the last of us",
            "red dead redemption",
            "grand theft auto",
            "game of thrones",
            "breaking bad",
            "stranger things",
            "harry potter",
            "lord of the rings",
            "the boys",
            "rick and morty"
        ],

        "sports": [
            "world cup",
            "champions league",
            "copa libertadores",
            "formula 1",
            "super bowl",
            "olympic games",
            "ballon d'or",
            "michael jordan",
            "lionel messi",
            "cristiano ronaldo"
        ],

        "rend_core": [
            "what is rend",
            "who created rend",
            "who created you",
            "your name",
            "your creator",
            "context memory"
        ]
    }

    for pack_name, phrases in phrase_rules.items():

        for phrase in phrases:

            if phrase in text:

                return pack_name

    pack_rules = {

        "programming": [
            "python", "java", "javascript", "typescript",
            "cpp", "csharp", "php", "ruby", "rust",
            "kotlin", "swift", "algorithm", "api",
            "json", "html", "css", "xml", "sql",
            "code", "coding", "programming", "software",
            "database", "function", "variable", "class",
            "object", "loop", "array", "list", "dictionary",
            "framework", "library", "github", "git",
            "compiler", "interpreter", "debug", "debugging",
            "ide", "syntax", "backend", "frontend", "script",
            "malloc", "calloc", "realloc", "pointer"
        ],

        "technology": [
            "cpu", "gpu", "ram", "ssd", "hdd",
            "internet", "computer", "hardware", "network",
            "browser", "windows", "linux", "android",
            "iphone", "smartphone", "wifi", "router",
            "motherboard", "processor", "keyboard", "mouse",
            "monitor", "screen", "bluetooth", "usb",
            "cloud", "server", "encryption", "password",
            "malware", "firewall", "ai", "intelligence",
            "machine", "learning", "neural", "turing",
            "alan", "enigma", "computing", "robot",
            "automation", "chip", "semiconductor", "binary",
            "digital", "compiler"
        ],

        "science": [
            "physics", "chemistry", "biology", "astronomy",
            "scientist", "atom", "molecule", "cell",
            "energy", "light", "gravity", "photosynthesis",
            "evolution", "einstein", "newton", "darwin",
            "penicillin", "planet", "star", "galaxy",
            "universe", "space", "dna", "electron", "proton",
            "neutron", "force", "mass", "matter", "oxygen",
            "carbon", "water", "temperature", "climate",
            "organism", "species", "plant", "animal",
            "human", "brain", "blood", "heart", "disease",
            "vaccine", "bacteria", "virus", "relativity",
            "quantum", "telescope", "microscope", "diamond",
            "mineral", "helium", "nitrogen", "calcium",
            "sodium", "potassium", "copper", "zinc",
            "iron", "gold", "silver", "lead"
        ],

        "geography": [
            "capital", "country", "continent", "city",
            "river", "ocean", "mountain", "population",
            "island", "border", "nation", "state",
            "province", "sea", "desert", "forest",
            "location", "map", "territory", "region",
            "hemisphere", "equator", "latitude", "longitude",
            "brazil", "argentina", "pakistan", "india",
            "japan", "china", "russia", "canada",
            "australia", "egypt", "france", "germany",
            "italy", "spain", "portugal", "mexico",
            "colombia", "chile", "peru", "sweden",
            "norway", "switzerland", "ireland", "turkey",
            "greece", "africa", "asia", "europe",
            "america"
        ],

        "history": [
            "war", "empire", "king", "queen", "president",
            "revolution", "historical", "ancient", "medieval",
            "civilization", "dynasty", "battle", "independence",
            "pharaoh", "roman", "greek", "viking", "napoleon",
            "hitler", "churchill", "cleopatra", "caesar",
            "alexander", "columbus", "gandhi", "lincoln",
            "century", "colonial", "colony", "slavery",
            "renaissance", "republic", "monarchy", "treaty",
            "invention", "invented", "discovered", "emperor",
            "picasso", "leonardo", "shakespeare"
        ],

        "math": [
            "math", "mathematics", "number", "equation",
            "algebra", "geometry", "triangle", "square",
            "angle", "fraction", "percent", "percentage",
            "multiply", "divide", "addition", "subtraction",
            "calculus", "integral", "derivative", "theorem",
            "prime", "root", "power", "exponent", "decimal",
            "average", "mean", "median", "mode", "probability",
            "ratio", "proportion", "area", "perimeter",
            "volume", "circle", "radius", "diameter",
            "polygon", "pentagon", "hexagon", "octagon",
            "degrees", "pi"
        ],

        "pop_culture": [
            "batman", "superman", "spiderman", "spider",
            "marvel", "dc", "joker", "thanos", "iron",
            "captain", "hulk", "thor", "anime", "manga",
            "movie", "film", "series", "tv", "television",
            "cartoon", "netflix", "disney", "pixar",
            "wars", "jedi", "sith", "vader", "dragon",
            "ball", "goku", "vegeta", "naruto", "sasuke",
            "luffy", "piece", "pokemon", "pikachu", "zelda",
            "mario", "sonic", "minecraft", "fortnite",
            "roblox", "undertale", "sans", "valorant",
            "overwatch", "game", "gaming", "character",
            "villain", "hero", "superhero", "homelander",
            "invincible", "omni", "potter", "hogwarts",
            "matrix", "neo", "frodo", "gandalf", "spongebob",
            "simpson", "rick", "morty", "grogu", "mandalorian"
        ],

        "sports": [
            "football", "soccer", "basketball", "nba",
            "fifa", "tennis", "volleyball", "baseball",
            "olympics", "cup", "player", "team", "coach",
            "championship", "league", "goal", "penalty",
            "offside", "striker", "goalkeeper", "midfielder",
            "defender", "messi", "ronaldo", "pele", "pelé",
            "neymar", "mbappe", "haaland", "bellingham",
            "jordan", "lebron", "kobe", "federer", "nadal",
            "djokovic", "senna", "hamilton", "verstappen",
            "boxing", "mma", "ufc", "wwe", "golf", "rugby",
            "cricket", "swimming", "athletics", "marathon",
            "cycling", "formula", "racing"
        ],

        "rend_core": [
            "rend", "renato", "creator", "created",
            "codename", "personality", "memory", "context",
            "profile"
        ]
    }

    scores = {}

    for pack_name, keywords in pack_rules.items():

        score = 0

        for keyword in keywords:

            if keyword in words:

                score += 1

        scores[pack_name] = score

    best_pack = max(
        scores,
        key=scores.get
    )

    if scores[best_pack] > 0:

        return best_pack

    return "general"

def handle_command(message):

    command = (
        message.lower()
        .strip()
    )

    if command == "/list":

        return list_questions(
            knowledge_base
        )

    if command == "/why":

        return search_engine.why()

    if command == "/related":

        return related(
            knowledge_base,
            search_engine,
            context
        )

    if command == "/stats":

        return stats(
            knowledge_base,
            context,
            get_personality()
        )

    if command == "/memory":

        return memory_status(
            context
        )

    if command in [
        "/memory clear",
        "/memory_clear"
    ]:

        return clear_memory(
            context
        )

    if command == "/personality":

        return list_personalities()

    if command.startswith(
        "/setpersonality"
    ):

        parts = command.split()

        if len(parts) < 2:

            return (
                "Use: "
                "/setpersonality dramatic"
            )

        new_personality = parts[1]

        success = set_personality(
            new_personality
        )

        if success:

            set_setting(
                "personality",
                get_personality()
            )

            return (
                f"Personality changed to: "
                f"{get_personality()}"
            )

        return "Invalid personality."

    if command == "/learn":

        pack_name = input(
            "Pack name or auto: "
        )

        question = input(
            "Question in English: "
        )

        if pack_name.lower().strip() == "auto":

            pack_name = suggest_pack(
                question
            )

            print(
                f"Selected pack: {pack_name}"
            )

        answer = input(
            "Answer in English: "
        )

        learn_with_pack(
            pack_name,
            question,
            answer
        )

        return "Knowledge saved."

    if command == "/learnpt":

        pack_name = input(
            "Nome do pack ou auto: "
        )

        question_pt = input(
            "Pergunta em português: "
        )

        question_en = translate_to_english(
            question_pt
        )

        if pack_name.lower().strip() == "auto":

            pack_name = suggest_pack(
                question_en
            )

            print(
                f"Pack selecionado: {pack_name}"
            )

        answer_pt = input(
            "Resposta em português: "
        )

        answer_en = translate_to_english(
            answer_pt
        )

        learn_with_pack(
            pack_name,
            question_en,
            answer_en
        )

        return "Knowledge saved."

    if command == "/reload":

        return reload_system()

    if command == "/debug":

        return debug_status()

    if command == "/remove":

        question = input(
            "Question to remove: "
        )

        success = remove_question(
            knowledge_base,
            question
        )

        if success:

            save_data(
                knowledge_base.all_data()
            )

            search_engine.update()

            return "Question removed."

        return "Question not found."

    if command == "/edit":

        question = input(
            "Question to edit: "
        )

        new_answer = input(
            "New answer: "
        )

        success = edit_question(
            knowledge_base,
            question,
            new_answer
        )

        if success:

            save_data(
                knowledge_base.all_data()
            )

            search_engine.update()

            return "Answer updated."

        return "Question not found."

    if command == "/help":

        return help_menu()

    if command == "/version":

        return version()
    
    if command == "/about":

        return about(
            knowledge_base,
            get_personality()
        )

    if command == "/packstats":

        return packstats()
    
    if command == "/languages":

        return languages()


    if command.startswith(
        "/translate"
    ):

        return translate_command(
            message
        )
    
    if command.startswith(
        "/findalias"
    ):

        search_text = message[
            len("/findalias"):
        ].strip()

        return find_alias(
            search_text
        )

    if command.startswith(
        "/find"
    ):

        search_text = message[
            len("/find"):
        ].strip()

        return find_knowledge(
            knowledge_base,
            search_text
        )

    return "Unknown command."


def unknown_response(
    english_message,
    user_language
):

    similar = search_engine.explain_search(
        english_message
    )

    if user_language == "pt":

        similar = translate_from_english(
            similar,
            user_language
        )

        return (
            "Ainda não sei responder isso.\n\n"
            f"{similar}\n\n"
            "Use /learn para me ensinar."
        )

    return (
        "I don't know that yet.\n\n"
        f"{similar}\n\n"
        "Use /learn to teach me."
    )


def process_message(message):

    original_message = message

    message = resolve_context(
        message,
        context
    )

    user_language = detect_language(
        original_message
    )

    original_intent = detect_intent(
        message
    )

    english_message = translate_to_english(
        message
    )

    translated_intent = detect_intent(
        english_message
    )

    if original_intent != "knowledge":

        intent = original_intent

    else:

        intent = translated_intent

    if intent != "command":

        context.remember(
            "debug_language",
            user_language
        )

        context.remember(
            "debug_intent",
            intent
        )

        context.remember(
            "debug_original_message",
            original_message
        )

        context.remember(
            "debug_english_message",
            english_message
        )

    if (
        intent == "knowledge"
        and context.recall(
            "last_intent"
        ) == "weather"
        and (
            message.lower()
            .strip()
            .startswith("e em")
            or
            english_message.lower()
            .strip()
            .startswith("and in")
        )
    ):

        intent = "weather"

    response = None

    if intent == "command":

        response = handle_command(
            message
        )

    elif intent == "greeting":

        response = handle_greeting(
            message
        )

    elif intent == "memory":

        response = process_memory(
            english_message,
            context,
            profile
        )

    elif intent == "math":

        response = calculate(
            english_message
        )

    elif intent == "small_talk":

        response = handle_small_talk(
            message
        )

    elif intent == "time_date":

        response = handle_time_date(
            message
        )

    elif intent == "weather":

        context.remember(
            "last_subject",
            "weather"
        )

        context.remember(
            "last_topic",
            "weather"
        )

        context.remember(
            "last_entity",
            None
        )

        response = handle_weather(
            message
        )

    elif intent == "knowledge":

        response = search_engine.search(
            english_message
        )

    if response is not None:

        context.remember(
            "last_intent",
            intent
        )

        if intent == "knowledge":

            update_context(
                english_message,
                response,
                context
            )

        if intent != "command":

            response = apply_personality(
                response
            )

        return translate_from_english(
            response,
            user_language
        )

    return unknown_response(
        english_message,
        user_language
    )