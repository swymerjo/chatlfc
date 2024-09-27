from datetime import datetime
import streamlit as st
import langchain_helper as lch  
import textwrap

from scraper_functions import scrape_match_results

# Scrape match results
match_results = scrape_match_results()

# Get today's date
today = datetime.today().date()

# Filter past matches
past_matches = [match for match in match_results if datetime.strptime(match['date'], '%Y-%m-%d').date() <= today]
past_matches = past_matches[::-1]

# Set up Streamlit page configuration
st.set_page_config(page_title="ChatLFC", page_icon="⚽", layout="centered")

# Define LFC color palette
primary_color = "#A50034"  # Liverpool Red
secondary_color = "#FFFFFF"  # White
background_color = "#F3F3F3"  # Light Gray
card_color = "#FFDDC1"  # Soft Orange for card background

# Custom CSS for styling
st.markdown(
    f"""
    <style>
    body {{
        background-color: {background_color};
    }}
    .container {{
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        background-color: {card_color};
    }}
    .title {{
        font-size: 36px;
        color: {primary_color};
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }}
    .match-result {{
        background-color: {secondary_color};
        border-radius: 5px;
        padding: 10px;
        margin: 5px 0;
        box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.2);
        color: black;
    }}
    .header {{
        color: {primary_color};
        text-align: center;
    }}
    .response {{
        background-color: {primary_color};
        color: {secondary_color};
        padding: 10px;
        border-radius: 5px;
        margin-top: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Container for the chatbot
with st.container():
    # Title and recent results header
    st.markdown('<h1 class="title">ChatLFC</h1>', unsafe_allow_html=True)
    st.header("Recent Results:")

    # Display past match results
    for match in past_matches[:6]: 
        st.markdown(f'<div class="match-result">{match["date"]} - vs {match["opponent"]}: {match["goals_for"]} - {match["goals_against"]}</div>', unsafe_allow_html=True)

    # User query input
    query = st.text_input("Alright laa! Ask about recent Liverpool results or player stats:", max_chars=100)

    # Handle query response
    if query:
        docs = lch.create_documents_from_scraped_data()
        response, docs = lch.get_response_from_query(docs, query)

        st.subheader("Response:")
        st.markdown(f'<div class="response">{textwrap.fill(response, width=80)}</div>', unsafe_allow_html=True)

# Footer text
st.markdown("<p style='text-align: center;'>Data provided by FBref.com and OpenAI's GPT-3.5-turbo-instruct model.</p>", unsafe_allow_html=True)
