from more_itertools import last
from playergen import generate
from read_csv import get_players
from classes import team

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

def left_players(ranked):
    t =team("Team Final")
    for i in range(len(ranked)):
        t.add_player(ranked[i])
    ranked.clear()
    return t


def premade_teams(premade):
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
    all_players = get_players()
   # all_players.extend(genplayers)
    premade_players = [p for p in all_players if p.team!="None"]
    players = [p for p in all_players if p.team=="None"]
    ranked = sorted(players, key = lambda i: i.value,reverse=True)
    teams = []
    noteams = int(len(ranked)/5)
    for i in range(0,noteams,2):
        team1,team2 = make_teams(ranked,i)
        teams.append(team1)
        teams.append(team2)
    premade = premade_teams(premade_players)
    teams.extend(premade)
    #left players
    if len(ranked)>0 and len(ranked)<=5:
        last_team = left_players(ranked)
        teams.append(last_team)
    for p in teams:
        p.print_team()
    check_errors(teams,ranked)
    paired_teams,disparity,unpaired= make_fixture(teams)
    print("\nPaired Teams: ",paired_teams)
    print("Disparity: ",disparity,"(must be <=3)")
    print("Unpaired Teams: ",unpaired)

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