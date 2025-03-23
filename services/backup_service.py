import os
import shutil
from datetime import datetime

BACKUP_FOLDER = "backups/"


def backup_database():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"{BACKUP_FOLDER}backup_{timestamp}.json"

    os.system(f"mongodump --out {backup_filename}")

    return {"message": "Backup completed", "backup_file": backup_filename}


def restore_database(backup_file: str):
    os.system(f"mongorestore --drop {backup_file}")
    return {"message": "Database restored from backup"}