from typing import List, Optional, Tuple
from src.models.player import Player
from src.models.card import Card, Suit


class HumanAgent(Player):
    def make_bid(
        self, valid_bids: List[Tuple[int, Optional[Suit]]]
    ) -> Tuple[int, Optional[Suit]]:
        """
        Ask the human player to make a bid.
        """
        print(f"\n{self.name}'s hand: {self.hand}")
        print("\nValid bids:")
        for i, (number, suit) in enumerate(valid_bids):
            suit_str = suit.value if suit else "No Trump"
            print(f"{i}: {number} {suit_str}")

        while True:
            try:
                choice = int(input("\nEnter the number of your bid choice: "))
                if 0 <= choice < len(valid_bids):
                    return valid_bids[choice]
                print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def choose_card(
        self, valid_cards: List[Card], trick_suit: Optional[Suit] = None
    ) -> Card:
        """
        Ask the human player to choose a card to play.
        """
        print(f"\n{self.name}'s hand: {self.hand}")
        if trick_suit:
            print(f"Must follow suit: {trick_suit.value}")
        print("\nValid cards:")
        for i, card in enumerate(valid_cards):
            print(f"{i}: {card}")

        while True:
            try:
                choice = int(input("\nEnter the number of the card you want to play: "))
                if 0 <= choice < len(valid_cards):
                    return valid_cards[choice]
                print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
