from typing import List, Optional
from models.player import Player
from models.card import Card, Suit
from models.bid import Bid


# todo
class SimpleRlAgent(Player):
    def make_bid(self, valid_bids: List[Bid]) -> Bid:
        pass

    def choose_card(
        self, valid_cards: List[Card], trick_suit: Optional[Suit] = None
    ) -> Card:
        pass
