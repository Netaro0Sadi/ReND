import os
import json

from modules.core.related_knowledge import get_related_questions


PACKS_FOLDER = "data/knowledge_packs"
ALIASES_FILE = "data/aliases.json"


def load_json(path):

    if not os.path.exists(path):
        return {}

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def list_questions(knowledge_base):

    questions = knowledge_base.all_questions()

    if not questions:
        return "No questions learned yet."

    result = "\nLearned questions:\n\n"

    for index, question in enumerate(
        questions,
        start=1
    ):
        result += f"{index}. {question}\n"

    return result


def memory_status(context):

    return (
        "Memory Status\n\n"
        f"Last Intent: {context.recall('last_intent')}\n"
        f"Last Subject: {context.recall('last_subject')}\n"
        f"Last Entity: {context.recall('last_entity')}\n"
        f"Last Topic: {context.recall('last_topic')}"
    )


def clear_memory(context):

    context.clear()

    return "Memory cleared."


def stats(
    knowledge_base,
    context,
    personality
):

    total = len(
        knowledge_base.all_questions()
    )

    return (
        "ReND Statistics\n\n"
        f"Questions: {total}\n"
        f"Personality: {personality}\n\n"
        "Memory:\n"
        f"- Last Intent: {context.recall('last_intent')}\n"
        f"- Last Subject: {context.recall('last_subject')}\n"
        f"- Last Entity: {context.recall('last_entity')}"
    )


def remove_question(
    knowledge_base,
    question
):

    return knowledge_base.remove(
        question
    )


def edit_question(
    knowledge_base,
    question,
    new_answer
):

    if question in knowledge_base.data:

        knowledge_base.data[
            question
        ] = new_answer

        return True

    return False


def help_menu():

    return (
        "Available Commands\n\n"
        "/list - Show learned questions\n"
        "/stats - Show ReND statistics\n"
        "/about - Show ReND system information\n"
        "/packstats - Show knowledge pack statistics\n"
        "/find <text> - Search questions in the knowledge base\n"
        "/memory - Show context memory\n"
        "/memory clear - Clear context memory\n"
        "/personality - Show personalities\n"
        "/setpersonality <name> - Change personality\n"
        "/learn - Teach ReND in English\n"
        "/learnpt - Teach ReND in Portuguese\n"
        "/reload - Reload knowledge base\n"
        "/debug - Show debug information\n"
        "/why - Show why ReND chose the last answer\n"
        "/related - Show related knowledge\n"
        "/version - Show system version\n"
        "/edit - Edit a learned answer\n"
        "/remove - Remove a learned question\n"
        "/help - Show this help menu\n"
        "/findalias <text> - Search aliases"
    )


def version():

    return (
        "ReND Version Information\n\n"

        "Version: 2.1\n"
        "Status: Stable\n\n"

        "Core Features:\n"
        "✓ Semantic Search\n"
        "✓ Related Knowledge\n"
        "✓ Knowledge Base\n"
        "✓ Alias System\n"
        "✓ Context Resolver\n"
        "✓ Context Updater\n"
        "✓ Conversation Memory\n"
        "✓ User Profiles\n"
        "✓ Personalities\n"
        "✓ Translation System\n\n"

        "Tools:\n"
        "✓ Weather\n"
        "✓ Calculator\n"
        "✓ Time and Date\n"
        "✓ Small Talk\n"
        "✓ Greetings\n\n"

        "Learning System:\n"
        "✓ /learn\n"
        "✓ /learnpt\n"
        "✓ Knowledge Packs\n"
        "✓ Live Reload\n\n"

        "Developer:\n"
        "ReD (Renato Dias Machado)"
    )


def get_pack_counts():

    counts = {}

    if not os.path.exists(
        PACKS_FOLDER
    ):

        return counts

    for file_name in os.listdir(
        PACKS_FOLDER
    ):

        if not file_name.endswith(
            ".json"
        ):

            continue

        pack_name = file_name.replace(
            ".json",
            ""
        )

        path = os.path.join(
            PACKS_FOLDER,
            file_name
        )

        data = load_json(
            path
        )

        counts[
            pack_name
        ] = len(
            data
        )

    return counts


def packstats():

    counts = get_pack_counts()

    if not counts:

        return "No knowledge packs found."

    total = sum(
        counts.values()
    )

    result = (
        "Knowledge Pack Statistics\n\n"
        f"Total pack questions: {total}\n"
        f"Knowledge packs: {len(counts)}\n\n"
    )

    for pack_name, count in sorted(
        counts.items(),
        key=lambda item: item[1],
        reverse=True
    ):

        result += (
            f"- {pack_name}: {count}\n"
        )

    return result.strip()


def about(
    knowledge_base,
    personality
):

    aliases = load_json(
        ALIASES_FILE
    )

    pack_counts = get_pack_counts()

    total_questions = len(
        knowledge_base.all_questions()
    )

    total_alias_groups = len(
        aliases
    )

    total_aliases = sum(
        len(alias_list)
        for alias_list in aliases.values()
    )

    total_packs = len(
        pack_counts
    )

    largest_pack = None

    if pack_counts:

        largest_pack = max(
            pack_counts,
            key=pack_counts.get
        )

    result = (
        "ReND Information\n\n"
        "Version: 2.1\n"
        "Status: Stable\n\n"
        "Knowledge:\n"
        f"- Questions: {total_questions}\n"
        f"- Alias groups: {total_alias_groups}\n"
        f"- Total aliases: {total_aliases}\n"
        f"- Knowledge packs: {total_packs}\n"
    )

    if largest_pack:

        result += (
            f"- Largest pack: "
            f"{largest_pack} ({pack_counts[largest_pack]})\n"
        )

    result += (
        "\nSystem:\n"
        f"- Personality: {personality}\n"
        "- Semantic Search: enabled\n"
        "- Related Knowledge: enabled\n"
        "- Context Memory: enabled\n"
        "- Learning System: enabled\n"
        "- Debug Tools: enabled\n\n"
        "Developer:\n"
        "ReD (Renato Dias Machado)"
    )

    return result


def find_question_pack(question):

    if not os.path.exists(
        PACKS_FOLDER
    ):

        return None

    for file_name in os.listdir(
        PACKS_FOLDER
    ):

        if not file_name.endswith(
            ".json"
        ):

            continue

        path = os.path.join(
            PACKS_FOLDER,
            file_name
        )

        data = load_json(
            path
        )

        if question in data:

            return file_name.replace(
                ".json",
                ""
            )

    return None


def find_knowledge(
    knowledge_base,
    search_text,
    limit=20
):

    search_text = (
        search_text.lower()
        .strip()
    )

    if not search_text:

        return "Use: /find <text>"

    matches = []

    for question in knowledge_base.all_questions():

        answer = knowledge_base.get(
            question
        )

        question_lower = question.lower()
        answer_lower = (
            answer.lower()
            if answer
            else ""
        )

        if (
            search_text in question_lower
            or
            search_text in answer_lower
        ):

            matches.append(
                (
                    question,
                    answer,
                    find_question_pack(
                        question
                    )
                )
            )

    if not matches:

        return (
            "No matching knowledge found."
        )

    result = (
        f"Find Results for: {search_text}\n\n"
    )

    for index, (
        question,
        answer,
        pack
    ) in enumerate(
        matches[:limit],
        start=1
    ):

        result += (
            f"{index}. {question}\n"
            f"   Pack: {pack}\n"
            f"   Answer: {answer}\n\n"
        )

    if len(matches) > limit:

        result += (
            f"...and {len(matches) - limit} more results."
        )

    return result.strip()


def find_alias(
    search_text,
    limit=20
):

    search_text = (
        search_text.lower()
        .strip()
    )

    if not search_text:

        return "Use: /findalias <text>"

    aliases = load_json(
        ALIASES_FILE
    )

    results = []

    for question, alias_list in aliases.items():

        for alias in alias_list:

            if search_text in alias.lower():

                results.append(
                    (
                        question,
                        alias,
                        find_question_pack(
                            question
                        )
                    )
                )

    if not results:

        return "No matching aliases found."

    result = (
        f"Alias Results for: {search_text}\n\n"
    )

    for index, (
        question,
        alias,
        pack
    ) in enumerate(
        results[:limit],
        start=1
    ):

        result += (
            f"{index}. {alias}\n"
            f"   Main Question: {question}\n"
            f"   Pack: {pack}\n\n"
        )

    if len(results) > limit:

        result += (
            f"...and {len(results) - limit} more results."
        )

    return result.strip()


def related(
    knowledge_base,
    search_engine,
    context
):

    last_match = (
        search_engine.last_successful_match
    )

    if not last_match:

        return (
            "No successful search found.\n\n"
            "Ask a knowledge question first."
        )

    main_question = (
        last_match.get(
            "main_question"
        )
    )

    if not main_question:

        return (
            "Could not determine the last "
            "main question."
        )

    related_questions = (
        get_related_questions(
            current_question=main_question,

            all_questions=
            knowledge_base.all_questions(),

            find_question_pack=
            find_question_pack,

            current_entity=
            context.recall(
                "last_entity"
            ),

            current_subject=
            context.recall(
                "last_subject"
            ),

            current_topic=
            context.recall(
                "last_topic"
            ),

            max_results=3,

            search_engine=
            search_engine
        )
    )

    if not related_questions:

        return (
            "No related knowledge found."
        )

    result = (
        "Related Knowledge\n\n"
        f"Current Question:\n"
        f"{main_question}\n\n"
    )

    for question in related_questions:

        pack = find_question_pack(
            question
        )

        result += (
            f"• {question}\n"
            f"  Pack: {pack}\n\n"
        )

    return result.strip()