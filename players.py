from abc import ABC, abstractmethod


#ABC = abstract base class
class Player(ABC):

    def __init__(self, game, myColor):
        self.game = game
        # Am I the white player or the red player?
        self.whichOne = myColor

    @abstractmethod
    def yourTurn(self):
        self.game.rollOwnDice();
        


class ArtificialDumbComputerPlayer(Player): 
    def __init__(self,game,myColor):
        super().__init__(game,myColor)

    def yourTurn(self):
        pass
