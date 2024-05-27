import random

piece_score = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

'''
Picks and returns a random moves
'''
def findRandomMove(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves) - 1)]

'''
Find the best move based on material alone
'''
def findBestMoveMinMaxNoRecursion(gs, valid_moves):
    turn_multiplier = 1 if gs.white_to_move else -1
    opponent_minmax_score = CHECKMATE
    best_player_move = None
    random.shuffle(valid_moves)
    for player_move in valid_moves:
        gs.makeMove(player_move)
        opponents_moves = gs.getValidMoves()
        if gs.stalemate:
            opponent_max_score = STALEMATE
        elif gs.checkmate:
            opponent_max_score = -CHECKMATE
        else:
            opponent_max_score = -CHECKMATE
            for opponents_move in opponents_moves: 
                gs.makeMove(opponents_move)
                gs.getValidMoves
                if gs.checkmate:
                    score = CHECKMATE
                elif gs.stalemate:
                    score = STALEMATE
                else:
                    score = -turn_multiplier * scoreMaterial(gs.board)
                if score > opponent_max_score:
                    opponent_max_score = score
                gs.undoMove()
        if opponent_max_score < opponent_minmax_score:
            opponent_minmax_score = opponent_max_score
            best_player_move = player_move
        gs.undoMove()
    return best_player_move

'''
Helper method to make the first recursive call
'''
def findBestMove(gs, valid_moves):
    global next_move, counter
    next_move = None
    random.shuffle(valid_moves)
    counter = 0
    # findMoveMinMax(gs, valid_moves, DEPTH, gs.white_to_move)
    findMoveNegaMax(gs, valid_moves, DEPTH, 1 if gs.white_to_move else -1)
    # findMoveNegaMaxAlphaBeta(gs, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.white_to_move else -1)
    print(counter)
    return next_move

def findMoveMinMax(gs, valid_moves, depth, white_to_move):
    global next_move
    if depth == 0:
        return scoreMaterial(gs.board)
    
    if white_to_move:
        max_score = -CHECKMATE
        for move in valid_moves:
            gs.makeMove(move)
            next_moves = gs.getValidMoves()
            score = findMoveMinMax(gs, next_moves, depth - 1, False)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undoMove()
        return max_score
    
    else:
        min_score = CHECKMATE
        for move in valid_moves:
            gs.makeMove(move)
            next_moves = gs.getValidMoves()
            score = findMoveMinMax(gs, next_moves, depth - 1, True)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undoMove()
        return min_score


def findMoveNegaMax(gs, valid_moves, depth, turn_multiplier):
    global next_move, counter
    counter += 1
    if depth == 0:
        return turn_multiplier * scoreBoard(gs)
    
    max_score = -CHECKMATE
    for move in valid_moves:
        gs.makeMove(move)
        next_moves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, next_moves, depth-1, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undoMove()
    return max_score


def findMoveNegaMaxAlphaBeta(gs, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move, counter
    if depth == 0:
        return turn_multiplier * scoreBoard(gs)
    counter += 1
    # move ordering - implement later
    max_score = -CHECKMATE
    for move in valid_moves:
        gs.makeMove(move)
        next_moves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, next_moves, depth-1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undoMove()
        if max_score > alpha: # pruning happens
            alpha = max_score
        if alpha >= beta:
            break
    return max_score

'''
A positive score is good for white, a negative score is good for black
'''
def scoreBoard(gs):
    if gs.checkmate:
        if gs.white_to_move:
            return -CHECKMATE # black wins
        else:
            return CHECKMATE # white wins
    elif gs.stalemate:
        return STALEMATE
    
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]
    
    return score


'''
Score the board based on material
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]
    
    return score