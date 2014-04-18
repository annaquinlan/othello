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
    
def minimax(board, color, plies):
    moves = {}
    
    print "Starting minimax, legal moves are: " + str(board._legalMoves(color))
    for move in board._legalMoves(color):
        i = move[0]
        j = move[1]
        if color == -1:
            moves[maxVal(board.makeMove(i,j,color), color, plies, 1)] = move
        elif color == 1:
            moves[minVal(board.makeMove(i,j,color), color, plies, 1)] = move
    if  len(moves) == 0:
        return None
    if color == -1:
        optimal = min(moves.keys()) 
    elif color == 1:
        optimal = max(moves.keys())
    print "***Returning from minimax, optimal is: " + str(optimal) + "***"
    return moves[optimal] 
    
def minVal(board, color, plies, limit):
    print "Starting minVal"
    if len(board._legalMoves(color)) == 0 or limit == plies:
        print "minVal -- board's value is " + str(heuristic(board))
        return heuristic(board)
    val = 10000
    for move in board._legalMoves(color):
        i = move[0]
        j = move[1]
        val = min(val, maxVal(board.makeMove(i,j,color), color, plies, limit + 1)) 
    print " "*limit + str(val) + " - from minVal"
    return val

def maxVal(board, color, plies, limit):
    print "Starting maxVal"
    if len(board._legalMoves(color)) == 0 or limit == plies:
        print "maxVal -- board's value is " + str(heuristic(board))
        return heuristic(board)
    val = -10000
    for move in board._legalMoves(color):
        i = move[0]
        j = move[1]
        val = max(val, minVal(board.makeMove(i,j,color), color, plies, limit + 1)) 
    print " "*limit + str(val) + " - from maxVal"
    return val
    

class ComputerPlayer:
    '''Computer player: chooseMove is where the action is.'''
    def __init__(self,name,color,heuristic,plies):
        self.name = name
        self.color = color
        self.heuristic = heuristic
        self.plies = plies

    def chooseMove(self,board):
        best_move = minimax(board, self.color, self.plies)
        if best_move == None:
            return None
        i = best_move[0]
        j = best_move[1]
        bcopy = board.makeMove(i,j,self.color)
        if bcopy:
            #print 'Heuristic value = ',self.heuristic(bcopy)
            return (i,j)


