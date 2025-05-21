import random
import os

def shuffle_players(players):
    random.shuffle(players)
    return players


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

