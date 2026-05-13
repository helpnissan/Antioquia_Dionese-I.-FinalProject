"""Task data model for the Task Manager application."""

from __future__ import annotations

from datetime import datetime


class Task:
    """Represents a single task with properties and methods."""

    task_counter = 1  # Class variable to auto-generate IDs

    def __init__(
        self,
        title: str,
        description: str = "",
        category: str = "General",
        priority: str = "Medium",
        due_date: str | None = None,  # Format: "YYYY-MM-DD"
    ):
        self.id = Task.task_counter
        Task.task_counter += 1

        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.due_date = due_date
        self.status = "Incomplete"
        self.created_at = datetime.now().strftime("%Y-%m-%d")

    def mark_complete(self) -> None:
        self.status = "Complete"

    def mark_incomplete(self) -> None:
        self.status = "Incomplete"

    def is_overdue(self) -> bool:
        if self.status == "Complete" or not self.due_date:
            return False
        try:
            due = datetime.strptime(self.due_date, "%Y-%m-%d")
            return due < datetime.now()
        except ValueError:
            return False

    def get_details(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "due_date": self.due_date,
            "status": self.status,
            "created_at": self.created_at,
        }

    def to_dict(self) -> dict:
        return self.get_details()

    @staticmethod
    def from_dict(data: dict) -> "Task":
        task = Task(
            title=data.get("title"),
            description=data.get("description", ""),
            category=data.get("category", "General"),
            priority=data.get("priority", "Medium"),
            due_date=data.get("due_date"),
        )
        task.id = data.get("id")
        task.status = data.get("status", "Incomplete")
        task.created_at = data.get("created_at")
        Task.task_counter = max(Task.task_counter, task.id + 1)
        return task

    def __str__(self) -> str:
        overdue_indicator = " [OVERDUE!]" if self.is_overdue() else ""
        return f"[{self.id}] {self.title} - {self.status}{overdue_indicator}"

    def __repr__(self) -> str:
        return f"Task({self.id}, {self.title}, {self.status})"

