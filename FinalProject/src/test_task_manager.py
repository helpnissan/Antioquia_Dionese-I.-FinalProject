"""Unit tests for the Task Manager application."""

import unittest
import os
import json
from datetime import datetime, timedelta
from task import Task
from task_manager import TaskManager
from file_handler import FileHandler

class TestTask(unittest.TestCase):
    """Test cases for Task class."""
    
    def setUp(self):
        """Reset task counter before each test."""
        Task.task_counter = 1
    
    def test_task_creation(self):
        """Test creating a task."""
        task = Task("Buy groceries")
        self.assertEqual(task.title, "Buy groceries")
        self.assertEqual(task.status, "Incomplete")
        self.assertEqual(task.id, 1)
    
    def test_task_mark_complete(self):
        """Test marking task as complete."""
        task = Task("Study Python")
        task.mark_complete()
        self.assertEqual(task.status, "Complete")
    
    def test_task_mark_incomplete(self):
        """Test marking task as incomplete."""
        task = Task("Study Python")
        task.mark_complete()
        task.mark_incomplete()
        self.assertEqual(task.status, "Incomplete")
    
    def test_task_is_overdue(self):
        """Test overdue detection."""
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        task = Task("Late task", due_date=yesterday)
        self.assertTrue(task.is_overdue())
    
    def test_task_not_overdue(self):
        """Test task not overdue if complete."""
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        task = Task("Late task", due_date=yesterday)
        task.mark_complete()
        self.assertFalse(task.is_overdue())
    
    def test_task_future_date_not_overdue(self):
        """Test future date is not overdue."""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        task = Task("Future task", due_date=tomorrow)
        self.assertFalse(task.is_overdue())
    
    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task = Task("Test task", "Description", "Work", "High", "2026-05-20")
        task_dict = task.to_dict()
        self.assertEqual(task_dict["title"], "Test task")
        self.assertEqual(task_dict["category"], "Work")
        self.assertEqual(task_dict["priority"], "High")
    
    def test_task_from_dict(self):
        """Test creating task from dictionary."""
        data = {
            "id": 1,
            "title": "Test task",
            "description": "Description",
            "category": "Work",
            "priority": "High",
            "due_date": "2026-05-20",
            "status": "Incomplete",
            "created_at": "2026-05-11"
        }
        task = Task.from_dict(data)
        self.assertEqual(task.title, "Test task")
        self.assertEqual(task.id, 1)
    
    def test_task_string_representation(self):
        """Test task string representation."""
        task = Task("Test task")
        self.assertIn("Test task", str(task))
        self.assertIn("Incomplete", str(task))

class TestFileHandler(unittest.TestCase):
    """Test cases for FileHandler class."""
    
    def setUp(self):
        """Create test file handler."""
        self.test_file = "test_tasks.json"
        self.handler = FileHandler(self.test_file)
        Task.task_counter = 1
    
    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_save_and_load_tasks(self):
        """Test saving and loading tasks."""
        tasks = [
            Task("Task 1"),
            Task("Task 2", category="Work"),
            Task("Task 3", priority="High")
        ]
        
        self.handler.save_tasks(tasks)
        loaded_tasks = self.handler.load_tasks()
        
        self.assertEqual(len(loaded_tasks), 3)
        self.assertEqual(loaded_tasks[0].title, "Task 1")
        self.assertEqual(loaded_tasks[1].category, "Work")
    
    def test_load_nonexistent_file(self):
        """Test loading from nonexistent file returns empty list."""
        handler = FileHandler("nonexistent.json")
        tasks = handler.load_tasks()
        self.assertEqual(tasks, [])
    
    def test_backup_creation(self):
        """Test backup creation."""
        tasks = [Task("Test task")]
        self.handler.save_tasks(tasks)
        backup_created = self.handler.backup_tasks()
        self.assertTrue(backup_created)
        self.assertTrue(os.path.exists("backups"))

class TestTaskManager(unittest.TestCase):
    """Test cases for TaskManager class."""
    
    def setUp(self):
        """Create test task manager."""
        self.test_file = "test_manager.json"
        self.manager = TaskManager(self.test_file)
        Task.task_counter = 1
    
    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_add_task(self):
        """Test adding a task."""
        success, message = self.manager.add_task("Test task")
        self.assertTrue(success)
        self.assertEqual(len(self.manager.tasks), 1)
    
    def test_add_empty_task(self):
        """Test adding task with empty title."""
        success, message = self.manager.add_task("")
        self.assertFalse(success)
        self.assertEqual(len(self.manager.tasks), 0)
    
    def test_delete_task(self):
        """Test deleting a task."""
        self.manager.add_task("Task to delete")
        success, message = self.manager.delete_task(1)
        self.assertTrue(success)
        self.assertEqual(len(self.manager.tasks), 0)
    
    def test_delete_nonexistent_task(self):
        """Test deleting nonexistent task."""
        success, message = self.manager.delete_task(999)
        self.assertFalse(success)
    
    def test_get_task_by_id(self):
        """Test getting task by ID."""
        self.manager.add_task("Find me")
        task = self.manager.get_task_by_id(1)
        self.assertIsNotNone(task)
        self.assertEqual(task.title, "Find me")
    
    def test_update_task(self):
        """Test updating task."""
        self.manager.add_task("Original title")
        success, message = self.manager.update_task(1, title="Updated title")
        self.assertTrue(success)
        task = self.manager.get_task_by_id(1)
        self.assertEqual(task.title, "Updated title")
    
    def test_mark_complete(self):
        """Test marking task complete."""
        self.manager.add_task("Complete me")
        self.manager.mark_complete(1)
        task = self.manager.get_task_by_id(1)
        self.assertEqual(task.status, "Complete")
    
    def test_get_tasks_by_category(self):
        """Test filtering by category."""
        self.manager.add_task("Work task", category="Work")
        self.manager.add_task("Personal task", category="Personal")
        
        work_tasks = self.manager.get_tasks_by_category("Work")
        self.assertEqual(len(work_tasks), 1)
        self.assertEqual(work_tasks[0].category, "Work")
    
    def test_get_tasks_by_priority(self):
        """Test filtering by priority."""
        self.manager.add_task("High priority", priority="High")
        self.manager.add_task("Low priority", priority="Low")
        
        high_tasks = self.manager.get_tasks_by_priority("High")
        self.assertEqual(len(high_tasks), 1)
    
    def test_get_tasks_by_status(self):
        """Test filtering by status."""
        self.manager.add_task("Incomplete task")
        self.manager.add_task("Complete task")
        self.manager.mark_complete(2)
        
        incomplete = self.manager.get_tasks_by_status("Incomplete")
        self.assertEqual(len(incomplete), 1)
    
    def test_get_overdue_tasks(self):
        """Test getting overdue tasks."""
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        self.manager.add_task("Overdue", due_date=yesterday)
        
        overdue = self.manager.get_overdue_tasks()
        self.assertEqual(len(overdue), 1)
    
    def test_search_tasks(self):
        """Test searching tasks."""
        self.manager.add_task("Python project")
        self.manager.add_task("Java homework")
        
        results = self.manager.search_tasks("Python")
        self.assertEqual(len(results), 1)
        self.assertIn("Python", results[0].title)
    
    def test_sort_by_priority(self):
        """Test sorting by priority."""
        self.manager.add_task("Low", priority="Low")
        self.manager.add_task("High", priority="High")
        self.manager.add_task("Medium", priority="Medium")
        
        sorted_tasks = self.manager.sort_tasks_by_priority()
        self.assertEqual(sorted_tasks[0].priority, "High")
        self.assertEqual(sorted_tasks[1].priority, "Medium")
        self.assertEqual(sorted_tasks[2].priority, "Low")
    
    def test_sort_by_due_date(self):
        """Test sorting by due date."""
        today = datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        self.manager.add_task("Due tomorrow", due_date=tomorrow)
        self.manager.add_task("Due today", due_date=today)
        
        sorted_tasks = self.manager.sort_tasks_by_due_date()
        self.assertEqual(sorted_tasks[0].due_date, today)
        self.assertEqual(sorted_tasks[1].due_date, tomorrow)
    
    def test_get_statistics(self):
        """Test getting statistics."""
        self.manager.add_task("Task 1", category="Work", priority="High")
        self.manager.add_task("Task 2", category="Personal", priority="Low")
        self.manager.mark_complete(1)
        
        stats = self.manager.get_statistics()
        self.assertEqual(stats["total_tasks"], 2)
        self.assertEqual(stats["completed_tasks"], 1)
        self.assertEqual(stats["incomplete_tasks"], 1)
        self.assertEqual(stats["completion_rate"], 50.0)

if __name__ == "__main__":
    unittest.main()