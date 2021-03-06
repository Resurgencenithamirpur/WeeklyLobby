from operator import index
from read_csv import get_players
import sys
sys.path.append("..")
import json
import pandas as pd
# import method from sibling
# module
from Matchmaking.classes import team

"""
def make_teams(ranked,ind):
    team1 =team("Team "+str(ind+1))
    team2 =team("Team "+str(ind+2))

    switch = True
    for play in ranked[:10]:
        if switch:
            team1.add_player(play)
        else:
            team2.add_player(play)
        ranked.remove(play)
        switch = not switch
    return team1,team2
"""
def make_teams(ranked,ind):
    team1 =team("Team "+str(ind+1))
    team2 =team("Team "+str(ind+2))

    for play in ranked[:5]:
            team1.add_player(play)
            ranked.remove(play)

    for play in ranked[:5]:
            team2.add_player(play)
            ranked.remove(play)
    return team1,team2    

def left_players(ranked):
    t =team("Team Final")
    
    for i in range(len(ranked)):
        t.add_player(ranked[i])
    ranked.clear()
    return t


def premade_teams(premade,subs):
    teams = []
    team_names = []
    for player in premade:
        if player.team not in team_names:
            t1 = team(player.team)
            t1.add_player(player)
            teams.append(t1)
            team_names.append(t1.name)
        else:
            for t in teams:
                if t.name ==player.team:
                    t.add_player(player)

    for sub in subs:
        if player.team not in team_names:
            t1 = team(sub.team)
            t1.add_sub(sub)
            teams.append(t1)
            team_names.append(t1.name)
    return teams

def make_fixture(teams):
    disparity = 0
    paired_teams = []
    ranked_teams = sorted(teams, key = lambda i: i.average,reverse=True)
    for i in range(0,len(ranked_teams)-1,2):
        team_pairs = []
        team_pairs.append(ranked_teams[i].name)
        team_pairs.append(ranked_teams[i+1].name)
        disparity = disparity+(ranked_teams[i].average-ranked_teams[i+1].average)
        paired_teams.append(team_pairs)
    disparity = disparity/len(paired_teams)
    if len(ranked_teams)%2:
        return paired_teams,disparity,ranked_teams[len(ranked_teams)-1]
    return paired_teams,disparity,[]

def main():
    #genplayers = generate(39)
    all_players,subs = get_players()
   # all_players.extend(genplayers)
    premade_players = [p for p in all_players if p.team!="None"]
    players = [p for p in all_players if p.team=="None"]
    ranked = sorted(players, key = lambda i: i.value,reverse=True)
    print("Solo: ",len(ranked))

    teams = []
    noteams = int(len(ranked)/5)
    print("noteams: ",noteams)
    if noteams%2:
        noteams-=1
    for i in range(0,noteams,2):
        team1,team2 = make_teams(ranked,i)
        teams.append(team1)
        teams.append(team2)
    premade = premade_teams(premade_players,subs)
    teams.extend(premade)
    #left players
    if len(ranked)>0 and len(ranked)<=5:
        last_team = left_players(ranked)
        teams.append(last_team)
    for p in teams:
        p.print_team()
    print("\nTotal Teams: ",len(teams))
    check_errors(teams,ranked)
    paired_teams,disparity,unpaired= make_fixture(teams)
    print("\nPaired Teams: ",paired_teams)
    print("\nDisparity: ",disparity,"(must be <=3)")
    print("\nUnpaired Teams: ",unpaired)
    to_json(paired_teams)

def to_json(paired_teams):
    out = []
    tim = '05:00pm'
    date = '12/12/42'
    i = 0
    for pair in paired_teams:
        match = {'match':i,
                'team1':pair[0],
                 'team2':pair[1],
                 'time':tim,
                'date': date
        }
        i= i+1
        out.append(match)
    with open('final.json','w') as f:
        json.dump(out,f)

def to_csv(teams):
    columns = ['Name','Discord Username','WhatsApp Number','Valorant Rank','username','Team Name']
    df = pd.DataFrame(columns=columns)
    for t in teams:
        for p in t.players:
            df2 = {'Name':p.name,
            'Discord Username':p.discord,
            'WhatsApp Number':p.number,
            'Valorant Rank':p.rank,
            'username':p.username,
            'Team Name':p.team}
            df.append(df2,ignore_index=True)
    df.to_csv('out.csv',index=[0])


def check_errors(teams,ranked):
    print("\nLeft players:")
    for p in ranked:
        p.print_player()
    print("\nNot Full Teams:")
    for t in teams:
        if not t.is_full():
            print(t.name)
    print("\nTeam overflow:")
    for t in teams:
        if t.overflow():
            print(t.name)

if __name__ == '__main__':
    main()