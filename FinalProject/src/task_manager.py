"""Business logic layer for managing tasks (add/update/delete/filter/statistics)."""

from __future__ import annotations

from datetime import datetime

from file_handler import FileHandler
from task import Task


class TaskManager:
    """Manages all task operations."""

    def __init__(self, filename: str = "tasks.json"):
        self.tasks: list[Task] = []
        self.file_handler = FileHandler(filename)
        self.load_tasks()

    def load_tasks(self) -> None:
        self.tasks = self.file_handler.load_tasks()

    def save_tasks(self) -> bool:
        return self.file_handler.save_tasks(self.tasks)

    def add_task(
        self,
        title: str,
        description: str = "",
        category: str = "General",
        priority: str = "Medium",
        due_date: str | None = None,
    ):
        if not title.strip():
            return False, "Title cannot be empty"

        task = Task(title, description, category, priority, due_date)
        self.tasks.append(task)
        self.save_tasks()
        return True, f"Task '{title}' added successfully (ID: {task.id})"

    def delete_task(self, task_id: int):
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            return True, f"Task {task_id} deleted successfully"
        return False, f"Task {task_id} not found"

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        category: str | None = None,
        priority: str | None = None,
        due_date: str | None = None,
        status: str | None = None,
    ):
        task = self.get_task_by_id(task_id)
        if not task:
            return False, f"Task {task_id} not found"

        if title:
            task.title = title
        if description is not None:
            task.description = description
        if category:
            task.category = category
        if priority:
            task.priority = priority
        if due_date:
            task.due_date = due_date

        if status:
            if status.lower() == "complete":
                task.mark_complete()
            elif status.lower() == "incomplete":
                task.mark_incomplete()

        self.save_tasks()
        return True, f"Task {task_id} updated successfully"

    def mark_complete(self, task_id: int):
        task = self.get_task_by_id(task_id)
        if task:
            task.mark_complete()
            self.save_tasks()
            return True, f"Task {task_id} marked as complete"
        return False, f"Task {task_id} not found"

    def mark_incomplete(self, task_id: int):
        task = self.get_task_by_id(task_id)
        if task:
            task.mark_incomplete()
            self.save_tasks()
            return True, f"Task {task_id} marked as incomplete"
        return False, f"Task {task_id} not found"

    def get_task_by_id(self, task_id: int) -> Task | None:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_all_tasks(self):
        return self.tasks

    def get_tasks_by_category(self, category: str):
        return [t for t in self.tasks if t.category.lower() == category.lower()]

    def get_tasks_by_priority(self, priority: str):
        return [t for t in self.tasks if t.priority.lower() == priority.lower()]

    def get_tasks_by_status(self, status: str):
        return [t for t in self.tasks if t.status.lower() == status.lower()]

    def get_overdue_tasks(self):
        return [t for t in self.tasks if t.is_overdue()]

    def get_incomplete_tasks(self):
        return self.get_tasks_by_status("Incomplete")

    def search_tasks(self, keyword: str):
        keyword = keyword.lower()
        return [
            t
            for t in self.tasks
            if keyword in t.title.lower() or keyword in t.description.lower()
        ]

    def get_tasks_due_today(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return [t for t in self.tasks if t.due_date == today and t.status == "Incomplete"]

    def sort_tasks_by_due_date(self, tasks=None):
        if tasks is None:
            tasks = self.tasks

        def sort_key(task: Task):
            if task.due_date:
                try:
                    return datetime.strptime(task.due_date, "%Y-%m-%d")
                except ValueError:
                    return datetime.max
            return datetime.max

        return sorted(tasks, key=sort_key)

    def sort_tasks_by_priority(self, tasks=None):
        if tasks is None:
            tasks = self.tasks
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        return sorted(tasks, key=lambda t: priority_order.get(t.priority, 999))

    def get_statistics(self):
        total = len(self.tasks)
        complete = len(self.get_tasks_by_status("Complete"))
        incomplete = len(self.get_incomplete_tasks())
        overdue = len(self.get_overdue_tasks())
        completion_rate = (complete / total * 100) if total > 0 else 0

        categories = {}
        for t in self.tasks:
            categories[t.category] = categories.get(t.category, 0) + 1

        priorities = {}
        for t in self.tasks:
            priorities[t.priority] = priorities.get(t.priority, 0) + 1

        return {
            "total_tasks": total,
            "completed_tasks": complete,
            "incomplete_tasks": incomplete,
            "overdue_tasks": overdue,
            "completion_rate": completion_rate,
            "tasks_by_category": categories,
            "tasks_by_priority": priorities,
        }

