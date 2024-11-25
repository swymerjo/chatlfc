from datetime import datetime
from langchain_text_splitters import RecursiveCharacterTextSplitter
import streamlit as st
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import OpenAIEmbeddings
from scraper_functions import scrape_goalkeeper_stats, scrape_match_results, scrape_player_stats
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS

def create_documents_from_scraped_data():
    match_results = scrape_match_results()
    player_stats = scrape_player_stats()
    goalkeeper_stats = scrape_goalkeeper_stats()

    match_docs = [
        f"{match['date']} - vs {match['opponent']}: {match['goals_for']} - {match['goals_against']}, "
        f"Competition: {match['competition']}, Matchweek: {match['matchweek']}, playing {match['home_or_away']}, "
        f"Expected goals for: {match['expected_goals']}. Expected goals against: {match['expected_goals_against']}."
        f"Possession percentage for Liverpool: {match['possession']}. Result: {match['result']}."
        for match in match_results
    ]


    player_docs = [
        f"Player: {player['player']}, Position: {player['position']}, "
        f"Matches played: {player['matches_played']}, Matches started: {player["matches_started"]}, "
        f"Age: {player['age']}, Minutes Played: {player['minutes']}, "
        f"Goals: {player['goals']}, Assists: {player['assists']}, "
        f"Penalties scored: {player['penalities_scored']}, "
        f"Expected goals: {player['expected_goals']}, Expected assists: {player['expected_assists']}, "
        f"Progressive passes: {player['progressive_passes']}, Progressive carries: {player['progressive_carries']}, "
        for player in player_stats
    ]

    goalkeeper_docs = [
    f"Goalkeeper: {goalkeeper['goalkeeper']},"
    f"Goals conceded / goals against: {goalkeeper['goals_against']}, Saves made: {goalkeeper['saves']}."
    f"Save percentage: {goalkeeper['save_percentage']}. Clean sheets: {goalkeeper['clean_sheets']}."
    for goalkeeper in goalkeeper_stats
    ]


    match_scorers = [
        f"Goal scorers against Ipswich: Diogo Jota (60th minute) and Mohamed Salah (65th minute)."
        f"Goal scorers against Brentford: Luis Diaz (13th minute) and Mohamed Salah (70th minute)."
        f"Goal scorers against Manchester United: Luis Diaz (35th minute and 42nd minute) and Mohamed Salah (56th minute)."
        f"Goal scorers against AC Milan: Ibrahima Konaté (23rd minute), Virgil Van Dijk (41st minute) and Dominik Szoboszlai (67th minute)."
        f"Goal scorers against Bournemouth: Luis Diaz (26th minute and 28th minute) and Darwin Nunez (37th minute)."
        f"Goal scorers against West Ham: Diogo Jota (25th minute and 29th minute), Mohamed Salah (74th minute), and Cody Gakpo (90th minute and 93rd minute)."
        f"Goal scorers against Wolves: Ibrahima Konaté (45+2 minute) and Mohamed Salah (penalty goal in the 61st minute)."
        f"Goal scorers against Bologna: Alexis Mac Allister (11th minute) and Mohamed Salah (75th minute)."
        f"Goal scorers against Crystal Palace: Diogo Jota (9th minute)."
        f"Goal scorers against Chelsea: Mohamed Salah (29th minute) and Curtis Jones (51st minute)."
        f"Goal scorers against Leipzig: Darwin Núñez (27th minute)."
        f"Goal scorers against Arsenal: Virgil van Dijk (18th minute) and Mohamed Salah (81st minute)."
        f"Goal scorers against Brighton (Carabao Cup): Codky Gakpo (46th and 63rd minute) and Luis Diaz (85th minute)."
        f"Goal scorers against Brighton (Premier League): Cody Gakpo (69th minute) and Mohamed Salah (72nd minute)."
        f"Goal scorers against Bayer Leverkusen: Luis Diaz (61st, 63rd, and 92nd minute) and Cody Gakpo (63rd minute)."
        f"Goal scorers against Aston Villa: Darwin Núñez (20th minute) and Mohamed Salah (84th minute)."
        f"Goal scorers against Southampton: Dominik Szoboszlai (30th minute) and Mohamed Salah (63rd minute and a penalty in the 83th minute)."
    ]

    docs = match_docs + player_docs + goalkeeper_docs + match_scorers
    return docs

def create_vector_db(docs: str)-> FAISS:
    api_key = st.secrets["OPENAI_API_KEY"]
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    documents = [Document(page_content=doc) for doc in docs]
    docs = text_splitter.split_documents(documents)
    vector_store = FAISS.from_documents(docs, embeddings)

    return vector_store

def get_response_from_query_with_embeddings(db, query, k=4):
    docs = db.similarity_search(query, k=k) 
    docs_str = " ".join([doc.page_content for doc in docs])
    today = datetime.today().date()
    llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0, max_tokens=100)

    prompt = PromptTemplate(
        input_variables=["query", "docs", "today"], 
        template="""
        You are a helpful assistant who can answer questions about Liverpool FC's current 2024/25 season.
        Answer the user's question: {query} using this information: {docs}. 
        Don't make anything up and only answer the question you are asked. Don't provide additional information.
        Keep your answers as short as possible and be polite.
        If you don't know the answer, apologise and ask the user to ask another question. 
        When the user says 'this season' they mean the 2024/25 season. 
        When asked about Liverpool's last match, last game, or last result, this is the match closest to, but before today's date: {today}.
        When asked about Liverpool's next match or next game, say you don't know.
        """
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run(query=query, docs=docs_str, today=today)
    response = response.replace("\n", "")

    return response

