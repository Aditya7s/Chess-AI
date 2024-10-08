"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
import ChessEngine, SmartMoveFinder
BOARD_WIDTH = BOARD_HEIGHT = 512 # 400 is another option
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8 # dimeensions of a chess board are 8x8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15 # for animations later on
IMAGES = {}

'''
initialize a global dictionary of images. This will be called exactly once in the main
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))
    # Note: we can access an image by saying 'IMAGES['wp']'

'''
The main driver for our code. This will handle user input and updating the graphics
'''
def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    move_log_font = p.font.SysFont("Arial", 14, False, False)
    gs = ChessEngine.GameState()
    valid_moves = gs.getValidMoves()
    move_made = False # flag variable for when a move is made
    animate = False # flag variable for when we should animate a move
    
    loadImages() # only do this once, before the while loop
    sq_selected = () # no square is selected, keep track of the last click of the user (tuple: (row, column))
    player_clicks = [] # keep track of player clicks (two tuples: [(6,4), (4,4)])
    running = True
    game_over = False
    player_one = True # If a Human is playing white, then this will be True. if an AI is playing, then this will be false
    player_two = False # Same as above but for black
    while running:
        human_turn = (gs.white_to_move and player_one) or (not gs.white_to_move and player_two)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over and human_turn:
                    location = p.mouse.get_pos() # (x, y) location of mouse
                    col = location[0] // SQ_SIZE 
                    row = location[1] // SQ_SIZE
                    if sq_selected == (row, col) or col >= 8: # the user clicked the same square twice or use clicked move log
                        sq_selected = () # deselect
                        player_clicks = [] # clear player clicks
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected) # append for both 1st and 2nd clicks
                    if len(player_clicks) == 2: # after 2nd click
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(valid_moves)): 
                            if move == valid_moves[i]:
                                gs.makeMove(valid_moves[i])
                                move_made = True
                                animate = True
                                sq_selected = () # reset user clicks
                                player_clicks = []
                        if not move_made:
                            player_clicks = [sq_selected] # reset
            
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when 'z' is pressed
                    gs.undoMove()
                    move_made = True
                    animate = False
                    game_over = False
                if e.key == p.K_r: # reset the board when 'r' is pressed
                    gs = ChessEngine.GameState()
                    valid_moves = gs.getValidMoves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
        
        # AI move finder
        if not game_over and not human_turn:
            AI_move = SmartMoveFinder.findBestMove(gs, valid_moves)
            if AI_move is None:
                AI_move = SmartMoveFinder.findRandomMove(valid_moves)
            gs.makeMove(AI_move)
            move_made = True
            animate = True
            print(AI_move.getChessNotation())
        
        if move_made:
            if animate:
                animateMove(gs.move_log[-1], screen, gs.board, clock)
            valid_moves = gs.getValidMoves()
            move_made = False
            animate = False
                
        drawGameState(screen, gs, valid_moves, sq_selected, move_log_font)
        
        if gs.checkmate or gs.stalemate:
            game_over = True
            drawEndGameText(screen, 'Stalemate' if gs.stalemate else 'Black wins by checkmate' if gs.white_to_move else 'White wins by checkmate')


        
        clock.tick(MAX_FPS) 
        p.display.flip()

'''
Responsible for all the graphics within a current game state
'''
def drawGameState(screen, gs, valid_moves, sq_selected, move_log_font):
    drawBoard(screen) # draw squares on the board
    highlightSquares(screen, gs, valid_moves, sq_selected) # highlight selected squares and moves available
    drawPieces(screen, gs.board) # draw pieces on top of those squares
    drawMoveLog(screen, gs, move_log_font)

'''
Draw the squares on the board. The top left square is always light.
'''
def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Highlight square selected and moves for piece selecgted
'''
def highlightSquares(screen, gs, valid_moves, sq_selected):
    if sq_selected != ():
        r, c, = sq_selected
        if gs.board[r][c][0] == ('w' if gs.white_to_move else 'b'): # sq_selected is a piece that can be moved
            # highlight selectted square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # transparency value -> 0 transparent; 255 opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col*SQ_SIZE, move.end_row*SQ_SIZE))

'''
Draw the pieces on the board using the current GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": # not an empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draws the move log
'''
def drawMoveLog(screen, gs, font):
    move_log_rect = p.Rect(BOARD_HEIGHT, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), move_log_rect)
    move_log = gs.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i//2 + 1) + ". " + str(move_log[i]) + " "
        if i+1 < len(move_log): # make sure black made a move
            move_string += str(move_log[i+1]) + "  "
        move_texts.append(move_string)
    
    moves_per_row = 3
    padding = 5
    line_spacing = 2
    textY = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i+j]
        textObject = font.render(text, True, p.Color('white'))
        textLocation = move_log_rect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + line_spacing

'''
Animating a move
'''
def animateMove(move, screen, board, clock):
    global colors
    coords = [] # list of coords that the animation will move through
    dR = move.end_row - move.start_row
    dC = move.end_col - move.start_col
    frames_per_square = 10 # 10 frames per square the piece moves through
    frame_count = (abs(dR) + abs(dC)) * frames_per_square
    for frame in range(frame_count + 1):
        r, c = (move.start_row + dR*frame/frame_count, move.start_col + dC*frame/frame_count)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col*SQ_SIZE, move.end_row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            if move.en_passant:
                enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row -1
                end_square = p.Rect(move.end_col*SQ_SIZE, enpassant_row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(240)
        
def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, False, p.Color('Gray'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width()/2, BOARD_HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))
    

if __name__ == "__main__":
    main()