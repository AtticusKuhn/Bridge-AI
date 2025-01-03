from models.game import Game
from agents.human_agent import HumanAgent
from agents.random_agent import RandomAgent
from agents.heuristic_agent import HeuristicAgent


def main():
    # Create players - one human player and three random agents
    players = [
        HumanAgent("You"),
        RandomAgent("Bot 1"),
        HeuristicAgent("Heuristic 2"),
        RandomAgent("Bot 3"),
    ]

    # Create and play the game
    game = Game(players)
    game.play()


if __name__ == "__main__":
    main()
