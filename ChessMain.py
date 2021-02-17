import pygame as p
from ChessEngine import GameState
from ChessEngine import Move

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15

IMAGES = {}


def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ',
              'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(
            "Assets/Pieces/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False  # flag for when a move is made
    load_images()

    sq_selected = ()
    player_clicks = []
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            # mouse handlers
            elif event.type == p.MOUSEBUTTONDOWN:
                mouse_location = p.mouse.get_pos()
                col = mouse_location[0]//SQ_SIZE
                row = mouse_location[1]//SQ_SIZE
                if sq_selected == (row, col):  # the user clicked the same square twice
                    sq_selected = ()  # clear selection
                    player_clicks = []  # clear player clicks
                else:
                    sq_selected = (row, col)
                    # append for both 1st and 2nd clicks
                    player_clicks.append(sq_selected)

                if len(player_clicks) == 2:
                    move = Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation())
                    if move in valid_moves:
                        gs.make_move(move)
                        move_made = True
                        sq_selected = ()  # reset user selection
                        player_clicks = []  # reset player clicks
                    else:
                        player_clicks = [sq_selected]
            # key handlers
            elif event.type == p.KEYDOWN:
                if event.key == p.K_u:
                    gs.undo_move()
                    move_made = True
        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row+column) % 2)]
            p.draw.rect(screen, color, p.Rect(
                column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(
                    column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
