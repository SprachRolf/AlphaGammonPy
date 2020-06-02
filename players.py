from abc import ABC, abstractmethod
from board_analyzer import BoardAnalyzer
from board_evaluator import *
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

        #self.allBoards = []
        #self.allValues = []
        self.allBoardsLoaded = False

    def yourTurn(self):
        super().yourTurn()

        if not self.allBoardsLoaded:
            if self.game.currentPlayer == game.Game.white:
                file = open("boards_n_values_white.p", "rb")
                self.allBoards = pickle.load(file)
                self.allValues = pickle.load(file)
            else:
                file = open("boards_n_values_red.p", "rb")
                self.allBoards = pickle.load(file)
                self.allValues = pickle.load(file)

            print("unpickled bords andn values, length:", len(self.allBoards))
            a = next(iter(self.allBoards))
            print("first board: ", a)
            #for val in self.allValues:
            #    print(val)

            self.allBoardsLoaded = True

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

            flippedTokens = BoardAnalyzer.flipBoard(list(tokens))
            try:
                knownBoardIndex = self.allBoards.index(tokens)
                print("k ",end="")
                #print("board is known: ", tokens)
                knownBoard = self.allBoards[knownBoardIndex]
                #!! update winning status
                #print("Last time's value:", self.allValues[knownBoardIndex])
                print(value, end="")
            except:
                try:
                    knownBoardIndex = self.allBoards.index(flippedTokens)
                    #print("flipped board is known: ", flippedTokens)
                    print("f ",end="")
                    knownBoard = self.allBoards[knownBoardIndex]
                    #!! update winning status
                    #print("last time's value:", self.allValues[knownBoardIndex])
                    print(value, end="")
                except:
                    self.allBoards.append(tokens)
                    self.allValues.append(value)

            self.evaluatedBoardCount += 1
            if value > highestValue:
                highestValue = value
                #print(value)
                bestMove = moveSet

        self.game.board.moveTokens(bestMove)


    def gamePlayFinished(self):
        # if I am white player:

        #print("pickling in gamePlayFinished(). Player color: ", self.game.currentPlayer)
        #print("Hit player has evaluated", self.evaluatedBoardCount, "boards.")
        if self.game.currentPlayer == game.Game.white:
            file = open("boards_n_values_white.p", "wb")
            pickle.dump(self.allBoards, file)
            pickle.dump(self.allValues, file)
        else:
            file = open("boards_n_values_red.p", "wb")
            pickle.dump(self.allBoards, file)
            pickle.dump(self.allValues, file)
            

class NetHitPlayer(Player):
    def __init__(self, color):
        random.seed(datetime.datetime.now())
        self.evaluator = HitBoardEvaluator(color)
        self.seenBoards = []

    def yourTurn(self):
        super().yourTurn()
        self.seenBoards.append(self.game.board.tokens.copy())

        moves, boards = self.analyzer.getAllLegalMoveSetsAndResultingBoards()
        #print(len(moves), "legal moves.")
        if len(moves) == 0:
            # There are no legal moves.
            # Don't move, it's the opponents turn
            return

        #print("Game state:", self.game.board.tokens, "(", self.game.whiteDice1.faceUp, "", self.game.whiteDice2.faceUp,")")
        bestMove = moves[0]
        highestWinningProbability = -sys.maxsize
        for moveSet in moves:
            # Setting board.tokens to a tuple instead of a list 
            # works only because no tokens are moved.
            tokens = boards[moveSet]
            winningProbability = self.evaluator.getBoardRating(tokens)

            if winningProbability > highestWinningProbability:
                highestWinningProbability = winningProbability
                bestMove = moveSet

        self.game.board.moveTokens(bestMove)

    def gamePlayFinished(self):
        #knownBoards = []
        #knownWhiteWins = []
        #knownRedWins = []
        
        file = open("boards_whitewins_redwins.p", "rb")
        knownBoards = pickle.load(file)
        knownWhiteWins = pickle.load(file)
        knownRedWins = pickle.load(file)
        print("unpickled bords andn values, length:", len(knownBoards))

        if self.game.whiteWon():
            winForWhite = 1
            winForRed = 0
        else:
            winForWhite = 0
            winForRed = 1

        nrKnownBoards = 0
        nrKnownFlippedBoards = 0
        nrNewBoards = 0
        for tokens in self.seenBoards:
            flippedTokens = BoardAnalyzer.flipBoard(list(tokens))

            whichBoard = -1
            try:
                whichBoard = knownBoards.index(tokens)
                #print("board", whichBoard,"is known:", knownBoards[whichBoard])
                nrKnownBoards +=1
            except ValueError:
                try:
                    whichBoard = knownBoards.index(flippedTokens)
                    # If the board is flipped, a white win becomes a red win
                    store = winForWhite
                    winForWhite = winForRed
                    winForRed = store
                    nrKnownFlippedBoards +=1
                except ValueError:
                    pass

            if whichBoard >= 0:
                whiteWins = knownWhiteWins[whichBoard] + winForWhite
                knownWhiteWins[whichBoard] = whiteWins

                redWins   = knownRedWins[whichBoard] + winForRed
                knownRedWins[whichBoard] = redWins

                #print("board known:", knownBoards[whichBoard])
                #print(whiteWins, "white wins and ", redWins, "red wins")
            else:
                nrNewBoards +=1
                knownBoards.append(tokens)
                knownWhiteWins.append(winForWhite)
                knownRedWins.append(winForRed)


        print("Boards new:", nrNewBoards,'known:',nrKnownBoards,"knownFlipped:",nrKnownFlippedBoards)
        self.seenBoards = []
        # The red player only records the game states at the beginning of his move.
        # These are different than the game states recoreded by the white player.
        # --> write both to file.
        file = open("boards_whitewins_redwins.p", "wb")
        pickle.dump(knownBoards, file)
        pickle.dump(knownWhiteWins, file)
        pickle.dump(knownRedWins, file)

class WinningProbabilityPlayer(Player):
    def __init__(self):
        random.seed(datetime.datetime.now())
        self.evaluator = WinningColorBoardEvaluator()
        self.seenBoards = []

    def yourTurn(self):
        super().yourTurn()
        self.seenBoards.append(self.game.board.tokens.copy())

        moves, boards = self.analyzer.getAllLegalMoveSetsAndResultingBoards()
        #print(len(moves), "legal moves.")
        if len(moves) == 0:
            # There are no legal moves.
            # Don't move, it's the opponents turn
            return

        #print("Game state:", self.game.board.tokens, "(", self.game.whiteDice1.faceUp, "", self.game.whiteDice2.faceUp,")")
        bestMove = moves[0]
        highestWinningProbability = -sys.maxsize
        for moveSet in moves:
            # Setting board.tokens to a tuple instead of a list 
            # works only because no tokens are moved.
            tokens = boards[moveSet]
            winningProbability = self.evaluator.getBoardRating(tokens)*self.game.currentPlayer

            if winningProbability > highestWinningProbability:
                highestWinningProbability = winningProbability
                bestMove = moveSet

        self.game.board.moveTokens(bestMove)

    def gamePlayFinished(self):
        pass
        #knownBoards = []
        #knownWhiteWins = []
        #knownRedWins = []
        
        """
        file = open("boards_whitewins_redwins.p", "rb")
        knownBoards = pickle.load(file)
        knownWhiteWins = pickle.load(file)
        knownRedWins = pickle.load(file)
        print("unpickled bords andn values, length:", len(knownBoards))

        if self.game.whiteWon():
            winForWhite = 1
            winForRed = 0
        else:
            winForWhite = 0
            winForRed = 1

        nrKnownBoards = 0
        nrKnownFlippedBoards = 0
        nrNewBoards = 0
        for tokens in self.seenBoards:
            flippedTokens = BoardAnalyzer.flipBoard(list(tokens))

            whichBoard = -1
            try:
                whichBoard = knownBoards.index(tokens)
                #print("board", whichBoard,"is known:", knownBoards[whichBoard])
                nrKnownBoards +=1
            except ValueError:
                try:
                    whichBoard = knownBoards.index(flippedTokens)
                    # If the board is flipped, a white win becomes a red win
                    store = winForWhite
                    winForWhite = winForRed
                    winForRed = store
                    nrKnownFlippedBoards +=1
                except ValueError:
                    pass

            if whichBoard >= 0:
                whiteWins = knownWhiteWins[whichBoard] + winForWhite
                knownWhiteWins[whichBoard] = whiteWins

                redWins   = knownRedWins[whichBoard] + winForRed
                knownRedWins[whichBoard] = redWins

                #print("board known:", knownBoards[whichBoard])
                #print(whiteWins, "white wins and ", redWins, "red wins")
            else:
                nrNewBoards +=1
                knownBoards.append(tokens)
                knownWhiteWins.append(winForWhite)
                knownRedWins.append(winForRed)


        print("Boards new:", nrNewBoards,'known:',nrKnownBoards,"knownFlipped:",nrKnownFlippedBoards)
        self.seenBoards = []
        # The red player only records the game states at the beginning of his move.
        # These are different than the game states recoreded by the white player.
        # --> write both to file.
        file = open("boards_whitewins_redwins.p", "wb")
        pickle.dump(knownBoards, file)
        pickle.dump(knownWhiteWins, file)
        pickle.dump(knownRedWins, file)

        """
