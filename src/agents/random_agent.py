import random
from typing import List, Optional, Tuple
from src.models.player import Player
from src.models.card import Card, Suit


class RandomAgent(Player):
    def make_bid(
        self, valid_bids: List[Tuple[int, Optional[Suit]]]
    ) -> Tuple[int, Optional[Suit]]:
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
