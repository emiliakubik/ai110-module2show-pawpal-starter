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

My scheduler considers multiple constraints in a hierarchical order:
1. Priority (1-5 scale)
2. Time availability
3. Frequency and due dates
4. Task duration
5. Pet grouping

How I decided priority:
- Priority came first because missing medication or feeding can harm a pet's health
- Time is non-negotiable because owners have real constraints
- Frequency filtering prevents redundant work (no need to groom twice in a week)
- Pet batching improves workflow efficiency without compromising critical care

**b. Tradeoffs** Pet batching vs strict priority order

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

After scheduling all Priority 5 tasks, the scheduler groups remaining tasks by pet rather than strictly following priority order (4→3→2→1). For example, it might schedule Max's Priority 3 task before Whiskers' Priority 4 task if it's already working on Max's tasks.

Why this is reasonable:
- Context switching is expensive in pet care. If you're already walking Max outside, it makes sense to play fetch with him while you're there, rather than going inside to clean Whiskers' litter box and then going back outside.
- Critical tasks are protected. This tradeoff only applies to non-critical tasks (Priority 4 and below), so essential care is never compromised.
- Real-world workflow. Pet owners naturally batch tasks by pet, location, or activity type. The scheduler mirrors realistic human behavior.
- Minimal priority impact. The priority difference within Phase 2 (Priority 4 vs 3) is less significant than the Phase 1 vs Phase 2 divide (Priority 5 vs everything else).

This tradeoff optimizes for practical efficiency over theoretical perfect priority ordering, which better matches how busy pet owners actually work.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used ai to help me implement efficient code as well as helping me get started on brainstorming when I wasn't sure how exactly to get started.

The most helpful prompts for me are the ones where I specify that I do not want to be given the answer, rather I just want help on getting my brain flowing with ideas.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

at first I asked it what classes it suggested I used and it gave me way too complex ideas and not at all what I was going for. It really helped me hone in on what was needed and got me started but what it actually gave me was not that useful for what this project really needed.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    Task behaviors, pet management, and scheduler intelligence

- Why were these tests important?
    1. Critical task guarantee
    2. Frequency logic
    3. Recurrence automation
    4. Edge case protextion
    5. Sorting verification
    6. Pet batching validation

**b. Confidence**

- How confident are you that your scheduler works correctly?
    Confidence: 4/5
- What edge cases would you test next if you had more time?
    1. Boundary conditions for frequency logic
    2. Multiple pets with identical priorities
    3. Extreme scale scenarios
    4. Invalid input handling
    5. Rapid state changes

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I really enjoyed using copilot as a partner but learning the difference between using it as a tool and fully relying on it

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    1. Add task location/category attributes
    2. Implement data persistence
    3. Enhance frequency handling
    4. Multi-day planning
    5. Task dependency system

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Start simple and then iterate based on real needs-not theoreitcal complexity.