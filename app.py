import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(st.session_state.owner)

if "pet" not in st.session_state:
    st.session_state.pet = Pet(pet_name, species)
    st.session_state.owner.add_pet(st.session_state.pet)

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    task_time = st.time_input("Time")
with col3:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col4:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    new_task = Task(task_title, task_time.strftime("%H:%M"), int(duration), priority, "daily")
    st.session_state.pet.add_task(new_task)

current_tasks = st.session_state.pet.get_tasks()
if current_tasks:
    st.write("Current tasks:")
    st.table([{
        "Title": t.description,
        "Duration": f"{t.duration_minutes} min",
        "Priority": t.priority
    } for t in current_tasks])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    sorted_tasks = st.session_state.scheduler.sort_by_time()
    if sorted_tasks:
        st.table([{
            "Time": t.time,
            "Task": t.description,
            "Duration": f"{t.duration_minutes} min",
            "Priority": t.priority,
            "Done": "✓" if t.completed else "✗"
        } for t in sorted_tasks])
    else:
        st.info("No tasks scheduled yet.")

    conflicts = st.session_state.scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(warning)
    else:
        st.success("No conflicts found!")