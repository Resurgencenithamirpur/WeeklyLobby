from const import ranks
from random import choice
from classes import player

def generate(num):
    players = []
    for i in range(num):
        play = player(str(i),choice(list(ranks)))
        players.append(play)
    return players