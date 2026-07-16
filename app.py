import streamlit as st
import matplotlib.pyplot as plt

# -----------------------------
# PERSISTENT DATA STORAGE
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

history = st.session_state.history


# -----------------------------
# FUNCTIONS FROM YOUR KAGGLE APP
# -----------------------------

def average_study(history):
    return sum(day["study"] for day in history) / len(history)

def average_sleep(history):
    return sum(day["sleep"] for day in history) / len(history)

def average_mood(history):
    return sum(day["mood"] for day in history) / len(history)

def average_screen(history):
    return sum(day["screen"] for day in history) / len(history)

def average_tasks(history):
    return sum(day["tasks"] for day in history) / len(history)

def give_recommendations(history):
    recs = []
    if average_sleep(history) < 7:
        recs.append("Try to get at least 7 hours of sleep.")
    if average_study(history) < 2:
        recs.append("Increase study time to stay consistent.")
    if average_mood(history) < 5:
        recs.append("Take breaks and do something relaxing.")
    if average_screen(history) > 5:
        recs.append("Reduce screen time to avoid burnout.")
    if average_tasks(history) < 3:
        recs.append("Aim to complete more tasks each day.")
    return recs

def plot_combined(history):
    days = list(range(1, len(history) + 1))

    study = [day["study"] for day in history]
    sleep = [day["sleep"] for day in history]
    mood = [day["mood"] for day in history]
    screen = [day["screen"] for day in history]
    tasks = [day["tasks"] for day in history]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(days, study, marker='o', linewidth=3, color='red', label="Study Hours")
    ax.plot(days, sleep, marker='o', linewidth=3, color='blue', label="Sleep Hours")
    ax.plot(days, mood, marker='o', linewidth=3, color='green', label="Mood Rating")
    ax.plot(days, screen, marker='o', linewidth=3, color='purple', label="Screen Time")
    ax.plot(days, tasks, marker='o', linewidth=3, color='orange', label="Tasks Completed")

    ax.set_title("Combined Productivity Trends")
    ax.set_xlabel("Day")
    ax.set_ylabel("Values")
    ax.grid(True)
    ax.legend()

    return fig

# -----------------------------
# STREAMLIT UI
# -----------------------------

st.title("Personal Data Analyzer")

st.write("Enter your daily data below:")

study = st.number_input("Study hours", min_value=0.0, step=0.5)
sleep = st.number_input("Sleep hours", min_value=0.0, step=0.5)
mood = st.slider("Mood rating", 1, 10)
screen = st.number_input("Screen time (hours)", min_value=0.0, step=0.5)
tasks = st.number_input("Tasks completed", min_value=0, step=1)

if st.button("Save Day"):
    history.append({
        "study": study,
        "sleep": sleep,
        "mood": mood,
        "screen": screen,
        "tasks": tasks
    })
    st.success("Day saved!")

if len(history) > 0:
    st.subheader("Averages")
    st.write("Average Study:", round(average_study(history), 2))
    st.write("Average Sleep:", round(average_sleep(history), 2))
    st.write("Average Mood:", round(average_mood(history), 2))
    st.write("Average Screen:", round(average_screen(history), 2))
    st.write("Average Tasks:", round(average_tasks(history), 2))

    st.subheader("Recommendations")
    for r in give_recommendations(history):
        st.write("- " + r)

    st.subheader("Graph")
    fig = plot_combined(history)
    st.pyplot(fig)
