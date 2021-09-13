'''
Class representing and recording pieces.
'''


class Piece:
    '''
        Class -- Piece
        Attributes:
            color -- Color of the piece
            is_king -- Whether piece is king piece
            location -- Location of the piece, a tuple
        Methods:
            find_direction -- Helper function
    '''
    BLACK = "black"
    RED = "red"
    BLACK_MOVES = [(1, -1), (1, 1)]
    RED_MOVES = [(-1, -1), (-1, 1)]

    def __init__(self, color, is_king, location):
        self.color = color
        self.is_king = is_king
        self.location = location
        self.directions = self.find_direction()

    def find_direction(self):
        if not self.is_king:
            if self.color == Piece.BLACK:
                return Piece.BLACK_MOVES
            else:
                return Piece.RED_MOVES
        return Piece.RED_MOVES + Piece.BLACK_MOVES
