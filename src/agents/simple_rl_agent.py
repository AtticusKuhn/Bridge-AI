import random
from typing import List, Optional
from src.models.player import Player
from src.models.card import Card, Suit
from src.models.bid import Bid

# todo
class SimpleRlAgent(Player):
    def make_bid(self, valid_bids: List[Bid]) -> Bid:
        pass

    def choose_card(
        self, valid_cards: List[Card], trick_suit: Optional[Suit] = None
    ) -> Card:
        pass