'''
Check-it-all -- a graphical game of Checkers.
The program implements the main function of this project
-- handling both user and computer moves.
'''
import turtle
from draw import Draw
from state import GameState
from piece import Piece


NUM_SQUARES = 8  # The number of squares on each row.
SQUARE = 50  # The size of each square in the checkerboard.
SQUARE_COLORS = ("light gray", "white")
# PIECE_COLOR = {BLACK: "black", RED: "firebrick"}
EMPTY = ""
BLACK = "black"
RED = "red"
NESTED_LIST = [
    [EMPTY, BLACK, EMPTY, BLACK, EMPTY, BLACK, EMPTY, BLACK],
    [BLACK, EMPTY, BLACK, EMPTY, BLACK, EMPTY, BLACK, EMPTY],
    [EMPTY, BLACK, EMPTY, BLACK, EMPTY, BLACK, EMPTY, BLACK],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [RED, EMPTY, RED, EMPTY, RED, EMPTY, RED, EMPTY],
    [EMPTY, RED, EMPTY, RED, EMPTY, RED, EMPTY, RED],
    [RED, EMPTY, RED, EMPTY, RED, EMPTY, RED, EMPTY],
]


# Black(User) plays first
current_state = GameState(BLACK, GameState.INITIAL_STATE)


def convert_to_index(x, y):
    '''
        Function -- convert_to_index
            Called when a click occurs. Convert current cartesian coordinates
            to matrix indices.
        Parameters:
            x -- X coordinate of the click. Auto provided by Turtle.
            y -- Y coordinate of the click. Auto provided by Turtle.
        Returns:
            An indices pair denoting row and column.
    '''
    corner = NUM_SQUARES * SQUARE / 2
    convert_x = x + corner
    convert_y = y + corner
    if x <= -corner or x >= corner or y <= -corner or y >= corner:
        return None
    else:
        col = int(convert_x // SQUARE)
        row = int(convert_y // SQUARE)
        return (row, col)


def convert_to_cartesian(index_pair):
    '''
        Function -- convert_to_cartesian
            Called when a click occurs. Convert current indices pair (row, col)
            into corresponding cartesian pair (x, y).
        Parameters:
            index pair -- A pair of indices indicating current location
        Returns:
            An indices pair denoting row and column.
    '''
    corner = NUM_SQUARES * SQUARE / 2
    y = index_pair[0] * SQUARE - corner
    x = index_pair[1] * SQUARE - corner
    return (x, y)


def initiate_squares(current_state, nested_list):
    '''
        Function -- initiate_squares
            Initiate squares in initial game state, a nested list.
        Parameter:
            current_state -- An object of GameState class
            nested_list -- The game board
    '''
    initiate_squares = []
    for i in range(len(nested_list)):
        row = nested_list[i]
        list_in_row = []
        for j in range(len(row)):
            col = row[j]
            if col == EMPTY:
                list_in_row.append(None)
            else:
                piece = Piece(col, False, (i, j))
                list_in_row.append(piece)
        initiate_squares.append(list_in_row)
    current_state.squares = initiate_squares


def ai_move(pen, ai_state):
    '''
        Function -- ai_move
            Moves implemented automatically by computer player
        Parameters:
            pen -- An instance of turtle
            ai_state -- An object of GameState representing AI moves
    '''
    move = None
    current_player = ai_state.current_player
    piece_locations = ai_state.piece_locations_by_player[current_player]
    for piece_location in piece_locations:
        possible_moves = ai_state.find_possible_moves(piece_location)
        if len(possible_moves) != 0:
            # Use the first possible move if it exists
            move = possible_moves[0]
            ai_state.possible_moves = possible_moves
            break

    if move is None:
        winner = ai_state.get_enemy_color(ai_state.current_player)
        pen.claim_winner(winner)
        return

    while move is not None:
        origin_xy = convert_to_cartesian(move.start)
        target_xy = convert_to_cartesian(move.end)

        pen.draw_empty_square(origin_xy)

        ai_state.move(move)
        is_king = ai_state.get_square_by_location(move.end).is_king

        pen.draw_actual_move(target_xy, ai_state.current_player, is_king)

        if move.is_capture:
            captured_xy = convert_to_cartesian(move.captured_location)
            pen.draw_empty_square(captured_xy)
            # check if there is next capturing move
            next_possible_moves = ai_state.find_possible_moves(move.end)

            moves_left = len(next_possible_moves)
            if moves_left != 0 and \
                    ai_state.is_valid_move(next_possible_moves[0]):
                ai_state.possible_moves = next_possible_moves
                move = next_possible_moves[0]
            else:
                move = None
        else:
            move = None

    # determine if game is over
    winner = current_state.who_wins()
    if winner is None:
        # end this round for current player
        current_state.next_round()
    else:
        pen.claim_winner(winner)


def click_handler(x, y):
    '''
        Function -- click_handler
            Called when a click occurs.
        Parameters:
            x -- X coordinate of the click. Automatically provided by Turtle.
            y -- Y coordinate of the click. Automatically provided by Turtle.
        Returns:
            Does not and should not return. Click handlers are a special type
            of function automatically called by Turtle. You will not have
            access to anything returned by this function.
    '''
    turt = turtle.Turtle()
    turt.penup()
    pen = Draw(turt)
    # Clean up red possible move squares before taking action
    for move in current_state.possible_moves:
        cartesian_location = convert_to_cartesian(move.end)
        pen.outline_possible_move(cartesian_location, "black")

    # Convert cartesian coordinate to location in squares
    current_location = convert_to_index(x, y)

    # Do nothing if location is invalid
    in_bounds = current_state.is_in_bounds(current_location)
    if current_location is None or not in_bounds:
        return

    move = current_state.get_move_by_end_location(current_location)
    if move is None:
        start_square = current_state.get_square_by_location(current_location)
        # No possible moves if current square is empty or enemy piece
        if start_square is None or \
                start_square.color != current_state.current_player:
            return
        current_state.possible_moves = \
            current_state.find_possible_moves(current_location)
        # Draw the outline of possible moves
        for move in current_state.possible_moves:
            cartesian_location = convert_to_cartesian(move.end)
            pen.outline_possible_move(cartesian_location, "red")
    else:
        if not current_state.is_valid_move(move):
            # if the selected move is not valid, gives feedback and return
            print("Not valid move. Capture move must be made if available.")
            return

        # move the piece if it is valid move
        origin_xy = convert_to_cartesian(move.start)
        target_xy = convert_to_cartesian(move.end)
        # clean up current square:
        pen.draw_empty_square(origin_xy)

        current_state.move(move)
        is_king = current_state.get_square_by_location(move.end).is_king

        # draw moved piece
        pen.draw_actual_move(target_xy, current_state.current_player, is_king)

        if move.is_capture:
            # remove captured sqaure if it's capturing move
            captured_xy = convert_to_cartesian(move.captured_location)
            pen.draw_empty_square(captured_xy)

            # check if there are multiple-capture moves
            current_state.possible_moves = \
                current_state.find_possible_moves(move.end)

            # Don't end this round if there is still capturing move
            if current_state.has_capturing_move():
                return

        # determine if game is over
        winner = current_state.who_wins()
        if winner is None:
            # end this round for current player
            current_state.next_round()
            ai_move(pen, current_state)
        else:
            pen.claim_winner(winner)


def main():
    board_size = NUM_SQUARES * SQUARE
    # Create the UI window
    window_size = board_size + SQUARE  # The extra + SQUARE is the margin
    turtle.setup(window_size, window_size)

    # Set the drawing canvas size. The should be actual board size
    turtle.screensize(board_size, board_size)
    turtle.bgcolor("white")     # The window's background color
    turtle.tracer(0, 0)     # makes the drawing appear immediately

    pen = turtle.Turtle()   # This variable does the drawing.
    pen.penup()     # This allows the pen to be moved.
    pen.hideturtle()    # This gets rid of the triangle cursor.

    # The first parameter is the outline color, the second is the fille
    pen.color("black", "white")

    # Outline of the board
    corner = -board_size / 2    # Bottom left of checkboard
    pen.setposition(corner, corner)
    turt = Draw(pen)
    turt.draw_square(board_size)
    # Draw & fill the squares
    turt.color_board(corner)
    # Draw all pieces
    turt.draw_orig_pieces(corner)

    initiate_squares(current_state, NESTED_LIST)
    current_state.load_current_piece_locations()

    # Click handling
    screen = turtle.Screen()
    # This will call call the click_handler function when a click occurs
    screen.onclick(click_handler)
    turtle.done()  # Stops the window from closing.


if __name__ == "__main__":
    main()
