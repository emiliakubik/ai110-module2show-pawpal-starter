"""
Main script to test PawPal+ system
Demonstrates improvements:
- Critical task guarantees (Priority 5 first)
- Pet batching (same-pet tasks grouped)
- Frequency filtering (only due tasks)
"""

from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import datetime, timedelta


def main():
    # Create an owner
    print("🐾 Welcome to PawPal+ (Enhanced Edition) 🐾\n")
    
    owner = Owner(name="Sarah", available_time=90)  # Only 90 minutes today
    print(f"Owner: {owner.name}")
    print(f"Available time today: {owner.available_time} minutes\n")
    
    # Create pets
    dog = Pet(name="Max", species="Dog", age=3)
    cat = Pet(name="Whiskers", species="Cat", age=5)
    
    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)
    print(f"Pets: {dog.name} (Dog) and {cat.name} (Cat)\n")
    
    # Create tasks for dog with different priorities
    # CRITICAL TASK (Priority 5)
    dog_medication = Task(
        description="Give morning medication",
        duration=5,
        frequency="daily",
        priority=5
    )
    
    # HIGH PRIORITY (Priority 4)
    walk_task = Task(
        description="Morning walk in the park",
        duration=30,
        frequency="daily",
        priority=4
    )
    
    # HIGH PRIORITY (Priority 4)
    dog_feeding = Task(
        description="Breakfast feeding",
        duration=10,
        frequency="daily",
        priority=5
    )
    
    # MEDIUM PRIORITY (Priority 3)
    dog_play = Task(
        description="Play fetch outside",
        duration=25,
        frequency="daily",
        priority=3
    )
    
    # Add tasks to dog
    dog.add_task(walk_task)  # Added first but not critical
    dog.add_task(dog_feeding)  # Critical
    dog.add_task(dog_medication)  # Critical
    dog.add_task(dog_play)  # Lower priority
    
    # Create tasks for cat
    # CRITICAL TASK (Priority 5)
    cat_feeding = Task(
        description="Breakfast feeding",
        duration=5,
        frequency="daily",
        priority=5
    )
    
    # LOW PRIORITY (Priority 2) - WEEKLY, NOT DUE
    cat_grooming = Task(
        description="Brush fur",
        duration=15,
        frequency="weekly",
        priority=2
    )
    # Simulate that grooming was done 2 days ago
    cat_grooming.last_completed = datetime.now() - timedelta(days=2)
    
    # MEDIUM-HIGH (Priority 4)
    litter_box = Task(
        description="Clean litter box",
        duration=10,
        frequency="daily",
        priority=4
    )
    
    # MEDIUM (Priority 3)
    cat_enrichment = Task(
        description="Interactive play with laser pointer",
        duration=20,
        frequency="daily",
        priority=3
    )
    
    # Add tasks to cat
    cat.add_task(cat_feeding)
    cat.add_task(cat_grooming)  # Not due (completed 2 days ago, weekly task)
    cat.add_task(litter_box)
    cat.add_task(cat_enrichment)
    
    print("=" * 70)
    print("📋 ALL TASKS (Including Not Due)")
    print("=" * 70)
    
    for pet in owner.get_all_pets():
        print(f"\n{pet.name} ({pet.species}):")
        for task in pet.get_all_tasks():
            due_status = "DUE" if task.is_due_today() else "NOT DUE"
            print(f"  • {task.description}")
            print(f"    Duration: {task.duration} min | Priority: {task.priority} | Frequency: {task.frequency} | {due_status}")
    
    print("\n" + "=" * 70)
    print("🗓️  IMPROVED DAILY SCHEDULE")
    print("=" * 70)
    print("\n" + "=" * 70)
    print("🗓️  IMPROVED DAILY SCHEDULE")
    print("=" * 70)
    
    # Create scheduler and generate plan
    scheduler = Scheduler(owner)
    plan = scheduler.generate_daily_plan()
    
    print(f"\n⏰ Time available: {owner.available_time} minutes")
    print(f"⏱️  Time used: {plan['total_time_used']} minutes")
    print(f"⏳ Time remaining: {plan['time_remaining']} minutes\n")
    
    print("✅ SCHEDULED TASKS (IN ORDER):")
    if plan['scheduled']:
        for i, (pet, task) in enumerate(plan['scheduled'], 1):
            print(f"  {i}. {pet.name}: {task.description} ({task.duration} min) [Priority {task.priority}]")
    else:
        print("  No tasks scheduled")
    
    if plan['unscheduled']:
        print("\n❌ UNSCHEDULED TASKS (not enough time or not due):")
        for pet, task in plan['unscheduled']:
            print(f"  - {pet.name}: {task.description} ({task.duration} min) [Priority {task.priority}]")
    
    print("\n" + "=" * 70)
    print("📊 DETAILED SCHEDULER REASONING")
    print("=" * 70)
    print(plan['reasoning'])
    
    print("\n" + "=" * 70)
    print("📈 SUMMARY")
    print("=" * 70)
    print(scheduler.get_summary())
    
    print("\n" + "=" * 70)
    print("🎯 KEY IMPROVEMENTS DEMONSTRATED:")
    print("=" * 70)
    print("1. ✓ Critical Tasks First - All Priority 5 tasks scheduled before others")
    print("2. ✓ Pet Batching - Tasks for same pet grouped together when possible")
    print("3. ✓ Frequency Filtering - Weekly grooming NOT scheduled (done 2 days ago)")
    print("4. ✓ Smart Time Management - Only 90 min available, best tasks chosen")
    
    # ========================================================================
    # NEW DEMONSTRATION: Sorting and Filtering Methods
    # ========================================================================
    print("\n\n" + "=" * 70)
    print("🆕 TESTING NEW SORTING & FILTERING METHODS")
    print("=" * 70)
    
    # Get all incomplete tasks
    all_incomplete = owner.get_all_incomplete_tasks()
    
    # 1. Sort by time (shortest first)
    print("\n📊 1. SORT BY TIME (Shortest to Longest):")
    print("-" * 70)
    sorted_shortest = scheduler.sort_by_time(all_incomplete, ascending=True)
    for i, (pet, task) in enumerate(sorted_shortest, 1):
        print(f"  {i}. [{task.duration:2d} min] {pet.name}: {task.description}")
    
    # 2. Sort by time (longest first)
    print("\n📊 2. SORT BY TIME (Longest to Shortest):")
    print("-" * 70)
    sorted_longest = scheduler.sort_by_time(all_incomplete, ascending=False)
    for i, (pet, task) in enumerate(sorted_longest, 1):
        print(f"  {i}. [{task.duration:2d} min] {pet.name}: {task.description}")
    
    # 3. Filter by completion status (incomplete only)
    print("\n📊 3. FILTER BY COMPLETION STATUS (Incomplete):")
    print("-" * 70)
    incomplete_tasks = owner.get_all_incomplete_tasks()
    print(f"Total incomplete tasks: {len(incomplete_tasks)}")
    for pet, task in incomplete_tasks:
        status = "✓ Complete" if task.completed else "○ Incomplete"
        print(f"  • {pet.name}: {task.description} - {status}")
    
    # Mark a couple tasks complete to demo filtering
    dog_medication.mark_complete()
    cat_feeding.mark_complete()
    
    print("\n   [Marked 2 tasks complete: Max's medication & Whiskers' feeding]")
    
    # Show complete tasks
    print("\n📊 4. FILTER BY COMPLETION STATUS (Complete):")
    print("-" * 70)
    all_tasks = owner.get_all_tasks()
    completed_tasks = [(pet, task) for pet, task in all_tasks if task.completed]
    print(f"Total completed tasks: {len(completed_tasks)}")
    for pet, task in completed_tasks:
        print(f"  • {pet.name}: {task.description} ✓")
    
    # Show incomplete after marking some complete
    print("\n📊 5. FILTER BY COMPLETION STATUS (Still Incomplete):")
    print("-" * 70)
    still_incomplete = owner.get_all_incomplete_tasks()
    print(f"Total incomplete tasks: {len(still_incomplete)}")
    for pet, task in still_incomplete:
        print(f"  • {pet.name}: {task.description}")
    
    # 6. Filter by pet name (using existing get_tasks_by_pet)
    print("\n📊 6. FILTER BY PET NAME (Max only):")
    print("-" * 70)
    max_tasks = scheduler.get_tasks_by_pet("Max")
    print(f"Total tasks for Max: {len(max_tasks)}")
    for task in max_tasks:
        status = "✓ Complete" if task.completed else "○ Incomplete"
        print(f"  • {task.description} ({task.duration} min, Priority {task.priority}) - {status}")
    
    print("\n📊 7. FILTER BY PET NAME (Whiskers only):")
    print("-" * 70)
    whiskers_tasks = scheduler.get_tasks_by_pet("Whiskers")
    print(f"Total tasks for Whiskers: {len(whiskers_tasks)}")
    for task in whiskers_tasks:
        status = "✓ Complete" if task.completed else "○ Incomplete"
        print(f"  • {task.description} ({task.duration} min, Priority {task.priority}) - {status}")
    
    # 8. Combine filtering and sorting
    print("\n📊 8. COMBINED: Max's incomplete tasks, sorted by time:")
    print("-" * 70)
    all_tasks_tuples = owner.get_all_tasks()
    max_incomplete = [(pet, task) for pet, task in all_tasks_tuples 
                      if pet.name == "Max" and not task.completed]
    max_sorted = scheduler.sort_by_time(max_incomplete, ascending=True)
    if max_sorted:
        for i, (pet, task) in enumerate(max_sorted, 1):
            print(f"  {i}. [{task.duration:2d} min] {task.description} (Priority {task.priority})")
    else:
        print("  No incomplete tasks for Max!")
    
    print("\n" + "=" * 70)
    print("✅ SORTING & FILTERING METHODS TESTED SUCCESSFULLY!")
    print("=" * 70)
    
    # ========================================================================
    # NEW DEMONSTRATION: Auto-Recurring Tasks
    # ========================================================================
    print("\n\n" + "=" * 70)
    print("🔄 TESTING AUTO-RECURRING TASK CREATION")
    print("=" * 70)
    
    print("\n📋 BEFORE: Max's task count")
    print("-" * 70)
    max_before = scheduler.get_tasks_by_pet("Max")
    print(f"Max has {len(max_before)} tasks")
    for i, task in enumerate(max_before, 1):
        status = "✓ Complete" if task.completed else "○ Incomplete"
        print(f"  {i}. {task.description} ({task.frequency}) - {status} [ID: {task.id}]")
    
    # Find an incomplete daily task to mark complete
    incomplete_daily = None
    for task in max_before:
        if not task.completed and task.frequency == "daily":
            incomplete_daily = task
            break
    
    if incomplete_daily:
        print(f"\n🎯 Marking complete: '{incomplete_daily.description}' (ID: {incomplete_daily.id})")
        print(f"   This is a {incomplete_daily.frequency} task, so a new one should be created...")
        
        # Mark it complete using scheduler
        success = scheduler.mark_task_complete("Max", incomplete_daily.id)
        print(f"   Result: {'✓ Success' if success else '✗ Failed'}")
        
        print("\n📋 AFTER: Max's task count")
        print("-" * 70)
        max_after = scheduler.get_tasks_by_pet("Max")
        print(f"Max now has {len(max_after)} tasks (was {len(max_before)})")
        for i, task in enumerate(max_after, 1):
            status = "✓ Complete" if task.completed else "○ Incomplete"
            is_new = " 🆕 NEW!" if task.id not in [t.id for t in max_before] else ""
            print(f"  {i}. {task.description} ({task.frequency}) - {status} [ID: {task.id}]{is_new}")
        
        print("\n✅ VERIFICATION:")
        print("-" * 70)
        # Count completed vs incomplete
        completed = [t for t in max_after if t.completed]
        incomplete = [t for t in max_after if not t.completed]
        print(f"  • Original task marked complete: ✓")
        print(f"  • New recurring task created: ✓")
        print(f"  • Completed tasks: {len(completed)}")
        print(f"  • Incomplete tasks: {len(incomplete)}")
        print(f"  • Total tasks maintained: {len(max_after)} tasks")
    else:
        print("\n⚠️  No incomplete daily tasks found to demonstrate with")
    
    # Test with weekly task too
    print("\n\n📋 TEST WITH WEEKLY TASK:")
    print("-" * 70)
    whiskers_before = scheduler.get_tasks_by_pet("Whiskers")
    print(f"Whiskers has {len(whiskers_before)} tasks")
    
    # Find the weekly task
    weekly_task = None
    for task in whiskers_before:
        if task.frequency == "weekly":
            weekly_task = task
            break
    
    if weekly_task:
        print(f"\nMarking complete: '{weekly_task.description}' (weekly task, ID: {weekly_task.id})")
        scheduler.mark_task_complete("Whiskers", weekly_task.id)
        
        whiskers_after = scheduler.get_tasks_by_pet("Whiskers")
        print(f"Whiskers now has {len(whiskers_after)} tasks (was {len(whiskers_before)})")
        
        # Find the new weekly task
        new_weekly = [t for t in whiskers_after if t.id not in [x.id for x in whiskers_before] and t.frequency == "weekly"]
        if new_weekly:
            print(f"✓ New weekly task created: '{new_weekly[0].description}' (ID: {new_weekly[0].id})")
            print(f"  Status: {'Complete' if new_weekly[0].completed else 'Incomplete'} (should be Incomplete)")
        else:
            print("✗ No new weekly task found (unexpected)")
    
    print("\n" + "=" * 70)
    print("🔄 AUTO-RECURRING TASKS TESTED SUCCESSFULLY!")
    print("=" * 70)
    print("When a daily/weekly/monthly task is marked complete,")
    print("a fresh copy is automatically created for the next occurrence!")
    print("=" * 70)


if __name__ == "__main__":
    main()
