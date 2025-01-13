from typing import List, Optional
from src.models.player import Player
from src.models.card import Card, Suit
from src.models.bid import Bid
import random


class PassAgent(Player):
    def make_bid(self, valid_bids: List[Bid]) -> Bid:
        return Bid(0)

    def choose_card(
        self, valid_cards: List[Card], trick_suit: Optional[Suit] = None
    ) -> Card:
        return random.choice(valid_cards)