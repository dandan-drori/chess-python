class GameState():
    def __init__(self):
        # board is an 8x8 2d list
        # each piece is represented as a 2 letter string
        # first letter is color - 'b' or 'w' for black or white
        # second letter is type - 'p', 'R', 'N', 'B', 'Q', 'K'
        # '--' represents an empty square
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.move_functions = {'p': self.get_pawn_moves, 'R': self.get_rook_moves, 'B': self.get_bishop_moves,
                               'N': self.get_knight_moves, 'K': self.get_king_moves, 'Q': self.get_queen_moves}
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)

    def make_move(self, move):
        # make the square where the piece started empty
        self.board[move.start_row][move.start_col] = "--"
        # replace the piece where the piece ended with the new one
        self.board[move.end_row][move.end_col] = move.piece_moved
        # add move to move_log
        self.move_log.append(move)
        # swap players turns
        self.white_to_move = not self.white_to_move
        # update the king's location if moved
        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)

    def undo_move(self):
        if len(self.move_log) != 0:
            last_move = self.move_log.pop()
            self.board[last_move.start_row][last_move.start_col] = last_move.piece_moved
            self.board[last_move.end_row][last_move.end_col] = last_move.piece_captured
            self.white_to_move = not self.white_to_move
            # update the king's location if moved
            if last_move.piece_moved == 'wK':
                self.white_king_location = (
                    last_move.start_row, last_move.start_col)
            elif last_move.piece_moved == 'bK':
                self.black_king_location = (
                    last_move.start_row, last_move.start_col)

    # all moves considering checks
    def get_valid_moves(self):
        moves = self.get_all_possible_moves()

        # when removing from a list, go backwards through the list
        for i in range(len(moves)-1, -1, -1):
            self.make_move(moves[i])

            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(moves[i])

            self.white_to_move = not self.white_to_move
            self.undo_move()

        return moves

    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.white_king_location[1])

    def square_under_attack(self, row, col):
        # switch to opponent to check his moves
        self.white_to_move = not self.white_to_move
        opponent_moves = self.get_all_possible_moves()
        # switch turns back
        self.white_to_move = not self.white_to_move
        for move in opponent_moves:
            if move.end_row == row and move.end_col == col:  # square is under attack
                self.white_to_move = not self.white_to_move  # switch back turns
                return True
        return False

    # all moves without considering checks
    def get_all_possible_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[row][col][1]
                    # call the appropriate move function based on piece type
                    self.move_functions[piece](row, col, moves)
        return moves

    def get_pawn_moves(self, row, col, moves):
        if self.white_to_move:
            if self.board[row - 1][col] == '--':
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == '--':
                    moves.append(Move((row, col), (row - 2, col), self.board))
            if col - 1 >= 0:
                if self.board[row - 1][col - 1][0] == 'b':
                    moves.append(
                        Move((row, col), (row - 1, col - 1), self.board))
            if col + 1 < len(self.board[row]):
                if self.board[row - 1][col + 1][0] == 'b':
                    moves.append(
                        Move((row, col), (row - 1, col + 1), self.board))
        else:
            if self.board[row + 1][col] == '--':
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == '--':
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == 'w':
                    moves.append(
                        Move((row, col), (row + 1, col - 1), self.board))
            if col + 1 < len(self.board[row]):
                if self.board[row + 1][col + 1][0] == 'w':
                    moves.append(
                        Move((row, col), (row + 1, col + 1), self.board))
        # add pawn promotions later

    def get_rook_moves(self, row, col, moves):
        # up, left, down, right
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:  # on board
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # empty space at end square - valid
                        moves.append(Move((row, col),
                                          (end_row, end_col), self.board))
                    # enemy piece at end square - valid
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((row, col),
                                          (end_row, end_col), self.board))
                        break
                    else:  # frienly piece at end square - invalid
                        break
                else:  # off board
                    break

    def get_bishop_moves(self, row, col, moves):
        # up, left, down, right
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:  # on board
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # empty space at end square - valid
                        moves.append(Move((row, col),
                                          (end_row, end_col), self.board))
                    # enemy piece at end square - valid
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((row, col),
                                          (end_row, end_col), self.board))
                        break
                    else:  # frienly piece at end square - invalid
                        break
                else:  # off board
                    break

    def get_knight_moves(self, row, col, moves):
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                        (1, -2), (1, 2), (2, -1), (2, 1))
        ally_color = 'w' if self.white_to_move else 'b'
        for m in knight_moves:
            end_row = row + m[0]
            end_col = col + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # not an ally piece - empty or enemy piece
                    moves.append(
                        Move((row, col), (end_row, end_col), self.board))

    def get_king_moves(self, row, col, moves):
        king_moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1))
        ally_color = 'w' if self.white_to_move else 'b'
        for i in range(8):
            end_row = row + king_moves[i][0]
            end_col = col + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                # not an ally piece - empty or enemy piece
                if end_piece[0] != ally_color:
                    moves.append(
                        Move((row, col), (end_row, end_col), self.board))

    def get_queen_moves(self, row, col, moves):
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)


class Move():
    # map board indices to standard chess location notation
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * \
            100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, column):
        return self.cols_to_files[column] + self.rows_to_ranks[row]
