from abc import ABC, abstractmethod
from typing import List, Optional
from .card import Card, Suit
from .bid import Bid


class Player(ABC):
    """Abstract base class for all player types (human, random, AI, etc.)"""

    def __init__(self, name: str):
        self.name = name
        self.hand: List[Card] = []
        self.tricks_won = 0

    def receive_cards(self, cards: List[Card]):
        """Add cards to the player's hand."""
        self.hand.extend(cards)
        self.hand.sort(key=lambda card: (card.suit.value, card.rank.value))

    def has_suit(self, suit: Suit) -> bool:
        """Check if player has any cards of the specified suit."""
        return any(card.suit == suit for card in self.hand)

    def get_cards_of_suit(self, suit: Suit) -> List[Card]:
        """Get all cards of the specified suit from player's hand."""
        return [card for card in self.hand if card.suit == suit]

    def play_card(self, card: Card):
        """Remove and return the specified card from player's hand."""
        self.hand.remove(card)
        return card

    @abstractmethod
    def make_bid(self, valid_bids: List[Bid]) -> Bid:
        """
        Make a bid during the bidding phase.

        Args:
            valid_bids: List of valid bid options

        Returns:
            Chosen bid
        """
        pass

    @abstractmethod
    def choose_card(
        self, valid_cards: List[Card], trick_suit: Optional[Suit] = None
    ) -> Card:
        """
        Choose a card to play from valid options.

        Args:
            valid_cards: List of valid cards that can be played
            trick_suit: The suit that must be followed (if any)

        Returns:
            Chosen card
        """
        pass

    def __str__(self):
        return f"{self.name} ({len(self.hand)} cards)"
