import othelloBoard

'''You should modify the chooseMove code for the ComputerPlayer
class. You should also modify the heuristic function, which should
return a number indicating the value of that board position (the
bigger the better). We will use your heuristic function when running
the tournament between players.

Feel free to add additional methods or functions.'''

class HumanPlayer:
    '''Interactive player: prompts the user to make a move.'''
    def __init__(self,name,color):
        self.name = name
        self.color = color
        
    def chooseMove(self,board):
        while True:
            try:
                move = eval('(' + raw_input(self.name + \
                 ': enter row, column (or type "0,0" if no legal move): ') \
                 + ')')

                if len(move)==2 and type(move[0])==int and \
                   type(move[1])==int and (move[0] in range(1,9) and \
                   move[1] in range(1,9) or move==(0,0)):
                    break

                print 'Illegal entry, try again.'
            except Exception:
                print 'Illegal entry, try again.'

        if move==(0,0):
            return None
        else:
            return move

# This is a simple heuristic that we're keeping around to play with.
# Playing well = having the most pieces on the board, placed such that you
### can capture even more and won't get captured.

# If player is black, they want this heuristic value to be as small as possible.
# If player is white, they want this heuristic value to be as large as possible.
def simpleheuristic(board):
    return board.scores()[1] - board.scores()[0]

# This is a much better heuristic. By Sophia Davis and Anna Quinlan.   
# Playing well = having more pieces, even better on the edge, and best at the
# corners.
# Black pieces in the center are worth -1, on the edge -2, and in a corner, -3.
# White pieces are worth the same, respectively, but positive.
# Black wants the smallest utility, and white wants the largest utility.
def heuristic(board):
    sum = 0
    for i in range(1,othelloBoard.size-1):
        for j in range(1,othelloBoard.size-1):
            # If in corner, multiply by 3
            if i in [1, othelloBoard.size-1] and j in [1, othelloBoard.size-1]:
                sum += 3*(board.array[i][j])
            # If on edge, multiply by 2
            elif i in [1, othelloBoard.size-1] or j in [1, othelloBoard.size-1]:
                sum += 2*(board.array[i][j])
            # Otherwise, worth 1
            else:
                sum += board.array[i][j]
    return sum
    
'''
# The different players use the heuristic in different ways 
# if black, playerMax = min
# if white, playerMax = max
def playerMax(color, num_list):
    if color == "black":
        return min(num_list)
    if color == "white":
        return max(num_list)

def playerMin(color, num_list):
    if color == "black":
        return max(num_list)
    if color == "white":
        return min(num_list)
'''
## problems -- it needs to know which path to pick based on the value
## 
def minimax(board, color, plies):
    moves = {}
    for move in board._legalMoves(color):
        i = move[0]
        j = move[1]
        moves[minVal(board.makeMove(i,j,color), color, plies, 0)] = move
    
    total_min = min(moves.keys()) #playerMin(color, moves.keys())
    print "******* returning from minimax"
    return moves[total_min] #minVal(board, color, plies, 0) # argmax
    
def minVal(board, color, plies, limit):
    if len(board._legalMoves(color)) == 0 or limit == plies:
        print "Hit limit in minVal"
        return heuristic(board)
    val = 10000
    argmax = None
    for move in board._legalMoves(color):
        i = move[0]
        j = move[1]
        val = min(val, maxVal(board.makeMove(i,j,color), color, plies, limit + 1)) # playerMin(color, [val, maxVal(board.makeMove(i,j,color), color, plies, limit + 1)])
        print "-----Inside  minVal"
        print move
        print val
    return val

def maxVal(board, color, plies, limit):
    if len(board._legalMoves(color)) == 0 or limit == plies:
        print "Hit limit in maxVal"
        return heuristic(board)
    val = -10000
    argmax = None
    for move in board._legalMoves(color):
        i = move[0]
        j = move[1]
        val = min(val, minVal(board.makeMove(i,j,color), color, plies, limit + 1)) #playerMax(color, [val, minVal(board.makeMove(i,j,color), color, plies, limit + 1)])
        print "+++++Inside  maxVal"
        print move
        print val
    return val
    

class ComputerPlayer:
    '''Computer player: chooseMove is where the action is.'''
    def __init__(self,name,color,heuristic,plies):
        self.name = name
        self.color = color
        self.heuristic = heuristic
        self.plies = plies

    def chooseMove(self,board):
        '''This very silly player just returns the first legal move
        that it finds.'''
        print "MINIMAX"
        best_move = minimax(board, self.color, self.plies)
        i = best_move[0]
        j = best_move[1]
        bcopy = board.makeMove(i,j,self.color)
        if bcopy:
            print 'Heuristic value = ',self.heuristic(bcopy)
            return (i,j)
        '''
        for move in board._legalMoves(self.color):
            print move
            i = move[0]
            j = move[1]
            movemade = board.makeMove(i, j, self.color)
            print "HEURISTIC ON MOVEMADE"
            print heuristic(movemade)
        
        for i in range(1,othelloBoard.size-1):
            for j in range(1,othelloBoard.size-1):
                bcopy = board.makeMove(i,j,self.color)
                if bcopy:
                    print 'Heuristic value = ',self.heuristic(bcopy)
                    return (i,j)
        '''
        
        
        return None
