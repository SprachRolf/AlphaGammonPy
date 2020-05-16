from game import Game
from board import Board

class BoardAnalyzer:

    def __init__(self, game):
        self.game = game

    def getMoveEndings(self, board, unusedPips):
        moves = []
        if len(unusedPips) == 0:
            return moves

        for i in range(24):
            toPoint = board.ownPoint(i-unusedPips[0])
            if (board.hasOwnTokensAt( board.ownPoint(i) ) and board.pointIsOpen(toPoint)):
                step = ( board.ownPoint(i),toPoint)
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
                    if board.pointIsOpen(board.ownPoint(24-face1)):
                        stepBoard = board.copy()
                        step = (board.ownBarPoint(), board.ownPoint(24-face1))
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
                            toPoint = stepBoard.ownPoint(k-face2)
                            if (stepBoard.hasOwnTokensAt(fromPoint) and stepBoard.pointIsOpen(toPoint)):
                                foundSecondStep = True
                                step = (fromPoint,toPoint)
                                stepSteps = steps.copy()
                                stepSteps.append(step)
                                moveSet.append(tuple(stepSteps))
                        if not foundSecondStep:
                            moveSet.append(steps)

                    if (len(steps) > 0):
                        moveSet.append(tuple(steps))
        
                else:
                    # Move any combination of tokens that are not on the bar
                    for i in range(24):
                        fromPoint = board.ownPoint(i)
                        toPoint = board.ownPoint(i-face1)
                        if (board.hasOwnTokensAt(fromPoint) and board.pointIsOpen(toPoint)):
                            stepBoard = board.copy()
                            step = (fromPoint,toPoint)
                            steps = [step]
                            stepBoard.moveToken(step)
                            foundSecondStep = False
                            for k in range(24):
                                fromPoint = stepBoard.ownPoint(k)
                                toPoint = stepBoard.ownPoint(k-face2)
                                if (stepBoard.hasOwnTokensAt(fromPoint) and stepBoard.pointIsOpen(toPoint)):
                                    foundSecondStep = True
                                    step = (fromPoint,toPoint)
                                    stepSteps = steps.copy()
                                    stepSteps.append(step)
                                    moveSet.append(tuple(stepSteps))
                            if not foundSecondStep:
                                moveSet.append(steps)
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
            toPoint = stepBoard.ownPoint(24 - unusedPips[0])
            while (stepBoard.hasOwnTokensAt(stepBoard.ownBarPoint()) and (len(unusedPips) > 0) and stepBoard.pointIsOpen(toPoint)):
                step = (stepBoard.ownBarPoint(), toPoint)
                del unusedPips[0]
                steps.append(step)
                stepBoard.moveToken(step)

            #print("steps from the bar: " +str(steps))

            # The tokens on the bar couldn't move 
            # or there are no tokens on the bar any more
            # or the pips are used up.

            # If I have 4 pips left I would need 4 levels of loops with 
            # 4 local stepBoards to keep track and 4 local stepSteps.
            # This is error prone.

            # Recursively I would do one partial move and order 
            # "give me all possible combinations to use up the remaining 3 pips",
            # which returns me a list of move-endings.
            #print("unused Pips: "+ str(unusedPips))
            endings = self.getMoveEndings(stepBoard, unusedPips)
            #print("endings: "+ str(endings))

            # Glue the steps I used to get off the board to each move ending and I have all possible moves.
            for end in endings:
                #print("type steps: "+ str(type(steps)) +", type end: " +str(type(end)))
                #print("steps ("+ str(steps) +") with ending (" +str(end) +": " +str(steps + end))
                moveSet.append(steps + end)

        # Remove illegal moves (moves where pip values are wasted)
        # Remove equivalent moves (where the resulting boards are identical)
        boards = set()
        finalMoveSet = []
        
        #print("all moves: ")
        for move in moveSet:
            #print(str(move))
            if board.moveSetIsLegal(move):
                stepBoard = board.copy()
                stepBoard.moveTokens(move)
                tupleBoard = tuple(stepBoard.tokens)
                if not tupleBoard in boards:
                    boards.add(tupleBoard)
                    finalMoveSet.append(move)
                    #print("is in")

        #print("length: "+ str(len(finalMoveSet)))

        return tuple(finalMoveSet)

    # Return a move set, moving the tokens closest to bearing out.
    # A move is lower than another, when tokens on a lower position have been moved.
    # A move is lower than another, when tokens from a lower position have been moved farther.
    def getLowestLegalMoveSet(self):
        sets = self.getAllLegalMoveSets()
        if len(sets) > 0:
            return sets[0]
        return  ()

