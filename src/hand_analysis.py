from models.game import Game
from models.card import Suit
from convert_api import game_to_deal
from endplay.dds import calc_dd_table, ddtable, par
from endplay.types import Denom, Player, Vul
from collections import defaultdict
from random import shuffle
from statistics import median

"""
Analyse the theoretical contract based on double dummy analysis

Args: 
    game: The game wanting to analyse

Returns:
    A ddtable as specified here (first player is north): 
        https://github.com/dominicprice/endplay?tab=readme-ov-file#dd-tables

"""


def analyse_contract(game: Game) -> ddtable:
    hand_endplay = game_to_deal(game)
    table = calc_dd_table(hand_endplay)
    table.pprint()
    return table

"""
Fix first and third player's card.
Randomly distribute the rest of the card to second and fourth player.
Repeat and get the expected winnning tricks for each suite

Get the optimal score
"""
def get_suitable_score(game: Game) -> int:
    hand_endplay = game_to_deal(game)
    east = hand_endplay.east.__str__().split('.')
    west = hand_endplay.west.__str__().split('.')
    east_west = [str(i) + c for i, (x, y) in enumerate(zip(east, west)) for c in x + y]
    
    scores = []
    for _ in range(100):
        shuffle(east_west)
        new_east = ["", "", "", ""]
        for s in east_west[:len(east_west) // 2]:
            new_east[int(s[0])] += s[1]
            
        new_west = ["", "", "", ""]
        for s in east_west[len(east_west) // 2:]:
            new_west[int(s[0])] += s[1]
        
        new_east = ".".join(new_east)
        new_west = ".".join(new_west)
        
        hand_endplay.east = new_east
        hand_endplay.west = new_west
        
        scores.append(par(hand_endplay, Vul.none, Player.north).score)
    
    return median(scores)