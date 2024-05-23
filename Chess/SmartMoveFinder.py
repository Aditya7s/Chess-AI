import random

piece_score = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0

'''
Picks and returns a random moves
'''
def findRandomMove(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves) - 1)]

'''
Find the best move based on material alone
'''
def findBestMove(gs, valid_moves):
    turn_multiplier = 1 if gs.white_to_move else -1
    opponent_minmax_score = CHECKMATE
    best_player_move = None
    random.shuffle(valid_moves)
    for player_move in valid_moves:
        gs.makeMove(player_move)
        opponents_moves = gs.getValidMoves()

        opponent_max_score = -CHECKMATE
        for opponents_move in opponents_moves: 
            gs.makeMove(opponents_move)
            if gs.checkmate:
                score = -turn_multiplier * CHECKMATE
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