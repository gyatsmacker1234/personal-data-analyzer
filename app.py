import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Habit Analyzer", layout="wide")

st.title("🧠 Smart Habit Analyzer — Advanced Edition")

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.header("Habit Variables")

difficulty = st.sidebar.slider("Difficulty", 1, 10, 5)
reward = st.sidebar.slider("Reward", 1, 10, 7)
consistency = st.sidebar.slider("Consistency", 1, 10, 6)
time_cost = st.sidebar.slider("Time Cost", 1, 10, 4)
motivation = st.sidebar.slider("Motivation", 1, 10, 6)
friction = st.sidebar.slider("Friction", 1, 10, 3)

# -----------------------------
# Computation
# -----------------------------
def compute_scores():
    d = difficulty
    r = reward
    c = consistency
    t = time_cost
    m = motivation
    f = friction

    habit_strength = (r*1.5 + c*2 + m*1.2) - (d*1.3 + t*1.1 + f*1.4)
    habit_strength = max(0, min(100, habit_strength * 3))

    success_prob = max(0, min(100, (c*2 + m*1.5 - f*1.2) * 4))

    difficulty_penalty = d * 10

    return habit_strength, success_prob, difficulty_penalty

habit_strength, success_prob, difficulty_penalty = compute_scores()

# -----------------------------
# Main Display
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Habit Scores")
    st.write(f"**Habit Strength:** {habit_strength:.1f}/100")
    st.write(f"**Success Probability:** {success_prob:.1f}%")
    st.write(f"**Difficulty Penalty:** {difficulty_penalty:.1f}")

    # Color bar
    if habit_strength > 70:
        color = "green"
    elif habit_strength > 40:
        color = "yellow"
    else:
        color = "red"

    st.markdown(
        f"""
        <div style='width:100%;height:20px;background:{color};
                    border-radius:5px;margin-top:10px;'></div>
        """,
        unsafe_allow_html=True
    )

    # Recommendation
    st.subheader("📌 Recommendation")
    if habit_strength < 30:
        st.write("This habit is weak. Reduce friction or difficulty.")
    elif habit_strength < 60:
        st.write("Moderate habit. Increase consistency or motivation.")
    else:
        st.write("Strong habit! Keep going.")

# -----------------------------
# Radar Chart (FIXED VERSION)
# -----------------------------
with col2:
    st.subheader("📈 Habit Profile Radar Chart")

    labels = ["Difficulty", "Reward", "Consistency", "Time Cost", "Motivation", "Friction"]
    values = [difficulty, reward, consistency, time_cost, motivation, friction]

    # Base angles (6 values)
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)

    # Duplicate first value for closing the shape
    values_full = np.concatenate((values, [values[0]]))
    angles_full = np.concatenate((angles, [angles[0]]))

    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles_full, values_full, "o-", linewidth=2)
    ax.fill(angles_full, values_full, alpha=0.25)

    # FIX: Use angles WITHOUT the duplicate for labels
    ax.set_thetagrids(angles * 180/np.pi, labels)

    ax.grid(True)
    st.pyplot(fig)
