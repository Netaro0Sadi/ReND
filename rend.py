import os

os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

from modules.router import process_message

print("=" * 40)
print("ReND Artificial Intelligence")
print("=" * 40)

print("System Ready.")
print("Type 'exit' to close.\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":

        print("ReND: Goodbye.")
        break

    response = process_message(
        user_input
    )

    print("ReND:", response)