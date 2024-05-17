"""
This is responsible for stopping all the information about the current state of a chess game. 
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
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False
        self.enpassant_possible = () # Coordinates for the square where an enpassant capture is possible
    
    
    
    '''
    Takes a Move as a parameter and executes it (this will not work for castling, pawn promotion, and en-passant)
    '''
    def makeMove(self, move):
        self.board[move.start_row][move.start_col] = "--"

        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move) # log the move so we can undo it later
        self.white_to_move = not self.white_to_move # swap players
        # update the king's location if moved
        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)
            
        # Pawn promotion
        if move.is_pawn_promotion:
            # promotedPiece = input("Promote to Q, R, B, or N:") # make into UI later
            # self.board[move.end_row][move.end_col] = move.piece_moved[0] + promotedPiece
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'Q'
            
        if move.en_passant:
            self.board[move.start_row][move.end_col] = "--"
        
            
        # if pawn moves twice, next move can capture enpassant
        if move.piece_moved[1] == 'p' and abs(move.start_row - move.end_row) == 2: # only on 2 square pawn advances
            self.enpassant_possible = ((move.end_row + move.start_row)//2, move.start_col)
        else:
            self.enpassant_possible = ()
        # if enpassant move, must update the board to capture the pawn
        


        
        
    
    '''
    Undo the last move made
    '''
    def undoMove(self):
        if len(self.move_log) != 0: # make sure that there is amove to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move # switch turns back
            # update the king's position if needed
            if move.piece_moved == 'wK':
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == 'bK':
                self.black_king_location = (move.start_row, move.start_col)
            # undo enpassant
            if move.en_passant:
                self.board[move.end_row][move.end_col] = '--' # removes the pawn that was added in the wrong square
                self.board[move.start_row][move.end_col] = move.piece_captured # puts the pawn back on the correct square it was captured from
                self.enpassant_possible = (move.end_row, move.end_col) # allow an enpassant to happen on the next move
            #undo a 2 square pawn advance
            if move.piece_moved[1] == 'p' and abs(move.start_row - move.end_row) == 2:
                self.enpassant_possible = ()
    
    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.white_to_move:
            kingRow = self.white_king_location[0]
            kingCol = self.white_king_location[1]
        else:
            kingRow = self.black_king_location[0]
            kingCol = self.black_king_location[1]
        if self.inCheck:
            if len(self.checks) == 1: # only 1 check, block check or move king
                moves = self.getAllPossibleMoves()
                # to block a check you must move a piece into one of the squares between the enemy piece and king
                check = self.checks[0] # check information
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] # enemy piece causing the check
                validSquares = [] # squares that pieces can move to
                # if knight, must capture knight or move king, other pieces can be blocked
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i) # check[2] and check[3] are the check directions
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: # once you get to piece end checks
                            break
                # get rid of any moves that don't block or move king
                for i in range(len(moves) - 1, -1, -1): # go through backwards when you are removing from a list as iterating
                    if moves[i].piece_moved[1] != 'K': # move doesn't move king so it must block or capture
                        if not (moves[i].end_row, moves[i].end_col) in validSquares: # move doesn't block or capture piece
                            moves.remove(moves[i])
            else: # double check, king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else: # not in check so all moves are fine
            moves = self.getAllPossibleMoves()
        
        return moves
    
    '''
    Determine if the current player is in check
    '''
    def inCheck(self):
        if self.white_to_move:
            return self.squareUnderAttack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.squareUnderAttack(self.black_king_location[0], self.black_king_location[1])
    
    '''
    Determine if the enemy can attack the square r, c
    '''
    def squareUnderAttack(self, r, c):
        self.white_to_move = not self.white_to_move # switch to opponent's turn
        oppMoves = self.getAllPossibleMoves()
        self.white_to_move = not self.white_to_move # switch turns back
        for move in oppMoves:
            if move.end_row == r and move.end_col == c: # square is under attack
                return True
        return False
        
    
    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): # number of rows
            for c in range(len(self.board[r])): # number of cols in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) # calls the appropriate move function based on piece type
        return moves
    '''
    Returns if the player is in check, a list of pins, and a list of checks
    '''
    def checkForPinsAndChecks(self):
        pins = [] # squares pinned and the direction its pinned from
        checks = [] # squares where enemy is applying a check
        inCheck = False
        if self.white_to_move:
            enemy_color = "b"
            ally_color = "w"
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = "w"
            ally_color = "b"
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]
        
        # check outward from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = () # reset possible pins
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    endPiece = self.board[end_row][end_col]
                    if endPiece[0] == ally_color and endPiece[1] != 'K':
                        if possible_pin == (): # 1st allied piece could be pinned
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else: # 2nd allied piece, so no no pin or check possible in this direction
                            break
                    elif endPiece[0] == enemy_color:
                        type = endPiece[1]
                        # 5 possibilities here in this complex conditional
                        # 1.) orthogonally away from king and piece is a rook
                        # 2.) diagonally away from king and piece is a bishop
                        # 3.) 1 square away diagonally from king and piece is a pawn
                        # 4.) any direction and piece is a queen
                        # 5.) any direction 1 square away and piece is a king
                        if (0 <= j <= 3 and type == 'R') or \
                            (4 <= j <= 7 and type == 'B') or \
                            (i == 1 and type == 'p' and ((enemy_color == 'w' and 6 <= j <= 7) or (enemy_color == 'b' and 4 <= j <= 5))) or \
                            (type == 'Q') or (i == 1 and type == 'K'):
                            if possible_pin == (): # no piece blocking, so check
                                inCheck = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            else: # piece blocking so pin
                                pins.append(possible_pin)
                                break
                        else: # enemy piece not applying check
                            break
                else:
                    break # off board
        # check for knight checks
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            end_row = start_row + m[0]
            end_col = start_col + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                endPiece = self.board[end_row][end_col]
                if endPiece[0] == enemy_color and endPiece[1] == 'N': # enemy knight attacking
                    inCheck = True
                    checks.append((end_row, end_col, m[0], m[1]))
        return inCheck, pins, checks

    
    '''
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    '''
    def getPawnMoves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        if self.white_to_move:
            move_amount = -1
            start_row = 6
            # backRow = 0
            enemy_color = 'b'
        else:
            move_amount = 1
            start_row = 1
            # backRow = 7
            enemy_color = 'w'
        
        if self.board[r+move_amount][c] == "--": # 1 square move
            if not piece_pinned or pin_direction == (move_amount, 0):
                moves.append(Move((r, c), (r+move_amount, c), self.board))
                if r == start_row and self.board[r+2*move_amount][c] == "--": # 2 square moves
                    moves.append(Move((r,c), (r+2*move_amount, c), self.board))
        if c-1 >= 0: # captures to the left
            if not piece_pinned or pin_direction == (move_amount, -1):
                if self.board[r + move_amount][c - 1][0] == enemy_color:
                    moves.append(Move((r, c), (r+move_amount, c-1), self.board))
                if (r + move_amount, c - 1) == self.enpassant_possible:
                    enpassant = True
                    moves.append(Move((r, c), (r+move_amount, c-1), self.board, en_passant=enpassant))
        if c+1 <= 7: # captures to the right
            if not piece_pinned or pin_direction == (move_amount, +1):
                if self.board[r + move_amount][c + 1][0] == enemy_color:
                    moves.append(Move((r, c), (r+move_amount, c+1), self.board))
                if (r + move_amount, c + 1) == self.enpassant_possible:
                    moves.append(Move((r, c), (r+move_amount, c+1), self.board, en_passant=True))
            
        # if self.whiteToMove: # white pawn moves
        #     if self.board[r-1][c] == "--": # 1 square pawn advance
        #         if not piece_pinned or pin_direction == (-1, 0):
        #             moves.append(Move((r, c), (r-1, c), self.board))
        #             if r == 6 and self.board[r-2][c] == "--": # 2 square pawn advance 
        #                 moves.append(Move((r, c), (r-2, c), self.board))
        #     # captures
        #     if c-1 >= 0: # captures to the left
        #         if self.board[r-1][c-1][0] == 'b': # enemy piece to capture
        #             if not piece_pinned or pin_direction == (-1, -1):
        #                 moves.append(Move((r, c), (r-1, c-1), self.board))
        #     if c+1 <= 7: # captures to the right
        #         if self.board[r-1][c+1][0] == 'b': # enemy piece to capture
        #             if not piece_pinned or pin_direction == (-1, 1):
        #                 moves.append(Move((r, c), (r-1, c+1), self.board))
                        
        # else: # black pawn moves
        #     if self.board[r+1][c] == "--": # 1 square pawn advance
        #         if not piece_pinned or pin_direction == (1, 0):
        #             moves.append(Move((r, c), (r+1, c), self.board))
        #             if r == 1 and self.board[r+2][c] == "--": # 2 square pawn advance 
        #                 moves.append(Move((r, c), (r+2, c), self.board))
        #     # captures
        #     if c-1 >= 0: # captures to the left
        #         if self.board[r+1][c-1][0] == 'w': # enemy piece to capture
        #             if not piece_pinned or pin_direction == (1, -1):
        #                 moves.append(Move((r, c), (r+1, c-1), self.board))
        #     if c+1 <= 7: # captures to the right
        #         if self.board[r+1][c+1][0] == 'w': # enemy piece to capture
        #             if not piece_pinned or pin_direction == (1, 1):
        #                 moves.append(Move((r, c), (r+1, c+1), self.board))
        # # add pawn promotions later
    
    '''
    Get all the rook moves for the rook located at row, col and add these moves to the list
    '''
    def getRookMoves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q': # can't remove queen from pin on rook moves, only remove it on queen moves
                    self.pins.remove(self.pins[i])
                break
                
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) # up, left, down, right 
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8: # on board
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        endPiece = self.board[end_row][end_col]
                        if endPiece == "--": # empty space is valid
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                        elif endPiece[0] == enemy_color: # enemy piece is valid
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break
                        else: # friendly piece is invalid
                            break
                else: # off board
                    break
            
            
    
    '''
    Get all the knight moves for the knight located at row, col and add these moves to the list
    '''
    def getKnightMoves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break
        
        
        directions = ((-2, 1), (-1, 2), (1, 2), (2, 1), # 2 up 1 right, 1 up 2 right, 1 down 2 right, 2 down 1 right, 
                      (2, -1), (1, -2), (-1, -2), (-2, -1)) # 2 down 1 left, 1 down 2 left, 1 up 2 left, 2 up 1 left 
        ally_color = "w" if self.white_to_move else "b"
        for d in directions:
            end_row = r + d[0] 
            end_col = c + d[1] 
            if 0 <= end_row < 8 and 0 <= end_col < 8: # on board
                if not piece_pinned:
                    endPiece = self.board[end_row][end_col]
                    if endPiece[0] != ally_color: # empty or enemy piece, not ally
                        moves.append(Move((r, c), (end_row, end_col), self.board))
    
    '''
    Get all the bishop moves for the bishop located at row, col and add these moves to the list
    '''
    def getBishopMoves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # up and left, up and right, down and left, down and right 
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8: # on board
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        endPiece = self.board[end_row][end_col]
                        if endPiece == "--": # empty space is valid
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                        elif endPiece[0] == enemy_color: # enemy piece is valid
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break
                        else: # friendly piece is invalid
                            break
                else: # off board
                    break
                    
                    
    
    '''
    Get all the queen moves for the queen located at row, col and add these moves to the list
    '''
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves) 
    
    '''
    Get all the king moves for the king located at row, col and add these moves to the list
    '''
    def getKingMoves(self, r, c, moves):
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = "w" if self.white_to_move else "b"
        for i in range(8):
            end_row = r + row_moves[i]
            end_col = c + col_moves[i]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                endPiece = self.board[end_row][end_col]
                if endPiece[0] != ally_color: # not an ally piece (empty or enemy piece)
                    # place king on end square and check for checks
                    if ally_color == "w":
                        self.white_king_location = (end_row, end_col)
                    else:
                        self.black_king_location = (end_row, end_col)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    # place king back on original location 
                    if ally_color == "w":
                        self.white_king_location = (r, c)
                    else:
                        self.black_king_location = (r, c)
                        
        
        
class Move():
    # maps keys to values
    #key: value
    ranksToRows  = {"1": 7, "2": 6, "3": 5, "4": 4,
                    "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, 
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    
    def __init__(self, startSq, endSq, board, en_passant=False):
        self.start_row = startSq[0]
        self.start_col = startSq[1]
        self.end_row = endSq[0]
        self.end_col = endSq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        # Pawn promotion
        self.is_pawn_promotion = (self.piece_moved == 'wp' and self.end_row == 0) or (self.piece_moved == 'bp' and self.end_row == 7)
        # Enpassant
        # self.en_passant = (self.piece_moved[1] == 'p' and (self.end_row, self.end_col) == en_passantPossible)
        self.en_passant = en_passant
        if self.en_passant:
            self.piece_captured = 'wp' if self.piece_moved == 'bp' else 'bp'
        
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
    
    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def getChessNotation(self):
        # if needed, add to this to make it like real chess notation
        return self.getRankFile(self.start_row, self.start_col) + self.getRankFile(self.end_row, self.end_col)
        
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]