def list_questions(knowledge_base):

    questions = knowledge_base.all_questions()

    if not questions:
        return "No questions learned yet."

    result = "\nLearned questions:\n\n"

    for index, question in enumerate(
        questions,
        start=1
    ):

        result += (
            f"{index}. "
            f"{question}\n"
        )

    return result


def stats(
    knowledge_base,
    context,
    personality
):

    total_questions = len(
        knowledge_base.all_questions()
    )

    last_intent = context.recall(
        "last_intent"
    )

    last_subject = context.recall(
        "last_subject"
    )

    last_entity = context.recall(
        "last_entity"
    )

    last_topic = context.recall(
        "last_topic"
    )

    return (
        "ReND Statistics\n\n"
        f"Questions: {total_questions}\n"
        f"Personality: {personality}\n\n"
        "Memory:\n"
        f"- Last Intent: {last_intent}\n"
        f"- Last Subject: {last_subject}\n"
        f"- Last Entity: {last_entity}\n"
        f"- Last Topic: {last_topic}"
    )


def memory_status(context):

    last_intent = context.recall(
        "last_intent"
    )

    last_subject = context.recall(
        "last_subject"
    )

    last_entity = context.recall(
        "last_entity"
    )

    last_topic = context.recall(
        "last_topic"
    )

    return (
        "Memory Status\n\n"
        f"Last Intent: {last_intent}\n"
        f"Last Subject: {last_subject}\n"
        f"Last Entity: {last_entity}\n"
        f"Last Topic: {last_topic}"
    )


def clear_memory(context):

    context.clear()

    return "Memory cleared."


def help_menu():

    return (
        "Available Commands\n\n"
        "/list - Show learned questions\n"
        "/stats - Show ReND statistics\n"
        "/memory - Show context memory\n"
        "/memory clear - Clear context memory\n"
        "/personality - Show personalities\n"
        "/setpersonality <name> - Change personality\n"
        "/reload - Reload knowledge base\n"
        "/debug - Show debug information\n"
        "/version - Show system version\n"
        "/edit - Edit a learned answer\n"
        "/remove - Remove a learned question\n"
        "/help - Show this help menu\n"
        "/learn - Teach ReND in English\n"
        "/learnpt - Teach ReND in Portuguese\n"
        "/why - Show why ReND chose the last answer\n"
    )


def version():

    return (
        "ReND Version Information\n\n"

        "Version: 2.1\n"
        "Status: Stable\n\n"

        "Core Features:\n"
        "✓ Semantic Search\n"
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

        "Commands:\n"
        "✓ /help\n"
        "✓ /stats\n"
        "✓ /memory\n"
        "✓ /personality\n"
        "✓ /reload\n"
        "✓ /debug\n"
        "✓ /version\n"
        "✓ /edit\n"
        "✓ /remove\n\n"

        "Context Features:\n"
        "✓ Capital Follow-up\n"
        "✓ Continent Follow-up\n"
        "✓ Weather Follow-up\n"
        "✓ Person Follow-up\n"
        "✓ Concept Follow-up\n"
        "✓ Explain Better\n"
        "✓ Pronoun Resolution\n\n"

        "Architecture:\n"
        "✓ Knowledge Packs\n"
        "✓ Semantic Embeddings\n"
        "✓ Alias Generation\n"
        "✓ Context Tracking\n"
        "✓ Personality Persistence\n\n"

        "Developer:\n"
        "ReD (Renato Dias Machado)"
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