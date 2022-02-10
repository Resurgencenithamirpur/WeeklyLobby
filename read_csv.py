import pandas as pd
from classes import player

def get_players():
    df = pd.read_csv('WeeklyLobby.csv')
    players = []
    for row in df.iterrows():
        play = player(row[1]['Name'],row[1]['Valorant rank'])
        players.append(play)
    return players