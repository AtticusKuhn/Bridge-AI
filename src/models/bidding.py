from typing import List, Optional, Dict, Tuple
from .card import Suit
from .player import Player


class Bid:
    def __init__(self, number: int, suit: Optional[Suit] = None):
        self.number = number
        self.suit = suit

    @property
    def is_pass(self) -> bool:
        return self.number == 0

    def __eq__(self, other: 'Bid') -> bool:
        if not isinstance(other, Bid):
            return NotImplemented
        return self.number == other.number and self.suit == other.suit

    def __lt__(self, other: 'Bid') -> bool:
        if not isinstance(other, Bid):
            return NotImplemented
        if self.is_pass:
            return True
        if other.is_pass:
            return False
        if self.number != other.number:
            return self.number < other.number
        # No trump is higher than any suit
        if self.suit is None:
            return False
        if other.suit is None:
            return True
        return False  # Equal number and both have suits, not less than

    def __le__(self, other: 'Bid') -> bool:
        return self < other or self == other

    def __gt__(self, other: 'Bid') -> bool:
        if not isinstance(other, Bid):
            return NotImplemented
        return not (self <= other)

    def __ge__(self, other: 'Bid') -> bool:
        return not (self < other)

    def __str__(self) -> str:
        if self.is_pass:
            return "Pass"
        suit_str = self.suit.value if self.suit else "NT"
        return f"{self.number} {suit_str}"


class Bidding:
    def __init__(self, players: List[Player], dealer_index: int):
        self.players = players
        self.dealer_index = dealer_index
        self.current_player_index = (
            dealer_index + 1
        ) % 4  # Bidding starts left of dealer
        self.bids: Dict[Player, Optional[Bid]] = {
            player: None for player in players
        }
        self.passes = 0
        self.highest_bid = Bid(0)  # Pass bid
        self.highest_bidder: Optional[Player] = None

    def get_valid_bids(self) -> List[Bid]:
        """
        Get list of valid bids for the current player.

        Returns:
            List of valid bids
        """
        valid_bids = []
        current_highest = self.highest_bid.number

        # Can always pass
        valid_bids.append(Bid(0))  # Pass bid

        # Generate valid bids
        for number in range(max(1, current_highest + 1), 8):
            # No trump
            valid_bids.append(Bid(number))
            # Suits
            for suit in Suit:
                if number > current_highest or (
                    number == current_highest and self.highest_bid.suit is not None
                ):
                    valid_bids.append(Bid(number, suit))

        return valid_bids

    def make_bid(self, bid: Bid) -> bool:
        """
        Record a bid from the current player.

        Args:
            bid: The bid object

        Returns:
            True if bidding is complete, False otherwise
        """
        current_player = self.players[self.current_player_index]
        self.bids[current_player] = bid

        # Update highest bid if not a pass
        if not bid.is_pass and bid > self.highest_bid:
            self.highest_bid = bid
            self.highest_bidder = current_player
            self.passes = 0
        else:
            self.passes += 1

        # Move to next player
        self.current_player_index = (self.current_player_index + 1) % 4

        # Bidding is complete if we have 3 passes after a bid, or 4 passes total
        return (self.highest_bidder and self.passes == 3) or self.passes == 4

    def get_contract(self) -> Tuple[Optional[Player], Optional[Bid]]:
        """
        Get the final contract and winning bidder.

        Returns:
            Tuple of (winning_player, winning_bid)
        """
        if self.highest_bid.is_pass:
            return None, None
        return self.highest_bidder, self.highest_bid

    def __str__(self):
        result = "Bidding Status:\n"
        for player in self.players:
            bid = self.bids[player]
            bid_str = "No bid" if bid is None else str(bid)
            result += f"{player.name}: {bid_str}\n"
        return result
