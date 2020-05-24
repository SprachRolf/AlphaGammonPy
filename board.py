import game
from typing import Final


class Board:
    # tokens[24] is the bar
    # tokens[25] is white born out tokens
    # tokens[26] is red born out tokens
    whiteBarPoint: Final = 24
    redOffPoint: Final   = 25
    whiteOffPoint: Final = -2 # equivalent to 26
    redBarPoint: Final   = -1 # equivalent to 27
    initialTokenSetup: Final = [-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,2, 0,0,0,0]

    def __init__(self, game, tokens=initialTokenSetup):
        # white tokes are positive, red ones negative
        self.game = game

        # If the default parameter is used, we need to copy. 
        # Otherwise different Boards use the same tokens and a token move on one board moves the tokens for all boards.
        self.tokens = tokens.copy()

    def isInitial(self):
        return (self.tokens == [-2,0,0,0,0,5, 0,3,0,0,0,-5, 5,0,0,0,-3,0, -5,0,0,0,0,2, 0,0,0,0])

    def copy(self):
        return Board(self.game, self.tokens.copy())

    # returns true if there is a token of the current player at point
    def hasOwnTokensAt(self, point):
        return (self.tokens[point]*self.game.currentPlayer >= 1)

    # Translates point numbers for the white player 
    # into point numbers for the red player.
    def ownPoint(self, point):
        if (self.game.currentPlayer == game.Game.white):
            return point
        return 23 - point 

    def ownBarPoint(self):
        if self.game.currentPlayer == game.Game.white:
            return Board.whiteBarPoint
        return Board.redBarPoint

    def opponentBarPoint(self):
        if self.game.currentPlayer == game.Game.white:
            return Board.redBarPoint 
        return Board.whiteBarPoint

    def otherPlayer(self):
        return self.game.currentPlayer * -1

    # returns true if there are no or at most one token of the oponent at point
    def pointIsOpen(self, point):
        if self.mayBearOff() and (point == self.ownPoint(Board.whiteOffPoint)):
            return True;
        return ((point >= 0) and (point <=23) and
                self.tokens[point]*self.game.currentPlayer > -2)

    def hasOwnTokensInHome(self):
        if (self.game.currentPlayer == game.Game.white):
            for i in range(0,6):
                if self.hasOwnTokensAt(i):
                    return True
        else:
            for i in range(18,24):
                if self.hasOwnTokensAt(i):
                    return True
            
        return False
    

    def mayBearOff(self):
        if (self.hasOwnTokensAt(self.ownBarPoint())):
            return False
        if self.game.currentPlayer == game.Game.white:
            for i in range(6,24):
                if (self.hasOwnTokensAt(i)):
                    return False
        else:
            for i in range(0,18):
                if (self.hasOwnTokensAt(i)):
                    return False

        if self.hasOwnTokensInHome():
            return True

        # There is no own token left on the whole board at all.
        return False

    def hasWon(self):
        return (self.tokens[self.ownPoint(Board.whiteOffPoint)] == 15)

    def moveTokens(self, moves):
        "moves is a tuple of pairs describing the move of one token"
        "move == (from, to)"
        if self.moveSetIsLegal(moves):
            for move in moves:
                fromPoint, toPoint = move
                # A token is never moved by a player to the bar directly (point 24)
                assert(toPoint != Board.whiteBarPoint)
                assert(toPoint != Board.redBarPoint)

                self.moveToken(move)

    def moveToken(self,move):
        fromPoint, toPoint = move
        assert(fromPoint >= Board.redBarPoint)
        assert(toPoint >= Board.whiteOffPoint)
        # Tokens from the bar (red or white bar points) may be moved in again.
        # Tokens on off-points (born-out tokens) are never moved onto the board again
        assert(fromPoint <= Board.whiteBarPoint)
        # When bearing off, a player moves tokens to the off-points (25 or 26)
        assert(toPoint <= Board.redOffPoint)

        self.takeToken(fromPoint)
        self.putToken(toPoint)

    def takeToken(self, fromPoint):
        self.tokens[fromPoint] = self.tokens[fromPoint] - self.game.currentPlayer

    def putToken(self,toPoint):
        if (self.tokens[toPoint] == self.otherPlayer()):
            self.hitToken(toPoint)
        self.tokens[toPoint] = self.tokens[toPoint] + self.game.currentPlayer

    def hitToken(self,point):
        # there is exactly one token of the opponent on the target point
        assert(self.tokens[point] == self.otherPlayer())
        self.tokens[point] = 0

        # On the bar can be tokens of both player.
        # On redBarPoint can only be red tokens, on whiteBarPoint can only be white tokens
        barPoint = self.opponentBarPoint()
        assert(self.tokens[barPoint] * self.game.currentPlayer <= 0)
        self.tokens[barPoint] = self.tokens[barPoint] + self.otherPlayer()


    def moveSetIsLegal(self,moves):
        diceFaces = self.game.getDiceFaces()
        unusedPips = self.game.getPips(diceFaces)
        board = self.copy()
        if (len(moves) == 0 and board.hasLegalMoves(unusedPips)):
            return False;

        for move in moves:
            fromPoint, toPoint = move

            # Check if the move wants to move the tokens _on_ the board
            # Only when bearing off, tokens can be moved to the off-points
            if (board.mayBearOff()):
                if (board.game.currentPlayer == game.Game.white):
                    # may bear off, this means all tokens are in the home are, Point 0 to Point 5
                    if (toPoint < Board.whiteOffPoint or toPoint > 4):
                        return False
                    if (fromPoint < 0 or fromPoint >5):
                        return False
                else: # red player
                    # may bear off, this means all tokens are in the home are, Point 18 to Point 23
                    if (toPoint > Board.redOffPoint or toPoint < 18):
                        return False
                    if (fromPoint > 23 or fromPoint < 18):
                        return False
            else:
                if (toPoint < 0 or toPoint > 23):
                    return False
                if (fromPoint < Board.redBarPoint or fromPoint > Board.whiteBarPoint):
                    return False
            # Tokens can not be moved to the bar directly. Only by hitting.
            if (toPoint == Board.whiteBarPoint or toPoint == Board.redBarPoint):
                return False

            # Player has to move all own tokens from the bar before doing any other move
            if (board.hasOwnTokensAt(board.ownBarPoint()) and (fromPoint != board.ownBarPoint()) ):
                return False

            if not board.hasOwnTokensAt(fromPoint):
                # there is none of the players token on the source point
                return False
            if not board.pointIsOpen(toPoint):
                # there are 2 or more tokens of the opponent on the target point
                return False

            if (toPoint == Board.whiteOffPoint):
                if (board.game.currentPlayer == game.Game.red):
                    return False  # the red player may not move to white Off point
                #bearing off
                distance = fromPoint +1 # just move the token off the board
                try:
                    unusedPips.remove(distance)
                    # One of the dice showed the exact required pip
                    board.moveToken(move)
                except ValueError:
                    # The dice don't show the required pip
                    # The move is valid if there is a higher pip unused from the dice and
                    #                   and if there is no token on a higher position
                    for i in range(fromPoint +1,6):
                        if board.hasOwnTokensAt(i):
                            return False
                    # We need foundPip to remove only one of the pips.
                    foundPip = 0
                    for pip in unusedPips:
                        if pip > distance:
                            foundPip = pip
                    if foundPip:
                        unusedPips.remove(foundPip)
                        board.moveToken(move)
                    else:
                        return False

            elif (toPoint == Board.redOffPoint):
                if (board.game.currentPlayer == game.Game.white):
                    return False  # the white player may not move to red Off point
                #bearing off
                distance = 24-fromPoint # just move the token off the board
                try:
                    unusedPips.remove(distance)
                    # One of the dice showed the exact required pip
                    board.moveToken(move)
                except ValueError:
                    # The dice don't show the required pip
                    # The move is valid if there is a higher pip unused from the dice and
                    #                   and if there is no token on a higher position
                    for i in range(18,fromPoint):
                        if board.hasOwnTokensAt(i):
                            return False
                    # We need foundPip to remove only one of the pips.
                    foundPip = 0
                    for pip in unusedPips:
                        if pip > distance:
                            foundPip = pip
                    if foundPip > 0:
                        unusedPips.remove(foundPip)
                        board.moveToken(move)
                    else:
                        return False
                
            else:
                # It is a normal move, not a bearing-off move.
                try:
                    distance = fromPoint - toPoint
                    unusedPips.remove(distance*board.game.currentPlayer)
                    # move one token
                    # The following moves depend on the first moves.
                    # They may become legal or impossible.
                    board.moveToken(move)
                except ValueError:
                    # the die values don't allow that move
                    return False


        if (len(unusedPips) == 0):
            # all dice counts must be used up
            return True
        elif board.hasLegalMoves(unusedPips):
            return False
        elif (diceFaces[0] != diceFaces[1]):
            # There are unusedPips, but no moves possible.
            # Check if using the pips becomes possible by moving another.
            # This can not hapen for doublet dice values (both dice show the same count).

            # The unused Pip could become usable by using it first or by moving another token.


            #minPip will contain the smaller unused pip if only one can be used but not the other
            board = self.copy()
            minPip = 10 # bigger than 6, the maximum dice value

            # Move each token pip1 and see if any other token can move.
            # Then move each token pip2 and see if any other token can move.
            #distance1 = diceFaces[0]*self.game.currentPlayer
            #distance2 = diceFaces[1]*self.game.currentPlayer
            distance1 = diceFaces[0]
            distance2 = diceFaces[1]
            for twice in range(2):
                if (board.hasOwnTokensAt(board.ownBarPoint())):
                    fromPoint = board.ownBarPoint()
                    toPoint = board.ownPoint(Board.whiteBarPoint - distance1)
                    if (board.pointIsOpen(toPoint)):
                        if distance2 < minPip:
                            minPip = distance2
                        stepBoard = board.copy()
                        stepBoard.moveToken( (fromPoint,toPoint) )
                        if stepBoard.hasLegalMoves([distance2]):
                            # found a way to use both dice values
                            return False
                else:
                    if board.hasWon():
                        # A pip was left over because no tokens are left on the board any more.
                        # In this case using the lower pip is also legal 
                        # (with the higher pip the player can also just move the token off the board).
                        return True

                    for point in range(0,24):
                        fromPoint = board.ownPoint(point)
                        whiteToPoint = point - distance1
                        if whiteToPoint < 0:
                            whiteToPoint = Board.whiteOffPoint
                        toPoint = board.ownPoint(whiteToPoint)
                        if (board.hasOwnTokensAt(fromPoint) and board.pointIsOpen(toPoint) ):
                            if distance2 < minPip:
                                minPip = distance2

                            stepBoard = board.copy() # a board to test a single move
                            # We cannot use stepBoard.moveTokens() since moving a single move is not legal
                            stepBoard.moveToken( (fromPoint, toPoint))
                            if (stepBoard.hasWon()):
                                return True
                            if stepBoard.hasLegalMoves([distance2]):
                                # found a way to use both dice values
                                return False
                #distance2 = diceFaces[0]*self.game.currentPlayer
                #distance1 = diceFaces[1]*self.game.currentPlayer
                distance2 = diceFaces[0]
                distance1 = diceFaces[1]

            # I moved every possible token for dice value 1 and checked if any token can move after that.
            # Then I moved every possible token for dice value 2 and checked if any token can move after that.
            # There is no combination to use both dice values.

            # If neither dice value could be used, minPip is still 10.
            # unusedPips must contain both dice values (or 4 if both dice show the same vaule)
            # and "moves" must be an empty list then to be legal, 
            if minPip == 10:
                if (len(unusedPips) != 2):
                    print("Playercolor: ", board.game.currentPlayer,", minPip: ",minPip,sep="")
                    print("dice 1: ", diceFaces[0],", dice 2: ",diceFaces[1],", unusedPips: ",unusedPips,sep="")
                    print("original Board:", board.tokens)
                    print("moves:", moves)
                assert(len(unusedPips) == 2)
                assert(len(moves) == 0) # if moves would contain any moves, they must be impossible and be caught earliser.
            if (minPip < unusedPips[0]):
                return False
        return True

    def hasLegalMoves(self, unusedPips):
        if self.hasOwnTokensAt(self.ownBarPoint()):
            for pip in unusedPips:
                if self.pointIsOpen(self.ownBarPoint() -pip*self.game.currentPlayer):
                    return True
        elif self.mayBearOff():
            for pip in unusedPips:
                if self.hasOwnTokensAt(self.ownPoint(pip -1)):
                    # There is a token that can move off by moving exactly <pip> points.
                    return True
                foundTokenOnHigherPosition = False
                for homePos in range(pip, 6):
                    fromPoint = self.ownPoint(homePos)
                    toPoint = self.ownPoint(homePos - pip)
                    if self.hasOwnTokensAt(fromPoint):
                        foundTokenOnHigherPosition = True
                        if self.pointIsOpen(toPoint):
                            # A token on a higher position can move within the home Points
                            return False
                if not foundTokenOnHigherPosition:
                    # If there is any token on a lower position, it may be borne off (wasting some pip value)
                    for homePos in range(0,pip-1):
                        if self.hasOwnTokensAt(self.ownPoint(homePos)):
                            return True
                # There was no token on the "pip-position" (where it could be borne of without wasting pip values),
                # none was on a higher position and none was on a lowewr position.
                # There are unused pips and no move is possible. 
                # Either the player has won or there are blocked tokens on higher positions than pip-position.
                return False
        else:                    
            for point in range(0,24):
                if self.hasOwnTokensAt(point):
                    for pip in unusedPips:
                        if self.pointIsOpen(point - pip*self.game.currentPlayer):
                            return True

        return False                
