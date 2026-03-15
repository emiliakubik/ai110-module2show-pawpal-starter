"""
Main script to test PawPal+ system
Temporary testing ground to verify logic works in terminal
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # Create an owner
    print("🐾 Welcome to PawPal+ 🐾\n")
    
    owner = Owner(name="Sarah", available_time=120)  # 120 minutes available
    print(f"Owner: {owner.name}")
    print(f"Available time today: {owner.available_time} minutes\n")
    
    # Create pets
    dog = Pet(name="Max", species="Dog", age=3)
    cat = Pet(name="Whiskers", species="Cat", age=5)
    
    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)
    print(f"Pets: {dog.name} (Dog) and {cat.name} (Cat)\n")
    
    # Create tasks for dog
    walk_task = Task(
        description="Morning walk in the park",
        duration=30,
        frequency="daily",
        priority=5
    )
    
    dog_feeding = Task(
        description="Breakfast feeding",
        duration=10,
        frequency="daily",
        priority=5
    )
    
    dog_play = Task(
        description="Play fetch outside",
        duration=25,
        frequency="daily",
        priority=3
    )
    
    # Add tasks to dog
    dog.add_task(walk_task)
    dog.add_task(dog_feeding)
    dog.add_task(dog_play)
    
    # Create tasks for cat
    cat_feeding = Task(
        description="Breakfast feeding",
        duration=5,
        frequency="daily",
        priority=5
    )
    
    cat_grooming = Task(
        description="Brush fur",
        duration=15,
        frequency="weekly",
        priority=2
    )
    
    litter_box = Task(
        description="Clean litter box",
        duration=10,
        frequency="daily",
        priority=4
    )
    
    cat_enrichment = Task(
        description="Interactive play with laser pointer",
        duration=20,
        frequency="daily",
        priority=3
    )
    
    # Add tasks to cat
    cat.add_task(cat_feeding)
    cat.add_task(cat_grooming)
    cat.add_task(litter_box)
    cat.add_task(cat_enrichment)
    
    print("=" * 60)
    print("📋 ALL TASKS")
    print("=" * 60)
    
    for pet in owner.get_all_pets():
        print(f"\n{pet.name} ({pet.species}):")
        for task in pet.get_all_tasks():
            print(f"  • {task.description}")
            print(f"    Duration: {task.duration} min | Priority: {task.priority} | Frequency: {task.frequency}")
    
    print("\n" + "=" * 60)
    print("🗓️  TODAY'S SCHEDULE")
    print("=" * 60)
    
    # Create scheduler and generate plan
    scheduler = Scheduler(owner)
    plan = scheduler.generate_daily_plan()
    
    print(f"\n⏰ Time available: {owner.available_time} minutes")
    print(f"⏱️  Time used: {plan['total_time_used']} minutes")
    print(f"⏳ Time remaining: {plan['time_remaining']} minutes\n")
    
    print("✅ SCHEDULED TASKS:")
    if plan['scheduled']:
        for pet, task in plan['scheduled']:
            print(f"  {pet.name}: {task.description} ({task.duration} min) [Priority {task.priority}]")
    else:
        print("  No tasks scheduled")
    
    if plan['unscheduled']:
        print("\n❌ UNSCHEDULED TASKS (not enough time):")
        for pet, task in plan['unscheduled']:
            print(f"  {pet.name}: {task.description} ({task.duration} min) [Priority {task.priority}]")
    
    print("\n" + "=" * 60)
    print("📊 SCHEDULER REASONING")
    print("=" * 60)
    print(plan['reasoning'])
    
    print("\n" + "=" * 60)
    print("📈 SUMMARY")
    print("=" * 60)
    print(scheduler.get_summary())


if __name__ == "__main__":
    main()
