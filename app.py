import streamlit as st
import google.generativeai as genai
from src.model.rule_based_checker import RuleBasedChecker
from src.model.gemini_checker import GeminiChecker
import logging
import os

# Streamlit page configuration
st.set_page_config(
    page_title="SinGram",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize models
@st.cache_resource
def initialize_models():
    try:
        # Load Gemini model
        genai.configure(api_key="AIzaSyDyGMeILNntelqryNUa9g4XMHTXCSnf7UM")
        gemini_model = genai.GenerativeModel('gemini-pro')

        # Load rule-based checker
        dictionary_path = "data/sinhala_dictionary.txt"

        return {
            "gemini_checker": GeminiChecker(gemini_model),
            "rule_checker": RuleBasedChecker(dictionary_path)
        }
    except Exception as e:
        logging.error(f"Error initializing models: {e}")
        st.error("Error initializing models. Please try again later.")
        return None

models = initialize_models()

# Main UI
st.markdown("""<style>
    .main {background-color: #f5f5f5;}
    .stButton > button {background-color: #4CAF50; color: white; border-radius: 5px;}
    .stRadio > div {display: flex; justify-content: center; margin-bottom: 1rem;}
    .stMarkdown {color: #2c3e50;}
</style>""", unsafe_allow_html=True)

st.title("🎨 SinGram")

# Model Selection
model_options = ["AI Model", "Rule-based Model","LSTM model"]
selected_model = st.radio("Select a model for analysis:", model_options, horizontal=True, index=0)

# Text Input
text = st.text_area(
    "Enter Sinhala text:",
    placeholder="Type or paste your text here...",
    height=200
)

# Analysis Button
if st.button(f"Analyze with {selected_model}"):
    if text.strip():
        with st.spinner("Analyzing text..."):
            try:
                if models:
                    if selected_model == "AI Model":
                        response = models["gemini_checker"].check_grammar(text)
                        results = {
                            "response_text": response
                        }
                    else:  # Rule-based Model
                        results = models["rule_checker"].check_grammar(text)

                    # Display Results
                    if "grammar_errors" in results or "spelling_errors" in results:
                        st.markdown("### Errors Detected")
                        if results.get("grammar_errors"):
                            with st.expander("Grammar Errors"):
                                for error in results["grammar_errors"]:
                                    st.error(f"**{error['sentence']}**")
                                    st.markdown(f"**Description:** {error['errors'][0]['description']}")
                                    st.markdown(f"**Suggestion:** {error['errors'][0]['suggestion']}")
                        if results.get("spelling_errors"):
                            with st.expander("Spelling Errors"):
                                for error in results["spelling_errors"]:
                                    st.warning(f"**{error['sentence']}**")
                                    for spelling in error['errors']:
                                        st.markdown(f"**Word:** {spelling['word']}")
                                        st.markdown(f"**Suggestions:** {', '.join(spelling['suggestions'])}")
                    elif results.get("response_text"):
                        st.markdown("### Gemini AI Response")
                        st.write(results["response_text"])
                    else:
                        st.success("No errors found! 🎉")
                else:
                    st.error("Models failed to initialize. Please refresh the page and try again.")
            except Exception as e:
                logging.error(f"Analysis error: {e}")
                st.error("An error occurred during analysis. Please try again later.")
    else:
        st.error("Please enter some text to analyze.")
