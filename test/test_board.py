import unittest
from game import Game
from board import Board


class DiceTest (unittest.TestCase):
    def testRoll(self):
        self.game = Game()
        self.assertGreater(self.game.whiteDice1.faceUp, 0)
        self.assertLess(self.game.whiteDice1.faceUp, 7)
        


class BoardTest (unittest.TestCase):

    #def setGame(self):
    #    self.game = Game()
        

    def testHasOwnTokens(self):
        self.game = Game()

        #test as white
        self.assertFalse(self.game.board.hasOwnTokensAt(0))
        self.assertFalse(self.game.board.hasOwnTokensAt(1))
        self.assertTrue (self.game.board.hasOwnTokensAt(5))

        # test as red
        self.game.currentPlayer = Game.red
        self.assertTrue (self.game.board.hasOwnTokensAt(0))
        self.assertFalse(self.game.board.hasOwnTokensAt(1))
        self.assertFalse(self.game.board.hasOwnTokensAt(5))

    def testInitialBla(self):
        self.game = Game()
        self.assertTrue(self.game.board.isInitial())
        self.game.whiteDice1.faceUp = 1
        self.assertTrue(self.game.board.isInitial())
        self.game.board.moveToken( (5,4) )
        self.assertFalse(self.game.board.isInitial())
        
        self.game = Game()
        self.game.currentPlayer = Game.red
        self.game.redDice1 = 4
        self.assertTrue(self.game.board.isInitial())
        self.game.board.moveToken( (0,4) )
        self.assertFalse(self.game.board.isInitial())

    def testOwnPoint(self):
        self.game = Game()
        board = self.game.board
        self.assertEqual(board.ownPoint(23), 23)
        self.assertEqual(board.ownPoint(0), 0)
        self.assertEqual(board.ownPoint(-2), -2)
        self.assertEqual(board.ownPoint(-1), -1)
        self.assertEqual(board.ownPoint(24), 24)
        self.assertEqual(board.ownPoint(25), 25)
        self.assertEqual(board.ownPoint(5), 5)
        self.assertEqual(board.ownPoint(16), 16)

        self.game.currentPlayer = Game.red
        self.assertEqual(board.ownPoint(23), 0)
        self.assertEqual(board.ownPoint(0), 23)

        self.assertEqual(board.ownPoint(Board.whiteBarPoint), Board.redBarPoint)
        self.assertEqual(board.ownPoint(Board.redBarPoint), Board.whiteBarPoint)

        self.assertEqual(board.ownPoint(11), 12)
        self.assertEqual(board.ownPoint(12), 11)

        self.assertEqual(board.ownPoint(5), 18)
        self.assertEqual(board.ownPoint(18), 5)





    def testmoveSetIsLegalGoodMoves(self):
        self.game = Game()
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 2
        #[-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,2,  0,0,0,0]
        self.assertTrue(self.game.board.moveSetIsLegal( ((5,4),(5,3)) ))
        self.assertTrue(self.game.board.isInitial())
        self.assertTrue(self.game.board.moveSetIsLegal( ((5,3),(5,4)) ))
        self.assertTrue(self.game.board.moveSetIsLegal( ((5,4),(7,5)) ))
        self.assertTrue(self.game.board.moveSetIsLegal( ((7,5),(7,6)) ))
        self.assertTrue(self.game.board.moveSetIsLegal( ((7,6),(7,5)) ))
        self.assertTrue(self.game.board.moveSetIsLegal( ((5,4),(4,2)) ))
        self.assertTrue(self.game.board.moveSetIsLegal( ((23,22),(5,3)) ))

        self.game.currentPlayer = Game.red
        self.game.redDice1.faceUp = 1
        self.game.redDice2.faceUp = 2
        self.assertTrue(self.game.board.moveSetIsLegal( ((0,2),(16,17)) ))

    def testmoveSetIsLegalEmptyStart(self):
        self.game = Game()
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 2
        self.assertFalse(self.game.board.moveSetIsLegal( ((4,3),(5,4)) ))
        self.assertTrue (self.game.board.moveSetIsLegal( ((23,22),(23,21)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((23,21),(22,21)) ))

        self.game.currentPlayer = Game.red
        self.game.redDice1.faceUp = 1
        self.game.redDice2.faceUp = 2
        self.assertFalse(self.game.board.moveSetIsLegal( ((4,3), (5,4)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((1,2), (0,1)) ))
        self.assertTrue (self.game.board.moveSetIsLegal( ((0,1), (1,3)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((0,1), (2,4)) ))

    def testmoveSetIsLegalNoSuchDiceValue(self):
        self.game = Game()
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 2
        #[-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,2,  0,0,0,0]):
        self.assertFalse(self.game.board.moveSetIsLegal( ((4,0),(5,4)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((5,4),(4,0)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((5,3),(5,3)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((5,4),(5,3),(5,4)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((5,4),(5,3),(5,3)) ))
        self.assertTrue (self.game.board.moveSetIsLegal( ((5,4),(5,3)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((5,4),(5,3),(5,4),(5,3)) ))

        self.game.whiteDice1.faceUp = 2
        self.game.whiteDice2.faceUp = 2
        self.assertTrue(self.game.board.moveSetIsLegal( ((5,3),(5,3),(5,3),(5,3)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((5,3),(5,3),(5,3),(5,3),(5,3)) ))

        self.game.currentPlayer = Game.red
        self.game.redDice1.faceUp = 1
        self.game.redDice2.faceUp = 2
        self.assertFalse(self.game.board.moveSetIsLegal( ((0,3),(4,5)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((4,5),(0,3)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((0,2),(0,2)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((0,1),(0,2),(11,12)) ))
        self.assertTrue (self.game.board.moveSetIsLegal( ((11,13),(13,14)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((11,12),(11,13),(11,12),(11,13)) ))

        self.game.redDice1.faceUp = 2
        self.game.redDice2.faceUp = 2
        self.assertTrue(self.game.board.moveSetIsLegal( ((11,13),(11,13),(11,13),(11,13)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((11,13),(11,13),(11,13),(11,13),(11,13)) ))

    def testmoveSetIsLegalNotBackwards(self):
        self.game = Game()
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 2
        #[-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,2,  0,0,0,0]):
        self.assertFalse(self.game.board.moveSetIsLegal( ((5,6),(5,7)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((5,4),(4,6)) ))
        self.assertTrue(self.game.board.moveSetIsLegal( ((5,4),(5,3)) ))

        self.game.currentPlayer = Game.red
        self.game.redDice1.faceUp = 1
        self.game.redDice2.faceUp = 2
        self.assertFalse(self.game.board.moveSetIsLegal( ((11,10),(11,9)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((11,10),(10,12)) ))
        self.assertTrue(self.game.board.moveSetIsLegal( ((11,13),(16,17)) ))

    def testmoveSetIsLegalIndexOut(self):
        self.game = Game()
        self.game.whiteDice1.faceUp = 4
        self.game.whiteDice2.faceUp = 6
        #[-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,2,  0,0,0,0]):
        self.assertTrue(self.game.board.moveSetIsLegal( ((5,1),(7,1)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((5,1),(1,-5)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((24,20),(7,1)) ))

        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 2
        self.assertTrue(self.game.board.moveSetIsLegal( ((23,22),(23,21)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((23,22),(24,22)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((24,23),(23,21)) ))

        # moves to barPoint are allowed only if hit by an opponent
        # The move to the bar is an extra move that costs no pips and is caused by a hit
        # A single move to the bar is initiated by the board logic, not by a human or AI player.
        self.game.board.tokens = [1,0,0,-1,0,12, -1,0,1,0,0,-13, 0,0,0,0,0,0, 0,0,0,0,0,1,  0,0,0,0]
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 6
        self.assertTrue (self.game.board.moveSetIsLegal( ((5,4),(8,2)) ))

        # Trying to move a white token onto the red bar point
        self.assertTrue(self.game.board.moveSetIsLegal( ((23,22),(22,16)) ))
        self.assertEqual(Board.redBarPoint, -1)
        self.assertFalse(self.game.board.moveSetIsLegal( ((0,Board.redBarPoint),(8,2)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((8,2), (0,Board.redBarPoint)) ))

        self.assertTrue (self.game.board.moveSetIsLegal( ((23,17),(8,7)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((5,Board.redBarPoint),(8,7)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((8,7), (5,Board.redBarPoint)) ))

        self.game = Game()
        self.game.currentPlayer = Game.red
        self.game.redDice1.faceUp = 4
        self.game.redDice2.faceUp = 6
        #[-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,2,  0,0,0,0]):
        self.assertTrue(self.game.board.moveSetIsLegal( ((18,22),(16,22)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((18,22),(22,28)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((-1,3),(16,22)) ))

        self.game.redDice1.faceUp = 1
        self.game.redDice2.faceUp = 2
        self.assertTrue(self.game.board.moveSetIsLegal( ((0,1),(0,2)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((0,1),(-1,1)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((-2,0),(0,2)) ))

        #Trying to move a red token onto white bar point
        self.game.board.tokens = [0,0,0,0,0,14, 0,0,1,0,0,-9, 0,0,0,0,0,0, 0,0,0,-2,-2,-2,  0,0,0,0]
        self.assertTrue(self.game.board.moveSetIsLegal( ((21,22),(21,23)) ))
        self.assertEqual(Board.whiteBarPoint, 24)
        self.assertFalse(self.game.board.moveSetIsLegal( ((23,24),(21,23)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((21,23),(23,24)) ))


    def testmoveSetIsLegalUseUp(self):
        self.game = Game()
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 2
        #[-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,2,  0,0,0,0]):
        self.assertFalse(self.game.board.moveSetIsLegal( ((6,5),) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((5,3),) ))

        self.game.whiteDice1.faceUp = 3
        self.game.whiteDice2.faceUp = 3
        self.assertFalse(self.game.board.moveSetIsLegal( ((5,3),(5,3),(5,3)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((5,3),(5,3),(7,4)) ))
        self.assertTrue (self.game.board.moveSetIsLegal( ((5,2),(5,2),(7,4),(7,4)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((5,3),) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((5,3),(5,3)) ))

        self.game.currentPlayer = Game.red
        self.game.redDice1.faceUp = 3
        self.game.redDice2.faceUp = 3
        self.assertFalse(self.game.board.moveSetIsLegal( ((11,14),(11,14),) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((11,14),(11,14),(11,14),) ))

    def testmoveSetIsLegalUnusablePips(self):
        self.game = Game()
        self.game.board.tokens = [0,0,0,-1,0,-14, 14,0,1,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  0,0,0,0]
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 1
        self.assertTrue (self.game.board.moveSetIsLegal( ((8,7),(7,6)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((8,7),) ))

        self.game = Game()
        self.game.board.tokens = [0,0,0,-1,0,-14, 14,0,0,1,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  0,0,0,0]
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 1
        self.assertTrue (self.game.board.moveSetIsLegal( ((9,8),(8,7),(7,6)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((9,8),(8,7)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((9,8),) ))

        # Make a pip usable
        # A pip may be unusable by one token, but may become usable by another token by moving that other token
        self.game.board.tokens = [0,0,0,-2,-2,-2, 0,0,1,1,13,0, 0,-9,0,0,0,0, 0,0,0,0,0,0,  0,0,0,0]
        self.game.whiteDice1.faceUp = 2
        self.game.whiteDice2.faceUp = 4
        # The only token that can use pip 2 AND pip 4 is on point 8.
        # If the token on point 9 is moved or one of the tokens on point 10 (using dice value 2)
        # then dice value 4 is lost. --> illegal move.
        self.assertTrue (self.game.board.moveSetIsLegal( ((8,6),(6,2)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((9,7),) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((10,8),) ))

        # Not testing red player. This could leave a bug uncovered, but probably it will be implemented all right for red

    def testmoveSetIsLegalUseUpMustUseBiggerPip(self):
        # If either pip can be used, the bigger one must be used
        self.game = Game()
        self.game.board.tokens = [0,0,0,-1,-2,-12, 14,0,1,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  0,0,0,0]
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 2
        self.assertTrue (self.game.board.moveSetIsLegal( ((8,6),) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((8,7),) ))

    def testmoveSetIsLegalDontWastePips(self):
        # A pip can be used if a token can move this pip.
        # A pip can become unusable only if the token that it could be used with was the only one
        # and if it was moved

        # A pip can become usable by moving a token to a point where it can use the pip.
        # In this case a player may not move another token.

        # Don't waste a usable pip
        self.game = Game()
        self.game.board.tokens = [0,0,0,-1,0,-14, 14,0,1,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  0,0,0,0]
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 2
        self.assertTrue (self.game.board.moveSetIsLegal( ((6,4),(4,3)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((8,6),) ))

        self.game.currentPlayer = Game.red
        self.game.redDice1.faceUp = 1
        self.game.redDice2.faceUp = 2
        self.assertTrue (self.game.board.moveSetIsLegal( ((5,7),(7,8)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((3,5),) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((3,5),(5,6)) )) # testmoveSetIsLegalClosedPoint()


        # Make a pip usable
        self.game = Game()
        self.game.board.tokens = [0,0,0,-2,-2,-2, 0,14,1,0,0,0, 0,-9,0,0,0,0, 0,0,0,0,0,0,  0,0,0,0]
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 4
        self.assertTrue (self.game.board.moveSetIsLegal( ((7,6),(6,2)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((8,7),) ))
        #self.game.whiteDice1.faceUp = 3
        #self.game.whiteDice2.faceUp = 3
        # We don't need to test doublets. 
        # If a token can move 3, the 3 cannot become unusable if another token moves
        # The 3 will be used up which is legal.

        # Not testing red player. This could leave a bug uncovered, but probably it will be implemented all right for red

    def testmoveSetIsLegalPrimeBlocked(self):
        self.game = Game()
        self.game.board.tokens = [0,0,0,0,-2,-13, 15,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  0,0,0,0]
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 2
        self.assertFalse(self.game.board.moveSetIsLegal( ((6,5),(6,4)) ))
        self.assertTrue(self.game.board.moveSetIsLegal( () ))

        self.game.currentPlayer = Game.red
        self.game.board.tokens = [0,0,0,0,0,-15, 13,2,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  0,0,0,0]
        self.game.redDice1.faceUp = 1
        self.game.redDice2.faceUp = 2
        self.assertFalse(self.game.board.moveSetIsLegal( ((5,6),(5,7)) ))
        self.assertTrue(self.game.board.moveSetIsLegal( () ))


    def testmoveSetIsLegalHit(self):
        self.game = Game()
        self.game.board.tokens = [0,0,0,-1,-1,-13, 15,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  0,0,0,0]
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 2
        self.assertEqual(self.game.board.tokens[Board.redBarPoint], 0) # no tokens are on the bar
        self.assertTrue(self.game.board.moveSetIsLegal( ((6,4),(4,3)) ))
        self.game.board.moveTokens( ((6,4),(4,3)) )
        self.assertFalse(self.game.board.hasOwnTokensAt(4))
        self.assertTrue(self.game.board.hasOwnTokensAt(3))
        self.game.currentPlayer = Game.red
        self.assertFalse(self.game.board.hasOwnTokensAt(3))
        self.assertFalse(self.game.board.hasOwnTokensAt(4))
        self.assertEqual(self.game.board.tokens[Board.redBarPoint], -2) # two red tokens are on the bar

        self.game = Game()
        self.game.board.tokens = [0,0,0,-1,-1,-13, 13,1,1,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  0,0,0,0]
        self.game.whiteDice1.faceUp = 4
        self.game.whiteDice2.faceUp = 5
        self.assertFalse(self.game.board.hasOwnTokensAt(3))
        self.assertTrue(self.game.board.hasOwnTokensAt(7))
        self.assertTrue(self.game.board.hasOwnTokensAt(8))
        self.assertTrue(self.game.board.moveSetIsLegal( ((7,3),(8,3)) ))
        self.game.board.moveTokens( ((7,3),(8,3)) )
        self.assertTrue(self.game.board.hasOwnTokensAt(3))
        self.assertFalse(self.game.board.hasOwnTokensAt(7))
        self.assertFalse(self.game.board.hasOwnTokensAt(8))
        self.assertEqual(self.game.board.tokens[Board.redBarPoint], -1)

        # hit four tokens
        self.game = Game()
        self.game.board.tokens = [0,-11,-1,-1,-1,-1, 13,1,1,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  0,0,0,0]
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 1
        self.assertFalse(self.game.board.hasOwnTokensAt(2))
        self.assertFalse(self.game.board.hasOwnTokensAt(3))
        self.assertFalse(self.game.board.hasOwnTokensAt(4))
        self.assertFalse(self.game.board.hasOwnTokensAt(5))
        self.assertTrue(self.game.board.hasOwnTokensAt(6))
        self.assertTrue(self.game.board.hasOwnTokensAt(7))
        self.assertTrue(self.game.board.hasOwnTokensAt(8))
        self.assertTrue(self.game.board.moveSetIsLegal( ((6,5),(5,4),(4,3),(3,2)) ))
        self.game.board.moveTokens( ((6,5),(5,4),(4,3),(3,2)) )
        self.assertTrue(self.game.board.hasOwnTokensAt(2))
        self.assertFalse(self.game.board.hasOwnTokensAt(3))
        self.assertFalse(self.game.board.hasOwnTokensAt(4))
        self.assertFalse(self.game.board.hasOwnTokensAt(5))
        self.assertTrue(self.game.board.hasOwnTokensAt(6))
        self.assertTrue(self.game.board.hasOwnTokensAt(7))
        self.assertTrue(self.game.board.hasOwnTokensAt(8))
        self.assertTrue(self.game.board.tokens == [0,-11,1,0,0,0, 12,1,1,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  0,0,0,-4])
        self.assertEqual(self.game.board.tokens[Board.redBarPoint], -4)

        self.game = Game()
        self.game.currentPlayer = Game.red
        self.game.board.tokens = [-1,0,0,0,-1,-13, 1,13,0,1,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  0,0,0,0]
        self.game.redDice1.faceUp = 3
        self.game.redDice2.faceUp = 6
        self.assertEqual(self.game.board.tokens[Board.whiteBarPoint], 0) # no tokens are on the bar
        self.assertTrue(self.game.board.moveSetIsLegal( ((0,6),(6,9)) ))
        self.game.board.moveTokens( ((0,6),(6,9)) )
        self.assertFalse(self.game.board.hasOwnTokensAt(0))
        self.assertTrue(self.game.board.hasOwnTokensAt(9))
        self.game.currentPlayer = Game.white
        self.assertFalse(self.game.board.hasOwnTokensAt(6))
        self.assertFalse(self.game.board.hasOwnTokensAt(9))
        self.assertTrue(self.game.board.tokens == [0,0,0,0,-1,-13, 0,13,0,-1,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  2,0,0,0])
        self.assertEqual(self.game.board.tokens[Board.whiteBarPoint], 2) # two white tokens are on the bar


        self.game.currentPlayer = Game.white
        self.game.board.tokens = [-1,0,0,0,0,-10, 1,10,0,1,0,0, 0,0,0,0,0,0, 0,0,0,0,-1,0,  3,0,0,-3]
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 2
        self.assertTrue(self.game.board.moveSetIsLegal( ((Board.whiteBarPoint,23),(Board.whiteBarPoint,22)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((Board.whiteBarPoint,23),(9,7)) ))
        self.game.whiteDice1.faceUp = 2
        self.game.whiteDice2.faceUp = 2
        self.assertTrue(self.game.board.moveSetIsLegal( 
            ((Board.whiteBarPoint,22),(Board.whiteBarPoint,22),(Board.whiteBarPoint,22),(9,7)) ))
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 2
        self.game.board.moveTokens( ((Board.whiteBarPoint,23),(Board.whiteBarPoint,22)) )
        self.assertTrue(self.game.board.tokens == [-1,0,0,0,0,-10, 1,10,0,1,0,0, 0,0,0,0,0,0, 0,0,0,0,1,1,  1,0,0,-4])


    def testmoveSetIsLegalEnter(self):
        # Tokens of both players can be on the bar at the same time

        # must enter any tokens from the bar first, before moving any other token on the board
        self.game = Game()
        self.game.board.tokens = [0,0,0,-1,-1,-13, 13,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  2,0,0,0]
        assert(self.game.board.tokens[Board.whiteBarPoint] == 2) # not a test assert. a program logic assert
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 2

        self.assertTrue(self.game.board.moveSetIsLegal( ((Board.whiteBarPoint, 23), (Board.whiteBarPoint, 22)) ))

        # One token is still on the bar, cannot do another move
        self.assertFalse(self.game.board.moveSetIsLegal( ((Board.whiteBarPoint, 23), (6, 4)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((Board.whiteBarPoint, 23), (23, 22)) ))

        # leaving two tokens on the bar is illegal
        self.assertFalse(self.game.board.moveSetIsLegal( ((6, 4), (4, 3)) ))

        self.game.board.moveTokens( ((Board.whiteBarPoint, 23), (Board.whiteBarPoint, 22)) )
        self.assertFalse(self.game.board.hasOwnTokensAt(Board.whiteBarPoint))

        self.game = Game()
        self.game.board.tokens = [0,0,0,-1,-1,-13, 13,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  1,0,0,0]
        self.game.whiteDice1.faceUp = 6
        self.game.whiteDice2.faceUp = 6
        self.assertTrue(self.game.board.moveSetIsLegal( ((Board.whiteBarPoint, 18), (18, 12), (12, 6), (6,0)) ))
        self.assertTrue(self.game.board.moveSetIsLegal( ((Board.whiteBarPoint, 18), (6, 0), (6, 0), (6,0)) ))
        self.assertTrue(self.game.board.moveSetIsLegal( ((Board.whiteBarPoint, 18), (6, 0), (18, 12), (6,0)) ))
        self.assertTrue(self.game.board.moveSetIsLegal( ((Board.whiteBarPoint, 18), (6, 0), (18, 12), (12,6)) ))

        self.assertFalse(self.game.board.moveSetIsLegal( ((6, 0), (Board.whiteBarPoint, 18), (18, 12), (12,6)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((6, 0), (6, 0), (Board.whiteBarPoint, 18), (12,6)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((6, 0), (6, 0), (6, 0), (Board.whiteBarPoint, 18))  ))

        self.game.board.moveTokens( ((Board.whiteBarPoint, 18), (18, 12), (12, 6), (6,0)) )
        self.assertFalse(self.game.board.hasOwnTokensAt(Board.whiteBarPoint))
        self.assertTrue(self.game.board.tokens == [1,0,0,-1,-1,-13, 13,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  0,0,0,0])

        self.game = Game()
        self.game.board.tokens = [0,0,0,-1,-1,-13, 8,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  5,0,0,0]
        self.game.whiteDice1.faceUp = 6
        self.game.whiteDice2.faceUp = 6
        self.assertTrue(self.game.board.moveSetIsLegal( 
            ((Board.whiteBarPoint, 18), (Board.whiteBarPoint, 18), (Board.whiteBarPoint, 18),(Board.whiteBarPoint, 18)) ))

        self.assertFalse(self.game.board.moveSetIsLegal( ((Board.whiteBarPoint, 18), (18, 12), (12, 6), (6,1)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((Board.whiteBarPoint, 18), (6, 1), (6, 1), (6,1)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((Board.whiteBarPoint, 18), (6, 1), (18, 12), (6,1)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((Board.whiteBarPoint, 18), (6, 1), (18, 12), (12,6)) ))

        self.assertFalse(self.game.board.moveSetIsLegal( ((Board.whiteBarPoint, 18), (Board.whiteBarPoint, 18), (18, 12), (6,1)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( 
            ((Board.whiteBarPoint, 18), (Board.whiteBarPoint, 18), (Board.whiteBarPoint, 18), (18, 12)) ))

        self.game.board.moveTokens( ((Board.whiteBarPoint, 18), (Board.whiteBarPoint, 18), (Board.whiteBarPoint, 18),(Board.whiteBarPoint, 18)) )
        self.assertTrue(self.game.board.hasOwnTokensAt(Board.whiteBarPoint))
        self.assertTrue(self.game.board.tokens == [0,0,0,-1,-1,-13, 8,0,0,0,0,0, 0,0,0,0,0,0, 4,0,0,0,0,0,  1,0,0,0])


        self.game = Game()
        self.game.currentPlayer = Game.red
        self.game.board.tokens = [0,1,0,-1,-1,-11, 14,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  0,0,0,-2]
        assert(self.game.board.tokens[Board.redBarPoint] == -2) # not a test assert. a program logic assert
        self.game.redDice1.faceUp = 1
        self.game.redDice2.faceUp = 2

        # No own tokens may be on the bar in order to move a non-bar token
        self.assertTrue(self.game.board.moveSetIsLegal( ((Board.redBarPoint, 0), (Board.redBarPoint, 1)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((Board.redBarPoint, 1), (1, 2)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((3, 4), (Board.redBarPoint, 1)) ))
        self.game.board.moveTokens( ((Board.redBarPoint, 0), (Board.redBarPoint, 1)) )
        self.assertFalse(self.game.board.hasOwnTokensAt(Board.redBarPoint))
        self.assertTrue(self.game.board.tokens == [-1,-1,0,-1,-1,-11, 14,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  1,0,0,0])

        # When two tokens are on the bar, both must be moved first, before any other moves
        self.game.board.tokens = [0,1,0,-1,-1,-11, 14,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  0,0,0,-2]
        self.game.redDice1.faceUp = 2
        self.game.redDice2.faceUp = 2

        self.assertTrue(self.game.board.moveSetIsLegal( ((Board.redBarPoint, 1), (Board.redBarPoint, 1), (1,3), (1,3)) ))
        self.assertTrue(self.game.board.moveSetIsLegal( ((Board.redBarPoint, 1), (Board.redBarPoint, 1), (5,7), (3,5)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((5,7), (Board.redBarPoint, 1), (Board.redBarPoint, 1), (3,5)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((Board.redBarPoint, 1), (3,5), (Board.redBarPoint, 1), (5,7)) ))

        self.game.board.tokens = [0,1,0,-1,-1,-11, 14,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  0,0,0,-4]
        self.game.redDice1.faceUp = 2
        self.game.redDice2.faceUp = 2

        self.assertTrue(self.game.board.moveSetIsLegal( 
            ((Board.redBarPoint, 1), (Board.redBarPoint, 1), (Board.redBarPoint, 1), (Board.redBarPoint, 1)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( 
            ((Board.redBarPoint, 1), (Board.redBarPoint, 1), (Board.redBarPoint, 1), (3,5)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( 
            ((Board.redBarPoint, 1), (3,5), (Board.redBarPoint, 1), (Board.redBarPoint, 1)) ))


    # When a player cannot enter tokens from the bar, no other move is legal
    def testmoveSetIsLegalEnterClosedOut(self):
        self.game = Game()
        self.game.board.tokens = [5,0,0,0,0,-9, 0,8,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,-2,  2,0,0,-4]
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 1
        self.assertTrue(self.game.board.moveSetIsLegal( () ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((7,6),(7,6),(7,6),(7,6)) ))

        self.game.currentPlayer = Game.red
        self.game.redDice1.faceUp = 1
        self.game.redDice2.faceUp = 1
        self.assertTrue(self.game.board.moveSetIsLegal( () ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((5,6),(5,6),(5,6),(5,6)) ))


    def testMayBearOff(self):
        self.game = Game()
        self.game.board.tokens = [0,5,0,0,0,10, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,-15,  0,0,0,0]
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 1
        self.assertTrue(self.game.board.mayBearOff())

        self.game.redDice1.faceUp = 1
        self.game.redDice2.faceUp = 1
        self.game.currentPlayer = Game.red
        self.assertTrue(self.game.board.mayBearOff())

        self.game.board.tokens = [1,1,1,1,1,10, 0,0,0,0,0,0, 0,0,0,0,0,0, -2,-2,-2,-2,-2,-2,  0,-3,1,0]
        self.game.currentPlayer = Game.white
        self.assertTrue(self.game.board.mayBearOff())
        self.game.currentPlayer = Game.red
        self.assertTrue(self.game.board.mayBearOff())

        self.game.board.tokens = [1,1,1,1,1,9, 1,0,0,0,0,0, 0,0,0,0,0,-1, -2,-2,-2,-2,-2,-2,  0,-2,1,0]
        self.game.currentPlayer = Game.white
        self.assertFalse(self.game.board.mayBearOff())
        self.game.currentPlayer = Game.red
        self.assertFalse(self.game.board.mayBearOff())


        self.game.board.tokens = [0,4,0,0,0,10, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0,  1,0,0,-15]
        self.game.currentPlayer = Game.white
        self.assertFalse(self.game.board.mayBearOff())
        self.game.currentPlayer = Game.red
        self.assertFalse(self.game.board.mayBearOff())

        self.game.board.tokens = [0,4,0,0,-1,10, 1,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,-14,  0,0,0,0]
        self.game.currentPlayer = Game.white
        self.assertFalse(self.game.board.mayBearOff())
        self.game.currentPlayer = Game.red
        self.assertFalse(self.game.board.mayBearOff())


    def testmoveSetIsLegalBearOff(self):
        self.game = Game()

        # Bearing off two white tokens
        self.game.board.tokens = [0,5,0,0,0,10, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,-15,  0,0,0,0]
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 1
        self.assertTrue(self.game.board.mayBearOff())
        self.assertTrue(self.game.board.moveSetIsLegal( ((1,0),(1,0),(1,0),(1,0))  ))
        self.assertTrue(self.game.board.moveSetIsLegal( ((1,0),(0,Board.whiteOffPoint),(1,0),(0,Board.whiteOffPoint))  ))
        self.assertTrue(self.game.board.moveSetIsLegal( ((1,0),(1,0),(0,Board.whiteOffPoint),(0,Board.whiteOffPoint))  ))
        self.game.board.moveTokens( ((1,0),(0,Board.whiteOffPoint),(1,0),(0,Board.whiteOffPoint)) )
        self.assertTrue(self.game.board.tokens == [0,3,0,0,0,10, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,-15,  0,0,2,0])

        self.game.board.tokens = [0,5,0,0,0,10, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,-15,  0,0,0,0]
        self.game.whiteDice1.faceUp = 3
        self.game.whiteDice2.faceUp = 2
        self.assertTrue(self.game.board.moveSetIsLegal( ((5,3),(5,2))  ))
        self.assertTrue(self.game.board.moveSetIsLegal( ((5,3),(3,0))  ))
        # Test not legal bearing off a lower token than the dice value (wasting some dice points)
        #    as long as there are higher tokens.
        self.assertFalse(self.game.board.moveSetIsLegal( ((5,3),(1,Board.whiteOffPoint))  ))
        self.assertTrue(self.game.board.moveSetIsLegal( ((1,Board.whiteOffPoint),(5,2))  ))
        self.game.board.moveTokens( ((1,Board.whiteOffPoint),(5,2))  )
        self.assertTrue(self.game.board.tokens == [0,4,1,0,0,9, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,-15,  0,0,1,0])

        # Test not legal bearing off a lower token than the dice value (wasting some dice points)
        #    as long as there are higher tokens.
        self.game.board.tokens = [0,5,0,0,0,10, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,-15,  0,0,0,0]
        self.game.whiteDice1.faceUp = 5
        self.game.whiteDice2.faceUp = 6
        self.assertTrue(self.game.board.moveSetIsLegal( ((5,0),(5,Board.whiteOffPoint))  ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((1,Board.whiteOffPoint),(1,Board.whiteOffPoint))  ))
        
        # need to test other dice values (such that a token could go to -4)
        self.game.board.tokens = [1,4,1,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,-15,  0,0,9,0]
        self.game.whiteDice1.faceUp = 5
        self.game.whiteDice2.faceUp = 6
        self.assertTrue(self.game.board.moveSetIsLegal( ((2,Board.whiteOffPoint),(1,Board.whiteOffPoint))  ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((1,Board.whiteOffPoint),(2,Board.whiteOffPoint))  ))
        self.game.board.moveTokens( ((2,Board.whiteOffPoint),(1,Board.whiteOffPoint)) )
        self.assertTrue(self.game.board.tokens == [1,3,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,-15,  0,0,11,0])


        # Test a bearing off situation with a hit
        self.game.board.tokens = [1,4,-1,0,0,1, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,-14,  0,0,9,0]
        self.game.whiteDice1.faceUp = 3
        self.game.whiteDice2.faceUp = 3
        self.assertTrue(self.game.board.moveSetIsLegal( 
            ((5,2),(2,Board.whiteOffPoint),(1,Board.whiteOffPoint),(1,Board.whiteOffPoint))  ))
        self.game.board.moveTokens( ((5,2),(2,Board.whiteOffPoint),(1,Board.whiteOffPoint),(1,Board.whiteOffPoint)) )
        self.assertTrue(self.game.board.tokens == [1,2,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,-14,  0,0,12,-1])


        ## testing bearing of for the red player

        self.game.currentPlayer = Game.red

        # Bearing off two red tokens
        self.game.board.tokens = [0,5,0,0,0,10, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,-5,-10,  0,0,0,0]
        self.game.redDice1.faceUp = 1
        self.game.redDice2.faceUp = 1
        self.assertTrue(self.game.board.mayBearOff())
        self.assertTrue(self.game.board.moveSetIsLegal( ((22,23),(22,23),(22,23),(22,23))  ))
        self.assertTrue(self.game.board.moveSetIsLegal( ((22,23),(23,Board.redOffPoint),(22,23),(23,Board.redOffPoint))  ))
        self.game.board.moveTokens( ((22,23),(23,Board.redOffPoint),(22,23),(23,Board.redOffPoint))  )
        self.assertTrue(self.game.board.tokens == [0,5,0,0,0,10, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,-3,-10,  0,-2,0,0])

        self.game.board.tokens = [0,5,0,0,0,10, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,-3,0,0,-1,-14,  0,0,0,0]
        self.game.redDice1.faceUp = 3
        self.game.redDice2.faceUp = 2
        self.assertTrue(self.game.board.moveSetIsLegal( ((19,21),(19,22))  ))
        self.assertTrue(self.game.board.moveSetIsLegal( ((22,Board.redOffPoint),(19,22))  ))
        # Test not legal bearing off a lower token than the dice value (wasting some dice points)
        #    as long as there are higher tokens.
        self.assertFalse(self.game.board.moveSetIsLegal( ((19,21),(23,Board.redOffPoint))  ))
        self.game.board.moveTokens( ((22,Board.redOffPoint),(19,22)) )
        self.assertTrue(self.game.board.tokens == [0,5,0,0,0,10, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,-2,0,0,-1,-14,  0,-1,0,0])

        # Test not legal bearing off a lower token than the dice value (wasting some dice points)
        #    as long as there are higher tokens.
        self.game.board.tokens = [0,5,0,0,0,10, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,-3,0,0,-1,-14,  0,0,0,0]
        self.game.redDice1.faceUp = 5
        self.game.redDice2.faceUp = 6
        self.assertTrue(self.game.board.moveSetIsLegal( ((19,Board.redOffPoint),(19,Board.redOffPoint))  ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((19,Board.redOffPoint),(22,Board.redOffPoint))  ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((22,Board.redOffPoint),(23,Board.redOffPoint))  ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((23,Board.redOffPoint),(23,Board.redOffPoint))  ))
        
        # need to test other dice values (such that a token could go to -4)
        self.game.board.tokens = [1,4,1,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,-1,-1,-12,  0,0,9,0]
        self.game.redDice1.faceUp = 5
        self.game.redDice2.faceUp = 6
        self.assertTrue(self.game.board.moveSetIsLegal( ((21,Board.redOffPoint),(22,Board.redOffPoint))  ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((22,Board.redOffPoint),(21,Board.redOffPoint))  ))
        self.game.board.moveTokens( ((21,Board.redOffPoint),(22,Board.redOffPoint))  )
        self.assertTrue(self.game.board.tokens == [1,4,1,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,-12,  0,-2,9,0])

        # Test a bearing off situation with a hit
        self.game.board.tokens = [1,4,0,0,0,1, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,-1,0,0,1,-14,  0,0,9,0]
        self.game.redDice1.faceUp = 3
        self.game.redDice2.faceUp = 3
        self.assertTrue(self.game.board.moveSetIsLegal( 
            ((19,22),(22,Board.redOffPoint),(23,Board.redOffPoint),(23,Board.redOffPoint)) ))
        self.game.board.moveTokens( ((19,22),(22,Board.redOffPoint),(23,Board.redOffPoint),(23,Board.redOffPoint)) )
        self.assertTrue(self.game.board.tokens == [1,4,0,0,0,1, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,-12,  1,-3,9,0])


    def testmoveSetIsLegalUsedUp(self):
        "all dice values must be used if possible"
        self.game = Game()
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 2
        self.assertFalse(self.game.board.moveSetIsLegal( ((7,5),) ))

        self.game.whiteDice1.faceUp = 3
        self.game.whiteDice2.faceUp = 3
        self.assertTrue (self.game.board.moveSetIsLegal( ((7,4),(7,4),(7,4),(5,2)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((7,4),(7,4),(7,4)) ))
        self.assertTrue (self.game.board.moveSetIsLegal( ((7,4),(12,9),(23,20),(5,2)) ))


    def testMoveSetIsLegal_bearingOffWastingPips(self):
        self.game = Game()

        # Bearing off two white tokens
        self.game.board.tokens = [0,5,0,0,10,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,-15,  0,0,0,0]
        self.game.whiteDice1.faceUp = 6
        self.game.whiteDice2.faceUp = 1
        self.assertTrue(self.game.board.mayBearOff())
        self.assertTrue(self.game.board.moveSetIsLegal( ((1,0), (4,Board.whiteOffPoint))  ))
        self.assertTrue(self.game.board.moveSetIsLegal( ((4,Board.whiteOffPoint),(1,0))  ))

        # The following moves were recognized as legal before 12.5.2020 due to a bug:
        self.assertFalse(self.game.board.moveSetIsLegal( ((4,Board.whiteOffPoint),(1,0),(1,0))  ))
        self.assertFalse(self.game.board.moveSetIsLegal( 
            ((4,Board.whiteOffPoint),(1,0),(1,0),(1,0),(1,0),(1,0), 
            (0,Board.whiteOffPoint),(0,Board.whiteOffPoint),(0,Board.whiteOffPoint),
            (0,Board.whiteOffPoint),(0,Board.whiteOffPoint))  ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((4,Board.whiteOffPoint),(100,280))  ))


    def testMoveSetIsLegal_usingUpAndMovingArbitrarily(self):
        self.game = Game()
        self.game.whiteDice1.faceUp = 1
        self.game.whiteDice2.faceUp = 2
        #[-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,2,  0,0,0,0]
        self.assertTrue(self.game.board.moveSetIsLegal( ((5,4),(5,3)) ))

        self.assertFalse(self.game.board.moveSetIsLegal( ((5,4),(5,3),(5,3)) ))
        self.assertFalse(self.game.board.moveSetIsLegal( ((5,4),(5,3),(5,3),(5,3),(5,3),(5,3),(5,3),(5,3),(5,3),(5,3),(5,3) ) ))



if __name__ == '__main__':
    unittest.main()
