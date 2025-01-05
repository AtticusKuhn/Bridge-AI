"""Bridge trainer module for reinforcement learning agents."""

from typing import List, Optional
from dataclasses import dataclass, field
import numpy as np
import torch
import matplotlib.pyplot as plt
from models.game import Game
from agents.rl_agent import RLAgent
from agents.random_agent import RandomAgent


@dataclass
class TrainingMetrics:
    """Container for training metrics."""

    scores: List[float] = field(default_factory=list)
    tricks: List[int] = field(default_factory=list)
    def update(self, score: float, tricks: int) -> None:
        """Update metrics with new values."""
        self.scores.append(score)
        self.tricks.append(tricks)

    def get_recent_averages(self, window: int = 100) -> tuple[float, float]:
        """Calculate average metrics over recent episodes."""
        recent_scores = self.scores[-window:]
        recent_tricks = self.tricks[-window:]
        return np.mean(recent_scores), np.mean(recent_tricks)


class BridgeTrainer:
    """Trainer class for Bridge reinforcement learning agents."""

    # Class constants
    MADE_CONTRACT_MULTIPLIER = 10.0
    FAILED_CONTRACT_MULTIPLIER = -5.0
    DECLARER_TRICK_REWARD = 1.0
    DEFENDER_TRICK_REWARD = 0.5
    INITIAL_BID_ENCODING_SIZE = 35
    PROGRESS_UPDATE_FREQUENCY = 100
    NUM_PLAYERS = 4

    def __init__(self, num_episodes: int = 1000):
        """Initialize the Bridge trainer.

        Args:
            num_episodes: Number of training episodes to run.
        """
        self.num_episodes = num_episodes
        self.rl_agent = RLAgent("RL Player")
        self.opponents = [
            RandomAgent(f"Random {i+1}") for i in range(self.NUM_PLAYERS - 1)
        ]
        self.metrics = TrainingMetrics()

    def _get_reward_for_bid(self, contract_level: int, made_contract: bool) -> float:
        """Calculate reward for bidding phase.

        Args:
            contract_level: Level of the contract (1-7).
            made_contract: Whether the contract was fulfilled.

        Returns:
            float: Calculated reward value.
        """
        multiplier = (
            self.MADE_CONTRACT_MULTIPLIER
            if made_contract
            else self.FAILED_CONTRACT_MULTIPLIER
        )
        return contract_level * multiplier

    def _get_reward_for_trick(self, won_trick: bool, is_declarer: bool) -> float:
        """Calculate reward for each trick.

        Args:
            won_trick: Whether the trick was won.
            is_declarer: Whether the player is the declarer.

        Returns:
            float: Calculated reward value.
        """
        if not won_trick:
            return 0.0
        return self.DECLARER_TRICK_REWARD if is_declarer else self.DEFENDER_TRICK_REWARD

    def _setup_game(self, episode: int) -> tuple[Game, torch.Tensor]:
        """Set up a new game episode.

        Args:
            episode: Current episode number.

        Returns:
            tuple: Game instance and initial state tensor.
        """
        position = episode % self.NUM_PLAYERS
        players = self.opponents.copy()
        players.insert(position, self.rl_agent)

        game = Game(players)
        initial_state = torch.cat(
            [self.rl_agent._encode_hand(), torch.zeros(self.INITIAL_BID_ENCODING_SIZE)]
        )

        return game, initial_state

    def _process_bidding_rewards(
        self, game: Game, players: List[RandomAgent], initial_state: torch.Tensor
    ) -> None:
        """Process rewards for the bidding phase.

        Args:
            game: Current game instance.
            players: List of players in the game.
            initial_state: Initial state tensor for Q-network update.
        """
        if not game.contract or game.declarer != self.rl_agent:
            return

        partner_index = (players.index(self.rl_agent) + 2) % self.NUM_PLAYERS
        declarer_team_tricks = (
            game.declarer.tricks_won + players[partner_index].tricks_won
        )
        tricks_needed = 6 + game.contract.number
        made_contract = declarer_team_tricks >= tricks_needed

        bid_reward = self._get_reward_for_bid(game.contract.number, made_contract)

        final_state = torch.cat(
            [self.rl_agent._encode_hand(), torch.zeros(self.INITIAL_BID_ENCODING_SIZE)]
        )

        action = game.contract.number * 5 + game.contract.suit.index
        self.rl_agent.update_q_network(
            initial_state, action, bid_reward, final_state, True, is_bidding=True
        )

    def train(self) -> None:
        """Train the RL agent through self-play against random agents."""
        print(f"Starting training for {self.num_episodes} episodes...")

        for episode in range(self.num_episodes):
            game, initial_state = self._setup_game(episode)
            game.play()

            self._process_bidding_rewards(game, game.players, initial_state)

            # Update metrics
            self.metrics.update(game.score[self.rl_agent], self.rl_agent.tricks_won)

            # Print progress
            if (episode + 1) % self.PROGRESS_UPDATE_FREQUENCY == 0:
                avg_score, avg_tricks = self.metrics.get_recent_averages()
                print(f"Episode {episode + 1}")
                print(f"Average Score (last 100): {avg_score:.2f}")
                print(f"Average Tricks (last 100): {avg_tricks:.2f}")

        self._plot_training_results()

    def _plot_training_results(self) -> None:
        """Plot and save training metrics."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        # Plot scores
        ax1.plot(self.metrics.scores)
        ax1.set_title("Training Scores")
        ax1.set_xlabel("Episode")
        ax1.set_ylabel("Score")

        # Plot tricks
        ax2.plot(self.metrics.tricks)
        ax2.set_title("Tricks Won")
        ax2.set_xlabel("Episode")
        ax2.set_ylabel("Number of Tricks")

        plt.tight_layout()
        plt.savefig("training_results.png")
        plt.close()


def main() -> None:
    """Main entry point for training."""
    trainer = BridgeTrainer(num_episodes=1000)
    trainer.train()


if __name__ == "__main__":
    main()
