import random
from typing import List, Optional
from models.player import Player
from models.card import Card, Suit
from models.bid import Bid


class RandomAgent(Player):
    def make_bid(self, valid_bids: List[Bid]) -> Bid:
        """
        Make a random valid bid.
        """
        return random.choice(valid_bids)

    def choose_card(
        self, valid_cards: List[Card], trick_suit: Optional[Suit] = None
    ) -> Card:
        """
        Choose a random valid card to play.
        """
        return random.choice(valid_cards)
