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
        #self.spiel.setWhitePlayer(WinningProbabilityPlayer()) 
        #self.spiel.setRedPlayer(SelectRandomMovePlayer())
        # 90 : 13

        #self.spiel.setWhitePlayer(OnlineLearningPlayer())
        #self.spiel.setRedPlayer(OnlineLearningPlayer())
        # 528 : 472

        #self.spiel.setWhitePlayer(OnlineLearningPlayer())
        #self.spiel.setRedPlayer(NetHitPlayer(game.Game.red))
        # 6  :   93
        # 31 :  469
        # 39 :  461
        # 41 :  458
        # 37 :  463
        # 35 :  465
        # 37 :  463
        #385 : 4615
        #380 : 4620

        #self.spiel.setWhitePlayer(OnlineLearningPlayer())
        #self.spiel.setRedPlayer(OnlineLearningPlayer())
        # 243:257
        # 181:319
        # The red player plays better. There must be a bug in the training data.

        #self.spiel.setWhitePlayer(OnlineLearningPlayer())  # after 40x10.000 boards training + training on 2.6.2020
        #self.spiel.setRedPlayer(NetHitPlayer(game.Game.red))
        #  6:94
        #  6:94

        #self.spiel.setWhitePlayer(NetHitPlayer(game.Game.white))
        #self.spiel.setRedPlayer(OnlineLearningPlayer())  # after 40x10.000 boards training + training on 2.6.2020
        # 89:11

        #self.spiel.setWhitePlayer(NetHitPlayer(game.Game.white))
        #self.spiel.setRedPlayer(OnlineLearningPlayer())  # starting with 0 training, do partial_fit() for 1000-board batches and later 10.000
        #   932 :  68   # and learned trained 30x 1000 boards
        #   832 : 168   # and learned 3x 10.000 boards
        #   631 : 369   # and learned 4x 10.000 boards
        #   483 : 517   # and learned 4x 10.000 boards
        #   466 : 534   # and learned 4x 10.000 boards.
        #   524 : 475   # from other terminal window. -- unlearned something ??
        #   565 : 435
        #   512 : 488
        #   483 : 518
        # probably I should learn from another OnlineLearningPlayer, not from the NetHitPlayer that doesn't play superb.
        # Can't become better, because it learns from NetHitPlayer.

        # training against itself, starting from 0 knowledge.
        #self.spiel.setWhitePlayer(OnlineLearningPlayer())  # starting with 0 training, do partial_fit() 10.000 boards at a time.
        #self.spiel.setRedPlayer(OnlineLearningPlayer())    # starting with 0 training, do partial_fit() 10.000 boards at a time.
        # expect: always wins about half the games.
        # hope: after 6.000 gameplays it plays better than NetHitPlayer.
        # 714 : 286    # they don't know anything.
        # 772 : 228
        # (2534:1966)

        #self.spiel.setWhitePlayer(OnlineLearningPlayer("trained_net_online_2020-06-04 08:22:12.823709_white.p"))
        #self.spiel.setRedPlayer(NetHitPlayer(game.Game.red))
        # 25:75
        # 27:73
        # 25:75

        #self.spiel.setWhitePlayer(NetHitPlayer(game.Game.white))
        #self.spiel.setRedPlayer(OnlineLearningPlayer("trained_net_online_2020-06-04 08:22:09.209022_red.p"))
        # 68:32
        # 71:29
        # 66:34  # red is definitly stronger.

        # Simple net, no hidden layers.
        #self.spiel.currentPlayer = game.Game.white
        #self.spiel.setWhitePlayer(OnlineLearningPlayer(self.spiel))
        #self.spiel.currentPlayer = game.Game.red
        #self.spiel.setRedPlayer(OnlineLearningPlayer(self.spiel))
        #
        # After 29 trainings with 10.000 boards: run again:
        # 175:25
        # 176:24
        # 170:30

        #self.spiel.currentPlayer = game.Game.white
        #self.spiel.setWhitePlayer(OnlineLearningPlayer(self.spiel))
        #self.spiel.currentPlayer = game.Game.red
        #self.spiel.setRedPlayer(NetHitPlayer(self.spiel))
        # Super simple net (no hidden layer, activation "logistic")after 29 trainings with 10.000 boards
        # 1:39
        # 25:175

        #self.spiel.currentPlayer = game.Game.white
        #self.spiel.setWhitePlayer(NetHitPlayer(self.spiel))
        #self.spiel.currentPlayer = game.Game.red
        #self.spiel.setRedPlayer(OnlineLearningPlayer(self.spiel))
        # Super simple net (no hidden layer, activation "logistic")after 29 trainings with 10.000 boards
        # 184:16

        #self.spiel.currentPlayer = game.Game.white
        #self.spiel.setWhitePlayer(SelectRandomMovePlayer(self.spiel))
        #self.spiel.currentPlayer = game.Game.red
        #self.spiel.setRedPlayer(OnlineLearningPlayer(self.spiel))
        # 109:91 -- whoa my net doesn't do anything useful!

        #self.spiel.currentPlayer = game.Game.white
        #self.spiel.setWhitePlayer(OnlineLearningPlayer(self.spiel))
        #self.spiel.currentPlayer = game.Game.red
        #self.spiel.setRedPlayer(SelectRandomMovePlayer(self.spiel))
        # 181:19 -- oh, the white player did learn.

        #self.spiel.currentPlayer = game.Game.white
        #self.spiel.setWhitePlayer(OnlineLearningPlayer(self.spiel))
        #self.spiel.currentPlayer = game.Game.red
        #self.spiel.setRedPlayer(OnlineLearningPlayer(self.spiel))

        #self.spiel.currentPlayer = game.Game.white
        #self.spiel.setWhitePlayer(NetHitPlayer(self.spiel))
        #self.spiel.currentPlayer = game.Game.red
        #self.spiel.setRedPlayer(OnlineLearningPlayer(self.spiel))
        # training (56,2)relu 69 trainings, each > 10.000 boards
        # 138:62


        self.spiel.currentPlayer = game.Game.white
        #self.spiel.setWhitePlayer(OnlineLearningPlayer(self.spiel))
        self.spiel.setWhitePlayer(OnlineLearningPlayer(self.spiel, "trained_net_2020606_13uhr_training_data"))
        self.spiel.currentPlayer = game.Game.red
        self.spiel.setRedPlayer(NetHitPlayer(self.spiel))


    def letTheGamesBegin(self):
        aWins = 0
        bWins = 0
        passedRounds = 0
        rounds = 50
        print("Ladies and Gentlemen, ", self.spiel.playerA.__class__," is playing against ", self.spiel.playerB.__class__,".",sep="")
        for i in range(rounds):
            self.spiel.setup()
            winner = self.spiel.runMatch()
            if winner == game.Game.white:
                aWins = aWins +1
            else:
                bWins = bWins +1

            passedRounds = passedRounds +1
            if passedRounds == 10:
                print("Round", i+1,"of",rounds," rounds:")
                print("Score white: ", aWins,", red: ", bWins, sep="")
                passedRounds = 0
            


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