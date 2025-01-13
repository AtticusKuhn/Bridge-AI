from typing import List, Optional
from models.player import Player
from models.card import Card, Suit
from models.bid import Bid
import random


class PassAgent(Player):
    def make_bid(self, valid_bids: List[Bid]) -> Bid:
        return Bid(0)

    def choose_card(
        self, valid_cards: List[Card], trick_suit: Optional[Suit] = None
    ) -> Card:
        return random.choice(valid_cards)