"""
PawPal+ Backend Logic Layer
Contains all classes for pet care scheduling system
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class Owner:
    """Represents the pet owner and their constraints"""
    name: str
    available_time: int  # Total minutes available per day
    preferences: Dict[str, any] = field(default_factory=dict)
    
    def update_available_time(self, new_time: int) -> None:
        """Update the available time constraint"""
        pass
    
    def get_info(self) -> Dict:
        """Return summary of owner details"""
        pass


@dataclass
class Pet:
    """Represents the pet being cared for"""
    name: str
    species: str
    age: Optional[int] = None
    special_needs: List[str] = field(default_factory=list)
    
    def get_info(self) -> Dict:
        """Return summary of pet details"""
        pass


@dataclass
class Task:
    """Represents a single pet care activity"""
    id: str
    name: str
    task_type: str  # walk, feeding, medication, grooming, enrichment
    duration: int  # Minutes required
    priority: int  # 1-5 scale (5 = critical, 1 = optional)
    time_preference: Optional[str] = None  # morning, evening, anytime
    
    def update(self, **kwargs) -> None:
        """Modify task details"""
        pass
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage/display"""
        pass


class TaskManager:
    """Manages the collection of all tasks"""
    
    def __init__(self):
        self.tasks: List[Task] = []
    
    def add_task(self, task: Task) -> None:
        """Add a new task"""
        pass
    
    def remove_task(self, task_id: str) -> bool:
        """Delete a task by ID"""
        pass
    
    def edit_task(self, task_id: str, **kwargs) -> bool:
        """Modify existing task"""
        pass
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve specific task by ID"""
        pass
    
    def get_all_tasks(self) -> List[Task]:
        """Return all tasks"""
        pass
    
    def get_total_duration(self) -> int:
        """Calculate sum of all task durations"""
        pass


@dataclass
class ScheduledTask:
    """A task with timing and explanation"""
    task: Task
    time_slot: str  # e.g., "8:00 AM - 8:30 AM" or order number
    reason: str  # Why it was scheduled at this time/priority
    
    def to_dict(self) -> Dict:
        """Convert for display"""
        pass


class DailyPlan:
    """Represents the output schedule with reasoning"""
    
    def __init__(self, date: Optional[str] = None):
        self.scheduled_tasks: List[ScheduledTask] = []
        self.unscheduled_tasks: List[Task] = []
        self.total_time: int = 0
        self.date: str = date or datetime.now().strftime("%Y-%m-%d")
        self.reasoning: str = ""
    
    def add_scheduled_task(self, scheduled_task: ScheduledTask) -> None:
        """Add a task to the plan"""
        pass
    
    def add_unscheduled_task(self, task: Task) -> None:
        """Add a task that couldn't be scheduled"""
        pass
    
    def get_summary(self) -> str:
        """Return human-readable summary"""
        pass
    
    def to_dict(self) -> Dict:
        """Convert for display"""
        pass


class Scheduler:
    """Core logic that generates the daily plan"""
    
    def __init__(self, owner: Owner, tasks: List[Task]):
        self.owner = owner
        self.tasks = tasks
    
    def generate_plan(self) -> DailyPlan:
        """Main algorithm: generates and returns DailyPlan"""
        pass
    
    def _sort_by_priority(self) -> List[Task]:
        """Helper: sort tasks by priority (highest first)"""
        pass
    
    def _fits_in_time(self, task: Task, remaining_time: int) -> bool:
        """Check if task fits within remaining time"""
        pass
    
    def _explain_decision(self, task: Task, scheduled: bool) -> str:
        """Generate reasoning for including/excluding task"""
        pass
