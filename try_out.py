from typing import Final
from game import Game


#https://www.bkgm.com/rules.html
meinSpiel = Game()

print(meinSpiel.board.tokens)
meinSpiel.whiteDice1.faceUp = 3
meinSpiel.whiteDice2.faceUp = 2
meinSpiel.board.moveTokens( ((5,3), (23,20)) )
print(meinSpiel.board.tokens)
