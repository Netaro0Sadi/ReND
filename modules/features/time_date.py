from datetime import datetime


def handle_time_date(message):

    message = message.lower().strip()

    now = datetime.now()

    time_phrases = [
        "what time is it",
        "current time",
        "que horas sao",
        "que horas são",
        "qual horario",
        "qual horário"
    ]

    date_phrases = [
        "what is today's date",
        "today's date",
        "what date is it",
        "qual a data de hoje",
        "que dia é hoje",
        "que dia e hoje"
    ]

    for phrase in time_phrases:

        if phrase in message:

            return now.strftime(
                "It is %H:%M."
            )

    for phrase in date_phrases:

        if phrase in message:

            return now.strftime(
                "Today is %d/%m/%Y."
            )

    return None