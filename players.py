from abc import ABC, abstractmethod
from board_analyzer import BoardAnalyzer
import random
import datetime


#ABC = abstract base class
class Player(ABC):

    def __init__(self):
        #self.game = game
        # Am I the white player or the red player?
        #self.whichOne = myColor
        #self.analyzer = BoardAnalyzer(game)
        pass

    @abstractmethod
    def yourTurn(self):
        self.game.rollOwnDice();
        

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
            
        
