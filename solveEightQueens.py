import random
import copy
from optparse import OptionParser

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        solutionCounter = 0
        lectureCase = [[]]
        if lectureExample:
            lectureCase = [
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", "q", ".", ".", ".", "."],
            ["q", ".", ".", ".", "q", ".", ".", "."],
            [".", "q", ".", ".", ".", "q", ".", "q"],
            [".", ".", "q", ".", ".", ".", "q", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ]
        for i in range(0,numberOfRuns):
            if self.search(Board(lectureCase), verbose).getNumberOfAttacks() == 0:
                solutionCounter+=1
        print "Solved:",solutionCounter,"/",numberOfRuns

    def search(self, board, verbose):
        newBoard = board
        i = 0 
        while True:
            if verbose:
                print "iteration ",i
                print newBoard.toString()
                print newBoard.getCostBoard().toString()
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks) = newBoard.getBetterBoard()
            i+=1
            if currentNumberOfAttacks <= newNumberOfAttacks:
                break
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [["." for i in range(0,8)] for j in range(0,8)]
        for i in range(0,8):
            tmpSquareArray[random.randint(0,7)][i] = "q"
        return tmpSquareArray
          
    def toString(self):
        s = ""
        for i in range(0,8):
            for j in range(0,8):
                s += str(self.squareArray[i][j]) + " "
            s += "\n"
        return s + "# attacks: "+str(self.getNumberOfAttacks())

    def getCostBoard(self):
        costBoard = copy.deepcopy(self)
        for r in range(0,8):
            for c in range(0,8):
                if self.squareArray[r][c] == "q":
                    for rr in range(0,8):
                        if rr!=r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = "."
                            testboard.squareArray[rr][c] = "q"
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        #TODO: put your code here...
        
        # Keep track of the original number of attacks        
        minAttackOrig = self.getNumberOfAttacks()
        
        # Get the costbard of the current board
        costBoard = self.getCostBoard()
        
        possibleMove = []
        minAttack = minAttackOrig
        # Get Min Attacks possible in the costboard. If there are multiple moves, store positions in possibleMove
        for r in range(0,8):
            for c in range(0,8):
                if (costBoard.squareArray[r][c] == minAttack): possibleMove.append((r,c))

                if (costBoard.squareArray[r][c] < minAttack):
                    minAttack = costBoard.squareArray[r][c]
                    del possibleMove[:]
                    possibleMove.append((r,c))

        # If there are no better moves than the current one, return without moving a queen
        if (minAttack == minAttackOrig): return (self, minAttackOrig)

        # Choose a random position in possibleMove to use
        sel = random.randint(0,len(possibleMove)-1)
        row, col = possibleMove[sel]

        # Clear out queen already in that column
        for i in range(0,8):
            self.squareArray[i][col] = "."

        # Assign 'q' to selected row,col, return the board and the minAttack number
        self.squareArray[row][col] = "q"

        return (self, minAttack)

    def getNumberOfAttacks(self):
        #TODO: put your code here...
        numAttacks = 0

        # Check each column from 0 to 6 (no need to check attacks for last column)
        for col in range(0,7):
            for row in range(0,8):
                # If row,col contains a queen, check for attacks
                if (self.squareArray[row][col] == "q"):
                    r = 1
                    for c in range(col+1, 8):
                        # Test for horizontal attacks
                        if (self.squareArray[row][c] == "q"): numAttacks += 1
                        # Test NE for diagonal attacks
                        if ((row - r) >= 0):
                            if (self.squareArray[row-r][c] == "q"): numAttacks += 1
                        # Test SE for diagonal attacks
                        if ((row + r) < 8):
                            if (self.squareArray[row+r][c] == "q"): numAttacks += 1
                        
                        r += 1

        return numAttacks


if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    #random.seed(0)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)