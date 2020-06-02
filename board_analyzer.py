#from game import Game

import board as bo


class BoardAnalyzer:

    # flipBoard() is used to check the generation of allLegalMoves() -- I suspect for red there are some missing.
    # Change the white tokens to red (and red to white) and move to the respective position
    # and the red tokens become white and move to the corresponding white point.
    @staticmethod
    def flipBoard(liste):
        assert( (len(liste) % 2) == 0)
        flippedBoard = liste.copy()

        halfLength = (int) (len(flippedBoard)/2)
        for i in range(halfLength):
            a = flippedBoard[i-2]
            b = flippedBoard[23-(i-2)]
            flippedBoard[i-2] = -b
            flippedBoard[23-(i-2)] = -a
        return flippedBoard


    def __init__(self, game):
        self.game = game

    def getMoveEndings(self, board, unusedPips):
        moves = []
        if len(unusedPips) == 0:
            return moves

        for i in range(24):
            fromPoint = board.ownPoint(i)
            whiteToPoint = i-unusedPips[0]
            if whiteToPoint < 0:
                whiteToPoint = bo.Board.whiteOffPoint
            toPoint = board.ownPoint(whiteToPoint)
            if (board.hasOwnTokensAt(fromPoint) and board.pointIsOpen(toPoint)):
                step = (fromPoint,toPoint)
                stepBoard = board.copy()
                stepBoard.moveToken(step)
                stepUnusedPips = unusedPips.copy()
                del stepUnusedPips[0]
                endings = self.getMoveEndings(stepBoard, stepUnusedPips)
                if (len(endings) == 0):
                    moves.append([step])
                for end in endings:
                    end.insert(0,step)
                    moves.append(end)
        return moves

    def getAllLegalMoveSets(self):
        moves, boards = self.getAllLegalMoveSetsAndResultingBoards()
        return moves

    def getAllLegalMoveSetsAndResultingBoards(self):
        moveSet = []
        board = self.game.board
        face1, face2 = self.game.getDiceFaces()

        # We need to add all possible combinations of token moves.
        # A token needs to move once with pip1 first, and then with pip 2 first.
        # It may be necessary to move with pip2 first in order to make pip 1 possible.
        # And one way an opponent token may be hit on the way.

        # After getting all possible combinations, we throw out equivalent ones.
        # Moving pip1 first and then pip2 with a token is equivalent if no opponent tokens
        # where hit on the way. If on both way midpoints an opponent token was hit, the resulting board is different.
        # If an opponent was hit on the endpoint (pip1 + pip2), moving pip1 first or pip2 is equivalent.
        # --> I compare the boards (put them into a set if they are not in there yet)

        # If dice faces differ:
        #    create all combinations of pip 1 first and then pip 2
        #       move off the bar first
        #    also consider moving the same token both pips.
        #    create all compinations with pip 2 first and then pip 1
        #       move off the bar first
        #    also consider moving the same token both pips.
        #    include permutations with bearing off
        #
        # If dice faces are same
        #       create all combinations of tokens moving up to 4 times pip 1
        #           move off the bar first
        #       also bear off if possible

        if (face1 != face2):
            for twice in range(2):
                steps = []
                # Move one token (if possible from the bar)
                if board.hasOwnTokensAt(board.ownBarPoint()):
                    stepBoard = board.copy()
                    if stepBoard.pointIsOpen(stepBoard.ownPoint(24-face1)):
                        step = (stepBoard.ownBarPoint(), stepBoard.ownPoint(24-face1))
                        steps.append(step)
                        stepBoard.moveToken(step)
                    # else:
                        # No move possible with face 1 first.
                    # use the second face to move another token (if possible from the bar)
                    if stepBoard.hasOwnTokensAt(stepBoard.ownBarPoint()):
                        if stepBoard.pointIsOpen(stepBoard.ownPoint(24-face2)):
                            step = (stepBoard.ownBarPoint(), stepBoard.ownPoint(24-face2))
                            steps.append(step)
                    else:
                        foundSecondStep = False
                        for k in range(24):
                            fromPoint = stepBoard.ownPoint(k)
                            whiteToPoint = k-face2
                            if whiteToPoint < 0:
                                whiteToPoint = bo.Board.whiteOffPoint
                            toPoint = stepBoard.ownPoint(whiteToPoint)
                            if (stepBoard.hasOwnTokensAt(fromPoint) and stepBoard.pointIsOpen(toPoint)):
                                foundSecondStep = True
                                step = (fromPoint,toPoint)
                                stepSteps = steps.copy()
                                stepSteps.append(step)
                                moveSet.append(tuple(stepSteps))
                        if not foundSecondStep:
                            moveSet.append(tuple(steps))

                    if (len(steps) > 0):
                        moveSet.append(tuple(steps))
        
                else:
                    # Move any combination of tokens that are not on the bar
                    for i in range(24):
                        fromPoint = board.ownPoint(i)
                        whiteToPoint = i-face1
                        if whiteToPoint < 0:
                            whiteToPoint = bo.Board.whiteOffPoint
                        toPoint = board.ownPoint(whiteToPoint)
                        if (board.hasOwnTokensAt(fromPoint) and board.pointIsOpen(toPoint)):
                            stepBoard = board.copy()
                            step = (fromPoint,toPoint)
                            steps = [step]
                            stepBoard.moveToken(step)
                            foundSecondStep = False
                            for k in range(24):
                                fromPoint = stepBoard.ownPoint(k)
                                whiteToPoint = k-face2
                                if whiteToPoint < 0:
                                    whiteToPoint = bo.Board.whiteOffPoint
                                toPoint = board.ownPoint(whiteToPoint)
                                if (stepBoard.hasOwnTokensAt(fromPoint) and stepBoard.pointIsOpen(toPoint)):
                                    foundSecondStep = True
                                    step = (fromPoint,toPoint)
                                    stepSteps = steps.copy()
                                    stepSteps.append(step)
                                    moveSet.append(tuple(stepSteps))
                            if not foundSecondStep:
                                moveSet.append(tuple(steps))
                # Now moveSet contains all possible combinations of two tokens moving first pip 1 and then pip 2

                # Repeat, now moving step2 first, then step1
                temp = face1
                face1 = face2
                face2 = temp

        else:    
            # Both dice faces show the same number, We can move 4 tokens
            unusedPips = self.game.getPips((face1, face2))
            assert(unusedPips == [face1,face1,face1,face1])
            
            steps = []
            stepBoard = board.copy()
            # Move up to 4 tokens off the bar
            fromPoint = stepBoard.ownBarPoint()
            toPoint = stepBoard.ownPoint(24 - unusedPips[0])
            while (stepBoard.hasOwnTokensAt(stepBoard.ownBarPoint()) and (len(unusedPips) > 0) and stepBoard.pointIsOpen(toPoint)):
                step = (fromPoint, toPoint)
                del unusedPips[0]
                steps.append(step)
                stepBoard.moveToken(step)

            # The tokens on the bar couldn't move 
            # or there are no tokens on the bar any more
            # or the pips are used up.

            # If I have 4 pips left I would need 4 levels of loops with 
            # 4 local stepBoards to keep track and 4 local stepSteps.
            # This is error prone.

            # Recursively I would do one partial move and order 
            # "give me all possible combinations to use up the remaining 3 pips",
            # which returns me a list of move-endings.
            endings = self.getMoveEndings(stepBoard, unusedPips)

            if len(endings) > 0:
                # Glue the steps I used to get off the board to each move ending and I have all possible moves.
                for end in endings:
                    moveSet.append(tuple(steps + end))
            else:
                moveSet.append(tuple(steps))

        # Remove illegal moves (moves where pip values are wasted)
        # Remove equivalent moves (where the resulting boards are identical)
        boards = dict()
        finalMoveSet = []
        
        for move in moveSet:
            if board.moveSetIsLegal(move):
                stepBoard = board.copy()
                stepBoard.moveTokens(move)
                tupleBoard = tuple(stepBoard.tokens)
                if not tupleBoard in boards.values():
                    boards[move] = tupleBoard
                    finalMoveSet.append(move)

        return (tuple(finalMoveSet), boards)

    # Return a move set, moving the tokens closest to bearing out.
    # A move is lower than another, when tokens on a lower position have been moved.
    # A move is lower than another, when tokens from a lower position have been moved farther.
    def getLowestLegalMoveSet(self):
        sets = self.getAllLegalMoveSets()
        if len(sets) > 0:
            return sets[0]
        return  ()

    def getHighestLegalMoveSet(self):
        sets = self.getAllLegalMoveSets()
        if len(sets) > 0:
            return sets[len(sets)-1]
        return  ()

    # sum up the positions of all tokens
    def getStepsToGo(self):
        tokens = self.game.board.tokens
        stepsLeft = 0
        if self.game.currentPlayer == self.game.white:
            for i in range(0,25):
                if (tokens[i] > 0):
                    # Just count white tokens
                    stepsLeft += tokens[i]*(i+1)
        else:
            for i in range(-1,24):
                if (tokens[i] < 0):
                    stepsLeft += -tokens[i]*(24-i)

        return stepsLeft

    # sum up the positions of all tokens
    def getFoeStepsToGo(self):
        tokens = self.game.board.tokens
        stepsLeft = 0
        if self.game.currentPlayer == self.game.red:
            for i in range(0,25):
                if (tokens[i] > 0):
                    # Just count white tokens
                    stepsLeft += tokens[i]*(i+1)
        else:
            for i in range(-1,24):
                if (tokens[i] < 0):
                    stepsLeft += -tokens[i]*(24-i)

        #print("Foe Steps to go:", stepsLeft)
        return stepsLeft


    def getThreadSum(self):
        # !! Should I not add in the risk of tokens on lower points for dice value that can hit a token on a higher point?
        currentPlayer = self.game.currentPlayer
        threadSum = 0
        for i in range(24):
            toPoint = self.game.board.ownPoint(i)

            if self.game.board.hasOwnTokensAt(i) and self.game.board.pointIsOpenForFoe(i):
                probabilityOfOneSpecificDiceRollTimesPoint = (1/6)*(1/6)*(24-toPoint)
                #print("point:", toPoint, "i:", i, "loss:", (24-toPoint))
                for d1 in range(1,7):
                    for d2 in range(1,7):
                        # if this dice combination somehow hits point, add probability (1/6)*(1/6)
                        #fromPoint = toPoint - d1*currentPlayer
                        if self.game.board.hasFoeTokensAt(i - d1*currentPlayer):
                            #print("a", d1, d2)
                            threadSum += probabilityOfOneSpecificDiceRollTimesPoint
                        elif (self.game.board.pointIsOpenForFoe((i - d1*currentPlayer)) 
                              and self.game.board.hasFoeTokensAt(i -(d1+d2)*currentPlayer)):
                            #print("b", d1, d2)
                            threadSum += probabilityOfOneSpecificDiceRollTimesPoint
                        elif self.game.board.hasFoeTokensAt(i - d2*currentPlayer):
                            #print("c", d1, d2)
                            threadSum += probabilityOfOneSpecificDiceRollTimesPoint
                        elif (self.game.board.pointIsOpenForFoe((i -d2*currentPlayer)) 
                              and self.game.board.hasFoeTokensAt(i -(d2+d1)*currentPlayer)):
                            #print("d", d1, d2)
                            threadSum += probabilityOfOneSpecificDiceRollTimesPoint
                        elif ( (d1 == d2) and self.game.board.pointIsOpenForFoe(i - d1*currentPlayer)
                                          and self.game.board.pointIsOpenForFoe(i - 2*d1*currentPlayer) 
                                          and self.game.board.pointIsOpenForFoe(i - 3*d1*currentPlayer) 
                                          and self.game.board.hasFoeTokensAt(i - 3*d1*currentPlayer)):
                                            #print("e", d1, d2)
                                            threadSum += probabilityOfOneSpecificDiceRollTimesPoint
                        elif ( (d1 == d2) and self.game.board.pointIsOpenForFoe(i - d1*currentPlayer)
                                          and self.game.board.pointIsOpenForFoe(i - 2*d1*currentPlayer) 
                                          and self.game.board.pointIsOpenForFoe(i - 3*d1*currentPlayer) 
                                          and self.game.board.pointIsOpenForFoe(i - 4*d1*currentPlayer)
                                          and self.game.board.hasFoeTokensAt(i - 4*d1*currentPlayer)):
                                            #print("f", d1, d2)
                                            threadSum += probabilityOfOneSpecificDiceRollTimesPoint

        return threadSum


    def calculateDisadvantageOfGettingOnBar(self):
        # +add the annoyance of having a token on the bar after being hit
        # e.g. blocking status somewhere on the road.
        pass

    def calculateBenefitOfGettingOnBar(self):
        # -subtract the benefit of having a token on the bar: ability to hit oponent on a high point.
        pass



    