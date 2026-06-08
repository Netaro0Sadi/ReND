def handle_greeting(message):

    message = message.lower().strip()

    greetings = {
        "hi": "Hello!",
        "hello": "Hello!",
        "hey": "Hey!",
        "oi": "Olá!",
        "ola": "Olá!",
        "olá": "Olá!",
        "hola": "¡Hola!"
    }

    return greetings.get(message)