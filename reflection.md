# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

3 core actions a user should be able to perform:
    1. Enter and manage basic owner and pet details (name, preferences, time constraints)
    2. Add, edit, and configure pet care tasks like walks, feeding, meds, etc.
    3. generate and view a daily plan

Classes: 
    Task (Dataclass)
        Attributes:
        - description (str): what the task is
        - duration (int): minutes required
        - frequency (str): how often (daily, weekly, etc.)
        - priority (int): 1-5 scale (5 = critical)
        - completed (bool): completion status
        - id (str): auto-generated unique identifier
        Methods:
        - mark_complete(): mark task as done
        - mark_incomplete(): reset task status
        - to_dict(): convert to dictionary for display
        
    Pet
        Attributes:
        - name (str)
        - species (str)
        - age (Optional[int])
        - tasks (List[Task]): pet's task list
        Methods:
        - add_task(), remove_task(), get_task()
        - get_all_tasks(), get_incomplete_tasks()
        - get_info(): return pet summary
        
    Owner
        Attributes:
        - name (str)
        - available_time (int): total minutes per day
        - pets (List[Pet]): all pets under care
        Methods:
        - add_pet(), remove_pet(), get_pet()
        - get_all_tasks(): aggregate tasks across all pets
        - get_all_incomplete_tasks(): filter incomplete only
        - update_available_time()
        - get_info(): return owner summary
        
    Scheduler
        Attributes:
        - owner (Owner): reference to owner
        Methods:
        - generate_daily_plan(): main algorithm that schedules tasks
        - get_tasks_by_priority(), get_tasks_by_pet()
        - mark_task_complete()
        - get_summary(): overview of scheduling situation

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, the design evolved significantly during implementation:

1. Task ownership changed
2. Return types simplified
3. Added completion tracking
4. Validation added
5. Hierarchical structure

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
