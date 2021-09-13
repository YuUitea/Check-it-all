from main import convert_to_index, convert_to_cartesian, initiate_squares
from state import GameState
from piece import Piece


def test_convert_to_index():
    assert(convert_to_index(250, 250) is None)
    assert(convert_to_index(-250, -250) is None)
    assert(convert_to_index(0, 0) == (4, 4))
    assert(convert_to_index(-199, -199) == (0, 0))
    assert(convert_to_index(-50, 80) == (5, 3))


def test_convert_to_cartesian():
    assert(convert_to_cartesian((0, 0)) == (-200, -200))
    assert(convert_to_cartesian((2, 3)) == (-50, -100))
    assert(convert_to_cartesian((7, 4)) == (0, 150))
    assert(convert_to_cartesian((4, 5)) == (50, 0))


def test_initiate_squares():
    INIT_LST = [
        ["", "black"],
        ["red", ""]
    ]
    current = GameState("black", 0)
    initiate_squares(current, INIT_LST)
    for i in range(len(current.squares)):
        row = len(current.squares[i])
        for j in range(row):
            square = current.squares[i][j]
            if INIT_LST[i][j] == "":
                assert(square is None)
            else:
                assert(isinstance(square, Piece))
                assert(square.color == INIT_LST[i][j])
                assert(not square.is_king)
                assert(square.location == (i, j))
