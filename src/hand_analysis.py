from models.game import Game
from models.card import Suit
from endplay.dds import calc_dd_table, ddtable
from collections import defaultdict

"""
Analyse the theoretical contract based on double dummy analysis

Args: 
    game: The game wanting to analyse

Returns:
    A ddtable as specified here (first player is north): 
        https://github.com/dominicprice/endplay?tab=readme-ov-file#dd-tables

"""
def analyse_contract(game: Game) -> ddtable:
    hand_endplay = []
    for player in game.players:
        d = defaultdict(lambda:[])
        for card in player.hand:
            d[card.suit].append(card.rank)
    
        hand_endplay.append([])
        hand_endplay[-1].append(
            ".".join(
                "".join(d[Suit.SPADES]), 
                "".join(d[Suit.HEARTS]), 
                "".join(d[Suit.DIAMONDS]), 
                "".join(d[Suit.CLUBS]),    
            )
        )
    
    hand_endplay = " ".join(hand_endplay)
    table = calc_dd_table(hand_endplay)
    table.pprint()
    return table