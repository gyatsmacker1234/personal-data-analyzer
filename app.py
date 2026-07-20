import streamlit as st
import matplotlib.pyplot as plt
import json
import os
from datetime import datetime, timedelta

# -----------------------------
# Permanent History Storage
# -----------------------------

HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

def clear_history():
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
# Habit Score
# -----------------------------

def habit_score(day):
    score = (
        day["study"] * 10 +
        day["sleep"] * 8 +
        day["mood"] * 5 -
        day["screen"] * 4 +
        day["tasks"] * 6
    )
    return max(0, min(score, 100))

# -----------------------------
# Weekly Summary
# -----------------------------

def weekly_summary():
    if len(history) == 0:
        return None

    last_7_days = history[-7:]

    summary = {
        "study": sum(d["study"] for d in last_7_days) / len(last_7_days),
        "sleep": sum(d["sleep"] for d in last_7_days) / len(last_7_days),
        "mood": sum(d["mood"] for d in last_7_days) / len(last_7_days),
        "screen": sum(d["screen"] for d in last_7_days) / len(last_7_days),
        "tasks": sum(d["tasks"] for d in last_7_days) / len(last_7_days),
        "habit_score": sum(habit_score(d) for d in last_7_days) / len(last_7_days)
    }

    return summary

# -----------------------------
# Streak Tracker
# -----------------------------

def streak_tracker():
    if len(history) == 0:
        return 0, 0

    streak = 1
    longest = 1

    for i in range(len(history) - 1, 0, -1):
        today = history[i]["date"]
        prev = history[i - 1]["date"]

        if (datetime.fromisoformat(today) - datetime.fromisoformat(prev)).days == 1:
            streak += 1
        else:
            break

    # Calculate longest streak
    temp = 1
    for i in range(len(history) - 1, 0, -1):
        today = history[i]["date"]
        prev = history[i - 1]["date"]

        if (datetime.fromisoformat(today) - datetime.fromisoformat(prev)).days == 1:
            temp += 1
        else:
            longest = max(longest, temp)
            temp = 1

    longest = max(longest, temp)

    return streak, longest

# -----------------------------
# Streamlit UI
# -----------------------------

st.title("📊 Personal Data Analyzer")

st.write("Track your daily habits and get personalized insights.")

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
        "tasks": tasks,
        "date": datetime.now().date().isoformat()
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
# Weekly Summary Display
# -----------------------------

summary = weekly_summary()
if summary:
    st.subheader("📅 Weekly Summary (Last 7 Days)")
    st.write(f"**Average Study:** {summary['study']:.2f} hrs")
    st.write(f"**Average Sleep:** {summary['sleep']:.2f} hrs")
    st.write(f"**Average Mood:** {summary['mood']:.2f}/10")
    st.write(f"**Average Screen Time:** {summary['screen']:.2f} hrs")
    st.write(f"**Average Tasks:** {summary['tasks']:.2f}")
    st.write(f"**Average Habit Score:** {summary['habit_score']:.2f}/100")

# -----------------------------
# Streak Tracker Display
# -----------------------------

if len(history) > 0:
    streak, longest = streak_tracker()
    st.subheader("🔥 Streak Tracker")
    st.write(f"**Current Streak:** {streak} days")
    st.write(f"**Longest Streak:** {longest} days")

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