from state import GameState
from piece import Piece
from move import Move

SQUARE = [
    [None, Piece("black", False, (0, 1))],
    [Piece("red", False, (1, 0)), None]
]

BOARD = [
    [None, Piece("black", False, (0, 1)), None, Piece("black", False, (0, 3))],
    [None, None, Piece("red", False, (1, 2)), None],
    [None, None, None, None],
    [Piece("red", False, (3, 0)), None, None, None]
]

def test_constructor():
    player1 = "black"
    player2 = "red"
    init = 0
    move = 1
    state1 = GameState(player1, init)
    state2 = GameState(player2, move)
    assert(state1.current_player == player1)
    assert(state1.state == init)
    assert(state1.squares == [])
    assert(state2.state == move)
    assert(state2.current_player == player2)
    assert(state1.possible_moves == [])


def test_load_current_piece_locations():
    game = GameState("black", 1)
    game.squares = SQUARE
    game.load_current_piece_locations()
    test_dict = game.piece_locations_by_player
    assert(test_dict["black"] == {(0, 1)})
    assert(test_dict["red"] == {(1, 0)})


def test_is_in_bounds():
    game = GameState("red", 0)
    game.squares = SQUARE
    assert(game.is_in_bounds((0, 0)))
    assert(game.is_in_bounds((0, 1)))
    assert(not game.is_in_bounds((-1, 0)))
    assert(not game.is_in_bounds((0, 3)))
    assert(not game.is_in_bounds((-1, -1)))


def test_get_moved_location():
    game = GameState("black", 1)
    assert(game.get_moved_location((0, 0), (1, -1)) == (1, -1))
    assert(game.get_moved_location((1, 0), (1, 1)) == (2, 1))
    assert(game.get_moved_location((0, 1), (-1, -1)) == (-1, 0))


def test_get_square_by_location():
    game = GameState("red", 0)
    game.squares = SQUARE
    assert_eq_piece(game.get_square_by_location((0, 0)), SQUARE[0][0])
    assert_eq_piece(game.get_square_by_location((0, 1)), SQUARE[0][1])
    assert_eq_piece(game.get_square_by_location((1, 0)), SQUARE[1][0])
    assert_eq_piece(game.get_square_by_location((1, 1)), SQUARE[1][1])


def test_update_square():
    BOARD_FOR_UPDATE = [
        [None, Piece("black", False, (0, 1)), None,
         Piece("black", False, (0, 3))],
        [None, None, Piece("red", False, (1, 2)), None],
        [None, None, None, None],
        [Piece("red", False, (3, 0)), None, None, None]
    ]
    game = GameState("black", 1)
    piece1 = Piece("black", False, (0, 1))
    piece2 = Piece("black", False, (0, 3))
    piece3 = Piece("red", False, (1, 1))
    game.squares = BOARD_FOR_UPDATE
    game.update_square((0, 1), None)
    game.update_square((2, 3), piece1)
    game.update_square((3, 2), piece2)
    game.update_square((0, 0), piece3)
    assert(game.squares[0][1] is None)
    assert(piece1.location == (2, 3))
    assert(not piece1.is_king)
    assert(piece2.location == (3, 2))
    assert(piece2.is_king)
    assert(piece3.is_king)


def test_find_possible_moves():
    game = GameState("black", 1)
    game2 = GameState("red", 1)
    game.squares = BOARD
    game2.squares = BOARD
    assert_eq_move(game2.find_possible_moves((3, 0))[0],
                   Move((3, 0), (2, 1), False, None))
    assert_eq_move(game.find_possible_moves((0, 1))[0], 
                   Move((0, 1), (2, 3), True, (1, 2)))
    assert_eq_move(game.find_possible_moves((0, 1))[1],
                   Move((0, 1), (1, 0), False, None))
    assert_eq_move(game.find_possible_moves((0, 3))[0],
                   Move((0, 3), (2, 1), True, (1, 2)))


def test_get_move_by_end_location():
    game = GameState("black", 1)
    game.squares = BOARD
    game.possible_moves = game.find_possible_moves((0, 1))
    assert_eq_move(game.get_move_by_end_location(
        (1, 0)), Move((0, 1), (1, 0), False, None))
    assert_eq_move(game.get_move_by_end_location(
        (2, 3)), Move((0, 1), (2, 3), True, (1, 2)))
    assert(game.get_move_by_end_location((1, 2)) is None)


def test_is_valid_move():
    game = GameState("black", 1)
    game.squares = BOARD
    game.possible_moves = game.find_possible_moves((0, 1))
    move1 = Move((0, 1), (2, 3), True, (1, 2))
    move2 = Move((0, 1), (1, 0), False, None)
    assert(not game.is_valid_move(move2))
    assert(game.is_valid_move(move1))


def test_has_capturing_move():
    game1 = GameState("black", 1)
    game2 = GameState("red", 1)
    game1.squares = BOARD
    game2.squares = BOARD
    game1.possible_moves = game1.find_possible_moves((0, 1))
    game2.possible_moves = game2.find_possible_moves((3, 0))
    assert(game1.has_capturing_move())
    assert(not game2.has_capturing_move())


def test_move():
    BOARD_FOR_MOVE = [
        [None, Piece("black", False, (0, 1)), None,
         Piece("black", False, (0, 3))],
        [None, None, Piece("red", False, (1, 2)), None],
        [None, None, None, None],
        [Piece("red", False, (3, 0)), None, None, None]
    ]
    state = GameState("black", 1)
    state.squares = BOARD_FOR_MOVE
    move1 = Move((0, 1), (2, 3), True, (1, 2))
    move2 = Move((0, 3), (1, 2), False, None)
    state.load_current_piece_locations()
    assert(state.piece_locations_by_player["black"] == {(0, 1), (0, 3)})
    state.move(move1)
    assert(state.piece_locations_by_player["black"] == {(2, 3), (0, 3)})
    state.move(move2)
    assert(state.piece_locations_by_player["black"] == {(2, 3), (1, 2)})


def test_who_wins():
    NO_ENEMY_LEFT_WIN = [
        [Piece("black", True, (0, 0)), None, None],
        [None, Piece("black", False, (1, 1)), None],
        [None, None, None]
    ]
    win1 = GameState("black", 1)
    win1.squares = NO_ENEMY_LEFT_WIN
    win1.load_current_piece_locations()
    assert(win1.who_wins() == "black")

    NO_MORE_MOVES_WIN = [
        [Piece("black", True, (0, 0)), None, Piece("black", False, (0, 2))],
        [None, Piece("red", False, (1, 1)), None],
        [None, None, None]
    ]
    win2 = GameState("red", 1)
    win2.squares = NO_MORE_MOVES_WIN
    win2.load_current_piece_locations()
    assert(win2.who_wins() == "black")


def test_get_enemy_color():
    game = GameState("black", 1)
    assert(game.get_enemy_color("black") == "red")
    assert(game.get_enemy_color("red") == "black")


def test_next_round():
    game = GameState("black", 1)
    game.next_round()
    assert(game.state == 0)
    assert(game.possible_moves == [])
    assert(game.current_player == "red")


def assert_eq_piece(piece1, piece2):
    '''
        Helper function to compare piece attributes
    '''
    if piece1 == None or piece2 == None:
        assert(piece1 == piece2)
    else:
        assert(piece1.color == piece2.color)
        assert(piece1.is_king == piece2.is_king)
        assert(piece1.location == piece2.location)


def assert_eq_move(move1, move2):
    '''
        Helper function to compare two moves
    '''
    assert(move1.start == move2.start)
    assert(move1.end == move2.end)
    assert(move1.is_capture == move2.is_capture)
    if move1.is_capture and move2.is_capture:
        assert(move1.captured_location == move2.captured_location)

