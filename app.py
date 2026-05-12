import os
from groq import Groq
from textblob import TextBlob
import streamlit as st
import time

# Securely load your Groq API key (FREE)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Epistemic News Engine", layout="wide")
st.title("📰 AUTHENTIC NEWSROOM - GONDWE APP")
st.write("Upload a file or paste your news story below. The app will analyze it for news values, sentiment, decolonial awareness, and provide fact-checking suggestions.")

# About this App Section
with st.expander("ℹ️ About this App"):
    st.markdown("""
    **Creator**: Dr. Gregory Gondwe, Assistant Professor of Journalism at California State University San Bernardino and Faculty Associate at the Harvard Berkman Klein Center for Internet & Society.  

    **Purpose**: This app was born out of a concern for the growing perception that news is depressing, often because it focuses solely on tragedy and conflict while ignoring deeper, issue-based events.

    The **Authentic Newsroom** empowers student journalists to assess the real impact of their stories before publishing. It helps ensure that news content is not just timely or dramatic, but meaningful and impactful.

    This tool is especially valuable in college newsrooms where young reporters are learning not only how to report, but why they report. The goal is to help them produce journalism that informs, uplifts, and drives positive change.
    """)

# INPUT SECTION
location = st.text_input("Enter Location (City, Country)")
audience = st.selectbox("Select Audience Type", ["Local", "Diaspora", "Academic", "Government", "General Public"])
story_input = st.text_area("Paste News Story Here:", height=300)

def call_groq_with_retry(prompt, max_tokens=300, max_retries=3):
    """Call Groq API with retry logic for rate limits"""
    for attempt in range(max_retries):
        try:
            message = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for news analysis."},
                    {"role": "user", "content": prompt}
                ],
                model="mixtral-8x7b-32768",  # Free fast model
                max_tokens=max_tokens,
                temperature=0.7,
            )
            return message.choices[0].message.content
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                st.warning(f"⏳ Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                st.error(f"❌ **Error**: {str(e)[:200]}")
                return None

if st.button("Analyze Story") and story_input:
    with st.spinner("Analyzing... Please wait"):
        # NEWS VALUE ESTIMATION
        prompt = f"""
        Analyze the following news story and evaluate it across these news values:
        - Timeliness (0-100)
        - Proximity (0-100)
        - Impact (0-100)
        - Prominence (0-100)
        - Conflict (0-100)
        - Novelty (0-100)
        - Human Interest (0-100)

        For each value, provide a score from 0-100 and brief explanation.
        
        Story:
        {story_input}
        """
        news_values = call_groq_with_retry(prompt, max_tokens=500)
        
        if news_values is None:
            st.stop()

        # SENTIMENT ANALYSIS (TextBlob - Free, no API needed)
        sentiment = TextBlob(story_input).sentiment
        sentiment_score = round((sentiment.polarity + 1) * 50, 2)  # Normalize to 0-100
        sentiment_label = "Positive" if sentiment.polarity > 0.1 else ("Negative" if sentiment.polarity < -0.1 else "Neutral")

        # FACT-CHECK SUGGESTIONS
        fact_check = """Key claims in the story may require verification from credible sources such as AfricaCheck, PolitiFact, or local government records.
Suggested sources: 
- https://africacheck.org (African fact-checking)
- https://www.politifact.com (US fact-checking)
- https://www.snopes.com (General fact-checking)"""

        # DECOLONIAL AWARENESS SCORE
        decolonial_prompt = f"""
        Evaluate the following news story for decolonial awareness on a scale of 0-100. 
        
        Consider:
        - Does the narrative center marginalized or underrepresented voices?
        - Does it avoid Western-centric or colonial assumptions?
        - Does it reflect pluralistic knowledge and perspectives?
        - Are local/indigenous perspectives valued equally?
        - Is language inclusive and non-othering?
        
        Provide a score (0-100) and explanation.
        
        Story:
        {story_input}
        """
        decolonial_score = call_groq_with_retry(decolonial_prompt, max_tokens=300)
        
        if decolonial_score is None:
            st.stop()

        # DISPLAY RESULTS
        st.subheader("📊 News Value Breakdown")
        st.markdown(news_values)

        st.subheader("😊 Sentiment Analysis")
        st.write(f"Sentiment: **{sentiment_label}** ({sentiment_score}%)")

        st.subheader("🌍 Decolonial Awareness Score")
        st.markdown(decolonial_score)

        st.subheader("🔍 Fact-Checking Suggestions")
        st.write(fact_check)

        st.success("✅ Analysis Complete.")
