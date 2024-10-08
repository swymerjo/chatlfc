import requests
from bs4 import BeautifulSoup

url = "https://fbref.com/en/squads/822bd0ba/all_comps/Liverpool-Stats-All-Competitions"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

def scrape_match_results():
    results = get_result_info()
    return results

def scrape_player_stats():
     player_info = get_player_info()
     return player_info

def get_result_info():
    matches_table = soup.find("table", {"id": "matchlogs_for"})

    results = []
    
    for row in matches_table.find("tbody").find_all("tr"):
        cols = row.find_all("td")
        
        if len(cols) > 0:
        
            date = row.find('th', {'data-stat': 'date'}).text.strip()
            competition = row.find('td', {'data-stat': 'comp'}).text.strip()
            matchweek = row.find('td', {'data-stat': 'round'}).text.strip()
            home_or_away = row.find('td', {'data-stat': 'venue'}).text.strip()
            opponent = row.find('td', {'data-stat': 'opponent'}).text.strip()
            opponent = remove_emoji_text(opponent)
            result = row.find('td', {'data-stat': 'result'}).text.strip()
           
            try:
                goals_for = int(row.find('td', {'data-stat': 'goals_for'}).text.strip())  
            except (ValueError, AttributeError):
                goals_for = None  
            
            try:
                goals_against = int(row.find('td', {'data-stat': 'goals_against'}).text.strip())  
            except (ValueError, AttributeError):
                goals_against = None  
            
            try:
                expected_goals = float(row.find('td', {'data-stat': 'xg_for'}).text.strip()) 
            except (ValueError, AttributeError):
                expected_goals = None  

            try:
                possession = float(row.find('td', {'data-stat': 'possession'}).text.strip()) 
            except (ValueError, AttributeError):
                possession = None
            
            try:
                expected_goals_against = float(row.find('td', {'data-stat': 'xg_against'}).text.strip()) 
            except (ValueError, AttributeError):
                expected_goals_against = None
            
    
            results.append({
                "date": date,
                "competition": competition,
                "matchweek": matchweek,
                "home_or_away": home_or_away,
                "opponent": opponent,
                "goals_for": goals_for,
                "goals_against": goals_against,
                "expected_goals": expected_goals,
                "expected_goals_against": expected_goals_against,
                "possession": possession,
                "result": result
            })
    
    return results

def remove_emoji_text(opponent_name):
    text = opponent_name.split()
    
    if text and text[0].islower():
        text.pop(0)
    
    return ' '.join(text)     

def get_player_info():
    player_table = soup.find("table", {"id": "stats_standard_combined"})

    players = []

    for row in player_table.find("tbody").find_all("tr"):
        cols = row.find_all("td")

        if len(cols) > 0:

            player = row.find('th', {'data-stat': 'player'}).text.strip()
            position = row.find('td', {'data-stat': 'position'}).text.strip()
            age = row.find('td', {'data-stat': 'age'}).text.strip()

            try:
                minutes = int(row.find('td', {'data-stat': 'minutes'}).text.strip())  
            except (ValueError, AttributeError):
                minutes = None  


            try:
                goals = int(row.find('td', {'data-stat': 'goals'}).text.strip())  
            except (ValueError, AttributeError):
                goals = None  

            try:
                assists = int(row.find('td', {'data-stat': 'assists'}).text.strip())  
            except (ValueError, AttributeError):
                assists = None  
            
            try:
                matches_played = int(row.find('td', {'data-stat': 'games'}).text.strip())  
            except (ValueError, AttributeError):
                matches_played = None 

            try:
                matches_started = int(row.find('td', {'data-stat': 'games_starts'}).text.strip())  
            except (ValueError, AttributeError):
                matches_started = None 

            try:
                penalities_scored = int(row.find('td', {'data-stat': 'pens_made'}).text.strip())  
            except (ValueError, AttributeError):
                penalities_scored = None

            players.append({
                "player": player,
                "position": position,
                "age": age,
                "matches_played": matches_played,
                "matches_started": matches_started,
                "minutes": minutes,
                "goals": goals,
                "assists": assists,
                "penalities_scored": penalities_scored
            })
       
    return players        
