import unittest
#from game import Game
from game import *
from board import *
from board_analyzer import BoardAnalyzer

class BoardAnalyzerTest(unittest.TestCase):
    def testGetLowestLegalMoveSet(self):
        game = Game()
        #[-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,2, 0,0,0,0]
        game.whiteDice1.faceUp = 1
        game.whiteDice2.faceUp = 2
        # game.playerA = ArtificialDumbComputerPlayer(game, Game.whitePlayer)

        analyzer = BoardAnalyzer(game);

        #print("Board: ")
        #print( str(game.board.tokens))

        lowestMoveSet = analyzer.getLowestLegalMoveSet() 
        #print("lowest move set:" + str(lowestMoveSet))
        self.assertTrue(lowestMoveSet == ((5,4),(4,2)) or lowestMoveSet == ((5,3),(3,2)))
        
        game.board.tokens = [-2,0,0,0,0,5, 0,3,0,0,0,-5, 4,0,0,0,-3,0, -5,0,0,0,0,2, 1,0,0,0]
        lowestMoveSet = analyzer.getLowestLegalMoveSet() 
        self.assertTrue(lowestMoveSet == ((Board.whiteBarPoint,23),(5,3)) or lowestMoveSet == ((Board.whiteBarPoint,22),(5,4)))

        game.board.tokens = [-2,0,0,0,0,5, 0,3,0,0,0,-5, 3,0,0,0,-3,0, -5,0,0,0,0,2, 2,0,0,0]
        lowestMoveSet = analyzer.getLowestLegalMoveSet() 
        self.assertTrue(lowestMoveSet == ((Board.whiteBarPoint,23),(Board.whiteBarPoint,22)) or 
                        lowestMoveSet == ((Board.whiteBarPoint,22),(Board.whiteBarPoint,23)))


    def testGetAllLegalMoveSets(self):
        game = Game()
        #[-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,2, 0,0,0,0]
        game.whiteDice1.faceUp = 1
        game.whiteDice2.faceUp = 2
        # game.playerA = ArtificialDumbComputerPlayer(game, Game.whitePlayer)

        analyzer = BoardAnalyzer(game);

        allMoveSets = analyzer.getAllLegalMoveSets()
        self.assertEqual(len(allMoveSets), 15)

        game.board.tokens = [-2,0,0,0,0,5, 0,3,0,0,0,-5, 3,0,0,0,-3,0, -5,0,0,0,0,2, 2,0,0,0]
        allMoveSets = analyzer.getAllLegalMoveSets()
        self.assertEqual(len(allMoveSets), 1)

        game.board.tokens = [-2,0,0,0,0,5, 0,3,0,0,0,-5, 3,0,0,0,-3,0, -5,0,0,0,0,1, 3,0,0,0]
        game.whiteDice1.faceUp = 1
        game.whiteDice2.faceUp = 1
        allMoveSets = analyzer.getAllLegalMoveSets()
        self.assertEqual(len(allMoveSets), 3)


        game.board.tokens = [-2,0,0,0,0,5, 0,3,0,0,0,-5, 3,0,0,0,-3,0, -5,0,0,0,0,2, 2,0,0,0]
        game.whiteDice1.faceUp = 1
        game.whiteDice2.faceUp = 1
        allMoveSets = analyzer.getAllLegalMoveSets()
        self.assertEqual(len(allMoveSets), 9)

        # Test red player
        game.currentPlayer = Game.redPlayer
        #[-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,2, 0,0,0,0]
        game.redDice1.faceUp = 1
        game.redDice2.faceUp = 2
        # game.playerA = ArtificialDumbComputerPlayer(game, Game.whitePlayer)

        analyzer = BoardAnalyzer(game);

        allMoveSets = analyzer.getAllLegalMoveSets()
        self.assertEqual(len(allMoveSets), 15)

        game.board.tokens = [-2,0,0,0,0,5, 0,3,0,0,0,-5, 3,0,0,0,-3,0, -5,0,0,0,0,4, 0,0,0,-2]
        allMoveSets = analyzer.getAllLegalMoveSets()
        self.assertEqual(len(allMoveSets), 1)

        game.board.tokens = [-2,0,0,0,0,5, 0,3,0,0,0,-5, 3,0,0,0,-3,0, -5,0,0,0,0,4, 0,0,0,-3]
        game.redDice1.faceUp = 1
        game.redDice2.faceUp = 1
        allMoveSets = analyzer.getAllLegalMoveSets()
        self.assertEqual(len(allMoveSets), 3)


        game.board.tokens = [-2,0,0,0,0,5, 0,3,0,0,0,-5, 3,0,0,0,-3,0, -5,0,0,0,0,4, 0,0,0,-2]
        game.redDice1.faceUp = 1
        game.redDice2.faceUp = 1
        allMoveSets = analyzer.getAllLegalMoveSets()
        self.assertEqual(len(allMoveSets), 9)
        



