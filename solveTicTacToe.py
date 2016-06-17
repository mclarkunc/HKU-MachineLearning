import random
import copy
from optparse import OptionParser

boardAlgebra = []

"""
Global list to store the board state labels, given by the paper "The Secrets of Notakto" by Plambeck and Whitehead
http://arxiv.org/pdf/1301.1672v1.pdf
This will be used by the AI to evaluate board configurations and select moves
"""
boardAlgebra = [ 
                [0,1,2,3,4,5,6,7,8,'c'],
                ['X',1,2,3,4,5,6,7,8,1],
                [0,'X',2,3,4,5,6,7,8,1],
                [0,1,2,3,'X',5,6,7,8,'cc'],
                ['X','X',2,3,4,5,6,7,8,'ad'],
                ['X',1,'X',3,4,5,6,7,8,'b'],
                ['X',1,2,3,'X',5,6,7,8,'b'],
                ['X',1,2,3,4,'X',6,7,8,'b'],
                ['X',1,2,3,4,5,6,7,'X','a'],
                [0,'X',2,'X',4,5,6,7,8,'a'],
                [0,'X',2,3,'X',5,6,7,8,'b'],
                [0,'X',2,3,4,5,6,'X',8,'a'],
                ['X','X',2,'X',4,5,6,7,8,'b'],
                ['X','X',2,3,'X',5,6,7,8,'ab'],
                ['X','X',2,3,4,'X',6,7,8,'d'],
                ['X','X',2,3,4,5,'X',7,8,'a'],
                ['X','X',2,3,4,5,6,'X',8,'d'],
                ['X','X',2,3,4,5,6,7,'X','d'],
                ['X',1,'X',3,'X',5,6,7,8,'a'],
                ['X',1,'X',3,4,5,'X',7,8,'ab'],
                ['X',1,'X',3,4,5,6,'X',8,'a'],
                ['X',1,2,3,'X','X',6,7,8,'a'],
                ['X',1,2,3,4,'X',6,'X',8,1],
                [0,'X',2,'X','X',5,6,7,8,'ab'],
                [0,'X',2,'X',4,'X',6,7,8,'b'],
                ['X','X',2,'X','X',5,6,7,8,'a'],
                ['X','X',2,'X',4,'X',6,7,8,'a'],
                ['X','X',2,'X',4,5,6,7,'X','a'],
                ['X','X',2,3,'X','X',6,7,8,'b'],
                ['X','X',2,3,'X',5,'X',7,8,'b'],
                ['X','X',2,3,4,'X','X',7,8,'b'],
                ['X','X',2,3,4,'X',6,'X',8,'ab'],
                ['X','X',2,3,4,'X',6,7,'X','ab'],
                ['X','X',2,3,4,5,'X','X',8,'b'],
                ['X','X',2,3,4,5,'X',7,'X','b'],
                ['X','X',2,3,4,5,6,'X','X','a'],
                ['X',1,'X',3,'X',5,6,'X',8,'b'],
                ['X',1,'X',3,4,5,'X',7,'X','a'],
                ['X',1,2,3,'X','X',6,'X',8,'b'],
                [0,'X',2,'X',4,'X',6,'X',8,'a'],
                ['X','X',2,'X',4,'X',6,'X',8,'b'],
                ['X','X',2,'X',4,'X',6,7,'X','b'],
                ['X','X',2,3,'X','X','X',7,8,'a'],
                ['X','X',2,3,4,'X','X','X',8,'a'],
                ['X','X',2,3,4,'X','X',7,'X','a'],
                ['X','X',2,'X',4,'X',6,'X','X','a']
                ]


class solveTicTacToe:
    def __init__(self):
        

        global boardAlgebra

        # Add the tranformations of the labeled states to the boardAlgebra list
        self.addTransforms(boardAlgebra)
        
        # Initialize the game board
        gameBoard = Board()
        
        # AI goes first
        userTurn = False

        # Loop until no more valid moves
        while(len(gameBoard.validMoves) > 0):
            if (userTurn):
                playerMove = raw_input("Your move: ")

                if playerMove in gameBoard.validMoves:
                    # Update the board
                    gameBoard.updateMove(playerMove)
                    userTurn = False 
                else:
                    print "Not a valid move, try again"
            else:
                # Search for a move using local search
                AI_Move = self.searchForMove(gameBoard) 
                print "AI:", AI_Move
                gameBoard.updateMove(AI_Move)
                userTurn = True

            print "\n", gameBoard.toString()

        # No more valid moves
        if (userTurn):
            print "You won!"
        else:
            print "You completed the last board: AI won"

    def searchForMove(self, gameBoard):
        # Uses local search to search for a board configuration that returns a winning state
        algebraState = gameBoard.getAlgebraState()
        
        for move in gameBoard.validMoves:
            newBoard = copy.deepcopy(gameBoard)
            newBoard.updateMove(move)
            newAlgState = newBoard.getAlgebraState()
            # Checks if new Board is a winning state
            if newAlgState in ["a", "bb", "bc", "cc"]:
                return move

        # If gets here, no winning move found
        return gameBoard.validMoves[randint(0,len(gameBoard.validMoves))]

    # Add to the boardAlgebra all the transformations of the Tic Tac Toe Algebra lables
    def addTransforms(self, boardAlgebra):
        
        for board in boardAlgebra:
            tttBoard = list(board)

            # Rotation 90 Degree
            tttBoard90 = list(self.rotateRight(tttBoard))
            tttBoard180 = list(self.rotateRight(tttBoard90))
            tttBoard270 = list(self.rotateRight(tttBoard180))

            # Mirror Image
            tttBoard_mir = list(self.mirrorImage(tttBoard))
            tttBoard90_mir = list(self.mirrorImage(tttBoard90))
            tttBoard180_mir = list(self.mirrorImage(tttBoard180))
            tttBoard270_mir = list(self.mirrorImage(tttBoard270))

        
            if tttBoard90 not in boardAlgebra: boardAlgebra.append(tttBoard90)
            if tttBoard180 not in boardAlgebra: boardAlgebra.append(tttBoard180)
            if tttBoard270 not in boardAlgebra: boardAlgebra.append(tttBoard270)
            if tttBoard_mir not in boardAlgebra: boardAlgebra.append(tttBoard_mir)
            if tttBoard90_mir not in boardAlgebra: boardAlgebra.append(tttBoard90_mir)
            if tttBoard180_mir not in boardAlgebra: boardAlgebra.append(tttBoard180_mir)
            if tttBoard270_mir not in boardAlgebra: boardAlgebra.append(tttBoard270_mir)

    def rotateRight(self, tttBoard):
        # 90 deg right
        newtttBoard = [0,1,2,3,4,5,6,7,8,tttBoard[-1]]
        if tttBoard[0] == 'X': newtttBoard[2] = 'X'
        if tttBoard[1] == 'X': newtttBoard[5] = 'X'
        if tttBoard[2] == 'X': newtttBoard[8] = 'X'
        if tttBoard[3] == 'X': newtttBoard[1] = 'X'
        if tttBoard[4] == 'X': newtttBoard[4] = 'X'
        if tttBoard[5] == 'X': newtttBoard[7] = 'X'
        if tttBoard[6] == 'X': newtttBoard[0] = 'X'
        if tttBoard[7] == 'X': newtttBoard[3] = 'X'
        if tttBoard[8] == 'X': newtttBoard[6] = 'X'

        return newtttBoard

    def mirrorImage(self, tttBoard):
        # vertical mirror
        newtttBoard = [0,1,2,3,4,5,6,7,8,tttBoard[-1]]
        if tttBoard[0] == 'X': newtttBoard[2] = 'X'
        if tttBoard[1] == 'X': newtttBoard[1] = 'X'
        if tttBoard[2] == 'X': newtttBoard[0] = 'X'
        if tttBoard[3] == 'X': newtttBoard[5] = 'X'
        if tttBoard[4] == 'X': newtttBoard[4] = 'X'
        if tttBoard[5] == 'X': newtttBoard[3] = 'X'
        if tttBoard[6] == 'X': newtttBoard[8] = 'X'
        if tttBoard[7] == 'X': newtttBoard[7] = 'X'
        if tttBoard[8] == 'X': newtttBoard[6] = 'X'

        return newtttBoard


class Board:
    def __init__(self, dictBoard = {}, validMoves = []):
        
        # Initialize Board
        if dictBoard == {}:
             
            initialBoard = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        
            self.dictBoard = {'A' : list(initialBoard), 'B' : list(initialBoard), 'C' : list(initialBoard)} 
            
            # Initialize valid moves
            self.validMoves = ["A0","A1","A2","A3","A4","A5","A6","A7","A8",
                                "B0","B1","B2","B3","B4","B5","B6","B7","B8",
                                "C0","C1","C2","C3","C4","C5","C6","C7","C8"]
          
        else:
            self.dictBoard = dictBoard
            self.validMoves = validMoves


    def updateMove(self, move):
        boardLetter = move[0]
        boardNumber = int(move[1])
        self.dictBoard[boardLetter][boardNumber] = 'X'
        self.validMoves.remove(move)
        
        #Check for dead board
        if (self.checkTicTacToe(boardLetter)):
            # Remove all instances of the board in validMoves
            self.validMoves = [x for x in self.validMoves if not boardLetter in x]
            # Delete board from gameboard dictionary
            del self.dictBoard[boardLetter]

    # Check for dead boards
    def checkTicTacToe(self, letter):
        if letter in self.dictBoard:
            # If subBoard is in boardAlgebra, it is not a dead board
            if any(item[:-1] == self.dictBoard[letter] for item in boardAlgebra):    
                return False
        
        return True  #if it is not in boardAlgebra, it is a dead board

    # Return the overall algebra state of the board
    def getAlgebraState(self):
        algA = 1
        algB = 1
        algC = 1
        
        for item in boardAlgebra:
            if 'A' in self.dictBoard and item[:-1] == self.dictBoard['A']:
                algA = item[-1]
            if 'B' in self.dictBoard and item[:-1] == self.dictBoard['B']:
                algB = item[-1]
            if 'C' in self.dictBoard and item[:-1] == self.dictBoard['C']:
                algC = item[-1]

        # Reduce Algebra States
        algebraState = ""
        if algA != 1: 
            algebraState += algA
        if algB != 1: 
            algebraState += algB
        if algC != 1:
            algebraState += algC
        
        # Sort joined states in alphabetical order
        algebraState = ''.join(sorted(algebraState))
        oldAlgState = algebraState

        # Reduce until no changes
        while True:
            algebraState = algebraState.replace("aa","")
            algebraState = algebraState.replace("bbb","b")
            algebraState = algebraState.replace("bbc","c")
            algebraState = algebraState.replace("ccc","acc")
            algebraState = algebraState.replace("bbd","d")
            algebraState = algebraState.replace("cd","ad")
            algebraState = algebraState.replace("dd","cc")
            algebraState = ''.join(sorted(algebraState))

            if algebraState == oldAlgState:
                break
            oldAlgState = algebraState

        return algebraState             

    # Print out the Board
    def toString(self):
        s = ""
        
        for row in range(-1,3):
            if 'A' in self.dictBoard:
                if row == -1:
                    s += "A:    "
                else:
                    for col in range(0,3):
                        s += str(self.dictBoard['A'][col+(row*3)]) + " "
                s += " "
            if 'B' in self.dictBoard:
                if row == -1:
                    s += "B:    "
                else:
                    for col in range(0,3):
                        s += str(self.dictBoard['B'][col+(row*3)]) + " "
                s += " "
            if 'C' in self.dictBoard:
                if row == -1:
                    s += "C:    "
                else:
                    for col in range(0,3):
                        s += str(self.dictBoard['C'][col+(row*3)]) + " "
            s += "\n"  

        return s          
            

if __name__ == "__main__":
    
    solveTicTacToe()

