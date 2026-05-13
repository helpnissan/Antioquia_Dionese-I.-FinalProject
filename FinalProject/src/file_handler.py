"""File persistence utilities for saving/loading/restoring tasks."""

from __future__ import annotations

import json
import os
from datetime import datetime

from task import Task


class FileHandler:
    """Handles file operations for task persistence."""

    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.backup_folder = "backups"
        self.ensure_backup_folder()

    def ensure_backup_folder(self) -> None:
        if not os.path.exists(self.backup_folder):
            os.makedirs(self.backup_folder)

    def save_tasks(self, tasks: list[Task]) -> bool:
        try:
            data = {
                "tasks": [task.to_dict() for task in tasks],
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            return True
        except Exception as e:
            print(f"Error saving tasks: {e}")
            return False

    def load_tasks(self) -> list[Task]:
        try:
            if not os.path.exists(self.filename):
                return []
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
            return [Task.from_dict(t) for t in data.get("tasks", [])]
        except Exception as e:
            print(f"Error loading tasks: {e}")
            return []

    def backup_tasks(self) -> bool:
        """Create a backup of current tasks file."""
        try:
            if os.path.exists(self.filename):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"{self.backup_folder}/backup_{timestamp}.json"
                with open(self.filename, "r", encoding="utf-8") as original:
                    with open(backup_name, "w", encoding="utf-8") as backup:
                        backup.write(original.read())
                return True
            return False
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False

    def restore_backup(self, backup_name: str) -> bool:
        """Restore tasks from a backup file."""
        try:
            backup_path = f"{self.backup_folder}/{backup_name}"
            if os.path.exists(backup_path):
                with open(backup_path, "r", encoding="utf-8") as backup:
                    with open(self.filename, "w", encoding="utf-8") as original:
                        original.write(backup.read())
                return True
            return False
        except Exception as e:
            print(f"Error restoring backup: {e}")
            return False

