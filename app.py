import streamlit as st
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Page settings
st.set_page_config(
    page_title="AI FAQ Assistant",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
body {
    background-color: #0f172a;
}

.main {
    background-color: #0f172a;
}

.chat-container {
    padding: 20px;
    border-radius: 15px;
    background-color: #111827;
    margin-top: 20px;
}

.user-msg {
    background-color: #2563eb;
    color: white;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
}

.bot-msg {
    background-color: #1f2937;
    color: white;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 20px;
}

.title {
    text-align: center;
    color: white;
    font-size: 42px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: #9ca3af;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="title">🤖 AI FAQ Assistant</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Ask AI-related questions and get instant answers</p>',
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.header("📌 About")
    st.write("""
    This chatbot uses:
    - SpaCy NLP
    - TF-IDF Vectorization
    - Cosine Similarity
    
    Developed for CodeAlpha AI Internship.
    """)

# Preprocessing function
def preprocess(text):
    doc = nlp(text.lower())

    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct
    ]

    return " ".join(tokens)

# Load FAQ data
questions = []
answers = []

with open("faq.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

for line in lines:
    if "|" in line:
        q, a = line.strip().split("|")
        questions.append(preprocess(q))
        answers.append(a)

# Vectorization
vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(questions)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input
user_input = st.chat_input("Type your question here...")

if user_input:

    processed_input = preprocess(user_input)

    user_vector = vectorizer.transform([processed_input])

    similarity = cosine_similarity(user_vector, question_vectors)

    best_match = similarity.argmax()

    confidence = similarity[0][best_match]

    if confidence > 0.2:
        response = answers[best_match]
    else:
        response = "Sorry, I couldn't understand your question."

    # Save messages
    st.session_state.messages.append(("user", user_input))
    st.session_state.messages.append(("bot", response))

# Display chat
for sender, message in st.session_state.messages:

    if sender == "user":
        st.markdown(
            f'<div class="user-msg">🧑 {message}</div>',
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            f'<div class="bot-msg">🤖 {message}</div>',
            unsafe_allow_html=True
        )