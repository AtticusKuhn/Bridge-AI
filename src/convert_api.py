from models.game import Game
from models.card import Suit
from endplay.types import Deal
from endplay.dds import calc_dd_table, ddtable
from collections import defaultdict

"""
convert game to a endplay Deal object

"""
def game_to_deal(game: Game) -> Deal:
    hand_endplay = []
    for player in game.players:
        d = defaultdict(lambda:[])
        for card in player.hand:
            d[card.suit].append(str(card.rank.value))

        hand_endplay.append(
            ".".join(
                [
                    "".join(d[Suit.SPADES]), 
                    "".join(d[Suit.HEARTS]), 
                    "".join(d[Suit.DIAMONDS]), 
                    "".join(d[Suit.CLUBS]),    
                ]
            )
        )
        
    return Deal(" ".join(hand_endplay))


