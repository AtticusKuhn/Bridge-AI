from typing import List, Optional
import random
from .card import Suit
from .deck import Deck
from .player import Player
from .bidding import Bidding, Bid
from .trick import Trick


class Game:
    def __init__(self, players: List[Player]):
        if len(players) != 4:
            raise ValueError("Bridge requires exactly 4 players")
        self.players = players
        self.dealer_index = random.randint(0, 3)
        self.current_trick: Optional[Trick] = None
        self.tricks_played = []
        self.declarer: Optional[Player] = None
        self.contract: Optional[Bid] = None
        self.score = {player: 0 for player in players}

    def play(self):
        """Play a complete game of bridge."""
        print("\nStarting new game of Bridge")
        print("Players:", ", ".join(p.name for p in self.players))

        # Deal cards
        self._deal_cards()

        # Bidding phase
        self._conduct_bidding()
        if not self.contract:
            print("All players passed. Game over.")
            return

        print(
            f"\nFinal Contract: {self.contract} "
            f"by {self.declarer.name}"
        )

        # Playing phase
        self._play_tricks()

        # Score the game
        self._score_game()

    def _deal_cards(self):
        """Deal cards to all players."""
        deck = Deck()
        deck.shuffle()
        cards_per_player = len(deck) // len(self.players)

        for player in self.players:
            cards = deck.deal(cards_per_player)
            player.receive_cards(cards)

    def _conduct_bidding(self):
        """Conduct the bidding phase."""
        bidding = Bidding(self.players, self.dealer_index)

        while True:
            current_player = self.players[bidding.current_player_index]
            valid_bids = bidding.get_valid_bids()

            # Get bid from current player
            bid = current_player.make_bid(valid_bids)
            bidding_complete = bidding.make_bid(bid)

            # Show current bidding status
            print(bidding)

            if bidding_complete:
                self.declarer, self.contract = bidding.get_contract()
                break

    def _play_tricks(self):
        """Play out all tricks."""
        if not self.declarer or not self.contract:
            return

        # Start with player to the left of declarer
        current_player_index = (self.players.index(self.declarer) + 1) % 4
        trump_suit = self.contract.suit

        # Play 13 tricks
        for _ in range(13):
            leader = self.players[current_player_index]
            self.current_trick = Trick(leader, trump_suit)
            print(f"\nTrick {len(self.tricks_played) + 1}:")

            # Each player plays a card
            for _ in range(4):
                player = self.players[current_player_index]
                valid_cards = self.current_trick.get_valid_cards(player)

                # Get card from current player
                card = player.choose_card(valid_cards, self.current_trick.leading_suit)
                player.play_card(card)
                self.current_trick.play_card(player, card)

                print(f"{player.name} plays {card}")
                current_player_index = (current_player_index + 1) % 4

            # Determine winner and start next trick
            winner = self.current_trick.get_winner()
            winner.tricks_won += 1
            print(f"{winner.name} wins the trick")

            self.tricks_played.append(self.current_trick)
            current_player_index = self.players.index(winner)

    def _score_game(self):
        """Score the completed game."""
        if not self.declarer or not self.contract:
            return

        # Get declarer's team tricks
        declarer_index = self.players.index(self.declarer)
        partner_index = (declarer_index + 2) % 4
        declarer_team_tricks = (
            self.players[declarer_index].tricks_won
            + self.players[partner_index].tricks_won
        )

        # Calculate if contract was made
        tricks_needed = 6 + self.contract.number
        contract_made = declarer_team_tricks >= tricks_needed

        print(f"\nDeclarer's team took {declarer_team_tricks} tricks")
        print(f"Contract {'made' if contract_made else 'failed'}")

        # Simple scoring for now
        if contract_made:
            self.score[self.declarer] += 100
            self.score[self.players[partner_index]] += 100
        else:
            opponent1 = self.players[(declarer_index + 1) % 4]
            opponent2 = self.players[(declarer_index + 3) % 4]
            self.score[opponent1] += 50
            self.score[opponent2] += 50

        print("\nFinal Scores:")
        for player, score in self.score.items():
            print(f"{player.name}: {score}")
