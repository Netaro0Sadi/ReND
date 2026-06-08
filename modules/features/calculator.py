import re


def calculate(text):
    try:
        text = text.lower()

        text = text.replace("plus", "+")
        text = text.replace("minus", "-")
        text = text.replace("times", "*")
        text = text.replace("multiplied by", "*")
        text = text.replace("divided by", "/")

        expression = re.findall(
            r"[0-9+\-*/(). ]+",
            text
        )

        if not expression:
            return None

        expression = "".join(expression).strip()

        if not expression:
            return None

        return str(eval(expression))

    except:
        return None