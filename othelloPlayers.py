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

# An implementation of the minimax algorithm
def minimax(board, color, plies):
    moves = {} # {utility : move} -- keep track of possible next moves and their utilities
    
    for move in board._legalMoves(color):
        i = move[0]
        j = move[1]
        
        # Black wants the "opposite" of the traditional minimax optimal values (because of our heuristic)
        if color == -1:
            moves[maxVal(board.makeMove(i,j,color), color, plies, 1)] = move
        
        # White wants traditional minimax optimal values
        elif color == 1:
            moves[minVal(board.makeMove(i,j,color), color, plies, 1)] = move
    
    # no moves -- pass
    if  len(moves) == 0:
        return None
        
    if color == -1:
        optimal = min(moves.keys()) 
    elif color == 1:
        optimal = max(moves.keys())
        
    return moves[optimal] 

# Recursive helper function for minimax -- for "min" nodes of game tree
def minVal(board, color, plies, limit):
    if len(board._legalMoves(color)) == 0 or limit == plies:
        return heuristic(board)
    val = 10000
    for move in board._legalMoves(color):
        i = move[0]
        j = move[1]
        val = min(val, maxVal(board.makeMove(i,j,color), color, plies, limit + 1)) 
    return val

# Recursive helper function for minimax -- for "max" nodes of game tree
def maxVal(board, color, plies, limit):
    if len(board._legalMoves(color)) == 0 or limit == plies:
        return heuristic(board)
    val = -10000
    for move in board._legalMoves(color):
        i = move[0]
        j = move[1]
        val = max(val, minVal(board.makeMove(i,j,color), color, plies, limit + 1)) 
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
            return (i,j)


