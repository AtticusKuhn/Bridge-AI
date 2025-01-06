from models.game import Game
from models.card import Rank

"""
Analyse the theoretical contract based on Suit length and HCP

The only goal is to enter Game/Slam/Grand Slam contracts
"""
def analyse_contract(game: Game):
    cnt = [0 for _ in range(4)]
    for i, player in enumerate(game.players):
        for card in player.hand:
            if card.rank == Rank.ACE:
                cnt[i] += 4
            elif card.rank == Rank.KING:
                cnt[i] += 3
            elif card.rank == Rank.QUEEN:
                cnt[i] += 2
            elif card.rank == Rank.JACK:
                cnt[i] += 1
                
            # Potential extension to adjust HCP based on suit length
            pass
    
    if cnt[0] + cnt[2] >= 37:
        print(game.players[0].name, "and", game.players[2].name, "should enter grand slam contract.")
    elif cnt[0] + cnt[2] >= 25:
        print(game.players[0].name, "and", game.players[2].name, "should enter slam contract.")
    elif cnt[0] + cnt[2] >= 20:
        print(game.players[0].name, "and", game.players[2].name, "should enter partial contract.")
    if cnt[1] + cnt[3] >= 37:
        print(game.players[1].name, "and", game.players[3].name, "should enter grand slam contract.")
    elif cnt[1] + cnt[3] >= 25:
        print(game.players[1].name, "and", game.players[3].name, "should enter slam contract.")
    elif cnt[1] + cnt[3] >= 20:
        print(game.players[1].name, "and", game.players[3].name, "should enter partial contract.")
        