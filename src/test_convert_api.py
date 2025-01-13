from models.game import Game
from agents.human_agent import HumanAgent
from agents.random_agent import RandomAgent
from agents.heuristic_agent import HeuristicAgent
from models.game import Game
from models.card import Suit
from convert_api import game_to_deal
from endplay.types import Deal
from endplay.dds import calc_dd_table, ddtable
from collections import defaultdict
from hand_analysis import get_suitable_score


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
    game._deal_cards()
    deal = game_to_deal(game)
    
    print(deal.__str__())
    deal.pprint()
    
    print(get_suitable_score(game))

if __name__ == "__main__":
    main()