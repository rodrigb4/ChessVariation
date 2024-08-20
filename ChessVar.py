# Author: Brenda Rodriguez
# GitHub username: rodrigb4
# Date: 9/14/2023
# Description: This program contains a class ChessVar, which creates instances of ChessVar, which is a playable variant
# of Chess. Users only call on make_move method, entering a proposed move. A variety of tests are performed to check the
# validity of the move. If the move is valid, the move takes place, updating the board, capturing any piece, updating
# game state if necessary, player turn changes (if game has not ended), and True is returned. Otherwise, returns False.


class ChessVar:
    """Represents a modified version of a chess game"""

    def __init__(self):
        """Creates a new ChessVar, with the board and its pieces initialized as below, where 'r' in a piece string
        is for rook, 'k' is for king, 'b' is for bishop, 'h' is for knight, and 'w'/'b' are for white and black,
        respectively. Starts with white's turn, and no pieces captured."""
        self._board = [['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                       ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                       ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                       ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                       ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                       ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                       ['wr', 'wb', 'wh', '  ', '  ', 'bh', 'bb', 'br'],
                       ['wk', 'wb', 'wh', '  ', '  ', 'bh', 'bb', 'bk']]
        self._game_state = 'UNFINISHED'
        self._player_turn = 'white'
        self._captured = []
        self._wk_position = 'a1'
        self._bk_position = 'h1'
        self._wk_at_end = False
        self._bk_at_end = False
        self._index_val = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7,
                           '8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}

    def get_game_state(self):
        """Returns current game state, which can be one of the following: UNFINISHED, BLACK_WON, WHITE_WON, or TIE"""
        return self._game_state

    def get_board(self):
        """Prints visual of current board given all successful moves made"""
        for row in range(len(self._board)):
            print(self._board[row]), '\n'

    def get_player_turn(self):
        """Returns current player's turn"""
        return self._player_turn

    def make_move(self, from_square, to_square):
        """Performs entered move given that all tests pass, proving its validity. If initial tests pass, appropriate
        method is called to perform more tests specific to the piece being moved."""
        column_1 = self._index_val[from_square[0]]
        row_1 = self._index_val[from_square[1]]
        column_2 = self._index_val[to_square[0]]
        row_2 = self._index_val[to_square[1]]
        # initial checks
        if self._board[row_1][column_1][0] != self._player_turn[0]:  # if piece not of player whose turn it is/no piece
            return False
        if self._game_state == 'WHITE_WON' or self._game_state == 'BLACK_WON' or self._game_state == 'TIE':  # game over
            return False
        if self._board[row_2][column_2] != '  ' and self._board[row_2][column_2][0] == self._player_turn[0]:
            return False  # if trying to move onto where one's own piece is
        if self._board[row_2][column_2] != '  ' and self._board[row_2][column_2][1] == 'k':  # can't capture opp's king
            return False

        if self._board[row_1][column_1][1] == 'k':  # if piece trying to move is a KING
            return self.king_move(from_square, to_square)
        elif self._board[row_1][column_1][1] == 'r':  # if piece trying to move is a ROOK
            return self.rook_move(from_square, to_square)
        elif self._board[row_1][column_1][1] == 'b':  # if piece trying to move is a BISHOP
            return self.bishop_move(from_square, to_square)
        elif self._board[row_1][column_1][1] == 'h':  # if piece trying to move is a KNIGHT
            return self.knight_move(from_square, to_square)

    def king_move(self, from_square, to_square):  # moves one square at a time, any direction
        """Specific tests to check validity of proposed move by king. Some tests performed by calling king_check and
        king_final_check methods. If move passes, move is recorded, piece is captured (if any), game state updated if
        ends, or player turn changes (if game not over), and True is returned. Otherwise, returns False."""
        column_1 = self._index_val[from_square[0]]
        row_1 = self._index_val[from_square[1]]
        column_2 = self._index_val[to_square[0]]
        row_2 = self._index_val[to_square[1]]

        if abs(column_2 - column_1) > 1 or abs(row_2 - row_1) > 1:  # if try to move king by more than one square
            return False

        if self._player_turn == 'white':
            other_king_pos = self._bk_position
        else:
            other_king_pos = self._wk_position

        # if move exposes any king to check
        if self.king_check(other_king_pos, from_square, to_square) is False:
            return False
        if self.king_final_check(other_king_pos, from_square, to_square) is False:
            return False
        if self.king_final_check(to_square, from_square, to_square) is False:
            return False

        if self._board[row_2][column_2] != '  ':  # if piece to be captured
            self._captured.append(self._board[row_2][column_2])  # add to list of captured
        self._board[row_2][column_2] = self._board[row_1][column_1]  # move piece to new square
        self._board[row_1][column_1] = '  '  # free previous square

        if self._player_turn == 'black':
            self._bk_position = to_square  # updating king position
            if self._wk_at_end is True:
                if row_2 != 0:
                    self._game_state = 'WHITE_WON'

                else:
                    self._bk_at_end = True
                    self._game_state = 'TIE'

            else:
                if row_2 == 0:
                    self._bk_at_end = True
                    self._game_state = 'BLACK_WON'
                else:
                    self._player_turn = 'white'  # change player turn
            return True

        if self._player_turn == 'white':
            self._wk_position = to_square  # updating king position
            if row_2 == 0:
                self._wk_at_end = True
            self._player_turn = 'black'  # change player turn
            return True

    def rook_move(self, from_square, to_square):  # moves straight in any direction, as far as it can (no jumping)
        """Specific tests to check validity of proposed move by rook. Some tests performed by calling king_final_check
        method. If move passes, move is recorded, piece is captured (if any), game state updated if game ends, or player
         turn changes (if game not over), and True is returned. Otherwise, returns False."""
        column_1 = self._index_val[from_square[0]]
        row_1 = self._index_val[from_square[1]]
        column_2 = self._index_val[to_square[0]]
        row_2 = self._index_val[to_square[1]]

        if column_1 != column_2 and row_1 != row_2:  # if rook trying to move not straight - illegal move
            return False

        if column_1 < column_2:  # if moving right within row (so row_1 == row_2)
            for square in range(column_1 + 1, column_2):
                if self._board[row_1][square] != '  ':  # if trying to jump over other pieces
                    return False

        if row_1 < row_2:  # if moving within column, down (so column_1 == column_2)
            for square in range(row_1 + 1, row_2):
                if self._board[square][column_1] != '  ':  # if trying to jump over other pieces
                    return False

        if column_1 > column_2:  # if moving left within row (so row_1 == row_2)
            for square in range(column_1 - 1, column_2, -1):
                if self._board[row_1][square] != '  ':  # if trying to jump over other pieces
                    return False

        if row_1 > row_2:  # if moving within column, up (so column_1 == column_2)
            for square in range(row_1 - 1, row_2, -1):
                if self._board[square][column_1] != '  ':  # if trying to jump over other pieces
                    return False

        # if desired move puts a king in check
        if self.king_final_check(self._wk_position, from_square, to_square) is False:
            return False
        if self.king_final_check(self._bk_position, from_square, to_square) is False:
            return False

        if self._board[row_2][column_2] != '  ':  # if piece to be captured
            self._captured.append(self._board[row_2][column_2])  # add to list of captured
        self._board[row_2][column_2] = self._board[row_1][column_1]  # move piece to new square
        self._board[row_1][column_1] = '  '  # free previous square

        if self._wk_at_end is True:
            self._game_state = 'WHITE_WON'
            return True

        if self._player_turn == 'white':  # change player turn
            self._player_turn = 'black'
        else:
            self._player_turn = 'white'
        return True

    def bishop_move(self, from_square, to_square):  # moves only diagonally, as far as it can (no jumping)
        """Specific tests to check validity of proposed move by bishop. Some tests performed by calling king_final_check
        method. If move passes, move is recorded, piece is captured (if any), game state updated if game ends, or player
         turn changes (if game not over), and True is returned. Otherwise, returns False."""
        column_1 = self._index_val[from_square[0]]
        row_1 = self._index_val[from_square[1]]
        column_2 = self._index_val[to_square[0]]
        row_2 = self._index_val[to_square[1]]

        # if abs(column_2 - column_1) / abs(row_2 - row_1) != 1:
        if abs(column_2 - column_1) != abs(row_2 - row_1):  # if attempt moving non-diagonally (checks slope)
            return False

        if column_2 > column_1 and row_2 > row_1:  # moving down right diagonally
            for chn in range(1, column_2 - column_1):  # chn = change
                if self._board[row_1 + chn][column_1 + chn] != '  ':  # if attempting jumping over pieces
                    return False
        if column_2 < column_1 and row_2 < row_1:  # moving left up diagonally
            for chn in range(1, abs(column_2 - column_1)):
                if self._board[row_1 - chn][column_1 - chn] != '  ':  # if attempting jumping over pieces
                    return False
        if column_2 > column_1 and row_2 < row_1:  # moving right up diagonally
            for chn in range(1, abs(column_2 - column_1)):
                if self._board[row_1 - chn][column_1 + chn] != '  ':  # if attempting jumping over pieces
                    return False
        if column_2 < column_1 and row_2 > row_1:  # moving down left diagonally
            for chn in range(1, abs(column_2 - column_1)):
                if self._board[row_1 + chn][column_1 - chn] != '  ':
                    return False

        # if desired move puts a king in check
        if self.king_final_check(self._wk_position, from_square, to_square) is False:
            return False
        if self.king_final_check(self._bk_position, from_square, to_square) is False:
            return False

        if self._board[row_2][column_2] != '  ':  # if piece to be captured
            self._captured.append(self._board[row_2][column_2])  # add to list of captured
        self._board[row_2][column_2] = self._board[row_1][column_1]  # move piece to new square
        self._board[row_1][column_1] = '  '  # free previous square

        if self._wk_at_end is True:
            self._game_state = 'WHITE_WON'
            return True

        if self._player_turn == 'white':  # change player turn
            self._player_turn = 'black'
        else:
            self._player_turn = 'white'
        return True

    def knight_move(self, from_square, to_square):  # moves in L-shape, can jump over
        """Specific tests to check validity of proposed move by knight. Some tests performed by calling king_final_check
        method. If move passes, move is recorded, piece is captured (if any), game state updated if game ends, or player
         turn changes (if game not over), and True is returned. Otherwise, returns False."""
        column_1 = self._index_val[from_square[0]]
        row_1 = self._index_val[from_square[1]]
        column_2 = self._index_val[to_square[0]]
        row_2 = self._index_val[to_square[1]]
        l_check_1 = abs(column_2 - column_1) == 2 and abs(row_2 - row_1) == 1
        l_check_2 = abs(row_2 - row_1) == 2 and abs(column_2 - column_1) == 1
        l_check = l_check_1 or l_check_2  # checks for L-shape

        if l_check is False:  # if move is not an L-shape
            return False

        # if desired move puts a king in check
        if self.king_final_check(self._wk_position, from_square, to_square) is False:
            return False
        if self.king_final_check(self._bk_position, from_square, to_square) is False:
            return False

        if self._board[row_2][column_2] != '  ':  # if piece to be captured
            self._captured.append(self._board[row_2][column_2])  # add to list of captured
        self._board[row_2][column_2] = self._board[row_1][column_1]  # move piece to new square
        self._board[row_1][column_1] = '  '  # free previous square

        if self._wk_at_end is True:
            self._game_state = 'WHITE_WON'
            return True

        if self._player_turn == 'white':  # change player turn
            self._player_turn = 'black'
        else:
            self._player_turn = 'white'
        return True

    def king_check(self, position, from_square, to_square):
        """Tests if proposed move would put expose each king to check by the other (one space away from each other). If
        a test fails, returns False."""
        column_0 = self._index_val[position[0]]  # position: of king not getting moved
        row_0 = self._index_val[position[1]]
        column_1 = self._index_val[from_square[0]]
        row_1 = self._index_val[from_square[1]]
        column_2 = self._index_val[to_square[0]]  # to_square: proposed position of king player is attempting to move
        row_2 = self._index_val[to_square[1]]

        # faking move to test
        temp_hold = self._board[row_2][column_2]  # holding 'captured' piece/blank space
        self._board[row_2][column_2] = self._board[row_1][column_1]
        self._board[row_1][column_1] = '  '

        if abs(column_2 - column_0) == 1 and row_2 - row_0 == 0:  # if one space away horizontally
            self._board[row_1][column_1] = self._board[row_2][column_2]  # undoing move
            self._board[row_2][column_2] = temp_hold
            return False
        if column_2 - column_0 == 0 and abs(row_2 - row_0) == 1:  # if one space away vertically
            self._board[row_1][column_1] = self._board[row_2][column_2]  # undoing move
            self._board[row_2][column_2] = temp_hold
            return False
        if abs(column_2 - column_0) == 1 and abs(row_2 - row_0) == 1:  # if one space away diagonally
            self._board[row_1][column_1] = self._board[row_2][column_2]  # undoing move
            self._board[row_2][column_2] = temp_hold
            return False

        self._board[row_1][column_1] = self._board[row_2][column_2]  # undoing move regardless
        self._board[row_2][column_2] = temp_hold

    def king_final_check(self, position, from_square, to_square):  # position is king's position
        """Tests if proposed move by piece in question would expose either king to check. To perform tests, calls on
        knight_check, bishop_check, and rook_check methods. If a test fails, returns False."""
        column_1 = self._index_val[from_square[0]]
        row_1 = self._index_val[from_square[1]]
        column_2 = self._index_val[to_square[0]]  # to_square: proposed position of piece player is attempting to move
        row_2 = self._index_val[to_square[1]]

        # faking move to check against all pieces
        temp_hold = self._board[row_2][column_2]  # holding 'captured' piece/blank space
        self._board[row_2][column_2] = self._board[row_1][column_1]
        self._board[row_1][column_1] = '  '

        if self.knight_check(position) is False:
            self._board[row_1][column_1] = self._board[row_2][column_2]  # undoing move
            self._board[row_2][column_2] = temp_hold
            return False
        if self.bishop_check(position) is False:
            self._board[row_1][column_1] = self._board[row_2][column_2]  # undoing move
            self._board[row_2][column_2] = temp_hold
            return False
        if self.rook_check(position) is False:
            self._board[row_1][column_1] = self._board[row_2][column_2]  # undoing move
            self._board[row_2][column_2] = temp_hold
            return False

        self._board[row_1][column_1] = self._board[row_2][column_2]  # undoing move regardless
        self._board[row_2][column_2] = temp_hold

    def rook_check(self, position):  # position: of king being tested for exposure to check from proposed move
        """Testing if proposed move would put either king in check by a rook. If so, returns False."""
        column = self._index_val[position[0]]
        row = self._index_val[position[1]]

        for chn in range(1, len(self._board)):  # chn = change, straight down
            new_row = row + chn < len(self._board)
            if new_row and self._board[row + chn][column] != '  ':  # testing if first piece in this path is opp's rook
                if self._board[row][column] == 'wk' and self._board[row + chn][column] == 'br':
                    return False
                if self._board[row][column] == 'bk' and self._board[row + chn][column] == 'wr':
                    return False
                break  # if above doesn't return False, still stops this loop b/c don't need to keep going
            if new_row is False:  # if out of bounds of board
                break
        for chn in range(1, len(self._board)):  # straight up
            new_row = row - chn >= 0
            if new_row and self._board[row - chn][column] != '  ':  # testing if first piece in this path is opp's rook
                if self._board[row][column] == 'wk' and self._board[row - chn][column] == 'br':
                    return False
                if self._board[row][column] == 'bk' and self._board[row - chn][column] == 'wr':
                    return False
                break
            if new_row is False:
                break
        for chn in range(1, len(self._board)):  # straight right
            new_column = column + chn < len(self._board)
            if new_column and self._board[row][column + chn] != '  ':  # testing if first piece in path is opp's rook
                if self._board[row][column] == 'wk' and self._board[row][column + chn] == 'br':
                    return False
                if self._board[row][column] == 'bk' and self._board[row][column + chn] == 'wr':
                    return False
                break
            if new_column is False:
                break
        for chn in range(1, len(self._board)):  # straight left
            new_column = column - chn >= 0
            if new_column and self._board[row][column - chn] != '  ':  # testing if first piece in path is opp's rook
                if self._board[row][column] == 'wk' and self._board[row][column - chn] == 'br':
                    return False
                if self._board[row][column] == 'bk' and self._board[row][column - chn] == 'wr':
                    return False
                break
            if new_column is False:
                break
        return True

    def bishop_check(self, position):  # position: of king being tested for exposure to check from proposed move
        """Testing if proposed move would put either king in check by a bishop. If so, returns False."""
        column = self._index_val[position[0]]
        row = self._index_val[position[1]]

        for chn in range(1, len(self._board)):  # chn = change, down-right diagonal
            new_row = row + chn < len(self._board)
            new_column = column + chn < len(self._board)
            if new_row and new_column and self._board[row + chn][column + chn] != '  ':
                if self._board[row][column] == 'wk' and self._board[row + chn][column + chn] == 'bb':
                    return False
                if self._board[row][column] == 'bk' and self._board[row + chn][column + chn] == 'wb':
                    return False
                break
            if new_row is False or new_column is False:
                break
        for chn in range(1, len(self._board)):  # up-left diagonal
            new_row = row - chn >= 0
            new_column = column - chn >= 0
            if new_row and new_column and self._board[row - chn][column - chn] != '  ':
                if self._board[row][column] == 'wk' and self._board[row - chn][column - chn] == 'bb':
                    return False
                if self._board[row][column] == 'bk' and self._board[row - chn][column - chn] == 'wb':
                    return False
                break
            if new_row is False or new_column is False:
                break
        for chn in range(1, len(self._board)):  # up-right diagonal
            new_row = row - chn >= 0
            new_column = column + chn < len(self._board)
            if new_row and new_column and self._board[row - chn][column + chn] != '  ':
                if self._board[row][column] == 'wk' and self._board[row - chn][column + chn] == 'bb':
                    return False
                if self._board[row][column] == 'bk' and self._board[row - chn][column + chn] == 'wb':
                    return False
                break
            if new_row is False or new_column is False:
                break
        for chn in range(1, len(self._board)):  # down-left diagonal
            new_row = row + chn < len(self._board)
            new_column = column - chn >= 0
            if new_row and new_column and self._board[row + chn][column - chn] != '  ':
                if self._board[row][column] == 'wk' and self._board[row + chn][column - chn] == 'bb':
                    return False
                if self._board[row][column] == 'bk' and self._board[row + chn][column - chn] == 'wb':
                    return False
                break
            if new_row is False or new_column is False:
                break
        return True

    def knight_check(self, position):  # position: of king being tested for exposure to check from proposed move
        """Testing if proposed move would put either king in check by a knight. If so, returns False."""
        column = self._index_val[position[0]]
        row = self._index_val[position[1]]

        row_less_1 = row - 1 >= 0  # tests if in bounds
        row_less_2 = row - 2 >= 0
        row_plus_1 = row + 1 < len(self._board)
        row_plus_2 = row + 2 < len(self._board)
        column_less_1 = column - 1 >= 0
        column_less_2 = column - 2 >= 0
        column_plus_1 = column + 1 < len(self._board)
        column_plus_2 = column + 2 < len(self._board)

        if self._board[row][column] == 'wk':
            if row_plus_1 and column_plus_2 and self._board[row + 1][column + 2] == 'bh':  # right-down
                return False
            if row_less_1 and column_plus_2 and self._board[row - 1][column + 2] == 'bh':  # right-up
                return False
            if row_plus_2 and column_plus_1 and self._board[row + 2][column + 1] == 'bh':  # down-right
                return False
            if row_plus_2 and column_less_1 and self._board[row + 2][column - 1] == 'bh':  # down-left
                return False
            if row_less_2 and column_plus_1 and self._board[row - 2][column + 1] == 'bh':  # up-right
                return False
            if row_less_2 and column_less_1 and self._board[row - 2][column - 1] == 'bh':  # up-left
                return False
            if row_plus_1 and column_less_2 and self._board[row + 1][column - 2] == 'bh':  # left-down
                return False
            if row_less_1 and column_less_2 and self._board[row - 1][column - 2] == 'bh':  # left-up
                return False

        if self._board[row][column] == 'bk':
            if row_plus_1 and column_plus_2 and self._board[row + 1][column + 2] == 'wh':  # right-down
                return False
            if row_less_1 and column_plus_2 and self._board[row - 1][column + 2] == 'wh':  # right-up
                return False
            if row_plus_2 and column_plus_1 and self._board[row + 2][column + 1] == 'wh':  # down-right
                return False
            if row_plus_2 and column_less_1 and self._board[row + 2][column - 1] == 'wh':  # down-left
                return False
            if row_less_2 and column_plus_1 and self._board[row - 2][column + 1] == 'wh':  # up-right
                return False
            if row_less_2 and column_less_1 and self._board[row - 2][column - 1] == 'wh':  # up-left
                return False
            if row_plus_1 and column_less_2 and self._board[row + 1][column - 2] == 'wh':  # left-down
                return False
            if row_less_1 and column_less_2 and self._board[row - 1][column - 2] == 'wh':  # left-up
                return False
        return True
    