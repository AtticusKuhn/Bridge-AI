from src.models.game import Game
from src.agents.human_agent import HumanAgent
from src.agents.random_agent import RandomAgent


def main():
    # Create players - one human player and three random agents
    players = [
        HumanAgent("You"),
        RandomAgent("Bot 1"),
        RandomAgent("Bot 2"),
        RandomAgent("Bot 3"),
    ]

    # Create and play the game
    game = Game(players)
    game.play()


if __name__ == "__main__":
    main()
