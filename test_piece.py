from piece import Piece


def test_constructor():
    blackpiece = Piece("black", False, (1, 1))
    redpiece = Piece("red", True, (0, 2))
    assert(blackpiece.color == "black")
    assert(not blackpiece.is_king)
    assert(blackpiece.location == (1, 1))
    assert(redpiece.color == "red")
    assert(redpiece.is_king)
    assert(redpiece.location == (0, 2))


def test_find_direction():
    black = Piece("black", False, (1, 0))
    red = Piece("red", False, (2, 1))
    king = Piece("black", True, (1, 1))
    assert(black.find_direction() == [(1, -1), (1, 1)])
    assert(red.find_direction() == [(-1, -1), (-1, 1)])
    assert(king.find_direction() == [(-1, -1), (-1, 1), (1, -1), (1, 1)])
