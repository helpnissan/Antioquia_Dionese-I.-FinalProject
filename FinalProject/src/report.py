"""Utility functions and CLI helpers for the Task Manager application."""

from __future__ import annotations

from datetime import datetime


def validate_date(date_string: str) -> bool:
    """Validate date format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_priority(priority: str) -> bool:
    """Validate priority level."""
    return priority in ["High", "Medium", "Low"]


def validate_status(status: str) -> bool:
    """Validate status."""
    return status in ["Complete", "Incomplete"]


def get_valid_input(prompt: str, validation_func=None) -> str:
    """Get validated user input."""
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print("Input cannot be empty. Please try again.")
            continue

        if validation_func and not validation_func(user_input):
            print(f"Invalid input: {user_input}. Please try again.")
            continue

        return user_input


def get_integer_input(prompt: str, min_val=None, max_val=None) -> int:
    """Get validated integer input."""
    while True:
        try:
            value = int(input(prompt).strip())
            if min_val is not None and value < min_val:
                print(f"Value must be >= {min_val}. Please try again.")
                continue
            if max_val is not None and value > max_val:
                print(f"Value must be <= {max_val}. Please try again.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def format_task_display(task) -> str:
    """Format task for display."""
    overdue_indicator = " [OVERDUE!]" if task.is_overdue() else ""
    status_symbol = "✓" if task.status == "Complete" else "○"
    return (
        f"{status_symbol} [{task.id}] {task.title} - {task.priority} - {task.status}{overdue_indicator}"
    )


def display_tasks(tasks, show_details: bool = False) -> None:
    """Display a list of tasks."""
    if not tasks:
        print("\nNo tasks found.\n")
        return

    print("\n" + "=" * 80)
    for task in tasks:
        print(format_task_display(task))
        if show_details:
            print(f"   Category: {task.category}")
            print(f"   Due Date: {task.due_date if task.due_date else 'No due date'}")
            if task.description:
                print(f"   Description: {task.description}")
            print()
    print("=" * 80 + "\n")


def display_statistics(stats: dict) -> None:
    """Display task statistics."""
    print("\n" + "=" * 80)
    print("TASK STATISTICS".center(80))
    print("=" * 80)
    print(f"Total Tasks: {stats['total_tasks']}")
    print(f"Completed: {stats['completed_tasks']}")
    print(f"Incomplete: {stats['incomplete_tasks']}")
    print(f"Overdue: {stats['overdue_tasks']}")
    print(f"Completion Rate: {stats['completion_rate']:.1f}%")

    print("\nTasks by Priority:")
    for priority, count in sorted(stats["tasks_by_priority"].items()):
        print(f"  {priority}: {count}")

    print("\nTasks by Category:")
    for category, count in sorted(stats["tasks_by_category"].items()):
        print(f"  {category}: {count}")

    print("=" * 80 + "\n")


def clear_screen() -> None:
    """Clear console screen."""
    import os

    os.system("cls" if os.name == "nt" else "clear")


def display_menu() -> None:
    """Display main menu."""
    print("\n" + "=" * 80)
    print("TASK MANAGER APPLICATION".center(80))
    print("=" * 80)
    print("1.  View All Tasks")
    print("2.  Add New Task")
    print("3.  Delete Task")
    print("4.  View Tasks by Category")
    print("5.  View Tasks by Priority")
    print("6.  View Overdue Tasks")
    print("7.  View Tasks Due Today")
    print("8.  Mark Task as Complete")
    print("9.  Mark Task as Incomplete")
    print("10. Search Tasks")
    print("0.  Exit")
    print("=" * 80)

