import pandas as pd
import sys
  
# append the path of the
# parent directory
  
# import method from sibling
# module
from classes import player
def get_players():
    df = pd.read_csv('Lobby.csv')
    players = []
    subs = []
    for row in df.iterrows():
        rank = str(row[1]['Valorant Rank(if Solo) / Average Team Rank(if in team)']).lower()
        if row[1]['Do you have a team?'] =="Yes":
            tname = row[1]['Team Name ( enter “solo” if no team ) ']
            play = player(row[1]['Name'],rank,username=row[1]['Member 1 (Leader Riot ID and tag)'],discord=row[1]['Discord Username '],number=row[1]['WhatsApp Number '])
            play.team = tname
            players.append(play)
            for i in range(2,6):
                plays = player(row[1]['Member '+str(i)],rank,username=row[1]['Member '+str(i)])
                plays.team = tname
                players.append(plays)
            for i in range(1,3):
                sub = player(row[1]['Substitute '+str(i)],rank,username=row[1]['Substitute '+str(i)])
                sub.team = tname
                subs.append(sub)
        else:
            play = player(row[1]['Name'],rank,username=row[1]['Member 1 (Leader Riot ID and tag)'],discord=row[1]['Discord Username '],number=row[1]['WhatsApp Number '])
            players.append(play)
    return players,subs