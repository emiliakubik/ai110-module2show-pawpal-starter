"""
Tests for PawPal+ system
"""

import pytest
from datetime import datetime, timedelta
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
        assert task.last_completed is None
        
        # Mark task as complete
        task.mark_complete()
        
        # Verify status changed to complete
        assert task.completed == True
        assert task.last_completed is not None
        
        # Test mark_incomplete() as well
        task.mark_incomplete()
        assert task.completed == False
        assert task.last_completed is None
    
    def test_is_due_today_never_completed(self):
        """Verify tasks that have never been completed are due"""
        task = Task(
            description="Morning walk",
            duration=30,
            frequency="daily",
            priority=5
        )
        
        # Never completed, should be due
        assert task.is_due_today() == True
    
    def test_is_due_today_daily_task(self):
        """Verify daily task frequency logic"""
        task = Task(
            description="Morning walk",
            duration=30,
            frequency="daily",
            priority=5
        )
        
        # Completed just now, not due yet
        task.last_completed = datetime.now()
        assert task.is_due_today() == False
        
        # Completed 2 days ago, should be due
        task.last_completed = datetime.now() - timedelta(days=2)
        assert task.is_due_today() == True
    
    def test_is_due_today_weekly_task(self):
        """Verify weekly task frequency logic"""
        task = Task(
            description="Grooming",
            duration=30,
            frequency="weekly",
            priority=3
        )
        
        # Completed 3 days ago, not due yet
        task.last_completed = datetime.now() - timedelta(days=3)
        assert task.is_due_today() == False
        
        # Completed 8 days ago, should be due
        task.last_completed = datetime.now() - timedelta(days=8)
        assert task.is_due_today() == True


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


class TestScheduler:
    """Tests for Scheduler class"""
    
    def test_critical_tasks_scheduled_first(self):
        """Verify priority 5 tasks are scheduled before lower priority tasks"""
        owner = Owner(name="Test", available_time=60)
        pet = Pet(name="Max", species="Dog")
        
        # Add tasks with different priorities
        critical_task = Task(
            description="Medication",
            duration=5,
            frequency="daily",
            priority=5
        )
        low_task = Task(
            description="Play time",
            duration=30,
            frequency="daily",
            priority=2
        )
        
        # Add in reverse order (low priority first)
        pet.add_task(low_task)
        pet.add_task(critical_task)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        plan = scheduler.generate_daily_plan()
        
        # Critical task should be scheduled first
        assert len(plan['scheduled']) == 2
        assert plan['scheduled'][0][1].priority == 5
        assert plan['scheduled'][0][1].description == "Medication"
    
    def test_pet_batching(self):
        """Verify tasks are batched by pet when priorities are equal"""
        owner = Owner(name="Test", available_time=100)
        dog = Pet(name="Max", species="Dog")
        cat = Pet(name="Whiskers", species="Cat")
        
        # Add priority 3 tasks to both pets
        dog_task1 = Task(description="Walk", duration=20, frequency="daily", priority=3)
        dog_task2 = Task(description="Play", duration=15, frequency="daily", priority=3)
        cat_task = Task(description="Groom", duration=10, frequency="daily", priority=3)
        
        dog.add_task(dog_task1)
        dog.add_task(dog_task2)
        cat.add_task(cat_task)
        
        owner.add_pet(dog)
        owner.add_pet(cat)
        
        scheduler = Scheduler(owner)
        plan = scheduler.generate_daily_plan()
        
        # All tasks should be scheduled
        assert len(plan['scheduled']) == 3
        
        # Tasks for same pet should be consecutive (batched)
        if plan['scheduled'][0][0].name == "Max":
            assert plan['scheduled'][1][0].name == "Max"  # Second task should also be Max
        else:
            assert plan['scheduled'][0][0].name == "Whiskers"
