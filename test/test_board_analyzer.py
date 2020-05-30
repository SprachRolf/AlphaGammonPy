import unittest
import random

from game import *
from board import *
from board_analyzer import BoardAnalyzer


number_of_tested_boards = 100

# flipBoard() is used to check the generation of allLegalMoves() -- I suspect for red there are some missing.
# Change the white tokens to red (and red to white) and move to the respective position
# and the red tokens become white and move to the corresponding white point.
def flipBoard(liste):
    assert( (len(liste) % 2) == 0)
    halfLength = (int) (len(liste)/2)
    for i in range(halfLength):
        a = liste[i-2]
        b = liste[23-(i-2)]
        liste[i-2] = -b
        liste[23-(i-2)] = -a

# Transform point coordinates from white <-> to red (or back)
def translateMoveSet(set):
    moveSet = list(set)
    assert(False)

# Randomly distribute <tokenNr> tokens on the board
# Assume that there are 15 - tokenNr red and white tokens already placed
def sprinkleTokens(board, whiteTokenNr=15, redTokenNr=15, fromPoint=1, toPoint=24):
    whiteTokensOnBoard = 15 - whiteTokenNr
    redTokensOnBoard = 15 - redTokenNr

    for i in range(whiteTokenNr):
        point = random.randint(fromPoint-1,toPoint-1)
        if board[point] >=0:
            # dropping a white token
            board[point] = board[point] +1 
            whiteTokensOnBoard += 1
        
    for i in range(redTokenNr):
        whitePoint = random.randint(fromPoint-1,toPoint-1)
        point = 23-whitePoint
        if board[point] <=0:
            # dropping a red token
            board[point] = board[point] -1
            redTokensOnBoard += 1

    # There are at most 15 points with red tokens.
    # Put the remaining white tokens on the first point found, that has no red tokens
    if whiteTokensOnBoard < 15:
        i = fromPoint-1
        while (i < toPoint) and (whiteTokensOnBoard <15):
            if board[i] >= 0:
                board[i] += (15-whiteTokensOnBoard)
                whiteTokensOnBoard = 15
            i += 1

    if redTokensOnBoard < 15:
        i = fromPoint-1
        while (i < toPoint) and (redTokensOnBoard <15):
            if board[i] <= 0:
                board[i] -= (15-redTokensOnBoard)
                redTokensOnBoard = 15
            i += 1
    return board

    assert(whiteTokensOnBoard == 15)
    assert(redTokensOnBoard == 15)


# distribute 15 white and 15 red tokens on points 1..24
def randomPopulatedBoard():
    board = [0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0]
    #board = [0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0].copy()
    sprinkleTokens(board)
    return board

# distribute 15 white and 15 red tokens on points 1..24 + at least one red and white token on the bar
def randomPopulatedBoardBar():
    board = [0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 1,0,0,-1]
    sprinkleTokens(board,14, 14)
    return board

def randomPopulatedBoardManyBar():
    whiteTokensOnBar = random.randint(0,15)
    redTokensOnBar = random.randint(0,15)
    board = [0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, whiteTokensOnBar,0,0,-redTokensOnBar]
    sprinkleTokens(board, 15 - whiteTokensOnBar, 15 - redTokensOnBar)
    #board = [3, 2, -4, -1, -3, 0, 2, 1, 0, 0, 0, 1, 1, -1, 1, -1, 0, 1, -2, -1, 1, -1, -1, 1, 1, 0, 0, 0]
    return board

# distribute 15 white tokens on points 1..6, and 15 red tokens on points 19..24.
def randomPopulatedBoardBearingOff():
    board = [0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0]
    sprinkleTokens(board, 15, 15, 1, 6)
    return board


class BoardAnalyzerTest(unittest.TestCase):
    def testGetLowestLegalMoveSet(self):
        game = Game()
        #[-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,2, 0,0,0,0]
        game.whiteDice1.faceUp = 1
        game.whiteDice2.faceUp = 2

        analyzer = BoardAnalyzer(game);

        lowestMoveSet = analyzer.getLowestLegalMoveSet() 
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
        game.currentPlayer = Game.red
        #[-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,2, 0,0,0,0]
        game.redDice1.faceUp = 1
        game.redDice2.faceUp = 2

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

    def humanReadablyPrintMoves(self, game, allAMoveSets, allBMoveSets):
        #if game.whiteDice1.faceUp == game.whiteDice2.faceUp:
            print("Dice: (", game.whiteDice1.faceUp, ",", game.whiteDice2.faceUp, ")",sep="")
            print(game.board.tokens)
            print("White moves: ")
            for move in allAMoveSets:
                print(move)
            print("Red moves (translated to white coordinates): ")
            for move in allBMoveSets:
                print(move)

    def translateMoveSetsToWhiteCoordinates(self, moveSet):
        whiteMoveSets = []
        for move in moveSet:
            whiteMove = []
            for step in move:
                fromP, toP = step
                whiteMove.append( (23 - fromP, 23 - toP) )
            whiteMoveSets.append( tuple(whiteMove) )
        return tuple(whiteMoveSets)

    # "all leal moves" must be the same set for red and for white
    # If the white tokens are replaced by red ones (and vice versa) and the positions of the tokens flipped 
    # (because red is moving in the opposite direction of white).
    def checkMovesForRandomBoard(self, game, randomBoardInitializerFunction, analyzer):
        game.currentPlayer = Game.white
        game.rollOwnDice()

        a = randomBoardInitializerFunction()
        game.board.tokens = a
        allAMoveSets = analyzer.getAllLegalMoveSets();

        game.currentPlayer = Game.red
        game.redDice1.faceUp = game.whiteDice1.faceUp
        game.redDice2.faceUp = game.whiteDice2.faceUp
        b = a.copy()
        flipBoard(b)
        game.board.tokens = b
        allBMoveSets = self.translateMoveSetsToWhiteCoordinates(analyzer.getAllLegalMoveSets());

        game.board.tokens = a # display the original.
        #self.humanReadablyPrintMoves(game, allAMoveSets, allBMoveSets)
        self.assertEqual(len(allAMoveSets), len(allBMoveSets))
        self.assertEqual(allAMoveSets, allBMoveSets)


    def testGetAllLegalMoveSets_isSameForWhiteAndForRed(self):
        game = Game()
        a = [-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,2, 0,0,0,0]
        game.whiteDice1.faceUp = 1
        game.whiteDice2.faceUp = 2

        analyzer = BoardAnalyzer(game);

        aFlip = a.copy()
        flipBoard(aFlip)
        #print(a)
        #print(aFlip)
        self.assertEqual(aFlip, a)
        flipBoard(aFlip)
        self.assertEqual(a, aFlip)
        # The inital board is s symmetric. 
        # Here I don't need the flip() function

        # The initial board is symmetric.
        # red and white should have symmetric moves
        allAMoveSets = analyzer.getAllLegalMoveSets();
        game.currentPlayer = game.red
        game.redDice1.faceUp = game.whiteDice1.faceUp
        game.redDice2.faceUp = game.whiteDice2.faceUp
        
        allBMoveSets = analyzer.getAllLegalMoveSets();
        allBWhiteMoveSets = self.translateMoveSetsToWhiteCoordinates(allBMoveSets)

        #self.humanReadablyPrintMoves(game, allAMoveSets, allBWhiteMoveSets)

        self.assertTrue( ((5,4),(4,2)) in allAMoveSets)
        self.assertTrue( ( ((7,6),(6,4)) in allAMoveSets) or ( ((7,5),(5,4)) in allAMoveSets)  or ( ((5,4),(7,5)) in allAMoveSets) )
        
        self.assertEqual(len(allAMoveSets), len(allBMoveSets))
        self.assertEqual(allAMoveSets, allBWhiteMoveSets)

        a = randomPopulatedBoard()
        b = randomPopulatedBoard()
        #print(a)
        #print(b)
        # The assignment of a list as default parameter gives the same object.
        # The assignment of a list within a method creates a new object every time. Wow!
        self.assertNotEqual(a,b)

        a = randomPopulatedBoard()
        b = a.copy()
        flipBoard(b)
        self.assertNotEqual(a,b) # a random board will most likely not be symmetric
        flipBoard(b)
        self.assertEqual(a,b) # flipping back yields the original

# def testGetAllLegalMoveSetsManually(self):
#     game = Game()
#     analyzer = BoardAnalyzer(game);

        # game.board.tokens = [2, -1, 2, 0, 1, 2, 0, -1, 0, -2, -1, -1, 1, 0, 1, -2, 0, 0, -1, 0, -2, -1, -1, 3, 3, 0, 0, -2]
        # game.whiteDice1.faceUp, game.whiteDice2.faceUp = (3,3)
        # self.humanReadablyPrintMoves(game, analyzer.getAllLegalMoveSets(), (),)

        # game.board.tokens = [3, 1, -1, 2, 0, 0, 0, 2, -1, 1, 2, 0, 0, -1, 0, 0, -1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, -11]
        # game.whiteDice1.faceUp, game.whiteDice2.faceUp = (5,1)
        # self.humanReadablyPrintMoves(game, analyzer.getAllLegalMoveSets(), (),)

        # game.board.tokens = [0, 0, 0, 0, 0, 0, -3, -1, -1, -1, 0, 0, -1, 0, 0, -1, 0, 0, 0, -3, 0, 0, 0, -3, 15, 0, 0, -1]
        # game.whiteDice1.faceUp, game.whiteDice2.faceUp = (5,3)
        # self.humanReadablyPrintMoves(game, analyzer.getAllLegalMoveSets(), (),)

        # This resultet in "no legal moves for white".
        # It should move 4 white tokens off the bar.
        # Dice: (5,5)
        # [0, -1, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, -2, -1, -1, 0, 0, 0, 1, 14, 0, 0, -7]
            # print("should move 4 off bar:")
            # game.board.tokens = [0, -1, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, -2, -1, -1, 0, 0, 0, 1, 14, 0, 0, -7]
            # game.whiteDice1.faceUp, game.whiteDice2.faceUp = (5,5)
            # self.humanReadablyPrintMoves(game, analyzer.getAllLegalMoveSets(), (),)
        # --> there is a bug with double-dice in getAllLegalMoves().
        # fixed :-)


        # This moves out with 2 white bar tokens.
        # should only be able to move with one.
        #Dice: (1,4)
        #[1, 0, 0, 1, -2, -2, 1, 1, 1, -1, 1, 0, 0, 2, 1, 0, 0, 0, -1, 1, 3, -1, -1, -2, 2, 0, 0, -5]
        #White moves: 
        #((24, 23), (24, 20))
            # print("should move only one token off bar:")
            # game.board.tokens = [1, 0, 0, 1, -2, -2, 1, 1, 1, -1, 1, 0, 0, 2, 1, 0, 0, 0, -1, 1, 3, -1, -1, -2, 2, 0, 0, -5]
            # game.whiteDice1.faceUp, game.whiteDice2.faceUp = (1,4)
            # self.humanReadablyPrintMoves(game, analyzer.getAllLegalMoveSets(), (),)
        # --> correct. --> there is a bug in test_board_analyzer.py 
        # in checkMovesForRandomBoard() or in the flipping logic, or some variable overwrites another.

        #self.assertFalse(True)

    def testGetAllLegalMoveSets_randomBoards(self):

        game = Game()
        analyzer = BoardAnalyzer(game);

        #print("Testing all possible moves for random boards.")
        nrTestsPassed = 0
        for i in range(number_of_tested_boards):
            self.checkMovesForRandomBoard(game, randomPopulatedBoard, analyzer)
            nrTestsPassed += 1
            if nrTestsPassed == 50:
                nrTestsPassed = 0
                #print(i+1,"tests have passed.")

        #print("Testing all possible moves with at least 1 white and 1 red token on the bar.")
        nrTestsPassed = 0
        for i in range(number_of_tested_boards *20):
            self.checkMovesForRandomBoard(game, randomPopulatedBoardBar, analyzer)
            nrTestsPassed += 1
            if nrTestsPassed == 50:
                nrTestsPassed = 0
                #print(i+1,"tests have passed.")

        #print("Testing all possible moves with 0..15 white tokens on the bar and 0..15 red tokens.")
        nrTestsPassed = 0
        for i in range(number_of_tested_boards *20):
            self.checkMovesForRandomBoard(game, randomPopulatedBoardManyBar, analyzer)
            nrTestsPassed += 1
            if nrTestsPassed == 50:
                nrTestsPassed = 0
                #print(i+1,"tests have passed.")

        #print("Testing all possible moves when all tokens are in the home area.")
        nrTestsPassed = 0
        for i in range(number_of_tested_boards *10):
            self.checkMovesForRandomBoard(game, randomPopulatedBoardBearingOff, analyzer)
            nrTestsPassed += 1
            if nrTestsPassed == 50:
                nrTestsPassed = 0
                #print(i+1,"tests have passed.")


    def testGetStepsToGo(self):
        game = Game()
        analyzer = BoardAnalyzer(game);
        #[-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,2,  0,0,0,0]

        self.assertEqual(analyzer.getStepsToGo(), 5*6 + 3*8 + 5*13 + 2*24)
        game.currentPlayer = Game.red
        self.assertEqual(analyzer.getStepsToGo(), 5*6 + 3*8 + 5*13 + 2*24)

        game.board.tokens = [-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,1,  0,0,1,0]
        game.currentPlayer = Game.white
        self.assertEqual(analyzer.getStepsToGo(), 5*6 + 3*8 + 5*13 + 1*24)
        game.currentPlayer = Game.red
        self.assertEqual(analyzer.getStepsToGo(), 5*6 + 3*8 + 5*13 + 2*24)


    def testThreadSum(self):
        game = Game()
        analyzer = BoardAnalyzer(game);

        game.board.tokens = [-15,1,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,14,0]
        # -(1/6)*(1/6) because (1,1) will only hit the token once.
        self.assertAlmostEqual(analyzer.getThreadSum(), (2*(1/6) -(1/6)*(1/6) )*23)

        game.board.tokens = [-1,0,0,1,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,-14,14,0]
        # hits from (1,1), (1,2), (3,*), (2,1), (*,3)
        # --> 14*(1/36) on position 21 (oh, I mean position 4, loss 21)
        self.assertAlmostEqual(analyzer.getThreadSum(), (14*(1/36))*21)

        game.board.tokens = [0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,-1,0,1, 0,-14,14,0]
        # hits from (1,1), (2,*), (*,2)
        # --> 12*(1/36) on position 1
        self.assertAlmostEqual(analyzer.getThreadSum(), (12*(1/36))*1)
        game.board.tokens = [0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,-2,0,1, 0,-13,14,0]
        self.assertAlmostEqual(analyzer.getThreadSum(), (12*(1/36))*1)

        game.board.tokens = [-1,0,0,1,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,-1,0,1, 0,-13,13,0]
        # hits from (1,1), (1,2), (3,*), (2,1), (*,3) and from (1,1), (2,*), (*,2)
        # --> 14*(1/36) on position 21 + 12*(1/36) on position 1
        # + interference: 0
        # The risk at the low position (point 1) for (1,1), (1,2) and (2,1) is neglectible 
        # because there is a higher risk for these dice values losing token on point 21
        # Should be: 
        # self.assertAlmostEqual(analyzer.getThreadSum(), 14*(1/36)*21 + 9*(1/36)*1 )
        self.assertAlmostEqual(analyzer.getThreadSum(), 14*(1/36)*21 + 12*(1/36)*1 )

        game.board.tokens = [-1,0,0,1,0,0, 0,0,0,0,0,0, 0,0,0,0,-1,0, 1,0,0,0,0,0, 0,-13,13,0]
        # hits from (1,1), (1,2), (3,*), (2,1), (*,3) and from (1,1), (2,*), (*,2)
        # --> 14*(1/36) on position 21 + 12*(1/36) on position 6
        # + interference: (6,6) at position 6
        self.assertAlmostEqual(analyzer.getThreadSum(), 14*(1/36)*21 + (12+1)*(1/36)*6 )

        game.board.tokens = [-1,0,0,0,0,0, 0,0,1,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,-14,14,0]
        # hits from (2,2), (4,4), (6,2), (2,6), (3,5), (5,3)
        # --> (1/36) on position 16
        self.assertAlmostEqual(analyzer.getThreadSum(), 6*(1/36)*16)

        game.board.tokens = [0,0,-1,0,0,0, 0,0,1,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,-14,14,0]
        # hits from (2,2), (6,*), (*,6), (1,5), (5,1), (2,4). (4,2), (3,3)
        # --> (1/36) on position 16
        self.assertAlmostEqual(analyzer.getThreadSum(), 17*(1/36)*16)

        game.board.tokens = [0,0,0,0,-1,0, 0,0,1,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,-14,14,0]
        # hits from (1,1) (2,2), (4,*), (*,4), (1,3), (3,1)
        # --> (1/36) on position 16
        self.assertAlmostEqual(analyzer.getThreadSum(), 15*(1/36)*16)

        game.board.tokens = [-1,0,0,0,0,1, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,-14,14,0]
        # hits from (1,4), (4,1), (2,3), (3,2) (5,*), (*,5)
        # --> 15*(1/36) on position 19
        self.assertAlmostEqual(analyzer.getThreadSum(), (15*(1/36))*19)

        # test with blocked paths
        game.board.tokens = [-1,0,2,2,0,1, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,-14,12,0]
        # hits from (1,4), (4,1), (5,*), (*,5), but not from (2,3) and (3,2)
        # --> 13*(1/36) on position 19
        self.assertAlmostEqual(analyzer.getThreadSum(), (13*(1/36))*19)



        # Test for red player:
        game.currentPlayer = Game.red

        game.board.tokens = [-1,15,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,-14,0,0]
        # -(1/6)*(1/6) because (1,1) will only hit the token once.
        # Hits from (1,*), (*,1): 11*(1/36)
        self.assertAlmostEqual(analyzer.getThreadSum(), (2*(1/6) -(1/6)*(1/6) )*1)

        game.board.tokens = [-1,0,0,1,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,-14,14,0]
        # hits from (1,1), (1,2), (3,*), (2,1), (*,3)
        # --> 14*(1/36) on position 1
        self.assertAlmostEqual(analyzer.getThreadSum(), (14*(1/36))*1)

        game.board.tokens = [0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,-1,0,1, 0,-14,14,0]
        # hits from (1,1), (2,*), (*,2)
        # --> 12*(1/36) on position 22
        self.assertAlmostEqual(analyzer.getThreadSum(), (12*(1/36))*22)
        game.board.tokens = [0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,-2,0,1, 0,-13,14,0]
        self.assertAlmostEqual(analyzer.getThreadSum(), 0)

        game.board.tokens = [-1,0,0,1,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,-1,0,1, 0,-13,13,0]
        # hits from (1,1), (1,2), (3,*), (2,1), (*,3) and from (1,1), (2,*), (*,2)
        # --> 14*(1/36) on position 24, loss 1 + 12*(1/36) on position 3, loss 22
        # + interference: 0
        self.assertAlmostEqual(analyzer.getThreadSum(), 14*(1/36)*1 + 12*(1/36)*22)

        game.board.tokens = [-1,0,0,1,0,0, 0,0,0,0,0,0, 0,0,0,0,-1,0, 1,0,0,0,0,0, 0,-13,13,0]
        # hits from (1,1), (1,2), (3,*), (2,1), (*,3) and from (1,1), (2,*), (*,2)
        # --> 14*(1/36) on position 24, loss 1 + 12*(1/36) on position 8, loss 17
        # + interference: (6,6) at position 24, loss 1
        self.assertAlmostEqual(analyzer.getThreadSum(), (14+1)*(1/36)*1 + (12)*(1/36)*17 )

        game.board.tokens = [-1,0,0,0,0,0, 0,0,1,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,-14,14,0]
        # hits from (2,2), (4,4), (6,2), (2,6), (3,5), (5,3)
        # --> (1/36) on position 24, loss 1
        self.assertAlmostEqual(analyzer.getThreadSum(), 6*(1/36)*1)

        game.board.tokens = [0,0,-1,0,0,0, 0,0,1,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,-14,14,0]
        # hits from (2,2), (6,*), (*,6), (1,5), (5,1), (2,4). (4,2), (3,3)
        # --> (1/36) on position 22, loss 3
        self.assertAlmostEqual(analyzer.getThreadSum(), 17*(1/36)*3)

        game.board.tokens = [0,0,0,0,-1,0, 0,0,1,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,-14,14,0]
        # hits from (1,1) (2,2), (4,*), (*,4), (1,3), (3,1)
        # --> (1/36) on position 20, loss 5
        self.assertAlmostEqual(analyzer.getThreadSum(), 15*(1/36)*5)

        game.board.tokens = [-1,0,0,0,0,1, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,-14,14,0]
        # hits from (1,4), (4,1), (2,3), (3,2) (5,*), (*,5)
        # --> 15*(1/36) on position 24, loss 1
        self.assertAlmostEqual(analyzer.getThreadSum(), (15*(1/36))*1)

        # test with blocked paths
        game.board.tokens = [-1,0,-2,-2,0,1, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0,0, 0,-14,10,0]
        # hits from (1,4), (4,1), (5,*), (*,5), but not from (2,3) and (3,2)
        # --> 13*(1/36) on position 24, loss 1
        self.assertAlmostEqual(analyzer.getThreadSum(), (13*(1/36))*1)


