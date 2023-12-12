"""
This is responsible for stopring all the information about the cvurrent state of a chess game. 
It will also be responsible for determining the valid moves at the current state. It will also keep a move log.
"""
class GameState():
    def __init__(self):
        # board is an 8x8 2d list, each element of the list has 2 characters.
        # The first char represents the color of the piece, 'b' or 'w'.
        # The second char represents the type of the piece, 'K', 'Q', 'R', 'B', 'N' or 'P'.
        # "--" represents an empty space with no piece.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "wB", "--", "--", "wB", "--", "--", "--"],
            ["--", "--", "--", "bp", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
    
    
    '''
    Takes a Move as a parameter and executes it (this will not work for castling, pawn promotion, and en-passant)
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove # swap players
    
    
    '''
    Undo the last move made
    '''
    def undoMove(self):
        if len(self.moveLog) != 0: # make sure that there is amove to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # switch turns back
    
    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves() # for now we will not worry about checks
    
    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): # number of rows
            for c in range(len(self.board[r])): # number of cols in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) # calls the appropriate move function based on piece type
        return moves
    
    '''
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: # white pawn moves
            if self.board[r-1][c] == "--": # 1 square pawn advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": # 2 square pawn advance 
                    moves.append(Move((r, c), (r-2, c), self.board))
            # captures
            if c-1 >= 0: # captures to the left
                if self.board[r-1][c-1][0] == 'b': # enemy piece to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7: # captures to the right
                if self.board[r-1][c+1][0] == 'b': # enemy piece to capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        else: # black pawn moves
            if self.board[r+1][c] == "--": # 1 square pawn advance
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--": # 2 square pawn advance 
                    moves.append(Move((r, c), (r+2, c), self.board))
            # captures
            if c-1 >= 0: # captures to the left
                if self.board[r+1][c-1][0] == 'w': # enemy piece to capture
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7: # captures to the right
                if self.board[r+1][c+1][0] == 'w': # enemy piece to capture
                    moves.append(Move((r, c), (r+1, c+1), self.board))
        # add pawn promotions later
    
    '''
    Get all the rook moves for the rook located at row, col and add these moves to the list
    '''
    def getRookMoves(self, r, c, moves):
        if self.whiteToMove: # white Rook moves
            row, col = r, c
            while row + 1 <= 7: # rook advance down
                row += 1
                if self.board[row][c][0] == 'b':
                    moves.append(Move((r, c), (row, c), self.board))
                    break
                if self.board[row][c] == "--":
                    moves.append(Move((r,c), (row, c), self.board))
            while row - 1 >= 0: # rook advance up
                row -= 1
                if self.board[row][c][0] == 'b':
                    moves.append(Move((r, c), (row, c), self.board))
                    break
                if self.board[row][c] == "--":
                    moves.append(Move((r,c), (row, c), self.board))
            while col + 1 <= 7: # rook advance right
                col += 1
                if self.board[r][col][0] == 'b':
                    moves.append(Move((r, c), (r, col), self.board))
                    break
                if self.board[r][col] == "--":
                    moves.append(Move((r,c), (r, col), self.board))
            while col - 1 >= 0: # rook advance left
                col -= 1
                if self.board[r][col][0] == 'b':
                    moves.append(Move((r, c), (r, col), self.board))
                    break
                if self.board[r][col] == "--":
                    moves.append(Move((r,c), (r, col), self.board))
        
        else: # black Rook moves
            row, col = r, c
            while row + 1 <= 7: # rook advance down
                row += 1
                if self.board[row][c][0] == 'w':
                    moves.append(Move((r, c), (row, c), self.board))
                    break
                if self.board[row][c] == "--":
                    moves.append(Move((r,c), (row, c), self.board))
            while row - 1 >= 0: # rook advance up
                row -= 1
                if self.board[row][c][0] == 'w':
                    moves.append(Move((r, c), (row, c), self.board))
                    break
                if self.board[row][c] == "--":
                    moves.append(Move((r,c), (row, c), self.board))
            while col + 1 <= 7: # rook advance right
                col += 1
                if self.board[r][col][0] == 'w':
                    moves.append(Move((r, c), (r, col), self.board))
                    break
                if self.board[r][col] == "--":
                    moves.append(Move((r,c), (r, col), self.board))
            while col - 1 >= 0: # rook advance left
                col -= 1
                if self.board[r][col][0] == 'w':
                    moves.append(Move((r, c), (r, col), self.board))
                    break
                if self.board[r][col] == "--":
                    moves.append(Move((r,c), (r, col), self.board))
            
            
    
    '''
    Get all the knight moves for the knight located at row, col and add these moves to the list
    '''
    def getKnightMoves(self, r, c, moves):
        pass
    
    '''
    Get all the bishop moves for the bishop located at row, col and add these moves to the list
    '''
    def getBishopMoves(self, r, c, moves):
        if self.whiteToMove: # white Bishop moves
            row, col = r, c
            while row - 1 >= 0 and col - 1 >= 0: # bishop moves up and left
                row -= 1
                col -= 1 
                if self.board[row][col][0] == "b":
                    moves.append(Move((r, c), (row, col), self.board))
                    break
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    
            row, col = r, c      
            while row - 1 >= 0 and col + 1 <= 7: # bishop moves up and right
                row -= 1
                col += 1 
                if self.board[row][col][0] == "b":
                    moves.append(Move((r, c), (row, col), self.board))
                    break
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    
            row, col = r, c
            while row + 1 <= 7 and col - 1 >= 0: # bishop moves down and left
                row += 1
                col -= 1 
                if self.board[row][col][0] == "b":
                    moves.append(Move((r, c), (row, col), self.board))
                    break
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    
            row, col = r, c
            while row + 1 <= 7 and col + 1 <= 7: # bishop moves down and right
                row += 1
                col += 1 
                if self.board[row][col][0] == "b":
                    moves.append(Move((r, c), (row, col), self.board))
                    break
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    
                    
    
    '''
    Get all the queen moves for the queen located at row, col and add these moves to the list
    '''
    def getQueenMoves(self, r, c, moves):
        pass
    
    '''
    Get all the king moves for the king located at row, col and add these moves to the list
    '''
    def getKingMoves(self, r, c, moves):
        pass
    
        
        
class Move():
    # maps keys to values
    #key: value
    ranksToRows  = {"1": 7, "2": 6, "3": 5, "4": 4,
                    "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, 
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
    
    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def getChessNotation(self):
        # if needed, add to this to make it like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]