import subprocess
import sys

TOOLS = {

    "health": [
        "tools/health.py"
    ],

    "audit": [
        "tools/audit/alias_audit.py",
        "tools/audit/full_knowledge_audit.py"
    ],

    "fix": [
        "tools/maintenance/fix_duplicate_aliases.py",
        "tools/maintenance/fix_duplicate_questions.py"
    ],

    "generate": [
        "tools/generators/generate_aliases.py"
    ],

    "migrate": [
        "tools/migrations/auto_pack_migration.py"
    ],

    "import": [
        "tools/importers/import_knowledge.py"
    ]
}


def run_script(path):

    print("=" * 50)
    print(f"Running: {path}")
    print("=" * 50)

    result = subprocess.run(
        [sys.executable, path],
        text=True
    )

    if result.returncode != 0:

        print(f"Error running: {path}")
        return False

    return True


def show_help():

    print("ReND Toolbox\n")
    print("Usage:")
    print("python tools/toolbox.py <command>\n")

    print("Commands:")

    for command in TOOLS:

        print(f"- {command}")

    print("\nExamples:")
    print("python tools/toolbox.py audit")
    print("python tools/toolbox.py fix")
    print("python tools/toolbox.py generate")
    print("python tools/toolbox.py health")

def interactive_menu():

    commands = list(
        TOOLS.keys()
    )

    while True:

        print("\n" + "=" * 40)
        print("ReND Toolbox")
        print("=" * 40)

        for index, command in enumerate(
            commands,
            start=1
        ):

            DISPLAY_NAMES = {
                "health": "Health Check",
                "audit": "Audit",
                "fix": "Maintenance",
                "generate": "Generators",
                "migrate": "Migrations",
                "import": "Importers"
            }

            print(
                f"{index}. {DISPLAY_NAMES.get(command, command.title())}"
            )

        print("0. Exit")

        choice = input(
            "\nSelect an option: "
        ).strip()

        if choice == "0":

            print("Goodbye.")
            return

        if not choice.isdigit():

            print("Invalid option.")
            continue

        choice = int(choice)

        if choice < 1 or choice > len(commands):

            print("Invalid option.")
            continue

        command = commands[
            choice - 1
        ]

        success_count = 0
        fail_count = 0

        for script in TOOLS[
            command
        ]:

            success = run_script(
                script
            )

            if success:
                success_count += 1
            else:
                fail_count += 1

        print("\nSummary")
        print(
            f"Successful: {success_count}"
        )
        print(
            f"Failed: {fail_count}"
        )

        input(
            "\nPress ENTER to continue..."
        )

def main():

    if len(sys.argv) < 2:

        interactive_menu()
        return

    command = sys.argv[1].lower().strip()

    if command not in TOOLS:

        print(f"Unknown command: {command}\n")
        show_help()
        return

    success_count = 0
    fail_count = 0

    for script in TOOLS[command]:

        success = run_script(
            script
        )

        if success:
            success_count += 1
        else:
            fail_count += 1

    print("=" * 50)
    print("Toolbox Summary")
    print("=" * 50)
    print(f"Successful: {success_count}")
    print(f"Failed: {fail_count}")


if __name__ == "__main__":

    main()