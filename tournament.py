import game
from players import *
#from board_analyzer import *


# Set up an arena and let two players compete a 100 games, 
# show who wins how often
class Tournament:
    def __init__(self):
        self.spiel = game.Game()

        #self.spiel.setWhitePlayer(MoveRearTokensPlayer())
        #self.spiel.setRedPlayer(SelectRandomMovePlayer())

        #self.spiel.setWhitePlayer(SelectRandomMovePlayer())
        #self.spiel.setRedPlayer(MoveRearTokensPlayer())

        #self.spiel.setWhitePlayer(SelectRandomMovePlayer())
        #self.spiel.setRedPlayer(SelectRandomMovePlayer())
        # white starts.
        #white 119, red 81: 60%
        # 105 vs 95: 10%
        # 93 vs 107: -20%
        # 1097 vs 903: 20%
        # 1061 vs 939: 13%
        # 1062 vs 938
        # 1071 vs 929
        #
        # total: 4608	3992
        #   53,58% weiß gewinnt,  46,41 rot gewinnt; 7% Unterschied
        #
        # --> Weiß beginnt, weiß gewinnt

        # Rot beginnt,
        # white vs red:
        #
        # 325 vs 324
        # 9865 vs 10135
        # white: 4012, red: 3887
        # 4705 vs 4870
        #
        # If Red does not have 7% more wins, there is a bug in implementation
        # 4705 vs 4870, red is 1.7% better. There is a 5% bug somewhere, I guess.
        # Red has 10% more wins --> this is the starting advantage!
        #
        #


        #self.spiel.setWhitePlayer(SelectRandomMovePlayer())
        #self.spiel.setRedPlayer(HitPlayer())
        # RandomPlayer vs Hitplayer
        # 1 : 19
        # 0 : 20
        # 2 : 47 -- Hit player isn't that good!
        # 4 :196
        # 5 :195

        #self.spiel.setWhitePlayer(NetHitPlayer()) # trained on trained_4mb_net.p
        #self.spiel.setRedPlayer(SelectRandomMovePlayer())
        # net vs random
        #    55 : 44
        # ca 180:110

        #self.spiel.setWhitePlayer(HitPlayer())
        #self.spiel.setRedPlayer(HitPlayer())

        #self.spiel.setWhitePlayer(NetHitPlayer()) # trained on trained_35mb_net.p
        #self.spiel.setRedPlayer(HitPlayer())
        # net vs hit
        # 21 : 178
        #

        #self.spiel.setWhitePlayer(NetHitPlayer()) # trained on trained_880mb_net.p
        #self.spiel.setRedPlayer(HitPlayer())
        # net vs hit
        # (19 : 180)
        # 46 : 353

        #self.spiel.setWhitePlayer(NetHitPlayer()) # trained on trained_880mb_net.p
        #self.spiel.setRedPlayer(SelectRandomMovePlayer())
        # net vs random
        # (188 : 11)
        # 468 : 31

        #self.spiel.setWhitePlayer(NetHitPlayer()) # trained on trained_35mb_net.p
        #self.spiel.setRedPlayer(SelectRandomMovePlayer())
        # net vs random
        # almost same as the 880mb net --> the hidden layers may be too few.
        # 464 : 35

        #self.spiel.setWhitePlayer(NetHitPlayer(game.Game.white)) # trained with 100 runs
        #self.spiel.setRedPlayer(HitPlayer())
        # net vs hit: 5:94

        
        #self.spiel.setWhitePlayer(NetHitPlayer(game.Game.white))
        #self.spiel.setRedPlayer(NetHitPlayer(game.Game.red))
        # 40:60
        # 46:54

        #self.spiel.setWhitePlayer(NetHitPlayer(game.Game.white)) # hidden layers: 10 and 4 neurons
        #self.spiel.setRedPlayer(HitPlayer())
        # 20: 80

        #self.spiel.setRedPlayer(NetHitPlayer(game.Game.red)) # hidden layers: 10 and 4 neurons
        #self.spiel.setWhitePlayer(HitPlayer())
        # 75:25
        # Das rote neuronale Netz ist ein bisschen besser trainiert!
        #
        # 82:18
        # Oder auch nicht.

        #self.spiel.setWhitePlayer(NetHitPlayer(game.Game.white)) # hidden layers: 10 and 4 neurons
        #self.spiel.setRedPlayer(NetHitPlayer(game.Game.red)) # hidden layers: 10 and 4 neurons
        # white vs red
        # 765:1235

        #self.spiel.setWhitePlayer(WinningProbabilityPlayer()) #still with a linear output neuron
        #self.spiel.setRedPlayer(SelectRandomMovePlayer())
        # 7  :  3
        # 81 : 18

        #self.spiel.setWhitePlayer(SelectRandomMovePlayer())
        #self.spiel.setRedPlayer(WinningProbabilityPlayer()) # playing as red player, still with a linear output neuron
        # 1  :  9
        # 1  :  9
        # 12 : 87

        #self.spiel.setWhitePlayer(SelectRandomMovePlayer())
        #self.spiel.setRedPlayer(WinningProbabilityPlayer()) # playing as red player, logistic output, 305000 training boards.
        # 7  : 92
        self.spiel.setWhitePlayer(WinningProbabilityPlayer()) # playing as red player, logistic output, 305000 training boards.
        self.spiel.setRedPlayer(SelectRandomMovePlayer())
        # 90 : 13

        #self.spiel.setWhitePlayer(OnlineLearningPlayer()) # playing as red player, logistic output, 305000 training boards.
        #self.spiel.setRedPlayer(OnlineLearningPlayer())



    def letTheGamesBegin(self):
        aWins = 0
        bWins = 0
        passedRounds = 0
        rounds = 100
        print("Ladies and Gentlemen, ", self.spiel.playerA.__class__," is playing against ", self.spiel.playerB.__class__,".",sep="")
        for i in range(rounds):
            self.spiel.setup()
            winner = self.spiel.runMatch()
            passedRounds = passedRounds +1
            if passedRounds == 10:
                print("Round", i+1,"of",rounds," rounds:")
                print("Score white: ", aWins,", red: ", bWins, sep="")
                passedRounds = 0
            if winner == game.Game.white:
                aWins = aWins +1
            else:
                bWins = bWins +1
            


        print("Player A (", self.spiel.playerA.__class__,") won ", aWins," times.", sep="")
        print("Player B (", self.spiel.playerB.__class__,") won ", bWins," times.", sep="")
        if aWins == bWins:
            print("Draw!")
        elif aWins > bWins:
            print("A wins.")
        else:
            print("B wins.")
        

tourn = Tournament()
tourn.letTheGamesBegin()