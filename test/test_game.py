import unittest
from game import Game
from board import Board

class GameTest (unittest.TestCase):
    
  
    def testWhiteWon(self):
        game = Game()
        game.board.tokens = [0,0,0,0,0,0,  0,0,0,0,0,0,  0,0,0,0,0,0, 0,0,0,0,-15,15,  0,0,0,0]
        self.assertFalse(game.whiteWon())
        self.assertFalse(game.redWon())

        game.redGaveUp = True
        self.assertTrue(game.whiteWon())
        self.assertFalse(game.redWon())

        game.redGaveUp = False
        game.whiteGaveUp = True
        self.assertFalse(game.whiteWon())
        self.assertTrue(game.redWon())

        game.whiteGaveUp = False
        self.assertFalse(game.whiteWon())
        self.assertFalse(game.redWon())

        game.board.tokens = [0,0,0,0,0,0,  0,0,0,0,0,0,  0,0,0,0,0,0, 0,0,0,0,-15,0,  0,0,15,0]
        self.assertTrue(game.whiteWon())
        self.assertFalse(game.redWon())

        game.board.tokens = [0,0,0,0,0,0,  0,0,0,0,0,0,  0,0,0,0,0,0, 0,0,0,0,15,0,  0,-15,0,0]
        self.assertFalse(game.whiteWon())
        self.assertTrue(game.redWon())


        
 