import re


def process_memory(
    message,
    context,
    profile
):

    message_lower = message.lower().strip()

    name_match = re.search(
        r"my name is (.+)",
        message_lower
    )

    if name_match:

        name = name_match.group(1).strip()

        context.remember(
            "name",
            name
        )

        profile.remember(
            "name",
            name
        )

        return f"Nice to meet you, {name}."

    name_questions = [
        "what is my name",
        "what's my name",
        "whats my name",
        "do you know my name",
        "tell me my name"
    ]

    for question in name_questions:

        if question in message_lower:

            name = (
                context.recall("name")
                or profile.recall("name")
            )

            if name:
                return f"Your name is {name}."

            return "I don't know your name yet."

    return None