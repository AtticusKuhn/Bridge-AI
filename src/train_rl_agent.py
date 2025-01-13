"""Bridge trainer module for reinforcement learning agents."""

from typing import List, Optional
from dataclasses import dataclass, field
import numpy as np
import torch
import matplotlib.pyplot as plt
from models.game import Game
from agents.rl_agent import RLAgent
from agents.random_agent import RandomAgent
from agents.pass_agent import PassAgent

@dataclass
class TrainingMetrics:
    """Container for training metrics."""

    scores: List[float] = field(default_factory=list)
    tricks: List[int] = field(default_factory=list)
    contracts_declared: List[bool] = field(default_factory=list)  # True when agent is declarer
    contract_levels: List[int] = field(default_factory=list)  # Bid level when agent is declarer
    contracts_made: List[bool] = field(default_factory=list)  # Success when agent is declarer
    
    def update(self, score: float, tricks: int, is_declarer: bool = False, 
               contract_level: Optional[int] = None, made_contract: Optional[bool] = None) -> None:
        """Update metrics with new values."""
        self.scores.append(score)
        self.tricks.append(tricks)
        self.contracts_declared.append(is_declarer)
        if is_declarer and contract_level is not None:
            self.contract_levels.append(contract_level)
            self.contracts_made.append(made_contract)

    def get_recent_averages(self, window: int = 100) -> tuple[float, float, float, float, float]:
        """Calculate average metrics over recent episodes."""
        recent_scores = self.scores[-window:]
        recent_tricks = self.tricks[-window:]
        recent_declarations = self.contracts_declared[-window:]
        
        # Calculate declaration rate
        declaration_rate = sum(recent_declarations) / len(recent_declarations)
        
        # Calculate contract success rate and average level
        if any(recent_declarations):
            recent_successes = [made for made, is_decl in zip(self.contracts_made[-window:], recent_declarations) if is_decl]
            recent_levels = [level for level, is_decl in zip(self.contract_levels[-window:], recent_declarations) if is_decl]
            success_rate = sum(recent_successes) / len(recent_successes) if recent_successes else 0
            avg_level = sum(recent_levels) / len(recent_levels) if recent_levels else 0
        else:
            success_rate = 0
            avg_level = 0
            
        return (np.mean(recent_scores), np.mean(recent_tricks), 
                declaration_rate, success_rate, avg_level)


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
            PassAgent(f"Random {i+1}") for i in range(self.NUM_PLAYERS - 1)
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
    ) -> tuple[bool, Optional[int], Optional[bool]]:
        """Process rewards for the bidding phase.

        Args:
            game: Current game instance.
            players: List of players in the game.
            initial_state: Initial state tensor for Q-network update.

        Returns:
            tuple: (is_declarer, contract_level, made_contract) for metrics tracking
        """
        is_declarer = bool(game.contract and game.declarer == self.rl_agent)
        contract_level = None
        made_contract = None

        if is_declarer:
            partner_index = (players.index(self.rl_agent) + 2) % self.NUM_PLAYERS
            declarer_team_tricks = (
                game.declarer.tricks_won + players[partner_index].tricks_won
            )
            tricks_needed = 6 + game.contract.number
            made_contract = declarer_team_tricks >= tricks_needed
            contract_level = game.contract.number

            bid_reward = self._get_reward_for_bid(contract_level, made_contract)

            final_state = torch.cat(
                [self.rl_agent._encode_hand(), torch.zeros(self.INITIAL_BID_ENCODING_SIZE)]
            )

            action = (contract_level - 1) * 5 + game.contract.suit.index
            self.rl_agent.update_q_network(
                initial_state, action, bid_reward, final_state, True, is_bidding=True
            )

        return is_declarer, contract_level, made_contract

    def train(self) -> None:
        """Train the RL agent through self-play against random agents."""
        print(f"Starting training for {self.num_episodes} episodes...")

        for episode in range(self.num_episodes):
            game, initial_state = self._setup_game(episode)
            game.play()

            is_declarer, contract_level, made_contract = self._process_bidding_rewards(
                game, game.players, initial_state
            )

            # Update metrics
            self.metrics.update(
                game.score[self.rl_agent], 
                self.rl_agent.tricks_won,
                is_declarer,
                contract_level,
                made_contract
            )

            # Print progress
            if (episode + 1) % self.PROGRESS_UPDATE_FREQUENCY == 0:
                avg_score, avg_tricks, decl_rate, success_rate, avg_level = self.metrics.get_recent_averages()
                print(f"Episode {episode + 1}")
                print(f"Average Score (last 100): {avg_score:.2f}")
                print(f"Average Tricks (last 100): {avg_tricks:.2f}")
                print(f"Declaration Rate: {decl_rate:.2%}")
                print(f"Contract Success Rate: {success_rate:.2%}")
                print(f"Average Contract Level: {avg_level:.2f}")

        self._plot_training_results()

    def _plot_training_results(self) -> None:
        """Plot and save training metrics with rolling averages."""
        window = 100  # Window size for rolling average
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
        episodes = range(len(self.metrics.scores))
        
        # Helper function for rolling average
        def rolling_average(data, window_size):
            return np.convolve(data, np.ones(window_size)/window_size, mode='valid')
        
        # Plot scores
        raw_scores = np.array(self.metrics.scores)
        rolling_scores = rolling_average(raw_scores, window)
        ax1.plot(episodes, raw_scores, alpha=0.3, label='Raw Scores', color='blue')
        ax1.plot(episodes[window-1:], rolling_scores, label=f'{window}-Episode Average', color='blue', linewidth=2)
        ax1.set_title("Training Scores")
        ax1.set_xlabel("Episode")
        ax1.set_ylabel("Score")
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Plot tricks
        raw_tricks = np.array(self.metrics.tricks)
        rolling_tricks = rolling_average(raw_tricks, window)
        ax2.plot(episodes, raw_tricks, alpha=0.3, label='Raw Tricks', color='green')
        ax2.plot(episodes[window-1:], rolling_tricks, label=f'{window}-Episode Average', color='green', linewidth=2)
        ax2.set_title("Tricks Won")
        ax2.set_xlabel("Episode")
        ax2.set_ylabel("Number of Tricks")
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        # Plot declaration rate and contract success rate
        decl_episodes = [i for i, is_decl in enumerate(self.metrics.contracts_declared) if is_decl]
        if decl_episodes:  # Only plot if there are declarations
            success_data = [1 if made else 0 for made in self.metrics.contracts_made]
            rolling_success = rolling_average(success_data, min(window, len(success_data)))
            ax3.plot(decl_episodes[window-1:], rolling_success, label='Success Rate', color='purple', linewidth=2)
            
            # Plot average contract level when declaring
            level_data = self.metrics.contract_levels
            rolling_levels = rolling_average(level_data, min(window, len(level_data)))
            ax3.plot(decl_episodes[window-1:], rolling_levels, label='Avg Contract Level', color='orange', linewidth=2)
            
        ax3.set_title("Contract Performance (When Declaring)")
        ax3.set_xlabel("Episode")
        ax3.set_ylabel("Rate / Level")
        ax3.grid(True, alpha=0.3)
        ax3.legend()

        # Plot declaration rate
        decl_data = [1 if decl else 0 for decl in self.metrics.contracts_declared]
        rolling_decl = rolling_average(decl_data, window)
        ax4.plot(episodes[window-1:], rolling_decl, label='Declaration Rate', color='red', linewidth=2)
        ax4.set_title("Declaration Rate")
        ax4.set_xlabel("Episode")
        ax4.set_ylabel("Rate")
        ax4.grid(True, alpha=0.3)
        ax4.legend()

        plt.tight_layout()
        plt.savefig("training_results.png", bbox_inches='tight')
        plt.close()


def main() -> None:
    """Main entry point for training."""
    trainer = BridgeTrainer(num_episodes=10_000)
    trainer.train()


if __name__ == "__main__":
    main()
