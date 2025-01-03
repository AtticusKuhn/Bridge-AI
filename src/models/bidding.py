from typing import List, Optional, Tuple, Dict
from .card import Suit
from .player import Player


class Bidding:
    def __init__(self, players: List[Player], dealer_index: int):
        self.players = players
        self.dealer_index = dealer_index
        self.current_player_index = (
            dealer_index + 1
        ) % 4  # Bidding starts left of dealer
        self.bids: Dict[Player, Optional[Tuple[int, Optional[Suit]]]] = {
            player: None for player in players
        }
        self.passes = 0
        self.highest_bid: Tuple[int, Optional[Suit]] = (0, None)
        self.highest_bidder: Optional[Player] = None

    def get_valid_bids(self) -> List[Tuple[int, Optional[Suit]]]:
        """
        Get list of valid bids for the current player.

        Returns:
            List of valid bids as (number, suit) tuples
        """
        valid_bids = []
        current_highest = self.highest_bid[0]

        # Can always pass
        valid_bids.append((0, None))  # Pass is represented as (0, None)

        # Generate valid bids
        for number in range(max(1, current_highest + 1), 8):
            # No trump
            valid_bids.append((number, None))
            # Suits
            for suit in Suit:
                if number > current_highest or (
                    number == current_highest and self.highest_bid[1] is not None
                ):
                    valid_bids.append((number, suit))

        return valid_bids

    def make_bid(self, bid: Tuple[int, Optional[Suit]]) -> bool:
        """
        Record a bid from the current player.

        Args:
            bid: The bid as (number, suit) tuple

        Returns:
            True if bidding is complete, False otherwise
        """
        current_player = self.players[self.current_player_index]
        self.bids[current_player] = bid

        # Update highest bid if not a pass
        if bid[0] > 0:
            self.highest_bid = bid
            self.highest_bidder = current_player
            self.passes = 0
        else:
            self.passes += 1

        # Move to next player
        self.current_player_index = (self.current_player_index + 1) % 4

        # Bidding is complete if we have 3 passes after a bid, or 4 passes total
        return (self.highest_bidder and self.passes == 3) or self.passes == 4

    def get_contract(
        self,
    ) -> Tuple[Optional[Player], Optional[Tuple[int, Optional[Suit]]]]:
        """
        Get the final contract and winning bidder.

        Returns:
            Tuple of (winning_player, winning_bid)
        """
        return self.highest_bidder, self.highest_bid

    def __str__(self):
        result = "Bidding Status:\n"
        for player in self.players:
            bid = self.bids[player]
            if bid is None:
                bid_str = "No bid"
            elif bid[0] == 0:
                bid_str = "Pass"
            else:
                suit_str = bid[1].value if bid[1] else "NT"
                bid_str = f"{bid[0]} {suit_str}"
            result += f"{player.name}: {bid_str}\n"
        return result
