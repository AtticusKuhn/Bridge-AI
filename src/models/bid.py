from typing import Optional
from .card import Suit


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
