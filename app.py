import os
import openai
from textblob import TextBlob
import streamlit as st

# Securely load your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Epistemic News Engine", layout="wide")
st.title("📰 AUTHENTIC NEWSROOM - GONDWE APP")
st.write("Upload a file or paste your news story below. The app will analyze it for news values, sentiment, decolonial awareness, and provide fact-checking suggestions.")

# About this App Section
with st.expander("ℹ️ About this App"):
    st.markdown("""
    **Creator**: Dr. Gregory Gondwe, Assistant Professor of Journalism at California State University San Bernardino and Faculty Associate at the Harvard Berkman Klein Center for Internet & Society.  

    **Purpose**: This app was born out of a concern for the growing perception that news is depressing, often because it focuses solely on tragedy and conflict while ignoring deeper, issue-based events that shape our communities. Dr. Gondwe believes that journalism—especially student journalism—should inspire action, not apathy. 

    The **Authentic Newsroom** empowers student journalists to assess the real impact of their stories before publishing. It helps ensure that news content is not just timely or dramatic, but meaningful, ethically grounded, and culturally sensitive. The app provides a detailed breakdown of news values, analyzes the story’s sentiment, measures decolonial awareness, and highlights areas needing verification.

    This tool is especially valuable in college newsrooms where young reporters are learning not only how to report, but why they report. The goal is to help them produce journalism that informs, uplifts, and catalyzes positive change.
    """)

# INPUT SECTION
location = st.text_input("Enter Location (City, Country)")
audience = st.selectbox("Select Audience Type", ["Local", "Diaspora", "Academic", "Government", "General Public"])
story_input = st.text_area("Paste News Story Here:", height=300)

if st.button("Analyze Story") and story_input:
    with st.spinner("Analyzing... Please wait"):
        # NEWS VALUE ESTIMATION USING OPENAI (modern API)
        prompt = f"""
        Analyze the following story and evaluate it across these news values:
        - Timeliness
        - Proximity
        - Impact
        - Prominence
        - Conflict
        - Novelty
        - Human Interest

        Give a percentage score (0–100) for each based on content. Story:
        {story_input}
        """
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for news analysis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        news_values = response.choices[0].message.content.strip()

        # SENTIMENT ANALYSIS
        sentiment = TextBlob(story_input).sentiment
        sentiment_score = round(sentiment.polarity * 100, 2)
        sentiment_label = "Positive" if sentiment.polarity > 0.1 else ("Negative" if sentiment.polarity < -0.1 else "Neutral")

        # FACT-CHECK SUGGESTIONS (Simulated)
        fact_check = """Key claims in the story may require verification from credible sources such as AfricaCheck, PolitiFact, or local government records.
Suggested sources: https://africacheck.org, https://www.politifact.com, https://www.snopes.com"""

        # DECOLONIAL AWARENESS SCORE (modern API)
        decolonial_prompt = f"""
        Evaluate the following story for decolonial awareness. Score from 0-100 based on whether the narrative centers marginalized voices, avoids Western assumptions, and reflects pluralistic knowledge.
        Story:
        {story_input}
        """
        decolonial_response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for news analysis."},
                {"role": "user", "content": decolonial_prompt}
            ],
            max_tokens=150
        )
        decolonial_score = decolonial_response.choices[0].message.content.strip()

        # DISPLAY RESULTS
        st.subheader("📊 News Value Breakdown")
        st.code(news_values)

        st.subheader("😊 Sentiment Analysis")
        st.write(f"Sentiment: **{sentiment_label}** ({sentiment_score}%)")

        st.subheader("🌍 Decolonial Awareness Score")
        st.write(decolonial_score)

        st.subheader("🔍 Fact-Checking Suggestions")
        st.write(fact_check)

        st.success("Analysis Complete.")


