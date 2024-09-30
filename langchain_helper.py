from datetime import datetime
import streamlit as st
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import OpenAIEmbeddings
from scraper_functions import scrape_match_results, scrape_player_stats

today = datetime.today().date()

api_key = st.secrets["OPENAI_API_KEY"]

llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0, max_tokens=100)

embeddings = OpenAIEmbeddings()


def get_response_from_query(query, docs):

    prompt = PromptTemplate(
    input_variables=["query", "docs", "today"], 
    template="""
    You are a helpful assistant who can answer questions about Liverpool FC's current 2024/25 season. 
    Answer this question: {query} using the following information: {docs}. 
    When user says 'this season' they mean the 2024/25 season. 
    Use today's date: {today} to establish when Liverpool's last match was if asked about it. 
    The last match is the match closest to, but before today's date: {today} but don't mention this in your answer unless the user asks. 
    Don't make anything up. Keep your answers short and polite.
    """)

    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run(query=query, docs=docs, today=today)
    response = response.replace("\n", "")

    return response, docs


def create_documents_from_scraped_data():
    match_results = scrape_match_results()
    player_stats = scrape_player_stats()

    match_docs = [
        f"{match['date']} - vs {match['opponent']}: {match['goals_for']} - {match['goals_against']}, "
        f"Competition: {match['competition']}, Matchweek: {match['matchweek']}, playing {match['home_or_away']}, "
        f"Expected goals for: {match['expected_goals']}. Expected goals against: {match['expected_goals_against']}."
        f"Possession percentage for Liverpool: {match['possession']}. Result: {match['result']}"
        for match in match_results
    ]


    player_docs = [
        f"Player: {player['player']}, Position: {player['position']}, "
        f"Matches played: {player['matches_played']}, Matches started: {player["matches_started"]},"
        f"Age: {player['age']}, Minutes Played: {player['minutes']}, "
        f"Goals: {player['goals']}, Assists: {player['assists']}"
        for player in player_stats
    ]

    docs = match_docs + player_docs

    return docs