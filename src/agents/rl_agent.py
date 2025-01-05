"""Reinforcement Learning Agent for Bridge game."""

from __future__ import annotations

import random
from dataclasses import dataclass
import torch
import torch.nn as nn
import torch.optim as optim
from typing import List, Optional, Final, ClassVar
from models.player import Player
from models.card import Card, Suit, SUIT_INDEX, RANK_INDEX
from models.bid import Bid

# Type aliases
State = torch.Tensor
Action = int
Reward = float


@dataclass
class QNetworkConfig:
    """Configuration for Q-Network architecture."""

    hidden_size1: ClassVar[int] = 128
    hidden_size2: ClassVar[int] = 64
    gamma: ClassVar[float] = 0.99  # Discount factor


class QNetwork(nn.Module):
    """Neural network for Q-learning."""

    def __init__(self, state_size: int, action_size: int) -> None:
        """Initialize Q-Network with given state and action dimensions.

        Args:
            state_size: Dimension of the input state
            action_size: Dimension of the output action space
        """
        super().__init__()
        self.fc1 = nn.Linear(state_size, QNetworkConfig.hidden_size1)
        self.fc2 = nn.Linear(QNetworkConfig.hidden_size1, QNetworkConfig.hidden_size2)
        self.fc3 = nn.Linear(QNetworkConfig.hidden_size2, action_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through the network.

        Args:
            x: Input tensor

        Returns:
            Output tensor representing Q-values for each action
        """
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)


class RLAgent(Player):
    """Reinforcement Learning agent that learns to play bridge through Q-learning."""

    def __init__(
        self, name: str, learning_rate: float = 0.001, epsilon: float = 0.1
    ) -> None:
        """Initialize the RL agent.

        Args:
            name: Agent's name
            learning_rate: Learning rate for optimizer
            epsilon: Exploration rate for epsilon-greedy strategy
        """
        super().__init__(name)
        self.epsilon = epsilon

        # State dimensions
        self.card_state_size: Final[int] = 52  # One-hot encoding of cards
        self.bid_state_size: Final[int] = 35  # Possible bids
        self.trick_state_size: Final[int] = 4  # One-hot encoding of trick suit

        # Initialize networks
        self.bid_q_network = QNetwork(
            state_size=self.card_state_size + self.bid_state_size,
            action_size=self.bid_state_size,
        )
        self.play_q_network = QNetwork(
            state_size=self.card_state_size + self.trick_state_size,
            action_size=len(RANK_INDEX),
        )

        # Initialize optimizers
        self.bid_optimizer = optim.Adam(
            self.bid_q_network.parameters(), lr=learning_rate
        )
        self.play_optimizer = optim.Adam(
            self.play_q_network.parameters(), lr=learning_rate
        )

        self.criterion = nn.MSELoss()

    def _encode_hand(self) -> torch.Tensor:
        """Encode the player's hand as a binary vector.

        Returns:
            One-hot encoded tensor representing the cards in hand
        """
        encoding = torch.zeros(self.card_state_size, dtype=torch.float32)
        for card in self.hand:
            idx = 13 * SUIT_INDEX[card.suit] + RANK_INDEX[card.rank]
            encoding[idx] = 1.0
        return encoding

    def _encode_trick_suit(self, trick_suit: Optional[Suit]) -> torch.Tensor:
        """Encode the trick suit as a one-hot vector.

        Args:
            trick_suit: Current trick suit or None

        Returns:
            One-hot encoded tensor representing the trick suit
        """
        encoding = torch.zeros(self.trick_state_size, dtype=torch.float32)
        if trick_suit and trick_suit != Suit.NO_TRUMP:
            encoding[SUIT_INDEX[trick_suit]] = 1.0
        return encoding

    def _encode_valid_bids(self, valid_bids: List[Bid]) -> torch.Tensor:
        """Encode valid bids as a binary vector.

        Args:
            valid_bids: List of valid bids

        Returns:
            Binary tensor representing valid bids
        """
        encoding = torch.zeros(self.bid_state_size, dtype=torch.float32)
        for bid in valid_bids:
            if not bid.is_pass:
                idx = 5 * (bid.number - 1) + bid.suit.index
                encoding[idx] = 1.0
        return encoding

    def make_bid(self, valid_bids: List[Bid]) -> Bid:
        """Make a bid using epsilon-greedy strategy.

        Args:
            valid_bids: List of valid bids to choose from

        Returns:
            Selected bid
        """
        if random.random() < self.epsilon:
            return random.choice(valid_bids)

        state = torch.cat([self._encode_hand(), self._encode_valid_bids(valid_bids)])

        with torch.no_grad():
            q_values = self.bid_q_network(state)

        # Mask invalid actions
        valid_mask = torch.full_like(q_values, float("-inf"))
        valid_mask[0] = 0  # Pass is always valid

        for bid in valid_bids:
            if not bid.is_pass:
                idx = bid.number + SUIT_INDEX[bid.suit]
                valid_mask[idx] = 0

        action_idx = (q_values + valid_mask).argmax().item()

        # Convert action index to bid
        if action_idx == 0:
            pass_bids = [bid for bid in valid_bids if bid.is_pass]
            if not pass_bids:
                # If no pass bid available, choose a random valid bid
                return random.choice(valid_bids)
            return pass_bids[0]
        else:
            target_number = action_idx // 5
            target_suit = list(SUIT_INDEX.keys())[action_idx % 5]
            matching_bids = [
                bid
                for bid in valid_bids
                if not bid.is_pass
                and bid.number == target_number
                and bid.suit == target_suit
            ]
            if not matching_bids:
                # If no matching bid available, choose a random valid bid
                return random.choice(valid_bids)
            return matching_bids[0]

    def choose_card(
        self, valid_cards: List[Card], trick_suit: Optional[Suit] = None
    ) -> Card:
        """Choose a card using epsilon-greedy strategy.

        Args:
            valid_cards: List of valid cards to choose from
            trick_suit: Current trick suit or None

        Returns:
            Selected card
        """
        if random.random() < self.epsilon:
            return random.choice(valid_cards)

        state = torch.cat([self._encode_hand(), self._encode_trick_suit(trick_suit)])

        with torch.no_grad():
            q_values = self.play_q_network(state)

        # Create valid actions mask
        valid_mask = torch.full((len(RANK_INDEX),), float("-inf"))
        for card in valid_cards:
            valid_mask[RANK_INDEX[card.rank]] = 0

        action_idx = (q_values + valid_mask).argmax().item()
        selected_rank = list(RANK_INDEX.keys())[action_idx]

        return next(card for card in valid_cards if card.rank == selected_rank)

    def update_q_network(
        self,
        state: State,
        action: Action,
        reward: Reward,
        next_state: State,
        done: bool,
        is_bidding: bool,
    ) -> None:
        """Update the appropriate Q-network using experience replay.

        Args:
            state: Current state
            action: Chosen action
            reward: Received reward
            next_state: Next state
            done: Whether episode is done
            is_bidding: Whether updating bid network or play network
        """
        network = self.bid_q_network if is_bidding else self.play_q_network
        optimizer = self.bid_optimizer if is_bidding else self.play_optimizer

        # Ensure inputs are tensors
        state = torch.as_tensor(state, dtype=torch.float32)
        next_state = torch.as_tensor(next_state, dtype=torch.float32)
        reward = torch.as_tensor(reward, dtype=torch.float32)

        # Compute current Q-value
        current_q = network(state)[action]

        # Compute target Q-value
        with torch.no_grad():
            next_q = network(next_state).max()
            target_q = reward if done else reward + QNetworkConfig.gamma * next_q

        # Update network
        loss = self.criterion(current_q, target_q)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
