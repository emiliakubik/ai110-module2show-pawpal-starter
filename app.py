import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Initialize session state objects (persist across reruns)
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_time=120)

if "current_pet" not in st.session_state:
    st.session_state.current_pet = None

st.title("🐾 PawPal+")

st.markdown("Pet care planning assistant - manage your pets and schedule daily tasks!")

st.divider()

# Owner Configuration Section
st.subheader("👤 Owner Settings")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
with col2:
    available_time = st.number_input(
        "Available time (minutes/day)", 
        min_value=0, 
        max_value=1440, 
        value=st.session_state.owner.available_time
    )

# Update owner details if changed
if owner_name != st.session_state.owner.name:
    st.session_state.owner.name = owner_name
if available_time != st.session_state.owner.available_time:
    st.session_state.owner.update_available_time(available_time)

st.divider()

# Pet Management Section
st.subheader("🐕 Manage Pets")

# Add new pet
with st.expander("➕ Add New Pet", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        new_pet_name = st.text_input("Pet name", key="new_pet_name")
    with col2:
        new_pet_species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Other"], key="new_pet_species")
    with col3:
        new_pet_age = st.number_input("Age (optional)", min_value=0, max_value=50, value=0, key="new_pet_age")
    
    if st.button("Add Pet"):
        if new_pet_name:
            age = new_pet_age if new_pet_age > 0 else None
            new_pet = Pet(name=new_pet_name, species=new_pet_species, age=age)
            st.session_state.owner.add_pet(new_pet)
            st.success(f"✅ Added {new_pet_name} ({new_pet_species})!")
            st.rerun()
        else:
            st.error("Please enter a pet name")

# Display existing pets
pets = st.session_state.owner.get_all_pets()
if pets:
    st.write(f"**Your Pets ({len(pets)}):**")
    for pet in pets:
        info = pet.get_info()
        st.write(f"- **{info['name']}** ({info['species']}, Age: {info['age'] or 'Unknown'}) - {info['incomplete_tasks']} incomplete tasks")
else:
    st.info("No pets yet. Add one above!")

st.divider()

# Task Management Section
st.subheader("📋 Manage Tasks")

if pets:
    # Select which pet to add tasks to
    pet_names = [pet.name for pet in pets]
    selected_pet_name = st.selectbox("Select pet", pet_names)
    selected_pet = st.session_state.owner.get_pet(selected_pet_name)
    
    # Add new task
    with st.expander("➕ Add New Task", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            task_desc = st.text_input("Task description", key="task_desc")
        with col2:
            task_duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20, key="task_duration")
        with col3:
            task_priority = st.selectbox("Priority", [5, 4, 3, 2, 1], format_func=lambda x: f"{x} - {'Critical' if x==5 else 'High' if x==4 else 'Medium' if x==3 else 'Low' if x==2 else 'Optional'}", key="task_priority")
        with col4:
            task_freq = st.selectbox("Frequency", ["daily", "weekly", "monthly"], key="task_freq")
        
        if st.button("Add Task"):
            if task_desc:
                new_task = Task(
                    description=task_desc,
                    duration=task_duration,
                    frequency=task_freq,
                    priority=task_priority
                )
                selected_pet.add_task(new_task)
                st.success(f"✅ Added task '{task_desc}' to {selected_pet_name}!")
                st.rerun()
            else:
                st.error("Please enter a task description")
    
    # Display tasks for selected pet
    st.write(f"**Tasks for {selected_pet_name}:**")
    tasks = selected_pet.get_all_tasks()
    if tasks:
        for task in tasks:
            status = "✅" if task.completed else "⭕"
            st.write(f"{status} {task.description} - {task.duration} min, Priority {task.priority}, {task.frequency}")
    else:
        st.info(f"No tasks for {selected_pet_name} yet. Add one above!")

else:
    st.info("Add a pet first to start managing tasks!")

st.divider()

# Schedule Generation Section
st.subheader("🗓️ Generate Daily Schedule")

if pets and any(pet.get_incomplete_tasks() for pet in pets):
    # Show summary before generating
    scheduler = Scheduler(st.session_state.owner)
    st.write(scheduler.get_summary())
    
    if st.button("🚀 Generate Today's Schedule", type="primary"):
        # Generate the daily plan
        plan = scheduler.generate_daily_plan()
        
        st.success("✅ Schedule generated!")
        
        # Display scheduled tasks
        st.subheader("Scheduled Tasks")
        st.write(f"⏱️ **Time used:** {plan['total_time_used']} minutes")
        st.write(f"⏳ **Time remaining:** {plan['time_remaining']} minutes")
        
        if plan['scheduled']:
            st.write("**Tasks to complete today:**")
            for i, (pet, task) in enumerate(plan['scheduled'], 1):
                st.write(f"{i}. **{pet.name}**: {task.description} ({task.duration} min, Priority {task.priority})")
        
        # Display unscheduled tasks if any
        if plan['unscheduled']:
            st.warning("⚠️ Some tasks couldn't fit in today's schedule:")
            for pet, task in plan['unscheduled']:
                st.write(f"- **{pet.name}**: {task.description} ({task.duration} min, Priority {task.priority})")
        
        # Display reasoning
        with st.expander("📊 Scheduling Reasoning", expanded=True):
            st.text(plan['reasoning'])
        
        # Mark tasks complete option
        st.divider()
        st.subheader("Mark Tasks Complete")
        for pet, task in plan['scheduled']:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**{pet.name}**: {task.description}")
            with col2:
                if st.button("✅ Done", key=f"complete_{task.id}"):
                    scheduler.mark_task_complete(pet.name, task.id)
                    st.success("Task marked complete!")
                    st.rerun()
    
elif not pets:
    st.info("Add pets first to generate a schedule!")
else:
    st.info("No incomplete tasks. Add some tasks to your pets!")
