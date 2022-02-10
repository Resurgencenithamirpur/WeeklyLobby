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

def make_bracket():
    #players = generate(39)
    all_players = get_players()
 #   players.extend(genplayers)
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

    for p in teams:
        p.print_team()
    check_errors(teams,ranked)

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
    make_bracket()