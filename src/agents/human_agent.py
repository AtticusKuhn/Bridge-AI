from typing import List, Optional
from models.player import Player
from models.card import Card, Suit
from models.bid import Bid


class HumanAgent(Player):
    def make_bid(self, valid_bids: List[Bid]) -> Bid:
        """
        Ask the human player to make a bid.
        """
        print(f"\n{self.name}'s hand: {self.hand}")
        print("\nValid bids:")
        for i, bid in enumerate(valid_bids):
            print(f"{i}: {bid}")

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
