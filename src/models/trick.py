from typing import Dict, Optional, List
from .card import Card, Suit
from .player import Player


class Trick:
    def __init__(self, leader: Player, trump_suit: Optional[Suit]):
        self.leader = leader
        self.trump_suit = trump_suit
        self.cards_played: Dict[Player, Card] = {}
        self.leading_suit: Optional[Suit] = None

    def play_card(self, player: Player, card: Card) -> bool:
        """
        Record a card played by a player.

        Args:
            player: The player playing the card
            card: The card being played

        Returns:
            True if the play was valid, False otherwise
        """
        if player in self.cards_played:
            return False

        # If this is the first card, set the leading suit
        if not self.cards_played:
            self.leading_suit = card.suit

        self.cards_played[player] = card
        return True

    def get_valid_cards(self, player: Player) -> List[Card]:
        """
        Get list of valid cards that can be played by the player.

        Args:
            player: The player who needs to play

        Returns:
            List of valid cards from the player's hand
        """
        # Must follow suit if possible
        if self.leading_suit and player.has_suit(self.leading_suit):
            return player.get_cards_of_suit(self.leading_suit)
        # If can't follow suit, any card is valid
        return player.hand.copy()

    def get_winner(self) -> Optional[Player]:
        """
        Determine the winner of the trick.

        Returns:
            The winning player, or None if trick is not complete
        """
        if len(self.cards_played) < 4:
            return None

        winning_player = self.leader
        winning_card = self.cards_played[self.leader]

        for player, card in self.cards_played.items():
            if self._is_card_higher(card, winning_card):
                winning_player = player
                winning_card = card

        return winning_player

    def _is_card_higher(self, card: Card, current_winner: Card) -> bool:
        """
        Determine if a card beats the current winning card.

        Args:
            card: The card to compare
            current_winner: The current winning card

        Returns:
            True if the card beats the current winner
        """
        # Trump suit beats any non-trump suit
        if self.trump_suit != Suit.NO_TRUMP:
            if card.suit == self.trump_suit and current_winner.suit != self.trump_suit:
                return True
            if card.suit != self.trump_suit and current_winner.suit == self.trump_suit:
                return False

        # If suits match, higher rank wins
        if card.suit == current_winner.suit:
            return card.rank.value > current_winner.rank.value

        # If suits don't match and no trump, must follow leading suit to win
        return card.suit == self.leading_suit

    def __str__(self):
        result = f"Leading Suit: {self.leading_suit.value if self.leading_suit else 'None'}\n"
        result += (
            f"Trump Suit: {self.trump_suit.value if self.trump_suit else 'None'}\n"
        )
        for player, card in self.cards_played.items():
            result += f"{player.name}: {card}\n"
        return result
