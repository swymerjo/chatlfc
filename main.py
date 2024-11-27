from datetime import datetime
import streamlit as st
import langchain_helper as lch  
import textwrap
from scraper_functions import get_result_info

def format_match_dates(date):
    formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B %Y')
    return formatted_date

match_results = get_result_info()

now = datetime.now()
today = now.date()

past_matches = [
    match for match in match_results
    if datetime.strptime(f"{match['date']} {match['start_time']}", '%Y-%m-%d %H:%M') <= now
]
past_matches = past_matches[::-1]
upcoming_matches = [match for match in match_results if datetime.strptime(f"{match['date']} {match['start_time']}", '%Y-%m-%d %H:%M') > now]

st.set_page_config(page_title="StatLFC", page_icon="⚽", layout="wide")

primary_color = "#A50034"  # Liverpool Red
secondary_color = "#FFFFFF"  # White
background_color = "#F3F3F3"  # Light Gray
card_color = "#FFDDC1"  # Soft Orange for card background

st.markdown(
    f"""
    <style>
    body {{
        background-color: {background_color};
    }}
    .container {{
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        background-color: {card_color};
    }}
    .title {{
        font-size: 50px;
        color: {primary_color};
        text-align: center;
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
    .upcoming-match {{
        background-color: {primary_color};
        color: {secondary_color};
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 20px;
        box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.2);     
    }}
    .header {{
        color: {primary_color};
        text-align: center;
    }}
    .response {{
        background-color: {background_color};
        color: black;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

left_col, middle_col, right_col = st.columns([1, 2, 1])

with right_col:
   st.markdown("""
<div style='margin-top: 120px;'></div>
<p style='font-size: 16px; margin-left: 50px;'>
StatLFC can tell you about:
<ul style='margin-left: 50px;'>
    <li>Match results</li>
    <li>Goals scored</li>
    <li>Expected goals</li>
    <li>Assists</li>
    <li>Expected assists</li>
    <li>Possession</li>
    <li>Progressive passes</li>
    <li>Progressive carries</li>
    <li>Minutes played</li>
    <li>Penalties scored</li>
    <li>Matches played</li>
    <li>Matches started</li>
    <li>Goalkeepers: Clean sheets</li>
    <li>Goalkeepers: Save percentage</li>
    <li>Goalkeepers: Saves made</li>
    <li>Goalkeepers: Goals conceded</li>
</ul>
</p>
""", unsafe_allow_html=True)


with middle_col:
    with st.container():
        st.markdown('<h1 class="title">StatLFC</h1>', unsafe_allow_html=True)
        st.header("Recent Results:")

        for match in past_matches[:3]: 
            date = format_match_dates(match['date'])
            st.markdown(f'<div class="match-result">{date} - {match["home_or_away"]} vs {match["opponent"]}: {match["goals_for"]} - {match["goals_against"]} ({match["result"]})</div>', unsafe_allow_html=True)

        st.header("Upcoming match:")

        for match in upcoming_matches[:1]: 
            date = format_match_dates(match['date'])
            st.markdown(f'<div class="upcoming-match">{date} - {match["home_or_away"]} vs {match["opponent"]}</div>', unsafe_allow_html=True)

        query = st.text_input("Alright laa! Ask about recent Liverpool results or player stats:", max_chars=100)
        docs = lch.create_documents_from_scraped_data()

        if query and docs:
            db = lch.create_vector_db(docs)
            response = lch.get_response_from_query_with_embeddings(db, query)

            st.subheader("Response:")
            st.markdown(f'<div class="response">{textwrap.fill(response, width=80)}</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; padding-top: 20px;'>Data provided by FBref.com and OpenAI's GPT-3.5-turbo-instruct model.</p>", unsafe_allow_html=True)
