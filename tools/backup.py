import os
import shutil
from datetime import datetime


DATA_FOLDER = "data"
BACKUP_FOLDER = "data/backups"


def create_backup():

    os.makedirs(
        BACKUP_FOLDER,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    copied = 0

    for root, _, files in os.walk(
        DATA_FOLDER
    ):

        if root.startswith(
            BACKUP_FOLDER
        ):
            continue

        for file in files:

            if not file.endswith(".json"):
                continue

            source = os.path.join(
                root,
                file
            )

            relative = os.path.relpath(
                source,
                DATA_FOLDER
            )

            relative = relative.replace(
                "\\",
                "_"
            ).replace(
                "/",
                "_"
            )

            destination = os.path.join(
                BACKUP_FOLDER,
                f"{timestamp}_{relative}"
            )

            shutil.copy2(
                source,
                destination
            )

            copied += 1

    print(
        f"Backup created ({copied} files)."
    )