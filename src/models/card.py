from enum import Enum
from typing import Dict, Final


class Suit(Enum):
    CLUBS = "♣"
    DIAMONDS = "♦"
    HEARTS = "♥"
    SPADES = "♠"
    NO_TRUMP = "NT"

    @property
    def index(self):
        return SUIT_INDEX[self]

    @property
    def is_no_trump(self):
        return SUIT_INDEX[self] == 4


# Maps suits to their index values for encoding/comparison
SUIT_INDEX: Final[Dict[Suit, int]] = {
    Suit.CLUBS: 0,
    Suit.DIAMONDS: 1,
    Suit.HEARTS: 2,
    Suit.SPADES: 3,
    Suit.NO_TRUMP: 4,
}


# Compares two suits
def Compare_Suits(a: Suit, b: Suit):
    return SUIT_INDEX[a] < SUIT_INDEX[b]


class Rank(Enum):
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "T"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"

    @property
    def index(self):
        return RANK_INDEX[self]


# Maps ranks to their index values for encoding
RANK_INDEX: Final[Dict[Rank, int]] = {
    rank: idx
    for idx, rank in enumerate(
        [
            Rank.TWO,
            Rank.THREE,
            Rank.FOUR,
            Rank.FIVE,
            Rank.SIX,
            Rank.SEVEN,
            Rank.EIGHT,
            Rank.NINE,
            Rank.TEN,
            Rank.JACK,
            Rank.QUEEN,
            Rank.KING,
            Rank.ACE,
        ]
    )
}


class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank.value}{self.suit.value}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank

    def __hash__(self):
        return hash((self.suit, self.rank))
