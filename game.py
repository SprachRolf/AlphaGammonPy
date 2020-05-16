import random
from typing import Final
#from players import Player, ArtificialDumbComputerPlayer
import board

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
    whitePlayer: Final = 1
    redPlayer: Final = -1

    def __init__(self):
        self.board = board.Board(self)
        self.currentPlayer = Game.whitePlayer
        self.redDice1 = Dice()
        self.redDice2 = Dice()
        self.whiteDice1 = Dice()
        self.whiteDice2 = Dice()
        self.doublingDice = DoublingDice()

    def rollOwnDice(self):
        if self.currentPlayer == Game.whitePlayer:
            self.whiteDice1.roll()
            self.whiteDice2.roll()
        else:
            self.redDice1.roll()
            self.redDice2.roll()

    def getDiceFaces(self):
        if self.currentPlayer == Game.whitePlayer:
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

    #def getPips(self, faces):
        #return self.getPips(self.getDiceFaces())
