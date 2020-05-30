from abc import ABC, abstractmethod
from board_analyzer import BoardAnalyzer
import game
import sys
import random
import datetime
import pickle


#ABC = abstract base class
class Player(ABC):

    def __init__(self):
        #self.game = game
        # Am I the white player or the red player?
        #self.whichOne = myColor
        #self.analyzer = BoardAnalyzer(game)

        #Player.game and Player.analyzer are set in Game.setWhitePlayer() and Game.setRedPlayer()
        pass

    @abstractmethod
    def yourTurn(self):
        self.game.rollOwnDice();


    def gamePlayFinished(self):
        pass
        

class MoveFrontTokensPlayer(Player): 
    def __init__(self):
        super().__init__()
        random.seed(datetime.datetime.now())

    def yourTurn(self):
        super().yourTurn()
        self.game.board.moveTokens(self.analyzer.getLowestLegalMoveSet())

class MoveRearTokensPlayer(Player): 
    def __init__(self):
        super().__init__()
        random.seed(datetime.datetime.now())

    def yourTurn(self):
        super().yourTurn()
        self.game.board.moveTokens(self.analyzer.getHighestLegalMoveSet())

class SelectRandomMovePlayer(Player): 
    def __init__(self):
        super().__init__()

    def yourTurn(self):
        super().yourTurn()

        moveSets = self.analyzer.getAllLegalMoveSets();
        move = ()
        if len(moveSets) > 0:
            move = moveSets[random.randint(0, len(moveSets) -1)]
        self.game.board.moveTokens(move)
        
class HitPlayer(Player):
    def __init__(self):
        self.evaluatedBoardCount = 0
        self.previewGame = game.Game()
        self.previewAnalyzer = BoardAnalyzer(self.previewGame)

        self.allBoards = []
        self.allValues = []
        #self.allBoardsNvalues = pickle.load(open("boards_n_values.p", "rb"))
        #print("unpickled bords n values, length:")
        #print(len(self.allBoardsNvalues))
        #a = next(iter(self.allBoardsNvalues))
        #print("first board: ", a)
        # for a in self.allBoardsNvalues:
        #     print(a[1])

    def yourTurn(self):
        super().yourTurn()
        self.previewGame.currentPlayer = self.game.currentPlayer

        moves, boards = self.analyzer.getAllLegalMoveSetsAndResultingBoards()
        if len(moves) == 0:
            # There are no legal moves.
            # Don't move, it's the opponents turn
            return

        bestMove = moves[0]
        highestValue = -sys.maxsize
        #print("-sys.maxsize:", highestValue)
        for moveSet in moves:
            # Setting board.tokens to a tuple instead of a list 
            # works only because no tokens are moved.
            tokens = boards[moveSet]
            self.previewGame.board.tokens = tokens
            foeStepsToGo = self.previewAnalyzer.getFoeStepsToGo()
            threadSum = self.previewAnalyzer.getThreadSum()
            value = foeStepsToGo - threadSum
            self.allBoards.append(tokens)
            self.allValues.append(value)

            self.evaluatedBoardCount += 1
            if value > highestValue:
                highestValue = value
                #print(value)
                bestMove = moveSet

        self.game.board.moveTokens(bestMove)


    def gamePlayFinished(self):
        print("pickling in gamePlayFinished()")
        print("Hit player has evaluated", self.evaluatedBoardCount)
        file = open("boards_n_values.p", "wb")
        pickle.dump(self.allBoards, file)
        pickle.dump(self.allValues, file)