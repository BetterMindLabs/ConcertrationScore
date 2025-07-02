import streamlit as st
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("🧘‍♂️ Concentration Score Checker")

st.markdown("""
Check your current focus level and get AI-powered tips to improve your concentration!
""")

# Questions
q1 = st.slider("How easily are you distracted today?", 1, 10, 5)
q2 = st.slider("How many times did you check your phone in the last hour?", 0, 20, 5)
q3 = st.slider("How many focused work sessions have you done today?", 0, 10, 2)
q4 = st.selectbox("Did you sleep well last night?", ["Yes", "No"])
q5 = st.slider("Rate your mental energy today", 1, 10, 5)

if st.button("Check Concentration Score"):
    # Simple scoring logic
    score = 100
    score -= q1 * 5          # Higher distraction → lower score
    score -= q2 * 2          # More phone checks → lower score
    score += q3 * 5          # More work sessions → higher score
    score += (5 if q4 == "Yes" else -5)
    score += q5 * 3          # Higher energy → higher score

    # Clamp score between 0 and 100
    score = max(0, min(score, 100))

    st.success(f"🟢 Your Concentration Score: {score}/100")

    # Gemini prompt
    prompt = f"""
    Here is my concentration self-assessment:
    - Distraction level: {q1}/10
    - Phone checks in last hour: {q2}
    - Focused work sessions today: {q3}
    - Slept well: {q4}
    - Mental energy: {q5}/10
    Calculated concentration score: {score}/100.

    Please give me:
    - A brief analysis of why my focus may be low or high.
    - Personalized tips to improve focus today.
    - A short motivational message.
    Present this in a friendly, encouraging style.
    """

    with st.spinner("Analyzing with Gemini..."):
        response = model.generate_content(prompt)
        advice = response.text

    st.markdown("---")
    st.subheader("🤖 Gemini AI Suggestions")
    st.markdown(advice)

st.caption("✨ Built with Python, Streamlit & Gemini API")
