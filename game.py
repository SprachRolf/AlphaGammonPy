import random
import datetime
from typing import Final

import board
from board_analyzer import BoardAnalyzer
from players import Player
#import tkinter

class Dice:
    def __init__(self):
        self.roll()

    def roll(self):
        self.faceUp = random.randint(1, 6)

class DoublingDice:
    def __init__(self):
        self.faceUp = 1

    def double(self):
        if (self.faceUp < 64):
            self.faceUp = 2*self.faceUp
        else:
            self.faceUp = 1

class Game:
    white: Final = 1
    red: Final = -1

    def __init__(self):
        random.seed(datetime.datetime.now())
        self.board = board.Board(self)
        self.currentPlayer = Game.white
        self.redDice1 = Dice()
        self.redDice2 = Dice()
        self.whiteDice1 = Dice()
        self.whiteDice2 = Dice()
        self.doublingDice = DoublingDice()

        # A player gave up after being offered doubling the stakes (with the doubling dice)
        self.redGaveUp = False
        self.whiteGaveUp = False

    def setWhitePlayer(self, player):
        player.game = self
        player.analyzer = BoardAnalyzer(self)
        self.playerA = player

    def setRedPlayer(self, player):
        player.game = self
        player.analyzer = BoardAnalyzer(self)
        self.playerB = player


    def setup(self):
        self.board.tokens = board.Board.initialTokenSetup.copy()

    def whiteWon(self):
        return (self.board.tokens[board.Board.whiteOffPoint] == 15) or self.redGaveUp

    def redWon(self):
        return (self.board.tokens[board.Board.redOffPoint] == -15) or self.whiteGaveUp

    # Is true if one of the players has all tokens off the board
    # or if a player declined doubling the stakes
    def winnerDetermined(self):
        return self.whiteWon() or self.redWon()

    def runMatch(self):
        try:
            if (not isinstance(self.playerA, Player) or not isinstance(self.playerB, Player)):
                return 0
        except Exception:
            print(Exception.__class__)
            return 0

        # Let both players roll a dice
        # Let the player begin, who rolled the higher face

        turns = 0
        # For now white starts
        while not self.winnerDetermined():
            #self.currentPlayer = Game.white
            #self.playerA.yourTurn()
            self.currentPlayer = Game.red
            self.playerB.yourTurn()
            turns += 1
            if not self.winnerDetermined():
                #self.currentPlayer = Game.red
                #self.playerB.yourTurn()
                self.currentPlayer = Game.white
                self.playerA.yourTurn()
                turns += 1
        
        self.currentPlayer = Game.white
        self.playerA.gamePlayFinished()
        self.currentPlayer = Game.red
        self.playerB.gamePlayFinished()


        #print("both players together played", turns, "turns.")
        assert (not (self.whiteWon() and self.redWon()))
        if self.whiteWon():
            return self.white
        else:
            assert self.redWon()
            return self.red

    def rollOwnDice(self):
        if self.currentPlayer == Game.white:
            self.whiteDice1.roll()
            self.whiteDice2.roll()
        else:
            self.redDice1.roll()
            self.redDice2.roll()

    def getDiceFaces(self):
        if self.currentPlayer == Game.white:
            dice1 = self.whiteDice1
            dice2 = self.whiteDice2
        else:
            dice1 = self.redDice1
            dice2 = self.redDice2

        return (dice1.faceUp, dice2.faceUp)

    def getPips(self, faces=None):
        if faces == None:
            faces = self.getDiceFaces()
        if faces[0] == faces[1]:
            # a pip is a dice value or a point distance
            return [faces[0], faces[0], faces[0], faces[0]]
        else:
            return [faces[0], faces[1]]

