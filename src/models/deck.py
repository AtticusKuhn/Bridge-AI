import random
from typing import List
from .card import Card, Suit, Rank


class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self._create_deck()

    def _create_deck(self):
        """Creates a standard 52-card deck."""
        self.cards = [Card(suit, rank) for suit in [Suit][:-1] for rank in Rank]

    def shuffle(self):
        """Shuffles the deck of cards."""
        random.shuffle(self.cards)

    def deal(self, num_cards: int) -> List[Card]:
        """
        Deals a specified number of cards from the deck.

        Args:
            num_cards: Number of cards to deal

        Returns:
            List of dealt cards

        Raises:
            ValueError: If requested number of cards exceeds available cards
        """
        if num_cards > len(self.cards):
            raise ValueError("Not enough cards in deck")

        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return str(self.cards)
