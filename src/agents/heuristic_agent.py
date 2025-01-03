from typing import List, Optional, Dict
from models.player import Player
from models.card import Card, Suit, Rank
from models.bid import Bid
from dataclasses import dataclass


@dataclass
class HandEvaluation:
    """Represents the evaluation of a bridge hand."""

    high_card_points: int
    distribution_points: int
    suit_counts: Dict[Suit, int]

    @property
    def total_points(self) -> int:
        return self.high_card_points + self.distribution_points

    @property
    def is_balanced(self) -> bool:
        """Check if hand has balanced distribution (4-3-3-3, 4-4-3-2, or 5-3-3-2)."""
        return all(1 <= count <= 5 for count in self.suit_counts.values())


class HeuristicAgent(Player):
    """A bridge-playing agent that uses standard bidding and playing conventions."""

    # Bidding constants
    MIN_POINTS_TO_BID = 8
    MIN_POINTS_TO_OPEN = 12
    MIN_POINTS_FOR_TWO_BID = 16
    MIN_POINTS_FOR_THREE_BID = 19
    MIN_POINTS_FOR_NT = 15

    # Card evaluation constants
    HIGH_CARD_POINTS = {
        Rank.ACE: 4,
        Rank.KING: 3,
        Rank.QUEEN: 2,
        Rank.JACK: 1,
    }
    SUIT_LENGTH_FACTOR = 0.5
    HIGH_CARD_QUALITY_FACTOR = 0.3

    def __init__(self, name: str):
        super().__init__(name)

    def evaluate_hand(self) -> HandEvaluation:
        """Evaluate the hand using standard bridge point count system."""
        # Calculate high card points
        hcp = self.get_hcp()

        # Count cards in each suit
        suit_counts = self.get_suit_distribution()

        # Calculate distribution points
        distribution_points = self._calculate_distribution_points(suit_counts)

        return HandEvaluation(hcp, distribution_points, suit_counts)

    def _calculate_distribution_points(self, suit_counts: Dict[Suit, int]) -> int:
        """Calculate distribution points (void=3, singleton=2, doubleton=1)."""
        return sum(
            3 if count == 0 else 2 if count == 1 else 1 if count == 2 else 0
            for count in suit_counts.values()
        )

    def _evaluate_suit_quality(self, suit: Suit) -> float:
        """Evaluate the quality of a suit based on high cards and length."""
        suit_cards = self.get_cards_of_suit(suit)
        if not suit_cards:
            return 0.0

        # Base points from length
        quality = len(suit_cards) * self.SUIT_LENGTH_FACTOR

        # Add points for high cards
        quality += sum(
            self.HIGH_CARD_POINTS[card.rank] * self.HIGH_CARD_QUALITY_FACTOR
            for card in suit_cards
            if card.rank in self.HIGH_CARD_POINTS
        )

        return quality

    def _find_best_suit(self) -> Suit:
        """Find the most biddable suit in hand."""
        suit_qualities = {
            suit: self._evaluate_suit_quality(suit)
            for suit in Suit
            if suit != Suit.NO_TRUMP
        }
        return max(suit_qualities.items(), key=lambda x: x[1])[0]

    def _determine_bid_level(self, total_points: int) -> int:
        """Determine appropriate bid level based on total points."""
        if total_points >= self.MIN_POINTS_FOR_THREE_BID:
            return 3
        elif total_points >= self.MIN_POINTS_FOR_TWO_BID:
            return 2
        elif total_points >= self.MIN_POINTS_TO_OPEN:
            return 1
        return 0

    def _get_pass_bid(self, valid_bids: List[Bid]) -> Bid:
        """Get the pass bid from valid bids."""
        return next(bid for bid in valid_bids if bid.is_pass)

    def make_bid(self, valid_bids: List[Bid]) -> Bid:
        """Make a bid based on hand evaluation and basic bidding rules."""
        hand_eval = self.evaluate_hand()

        # Pass with weak hands
        if hand_eval.total_points < self.MIN_POINTS_TO_BID:
            return self._get_pass_bid(valid_bids)

        bid_level = self._determine_bid_level(hand_eval.total_points)
        if bid_level == 0:
            return self._get_pass_bid(valid_bids)

        # Choose between NT and suit bid
        if (
            hand_eval.is_balanced
            and hand_eval.high_card_points >= self.MIN_POINTS_FOR_NT
        ):
            desired_bid = Bid(bid_level, Suit.NO_TRUMP)
        else:
            desired_bid = Bid(bid_level, self._find_best_suit())

        # Find lowest valid bid that's higher than our desired bid
        valid_suit_bids = [b for b in valid_bids if not b.is_pass]
        if not valid_suit_bids:
            return self._get_pass_bid(valid_bids)

        for bid in valid_suit_bids:
            if bid >= desired_bid:
                return bid

        return self._get_pass_bid(valid_bids)

    def _get_suit_counts(self) -> Dict[Suit, int]:
        """Count cards in each suit in hand."""
        counts = {}
        for card in self.hand:
            counts[card.suit] = counts.get(card.suit, 0) + 1
        return counts

    def _choose_lead_card(self, valid_cards: List[Card]) -> Card:
        """Choose a card when leading a trick."""
        suit_counts = self._get_suit_counts()
        longest_suit = max(suit_counts.items(), key=lambda x: x[1])[0]
        suit_cards = [c for c in valid_cards if c.suit == longest_suit]

        if not suit_cards:
            return max(valid_cards, key=lambda c: c.rank.value)

        # Lead fourth highest from longest suit if possible
        if len(suit_cards) >= 4:
            suit_cards.sort(key=lambda c: c.rank.value)
            return suit_cards[-4]

        return max(suit_cards, key=lambda c: c.rank.value)

    def _choose_follow_card(self, valid_cards: List[Card], trick_suit: Suit) -> Card:
        """Choose a card when following to a trick."""
        trick_cards = [c for c in valid_cards if c.suit == trick_suit]
        if not trick_cards:
            return min(valid_cards, key=lambda c: (c.suit.value, c.rank.value))

        # Play high card if it's likely to win
        high_card = max(trick_cards, key=lambda c: c.rank.value)
        if high_card.rank in [Rank.ACE, Rank.KING]:
            return high_card

        return min(trick_cards, key=lambda c: c.rank.value)

    def choose_card(
        self, valid_cards: List[Card], trick_suit: Optional[Suit] = None
    ) -> Card:
        """Choose a card using basic bridge playing heuristics."""
        if not valid_cards:
            return None

        if not trick_suit:
            return self._choose_lead_card(valid_cards)

        return self._choose_follow_card(valid_cards, trick_suit)
