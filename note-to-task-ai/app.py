# Note-to-Task AI with Streamlit, spaCy, and dateparser
# Goal: Take natural language input like "Submit assignment by Monday"
# and extract tasks + due dates to display as a to-do checklist

# Step 1: Import necessary libraries
import streamlit as st
from utils import parse_tasks, tasks_to_pdf
from dashboard import show_dashboard
import datetime
import pandas as pd

st.set_page_config(page_title="Note-to-Task AI", layout="wide")

if 'tasks' not in st.session_state:
    st.session_state['tasks'] = []

st.title("📝 Note-to-Task AI")
st.write("Enter your notes below. Each sentence will become a task. Dates, priorities, and categories will be detected automatically!")

user_input = st.text_area("Your notes", height=150)

col1, col2 = st.columns([2, 1])

with col1:
    if st.button("Extract Tasks"):
        if user_input.strip():
            new_tasks = parse_tasks(user_input)
            st.session_state['tasks'].extend(new_tasks)
        else:
            st.warning("Please enter some notes to extract tasks.")

    st.subheader("Your To-Do List:")
    tasks = st.session_state['tasks']
    completed = sum(1 for t in tasks if t['done'])
    progress = completed / len(tasks) if tasks else 0
    st.progress(progress, text=f"Completed: {completed} / {len(tasks)}")

    to_delete = []
    today = datetime.date.today()
    for i, task in enumerate(tasks):
        due = task['due']
        if isinstance(due, datetime.datetime):
            due_date = due.date()
        elif isinstance(due, datetime.date):
            due_date = due
        else:
            try:
                due_date = pd.to_datetime(due).date()
            except:
                due_date = None
        # Highlight overdue/due today
        highlight = None
        if due_date:
            if due_date < today:
                highlight = 'red'
            elif due_date == today:
                highlight = 'yellow'
        cols = st.columns([0.05, 0.35, 0.15, 0.15, 0.15, 0.1, 0.05])
        with cols[0]:
            checked = st.checkbox("", value=task['done'], key=f"done_{i}")
            task['done'] = checked
        with cols[1]:
            st.text_area("", value=task['task'], key=f"edit_{i}", height=70)
        with cols[2]:
            st.write(f"Due: {task['due']}")
            if highlight:
                st.markdown(f'<span style="color:{highlight};font-weight:bold;">{"Overdue" if highlight=="red" else "Due Today"}</span>', unsafe_allow_html=True)
        with cols[3]:
            st.write(f"Priority: {task['priority']}")
        with cols[4]:
            st.write(f"Category: {task['category']}")
        with cols[5]:
            if st.button("Delete", key=f"del_{i}"):
                to_delete.append(i)
        with cols[6]:
            st.write(":white_check_mark:" if task['done'] else ":hourglass:")
    for idx in sorted(to_delete, reverse=True):
        del st.session_state['tasks'][idx]
    if tasks:
        if st.button("Clear All Tasks"):
            st.session_state['tasks'] = []
    # Download options
    if tasks:
        df = pd.DataFrame(tasks)
        txt = df.to_string(index=False)
        st.download_button("Download as TXT", txt, file_name="tasks.txt")
        pdf_bytes = tasks_to_pdf(tasks)
        st.download_button("Download as PDF", pdf_bytes, file_name="tasks.pdf", mime="application/pdf")

with col2:
    st.header("📊 Analytics Dashboard")
    show_dashboard(st.session_state['tasks'])
    st.markdown("---")
    st.header("🔐 Login & Integrations")
    st.info("User authentication, Google Calendar sync, recurring tasks, dependencies, and voice input coming soon!")
