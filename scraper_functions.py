import requests
from bs4 import BeautifulSoup

url = "https://fbref.com/en/squads/822bd0ba/all_comps/Liverpool-Stats-All-Competitions"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

def get_result_info():
    matches_table = soup.find("table", {"id": "matchlogs_for"})

    results = []
    
    for row in matches_table.find("tbody").find_all("tr"):
        cols = row.find_all("td")
        
        if len(cols) > 0:
        
            date = row.find('th', {'data-stat': 'date'}).text.strip()
            start_time = row.find('td', {'data-stat': 'start_time'}).text.strip()
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
                "start_time": start_time,
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
            minutes = row.find('td', {'data-stat': 'minutes'}).text.strip()
            goals = row.find('td', {'data-stat': 'goals'}).text.strip()
            expected_goals = row.find('td', {'data-stat': 'xg'}).text.strip()
            assists = row.find('td', {'data-stat': 'assists'}).text.strip()
            expected_assists = row.find('td', {'data-stat': 'xg_assist'}).text.strip()
            matches_played = row.find('td', {'data-stat': 'games'}).text.strip()
            matches_started = row.find('td', {'data-stat': 'games_starts'}).text.strip()
            penalities_scored = row.find('td', {'data-stat': 'pens_made'}).text.strip()
            progressive_passes = row.find('td', {'data-stat': 'progressive_passes'}).text.strip()
            progressive_carries = row.find('td', {'data-stat': 'progressive_carries'}).text.strip()

            players.append({
                "player": player,
                "position": position,
                "age": age,
                "matches_played": matches_played,
                "matches_started": matches_started,
                "minutes": minutes,
                "goals": goals,
                "assists": assists,
                "expected_goals": expected_goals,
                "expected_assists": expected_assists,
                "penalities_scored": penalities_scored,
                "progressive_passes": progressive_passes,
                "progressive_carries": progressive_carries,

            })

    
    return players      

def get_goalkeeper_info():
     
     goalkeeping_table = soup.find("table", {"id": "stats_keeper_combined"})

     goalkeepers = []


     for row in goalkeeping_table.find("tbody").find_all("tr"):
        cols = row.find_all("td")

        if len(cols) > 0:
            
            goalkeeper = row.find('th', {'data-stat': 'player'}).text.strip()
            goals_against = row.find('td', {'data-stat': 'gk_goals_against'}).text.strip()
            saves = row.find('td', {'data-stat': 'gk_saves'}).text.strip()
            save_percentage = row.find('td', {'data-stat': 'gk_save_pct'}).text.strip()
            clean_sheets = row.find('td', {'data-stat': 'gk_clean_sheets'}).text.strip()

            goalkeepers.append({
                "goalkeeper": goalkeeper,
                "goals_against": goals_against,
                "saves": saves,
                "save_percentage": save_percentage,
                "clean_sheets": clean_sheets
        })


     return goalkeepers
