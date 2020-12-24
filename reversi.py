class Reversi:
    white = "w"
    black = "b"
    empty = "."
    size = 8

    def __init__(self):
        self.newGame()
        self.currentTurn = 'b'

    def newGame(self):
        # Creates an 8 by 8 gameboard with intial pieces
        self.gameBoard = [[Reversi.empty] * Reversi.size for i in range(Reversi.size)]
        self.gameBoard[3][3] = Reversi.white
        self.gameBoard[4][3] = Reversi.black
        self.gameBoard[3][4] = Reversi.black
        self.gameBoard[4][4] = Reversi.white

    def getScore(self, colour):
        # Loops thorugh board and each time it encounters the color specified then increament count. Returns count at the end
        count = 0
        for row in range(Reversi.size):
            for column in range(Reversi.size):
                if self.gameBoard[row][column] == colour:
                    count += 1
        return count

    def setPlayerColour(self, colour):
        # Set player colour to specified colour with computer colour as the remaining colour
        self.playerColour = colour
        if colour == self.black:
            self.computerColour = Reversi.white
        else:
            self.computerColour = Reversi.black

    def displayBoard(self):
        # Prints the board along with row and column numbers
        print("  0 1 2 3 4 5 6 7") # Printing column numbers
        for row in range(Reversi.size):
            if row != 0:
                print("")
            print(row, end=' ')
            for column in range(Reversi.size):
                print(self.gameBoard[row][column], end=' ')

    def isPositionValid(self, position, colour):
        # Checks in all 8 directions surounding the position for a valid move
        posy = position[0]
        posx = position[1]
        piecesFlanked = False
        # If position is not on board
        if posy not in [0,1,2,3,4,5,6,7] or posx not in [0,1,2,3,4,5,6,7]:
            return False
        # If position is empty
        if self.gameBoard[posy][posx] == Reversi.empty:
            for y,x in [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]:
                posy = position[0]
                posx = position[1]
                piecesFlanked = False
                # Keeps looping while line being checked is still valid
                while True:
                    posy += y
                    posx += x
                    # Position not on board
                    if posy not in [0,1,2,3,4,5,6,7] or posx not in [0,1,2,3,4,5,6,7]:
                        break
                    # Position is an empty space
                    if self.gameBoard[posy][posx] == Reversi.empty:
                        break
                    # Position is not equal to colour, that means it is the opposite colour which means pieces will be changes
                    if self.gameBoard[posy][posx] != colour:
                        piecesFlanked = True
                    # If you pass a pieces thats not your colour and you reach a piece that is your colour the move is valid
                    if self.gameBoard[posy][posx] == colour and piecesFlanked:
                        return True
                    # Already checked piecesFlanked that means the pos equaling colour is an invalid position
                    if self.gameBoard[posy][posx] == colour:
                        break
        return False

    def isGameOver(self):
        # Ends the games when the current player has no valid mode
        # First check valid moves for each player then checks current turn to decide if game is over
        validMoveCpu = False
        validMovePlayer = False
        for row in range(Reversi.size):
            for column in range(Reversi.size):
                if self.isPositionValid([row,column], self.computerColour):
                    validMoveCpu = True
                if self.isPositionValid([row,column], self.playerColour):
                    validMovePlayer = True
        # Check turn
        if self.currentTurn == 'b':
            if self.playerColour == 'b' and validMovePlayer == True:
                return False
            if self.computerColour == 'b' and validMoveCpu == True:
                return False           
        if self.currentTurn == 'w':
            if self.playerColour == 'w' and validMovePlayer == True:
                return False
            if self.computerColour == 'w' and validMoveCpu == True:
                return False             
        return True
        
    def makeMovePlayer(self, position):
        # Loops through gameBoard like isPositionValid but this time pieces to be changed are added to piecesFlanked
        # If a move is valid in a direction then the pieces in piecesFlanked for that direction are flipped
        posy = position[0]
        posx = position[1]
        if self.gameBoard[posy][posx] == Reversi.empty:
            # Set position to a piece for whoevers turn it is
            self.gameBoard[posy][posx] = self.currentTurn
            for y,x in [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]:
                posy = position[0]
                posx = position[1]
                piecesFlanked = []
                while True: # Keeps looping while line being checked is still valid
                    posy += y
                    posx += x
                    if posy not in [0,1,2,3,4,5,6,7] or posx not in [0,1,2,3,4,5,6,7]:
                        break
                    if self.gameBoard[posy][posx] == Reversi.empty:
                        break
                    if self.gameBoard[posy][posx] != self.currentTurn:
                        piecesFlanked.append([posy,posx])
                    # When the move is sucessful then flip the opposite colour pieces
                    if self.gameBoard[posy][posx] == self.currentTurn and len(piecesFlanked) != 0:
                        for posList in piecesFlanked:
                            self.gameBoard[posList[0]][posList[1]] = self.currentTurn
            # After a move has been made change the currentTurn to the other colour
            self.oppColour()

    def makeMoveNaive(self):
        # Makes the first valid move while looping through from top left corner to bottom right corner
        for row in range(Reversi.size):
            for column in range(Reversi.size):
                if self.isPositionValid([row,column], self.computerColour):
                    self.makeMovePlayer([row,column])
                    print("Computer making move: [%d,%d]" % (row,column))
                    return
                    
    def makeMoveSmart(self):
        # Checks all possible moves and the points it will result in and picks the first move which gives the most points
        moveScore = {}
        for row in range(Reversi.size):
            for column in range(Reversi.size):
                if self.gameBoard[row][column] == Reversi.empty:
                    for y,x in [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]:
                        posy = row
                        posx = column
                        piecesFlanked = False
                        score = 0
                        while True: # Keeps looping while line being checked is still valid
                            posy += y
                            posx += x
                            if posy not in [0,1,2,3,4,5,6,7] or posx not in [0,1,2,3,4,5,6,7]:
                                break
                            if self.gameBoard[posy][posx] == Reversi.empty:
                                break
                            if self.gameBoard[posy][posx] == self.playerColour:
                                piecesFlanked = True
                                score += 1
                            if self.gameBoard[posy][posx] == self.computerColour and piecesFlanked:
                                # Each tile to be flipped will increment score for that move
                                if (row,column) not in moveScore.keys():
                                    moveScore[(row,column)] = score
                                else:
                                    moveScore[(row,column)] += score
                                break
                            if self.gameBoard[posy][posx] == self.computerColour:
                                # Already checked piecesFlanked that means the pos equaling colour is an invalid position
                                break
        maxScore = 0
        maxMove = []
        
        # Checks all moves and chooses the move which results in the greatest score to be maxMove (The move which will be made)
        for movey, movex in moveScore:
            if moveScore[movey,movex] > maxScore:
                maxMove = [movey,movex]
                maxScore = moveScore[movey,movex]
        self.makeMovePlayer(maxMove)        
        print("Computer making move: [" + str(maxMove[0]) + " " + str(maxMove[1]) + "]")
        
    def oppColour(self):
        # Changes currentTurn to the opposite colour
        if self.currentTurn == 'b':
            self.currentTurn = 'w'
        else:
            self.currentTurn = 'b'
            
    def checkEmpty(self, position):
        # Checks if the position that was given is empty. Returns True if it is otherwise False
        if self.gameBoard[position[0]][position[1]] != Reversi.empty:
            return False
        return True
            