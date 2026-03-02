import streamlit as st
import pickle
from utils import clean_text
from config import load_css

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Fake News Detector",
    page_icon="📰",
    layout="centered"
)

# ---------------- LOAD CSS ----------------
load_css("style.css")

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model/rf_fake_news_model.pkl", "rb"))
vectorizer = pickle.load(open("model/tfidf_vectorizer.pkl", "rb"))

# ---------------- UI ----------------
st.markdown("<h1 class='title'>📰 AI Fake News Detector</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Detect whether a news article is Real or Fake using Machine Learning</p>", unsafe_allow_html=True)

user_input = st.text_area("Enter News Article Here", height=200)

if st.button("🔍 Analyze News"):

    if user_input.strip() == "":
        st.warning("Please enter some news text.")
    else:
        cleaned = clean_text(user_input)
        vectorized = vectorizer.transform([cleaned])

        prediction = model.predict(vectorized)
        probability = model.predict_proba(vectorized)

        confidence = max(probability[0]) * 100

        st.markdown("---")

        if prediction[0] == 1:
            st.markdown("<div class='real'>✅ This News is Real</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='fake'>❌ This News is Fake</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='confidence'>🔎 Model Confidence: {confidence:.2f}%</div>", unsafe_allow_html=True)