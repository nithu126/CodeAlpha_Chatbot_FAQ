import streamlit as st

# Page Settings
st.set_page_config(
    page_title="AI FAQ Assistant",
    page_icon="🤖"
)

st.title("🤖 AI FAQ Assistant")
st.write("Ask AI-related questions and get instant answers")

# Load FAQ Data
faq = {}

try:
    with open("faq.txt", "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            if "|" not in line:
                continue

            question, answer = line.split("|", 1)

            faq[question.strip().lower()] = answer.strip()

except Exception as e:
    st.error(f"Error reading faq.txt: {e}")
    st.stop()

# Debug Information
st.write("Questions loaded:", len(faq))

# User Input
user_question = st.text_input("Enter your question:")

if st.button("Ask"):

    user_question = user_question.strip().lower()

    answer_found = None

    # Exact Match
    if user_question in faq:
        answer_found = faq[user_question]

    # Partial Match
    else:
        for question, answer in faq.items():

            if user_question in question:
                answer_found = answer
                break

    if answer_found:
        st.success(answer_found)
    else:
        st.warning("Sorry, answer not found.")