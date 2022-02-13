import pandas as pd
from classes import player

def get_players():
    df = pd.read_csv('WeeklyLobby.csv')
    players = []
    for row in df.iterrows():
        play = player(row[1]['Name'],row[1]['Valorant rank'],username=row[1]['Riot ID and tag'])
        if row[1]['Do you have a team?'] =="Yes":
            play.team=row[1]['Team Name( enter "solo" if no team)']
        players.append(play)
    return players