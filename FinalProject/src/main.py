"""CLI entrypoint for the Task Manager application."""

import os
import sys

# Ensure imports work when running `python src/main.py` directly.
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from task_manager import TaskManager
from report import (
    display_menu,
    display_tasks,
    display_statistics,
    get_integer_input,
    get_valid_input,
    validate_date,
    validate_priority,
)


def main() -> None:
    """Main application loop."""
    manager = TaskManager()

    while True:
        display_menu()
        choice = input("Enter your choice (0-10): ").strip()

        if choice == "1":
            tasks = manager.get_all_tasks()
            if tasks:
                sorted_tasks = manager.sort_tasks_by_priority(tasks)
                display_tasks(sorted_tasks, show_details=True)
            else:
                print("\nNo tasks found.\n")

        elif choice == "2":
            print("\n" + "=" * 80)
            print("ADD NEW TASK".center(80))
            print("=" * 80)

            title = get_valid_input("Enter task title: ")
            description = input("Enter task description (optional): ").strip()
            category = input("Enter category (default: General): ").strip() or "General"

            while True:
                priority = input("Enter priority (High/Medium/Low): ").strip()
                if validate_priority(priority):
                    break
                print("Invalid priority. Please enter High, Medium, or Low.")

            due_date = None
            while True:
                due_date_input = input(
                    "Enter due date (YYYY-MM-DD) or press Enter to skip: "
                ).strip()
                if not due_date_input:
                    break
                if validate_date(due_date_input):
                    due_date = due_date_input
                    break
                print("Invalid date format. Please use YYYY-MM-DD.")

            success, message = manager.add_task(title, description, category, priority, due_date)
            print(f"\n{message}\n")

        elif choice == "3":
            print("\n" + "=" * 80)
            print("DELETE TASK".center(80))
            print("=" * 80)

            tasks = manager.get_all_tasks()
            if not tasks:
                print("No tasks to delete.\n")
                continue

            display_tasks(tasks)
            task_id = get_integer_input("Enter task ID to delete: ")

            confirm = input(
                f"Are you sure you want to delete task {task_id}? (yes/no): "
            ).strip().lower()
            if confirm == "yes":
                success, message = manager.delete_task(task_id)
                print(f"\n{message}\n")
            else:
                print("\nDeletion cancelled.\n")

        elif choice == "4":
            print("\n" + "=" * 80)
            categories = set(t.category for t in manager.get_all_tasks())
            if not categories:
                print("No tasks found.\n")
                continue

            print("Available categories:")
            for cat in sorted(categories):
                print(f"  - {cat}")

            category = get_valid_input("Enter category to filter by: ")
            tasks = manager.get_tasks_by_category(category)
            print(f"\nTasks in '{category}' category:")
            display_tasks(tasks, show_details=True)

        elif choice == "5":
            print("\n" + "=" * 80)
            for priority in ["High", "Medium", "Low"]:
                tasks = manager.get_tasks_by_priority(priority)
                print(f"\n{priority} Priority Tasks ({len(tasks)}):")
                if tasks:
                    display_tasks(tasks)
                else:
                    print("No tasks.\n")

        elif choice == "6":
            print("\n" + "=" * 80)
            print("OVERDUE TASKS".center(80))
            print("=" * 80)

            overdue_tasks = manager.get_overdue_tasks()
            display_tasks(overdue_tasks, show_details=True)

        elif choice == "7":
            print("\n" + "=" * 80)
            print("TASKS DUE TODAY".center(80))
            print("=" * 80)

            today_tasks = manager.get_tasks_due_today()
            display_tasks(today_tasks, show_details=True)

        elif choice == "8":
            print("\n" + "=" * 80)
            incomplete_tasks = manager.get_incomplete_tasks()
            if not incomplete_tasks:
                print("No incomplete tasks.\n")
                continue

            display_tasks(incomplete_tasks)
            task_id = get_integer_input("Enter task ID to mark as complete: ")
            success, message = manager.mark_complete(task_id)
            print(f"\n{message}\n")

        elif choice == "9":
            print("\n" + "=" * 80)
            complete_tasks = manager.get_tasks_by_status("Complete")
            if not complete_tasks:
                print("No completed tasks.\n")
                continue

            display_tasks(complete_tasks)
            task_id = get_integer_input("Enter task ID to mark as incomplete: ")
            success, message = manager.mark_incomplete(task_id)
            print(f"\n{message}\n")

        elif choice == "10":
            print("\n" + "=" * 80)
            keyword = get_valid_input("Enter search keyword: ")
            tasks = manager.search_tasks(keyword)
            print(f"\nSearch results for '{keyword}':")
            display_tasks(tasks, show_details=True)

        elif choice == "0":
            print("\nThank you for using Task Manager. Goodbye!\n")
            break

        else:
            print("\nInvalid choice. Please try again.\n")


if __name__ == "__main__":
    main()

