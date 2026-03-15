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
    
    def test_sorting_correctness_ascending(self):
        """Verify tasks are sorted by duration in ascending order (shortest first)"""
        owner = Owner(name="Test", available_time=100)
        pet = Pet(name="Max", species="Dog")
        
        # Add tasks with different durations (out of order)
        task_30 = Task(description="Walk", duration=30, frequency="daily", priority=3)
        task_10 = Task(description="Feed", duration=10, frequency="daily", priority=3)
        task_45 = Task(description="Play", duration=45, frequency="daily", priority=3)
        task_5 = Task(description="Medication", duration=5, frequency="daily", priority=3)
        
        pet.add_task(task_30)
        pet.add_task(task_10)
        pet.add_task(task_45)
        pet.add_task(task_5)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        
        # Get all incomplete tasks
        all_tasks = owner.get_all_incomplete_tasks()
        
        # Sort by time (ascending)
        sorted_tasks = scheduler.sort_by_time(all_tasks, ascending=True)
        
        # Verify chronological order (shortest to longest)
        assert len(sorted_tasks) == 4
        assert sorted_tasks[0][1].duration == 5   # Shortest
        assert sorted_tasks[1][1].duration == 10
        assert sorted_tasks[2][1].duration == 30
        assert sorted_tasks[3][1].duration == 45  # Longest
    
    def test_sorting_correctness_descending(self):
        """Verify tasks are sorted by duration in descending order (longest first)"""
        owner = Owner(name="Test", available_time=100)
        pet = Pet(name="Max", species="Dog")
        
        # Add tasks with different durations
        task_15 = Task(description="Groom", duration=15, frequency="daily", priority=3)
        task_25 = Task(description="Walk", duration=25, frequency="daily", priority=3)
        task_10 = Task(description="Feed", duration=10, frequency="daily", priority=3)
        
        pet.add_task(task_15)
        pet.add_task(task_25)
        pet.add_task(task_10)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        all_tasks = owner.get_all_incomplete_tasks()
        
        # Sort by time (descending)
        sorted_tasks = scheduler.sort_by_time(all_tasks, ascending=False)
        
        # Verify reverse chronological order (longest to shortest)
        assert len(sorted_tasks) == 3
        assert sorted_tasks[0][1].duration == 25  # Longest
        assert sorted_tasks[1][1].duration == 15
        assert sorted_tasks[2][1].duration == 10  # Shortest
    
    def test_recurrence_logic_daily_task(self):
        """Verify marking a daily task complete creates a new task for the next occurrence"""
        owner = Owner(name="Test", available_time=60)
        pet = Pet(name="Max", species="Dog")
        
        # Create a daily task
        daily_task = Task(
            description="Morning walk",
            duration=30,
            frequency="daily",
            priority=4
        )
        
        pet.add_task(daily_task)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        
        # Get initial task count
        initial_tasks = pet.get_all_tasks()
        initial_count = len(initial_tasks)
        assert initial_count == 1
        
        # Store original task ID
        original_id = daily_task.id
        
        # Mark task complete
        result = scheduler.mark_task_complete("Max", daily_task.id)
        assert result == True
        
        # Get tasks after marking complete
        after_tasks = pet.get_all_tasks()
        assert len(after_tasks) == 2  # Should have 2 tasks now (original + new)
        
        # Verify original task is marked complete
        original_task = pet.get_task(original_id)
        assert original_task.completed == True
        assert original_task.last_completed is not None
        
        # Find the new task (different ID, same description)
        new_tasks = [t for t in after_tasks if t.id != original_id]
        assert len(new_tasks) == 1
        
        new_task = new_tasks[0]
        assert new_task.description == "Morning walk"
        assert new_task.frequency == "daily"
        assert new_task.duration == 30
        assert new_task.priority == 4
        assert new_task.completed == False
        assert new_task.last_completed is None
        assert new_task.id != original_id  # Different ID
    
    def test_recurrence_logic_weekly_task(self):
        """Verify marking a weekly task complete creates a new task"""
        owner = Owner(name="Test", available_time=60)
        pet = Pet(name="Whiskers", species="Cat")
        
        # Create a weekly task
        weekly_task = Task(
            description="Grooming",
            duration=20,
            frequency="weekly",
            priority=3
        )
        
        pet.add_task(weekly_task)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        
        # Mark task complete
        original_id = weekly_task.id
        scheduler.mark_task_complete("Whiskers", weekly_task.id)
        
        # Verify new task was created
        all_tasks = pet.get_all_tasks()
        assert len(all_tasks) == 2
        
        # Find the new task
        new_task = [t for t in all_tasks if t.id != original_id][0]
        assert new_task.frequency == "weekly"
        assert new_task.completed == False
    
    def test_recurrence_logic_non_recurring_task(self):
        """Verify non-recurring tasks do NOT create new tasks when completed"""
        owner = Owner(name="Test", available_time=60)
        pet = Pet(name="Max", species="Dog")
        
        # Create a one-time task (non-standard frequency)
        onetime_task = Task(
            description="Vet appointment",
            duration=60,
            frequency="once",  # Not daily/weekly/monthly
            priority=5
        )
        
        pet.add_task(onetime_task)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        
        # Initial count
        assert len(pet.get_all_tasks()) == 1
        
        # Mark task complete
        scheduler.mark_task_complete("Max", onetime_task.id)
        
        # Should still only have 1 task (no new task created)
        assert len(pet.get_all_tasks()) == 1
        assert onetime_task.completed == True
    
    def test_conflict_detection_insufficient_time(self):
        """Verify scheduler detects when there's not enough time for all tasks"""
        owner = Owner(name="Test", available_time=30)  # Only 30 minutes
        pet = Pet(name="Max", species="Dog")
        
        # Add tasks that total more than available time
        task1 = Task(description="Walk", duration=25, frequency="daily", priority=3)
        task2 = Task(description="Play", duration=20, frequency="daily", priority=3)
        task3 = Task(description="Groom", duration=15, frequency="daily", priority=3)
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        plan = scheduler.generate_daily_plan()
        
        # Some tasks should be unscheduled due to time constraint
        assert len(plan['unscheduled']) > 0
        
        # Total scheduled time should not exceed available time
        assert plan['total_time_used'] <= 30
        assert plan['time_remaining'] >= 0
    
    def test_conflict_detection_zero_time_available(self):
        """Verify scheduler handles zero available time gracefully"""
        owner = Owner(name="Test", available_time=0)  # No time available
        pet = Pet(name="Max", species="Dog")
        
        # Add a task
        task = Task(description="Walk", duration=30, frequency="daily", priority=5)
        pet.add_task(task)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        plan = scheduler.generate_daily_plan()
        
        # Nothing should be scheduled
        assert len(plan['scheduled']) == 0
        assert len(plan['unscheduled']) == 1
        assert plan['total_time_used'] == 0
        assert plan['time_remaining'] == 0
    
    def test_conflict_detection_critical_task_competition(self):
        """Verify behavior when multiple critical tasks compete for limited time"""
        owner = Owner(name="Test", available_time=15)  # Limited time
        pet = Pet(name="Max", species="Dog")
        
        # Add multiple critical (priority 5) tasks
        med1 = Task(description="Morning medication", duration=5, frequency="daily", priority=5)
        med2 = Task(description="Evening medication", duration=5, frequency="daily", priority=5)
        feeding = Task(description="Feeding", duration=10, frequency="daily", priority=5)
        
        pet.add_task(med1)
        pet.add_task(med2)
        pet.add_task(feeding)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        plan = scheduler.generate_daily_plan()
        
        # Should schedule as many critical tasks as possible
        assert len(plan['scheduled']) >= 2  # At least 2 should fit (5+10 or 5+5)
        assert plan['total_time_used'] <= 15
        
        # All scheduled tasks in phase 1 should be priority 5
        for pet_obj, task in plan['scheduled']:
            assert task.priority == 5
