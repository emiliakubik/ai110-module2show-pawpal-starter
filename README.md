# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

This implementation includes several intelligent scheduling improvements:

### Core Scheduling Algorithm
- **Critical Task Guarantees** - Priority 5 tasks are always scheduled first, ensuring critical care (medications, feeding) never gets skipped
- **Frequency-Aware Filtering** - Only schedules tasks due today based on their frequency (daily/weekly/monthly) and last completion timestamp
- **Pet Batching** - Groups tasks by pet to minimize context switching and improve workflow efficiency

### Utility Methods
- **Sort by Time** - `sort_by_time()` method sorts tasks by duration (shortest-first or longest-first strategies)
- **Filter by Pet/Status** - Built-in methods to filter tasks by pet name, completion status, or priority level

### Automation
- **Auto-Recurring Tasks** - When a recurring task (daily/weekly/monthly) is marked complete, a fresh instance is automatically created for the next occurrence, maintaining task continuity

All features are fully tested with pytest and demonstrated in `main.py`.

## Testing PawPal+

The test suite (`tests/test_pawpal.py`) includes **15 tests** covering:

### Task Behaviors (4 tests)
- Task completion status tracking
- Frequency-based due date logic (daily/weekly tasks)
- Never-completed tasks marked as due

### Pet Management (1 test)
- Adding tasks to pets and maintaining task lists

### Scheduler Intelligence (10 tests)
- **Priority scheduling**: Critical (Priority 5) tasks scheduled first
- **Pet batching**: Tasks grouped by pet to reduce context switching
- **Sorting correctness**: Tasks sorted by duration (ascending/descending)
- **Recurrence logic**: Auto-creation of new tasks when recurring tasks are completed
- **Conflict detection**: Handles insufficient time, zero time, and critical task competition

### Run Tests
```bash
python3 -m pytest tests/test_pawpal.py -v

### Confidence Level
4 out of 5 stars


## Final Reflectiion

The core concept students need to understand is designing a constraint-based scheduling system that balances multiple competing priorities (time, task urgency, efficiency) while making intentional tradeoffs—not just implementing a simple greedy algorithm. Students are most likely to struggle with over-engineering their initial design (too many classes, too much abstraction) and with testing their scheduling logic thoroughly enough to catch edge cases like zero available time or multiple critical tasks competing for limited slots.

AI is most helpful for brainstorming edge cases, generating test scenarios, and exploring tradeoffs (e.g., "What happens if two tasks have the same priority?"), but it can be misleading when it suggests overly complex architectures that look professional but don't match the actual problem scope—students must learn to simplify AI suggestions to fit their use case. To guide a student without giving the answer, I would ask: "Walk me through what happens in your scheduler when you have 30 minutes available and three Priority 5 tasks that each take 15 minutes—which ones get scheduled and why? How would you verify this behavior with a test?" This forces them to reason through their algorithm's logic, identify the gap (insufficient time for critical tasks), and think about how to validate their solution.