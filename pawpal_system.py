"""
PawPal+ Backend Logic Layer
Contains all classes for pet care scheduling system
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import uuid


def generate_task_id() -> str:
    """Generate a unique task ID"""
    return str(uuid.uuid4())[:8]


@dataclass
class Task:
    """Represents a single activity with description, time, frequency, and completion status"""
    description: str
    duration: int  # Minutes required
    frequency: str  # daily, weekly, etc.
    priority: int  # 1-5 scale (5 = critical, 1 = optional)
    completed: bool = False
    id: str = field(default_factory=generate_task_id)
    last_completed: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate task data"""
        if self.priority < 1 or self.priority > 5:
            raise ValueError("Priority must be between 1 and 5")
        if self.duration <= 0:
            raise ValueError("Duration must be positive")
    
    def mark_complete(self) -> None:
        """Mark task as completed"""
        self.completed = True
        self.last_completed = datetime.now()
    
    def mark_incomplete(self) -> None:
        """Mark task as incomplete"""
        self.completed = False
        self.last_completed = None
    
    def is_due_today(self) -> bool:
        """Check if task is due today based on frequency and last completion"""
        if not self.last_completed:
            return True  # Never completed, so it's due
        
        days_since_completion = (datetime.now() - self.last_completed).days
        
        if self.frequency == "daily":
            return days_since_completion >= 1
        elif self.frequency == "weekly":
            return days_since_completion >= 7
        elif self.frequency == "monthly":
            return days_since_completion >= 30
        else:
            return True  # Unknown frequency, assume due
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage/display"""
        return {
            'id': self.id,
            'description': self.description,
            'duration': self.duration,
            'frequency': self.frequency,
            'priority': self.priority,
            'completed': self.completed,
            'last_completed': self.last_completed.isoformat() if self.last_completed else None
        }


class Pet:
    """Stores pet details and a list of tasks"""
    
    def __init__(self, name: str, species: str, age: Optional[int] = None):
        self.name = name
        self.species = species
        self.age = age
        self.tasks: List[Task] = []
    
    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list"""
        self.tasks.append(task)
    
    def remove_task(self, task_id: str) -> bool:
        """Remove a task by ID"""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks.pop(i)
                return True
        return False
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a specific task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_all_tasks(self) -> List[Task]:
        """Return all tasks for this pet"""
        return self.tasks
    
    def get_incomplete_tasks(self) -> List[Task]:
        """Return only incomplete tasks"""
        return [task for task in self.tasks if not task.completed]
    
    def get_info(self) -> Dict:
        """Return summary of pet details"""
        return {
            'name': self.name,
            'species': self.species,
            'age': self.age,
            'total_tasks': len(self.tasks),
            'incomplete_tasks': len(self.get_incomplete_tasks())
        }


class Owner:
    """Manages multiple pets and provides access to all their tasks"""
    
    def __init__(self, name: str, available_time: int):
        self.name = name
        self.available_time = available_time  # Total minutes available per day
        self.pets: List[Pet] = []
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's care"""
        self.pets.append(pet)
    
    def remove_pet(self, pet_name: str) -> bool:
        """Remove a pet by name"""
        for i, pet in enumerate(self.pets):
            if pet.name == pet_name:
                self.pets.pop(i)
                return True
        return False
    
    def get_pet(self, pet_name: str) -> Optional[Pet]:
        """Retrieve a specific pet by name"""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None
    
    def get_all_pets(self) -> List[Pet]:
        """Return all pets"""
        return self.pets
    
    def get_all_tasks(self) -> List[tuple[Pet, Task]]:
        """Get all tasks across all pets with pet association"""
        all_tasks = []
        for pet in self.pets:
            for task in pet.get_all_tasks():
                all_tasks.append((pet, task))
        return all_tasks
    
    def get_all_incomplete_tasks(self) -> List[tuple[Pet, Task]]:
        """Get all incomplete tasks across all pets"""
        incomplete_tasks = []
        for pet in self.pets:
            for task in pet.get_incomplete_tasks():
                incomplete_tasks.append((pet, task))
        return incomplete_tasks
    
    def update_available_time(self, new_time: int) -> None:
        """Update the available time constraint"""
        if new_time < 0:
            raise ValueError("Available time cannot be negative")
        self.available_time = new_time
    
    def get_info(self) -> Dict:
        """Return summary of owner details"""
        return {
            'name': self.name,
            'available_time': self.available_time,
            'total_pets': len(self.pets),
            'total_tasks': sum(len(pet.tasks) for pet in self.pets)
        }


class Scheduler:
    """The 'Brain' that retrieves, organizes, and manages tasks across pets"""
    
    def __init__(self, owner: Owner):
        self.owner = owner
    
    def generate_daily_plan(self) -> Dict:
        """
        Generate a daily plan based on available time and task priorities
        Improvements:
        - Only schedules tasks due today (frequency-aware)
        - Guarantees critical tasks (priority 5) are scheduled first
        - Batches tasks by pet to reduce context switching
        Returns a dict with scheduled tasks, unscheduled tasks, and reasoning
        """
        # Get all incomplete tasks
        incomplete_tasks = self.owner.get_all_incomplete_tasks()
        
        # IMPROVEMENT 1: Filter to only tasks due today
        due_tasks = [(pet, task) for pet, task in incomplete_tasks if task.is_due_today()]
        
        if not due_tasks:
            return {
                'scheduled': [],
                'unscheduled': [],
                'total_time_used': 0,
                'time_remaining': self.owner.available_time,
                'reasoning': 'No tasks due today!'
            }
        
        scheduled = []
        unscheduled = []
        remaining_time = self.owner.available_time
        reasoning = []
        
        # IMPROVEMENT 2: Critical Task Guarantees - Schedule priority 5 tasks first
        critical_tasks = [t for t in due_tasks if t[1].priority == 5]
        non_critical_tasks = [t for t in due_tasks if t[1].priority < 5]
        
        reasoning.append("=== Phase 1: Critical Tasks (Priority 5) ===")
        for pet, task in sorted(critical_tasks, key=lambda x: x[1].duration):
            if self._fits_in_time(task, remaining_time):
                scheduled.append((pet, task))
                remaining_time -= task.duration
                reasoning.append(
                    f"✓ {pet.name}: {task.description} (CRITICAL, {task.duration} min)"
                )
            else:
                unscheduled.append((pet, task))
                reasoning.append(
                    f"✗ {pet.name}: {task.description} - Not enough time (needs {task.duration} min, only {remaining_time} min left)"
                )
        
        # IMPROVEMENT 3: Pet Batching - Group tasks by pet, then sort by priority
        reasoning.append("\n=== Phase 2: Other Tasks (Batched by Pet) ===")
        
        # Group non-critical tasks by pet
        pet_task_groups = {}
        for pet, task in non_critical_tasks:
            if pet.name not in pet_task_groups:
                pet_task_groups[pet.name] = []
            pet_task_groups[pet.name].append((pet, task))
        
        # Sort each pet's tasks by priority, then duration
        for pet_name in pet_task_groups:
            pet_task_groups[pet_name].sort(
                key=lambda x: (-x[1].priority, x[1].duration)
            )
        
        # Schedule tasks pet by pet
        while pet_task_groups and remaining_time > 0:
            # Find pet with highest priority task remaining
            best_pet = max(
                pet_task_groups.keys(),
                key=lambda p: pet_task_groups[p][0][1].priority if pet_task_groups[p] else 0
            )
            
            if not pet_task_groups[best_pet]:
                del pet_task_groups[best_pet]
                continue
            
            pet, task = pet_task_groups[best_pet].pop(0)
            
            if self._fits_in_time(task, remaining_time):
                scheduled.append((pet, task))
                remaining_time -= task.duration
                reasoning.append(
                    f"✓ {pet.name}: {task.description} (Priority {task.priority}, {task.duration} min)"
                )
            else:
                unscheduled.append((pet, task))
                reasoning.append(
                    f"✗ {pet.name}: {task.description} - Not enough time (needs {task.duration} min, only {remaining_time} min left)"
                )
            
            # Remove pet from groups if no more tasks
            if not pet_task_groups[best_pet]:
                del pet_task_groups[best_pet]
        
        # Add any remaining unscheduled tasks
        for pet_tasks in pet_task_groups.values():
            for pet, task in pet_tasks:
                unscheduled.append((pet, task))
                reasoning.append(
                    f"✗ {pet.name}: {task.description} - Not enough time"
                )
        
        return {
            'scheduled': scheduled,
            'unscheduled': unscheduled,
            'total_time_used': self.owner.available_time - remaining_time,
            'time_remaining': remaining_time,
            'reasoning': '\n'.join(reasoning)
        }
    
    def get_tasks_by_priority(self, priority: int) -> List[tuple[Pet, Task]]:
        """Get all incomplete tasks of a specific priority level"""
        all_tasks = self.owner.get_all_incomplete_tasks()
        return [(pet, task) for pet, task in all_tasks if task.priority == priority]
    
    def get_tasks_by_pet(self, pet_name: str) -> List[Task]:
        """Get all tasks for a specific pet"""
        pet = self.owner.get_pet(pet_name)
        if pet:
            return pet.get_all_tasks()
        return []
    
    def mark_task_complete(self, pet_name: str, task_id: str) -> bool:
        """Mark a specific task as complete
        
        For recurring tasks (daily, weekly, monthly), automatically creates
        a new task instance for the next occurrence.
        
        Returns:
            True if task was found and marked complete, False otherwise
        """
        pet = self.owner.get_pet(pet_name)
        if pet:
            task = pet.get_task(task_id)
            if task:
                task.mark_complete()
                
                # Auto-create recurring task for next occurrence
                if task.frequency in ["daily", "weekly", "monthly"]:
                    new_task = Task(
                        description=task.description,
                        duration=task.duration,
                        frequency=task.frequency,
                        priority=task.priority,
                        completed=False
                    )
                    # Note: new_task gets a fresh ID and last_completed=None automatically
                    pet.add_task(new_task)
                
                return True
        return False
    
    def _fits_in_time(self, task: Task, remaining_time: int) -> bool:
        """Check if task fits within remaining time"""
        return task.duration <= remaining_time
    
    def _sort_by_priority(self, tasks: List[tuple[Pet, Task]]) -> List[tuple[Pet, Task]]:
        """Helper: sort tasks by priority (highest first)"""
        return sorted(tasks, key=lambda x: -x[1].priority)
    
    def sort_by_time(self, tasks: List[tuple[Pet, Task]], ascending: bool = True) -> List[tuple[Pet, Task]]:
        """Sort tasks by duration (time required)
        
        Args:
            tasks: List of (Pet, Task) tuples to sort
            ascending: If True, shortest tasks first. If False, longest tasks first
        
        Returns:
            Sorted list of (Pet, Task) tuples
        """
        return sorted(tasks, key=lambda x: x[1].duration, reverse=not ascending)
    
    def get_summary(self) -> str:
        """Get a text summary of the owner's situation"""
        info = self.owner.get_info()
        all_tasks = self.owner.get_all_incomplete_tasks()
        total_duration = sum(task.duration for _, task in all_tasks)
        
        summary = f"Owner: {info['name']}\n"
        summary += f"Available time: {info['available_time']} minutes\n"
        summary += f"Pets: {info['total_pets']}\n"
        summary += f"Incomplete tasks: {len(all_tasks)}\n"
        summary += f"Total time needed: {total_duration} minutes\n"
        
        if total_duration > info['available_time']:
            summary += f"\n⚠️ Warning: Not enough time for all tasks (short by {total_duration - info['available_time']} minutes)"
        else:
            summary += f"\n✓ All tasks can be completed with {info['available_time'] - total_duration} minutes to spare"
        
        return summary
