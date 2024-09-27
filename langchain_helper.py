from datetime import datetime
import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import OpenAIEmbeddings
from scraper_functions import scrape_match_results, scrape_player_stats


load_dotenv()

today = datetime.today().date()

llm = OpenAI()
api_key = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings()


def get_response_from_query(query, docs):

    llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0, max_tokens=100)

    prompt = PromptTemplate(input_variables=["query", "docs", "today"], template="You are a helpful assistant that can answer questions about Liverpool FC's current 2024/25 season. Answer this question: {query} using the following information: {docs}. When someone says 'this season' they are talking about the 2024/25 season. Use today's date: {today} to establish when Liverpool's last match was. Don't make anything up. Only answer the information you are asked about. Keep your answers short and polite.")

    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run(query=query, docs=docs, today=today)
    response = response.replace("\n", "")

    return response, docs


def create_documents_from_scraped_data():
    match_results = scrape_match_results()
    player_stats = scrape_player_stats()

    match_docs = [
        f"{match['date']} - vs {match['opponent']}: {match['goals_for']} - {match['goals_against']}"
        for match in match_results
    ]


    player_docs = [
        f"Player: {player['player']}, Position: {player['position']}, "
        f"Age: {player['age']}, Minutes Played: {player['minutes']}, "
        f"Goals: {player['goals']}, Assists: {player['assists']}"
        for player in player_stats
    ]

    docs = match_docs + player_docs

    return docs