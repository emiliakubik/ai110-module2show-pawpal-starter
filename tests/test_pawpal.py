"""
Tests for PawPal+ system
"""

import pytest
from pawpal_system import Task, Pet, Owner, Scheduler


class TestTask:
    """Tests for Task class"""
    
    def test_task_completion(self):
        """Verify that calling mark_complete() actually changes the task's status"""
        # Create a task that starts incomplete
        task = Task(
            description="Morning walk",
            duration=30,
            frequency="daily",
            priority=5
        )
        
        # Verify initial state is incomplete
        assert task.completed == False
        
        # Mark task as complete
        task.mark_complete()
        
        # Verify status changed to complete
        assert task.completed == True
        
        # Test mark_incomplete() as well
        task.mark_incomplete()
        assert task.completed == False


class TestPet:
    """Tests for Pet class"""
    
    def test_task_addition(self):
        """Verify that adding a task to a Pet increases that pet's task count"""
        # Create a pet
        pet = Pet(name="Max", species="Dog", age=3)
        
        # Verify pet starts with 0 tasks
        initial_count = len(pet.get_all_tasks())
        assert initial_count == 0
        
        # Create and add a task
        task1 = Task(
            description="Morning walk",
            duration=30,
            frequency="daily",
            priority=5
        )
        pet.add_task(task1)
        
        # Verify task count increased to 1
        assert len(pet.get_all_tasks()) == 1
        
        # Add another task
        task2 = Task(
            description="Feeding",
            duration=10,
            frequency="daily",
            priority=5
        )
        pet.add_task(task2)
        
        # Verify task count increased to 2
        assert len(pet.get_all_tasks()) == 2
