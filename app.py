import streamlit as st
import matplotlib.pyplot as plt
import json
import os

# -----------------------------
# Permanent History Storage
# -----------------------------

HISTORY_FILE = "history.json"

def load_history():
    """Load history from JSON file."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history):
    """Save history to JSON file."""
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

def clear_history():
    """Clear history file."""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = load_history()

history = st.session_state.history

# -----------------------------
# Helper Functions
# -----------------------------

def average(key):
    if len(history) == 0:
        return 0
    return sum(day[key] for day in history) / len(history)

def give_recommendations():
    recs = []

    if average("sleep") < 7:
        recs.append("Try to get at least 7 hours of sleep.")

    if average("study") < 2:
        recs.append("Increase study time to stay consistent.")

    if average("mood") < 5:
        recs.append("Take breaks and do something relaxing.")

    if average("screen") > 5:
        recs.append("Reduce screen time to avoid burnout.")

    if average("tasks") < 3:
        recs.append("Aim to complete more tasks each day.")

    return recs

# -----------------------------
# Streamlit UI
# -----------------------------

st.title("📊 Personal Data Analyzer")

st.write("Track your daily habits and get personalized recommendations.")

# Inputs
study = st.number_input("Study hours", min_value=0.0, max_value=24.0, step=0.5)
sleep = st.number_input("Sleep hours", min_value=0.0, max_value=24.0, step=0.5)
mood = st.slider("Mood (1–10)", 1, 10)
screen = st.number_input("Screen time (hours)", min_value=0.0, max_value=24.0, step=0.5)
tasks = st.number_input("Tasks completed", min_value=0, max_value=20, step=1)

# Save Day Button
if st.button("Save Day"):
    day = {
        "study": study,
        "sleep": sleep,
        "mood": mood,
        "screen": screen,
        "tasks": tasks
    }
    history.append(day)
    save_history(history)
    st.success("Day saved!")

# Clear History Button
if st.button("Clear History"):
    clear_history()
    st.session_state.history = []
    history = []
    st.success("History cleared!")

# -----------------------------
# Display Graph
# -----------------------------

if len(history) > 0:
    st.subheader("📈 Progress Over Time")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot([day["study"] for day in history], label="Study Hours")
    ax.plot([day["sleep"] for day in history], label="Sleep Hours")
    ax.plot([day["mood"] for day in history], label="Mood")
    ax.plot([day["screen"] for day in history], label="Screen Time")
    ax.plot([day["tasks"] for day in history], label="Tasks Completed")

    ax.set_xlabel("Day")
    ax.set_ylabel("Values")
    ax.legend()
    st.pyplot(fig)

# -----------------------------
# Recommendations
# -----------------------------

if len(history) > 0:
    st.subheader("⭐ Personalized Recommendations")
    recs = give_recommendations()

    if len(recs) == 0:
        st.write("You're doing great! No recommendations needed.")
    else:
        for r in recs:
            st.write("- " + r)