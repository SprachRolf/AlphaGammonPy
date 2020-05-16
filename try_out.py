from typing import Final
from players import Player, ArtificialDumbComputerPlayer
from game import Game


#https://www.bkgm.com/rules.html
doofesSpiel = Game()
flasf = ArtificialDumbComputerPlayer(doofesSpiel, Game.whitePlayer)

#"""
print(doofesSpiel.board.tokens)
doofesSpiel.whiteDice1.faceUp = 3
doofesSpiel.whiteDice2.faceUp = 2
doofesSpiel.board.moveTokens( ((5,3), (23,20)) )
print(doofesSpiel.board.tokens)
#"""