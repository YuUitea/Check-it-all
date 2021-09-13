'''
This is part of the Check-it-all checker game.
The program handles all drawing functions of the checker game.
'''
from piece import Piece


class Draw:
    '''
        Class -- Draw
            Handles all drawing functions
        Attributes:
            turt -- An instance of turtle
        Methods:
            draw_square -- Draws square in the checkerboard.
            color_board -- Creates checkerboard before starting the game
            draw_piece -- Draws a single piece.
            draw_row -- Draws a row of pieces to create the checkerboard
            draw_orig_pieces -- Called to draw the initial checkerboard
            outline_possible_move -- Draws the outline of possible moves
            draw_empty_square -- Draw an empty square after each move
            draw_actual_move -- Draws actual moves after click
            add_king_sign -- Draws additional king sign to represent King piece
            claim_winner -- Claims the winner when game ends
    '''
    NUM_SQUARES = 8  # The number of squares on each row.
    SQUARE = 50  # The size of each square in the checkerboard.
    BLACK = "black"
    RED = "red"
    SQUARE_COLORS = ("light gray", "white")
    PIECE_COLOR = {"black": "black", "red": "firebrick"}

    def __init__(self, turt):
        '''
            Constructor -- Creates a new instance of Draw
        '''
        self.turt = turt

    def draw_square(self, size):
        '''
            Method -- draw_square
                Draws a square with given size in the graphical window.
            Parameters:
                self -- The current Draw object
                size -- the length of each side of the square drawn
        '''
        RIGHT_ANGLE = 90
        self.turt.pendown()
        for i in range(4):
            self.turt.forward(size)
            self.turt.left(RIGHT_ANGLE)
        self.turt.penup()

    def color_board(self, corner):
        '''
            Method -- color_board
                Draws a checkerboard patterned with diffrerent color segments
                in the graphical window.
            Parameters:
                self -- The current Draw object
                corner -- corner of the checkboard
        '''
        self.turt.color("black", Draw.SQUARE_COLORS[0])
        for row in range(Draw.NUM_SQUARES):
            for col in range(Draw.NUM_SQUARES):
                if (row + col) % 2 == 1:
                    set_x = corner + col * Draw.SQUARE
                    set_y = corner + row * Draw.SQUARE
                    self.turt.setposition(set_x, set_y)
                    self.turt.begin_fill()
                    self.draw_square(Draw.SQUARE)
                    self.turt.end_fill()

    def draw_piece(self, color):
        '''
            Method -- draw_piece
                Draw circle at certain square
            Parameters:
                self -- The current Draw object
                color -- color of each piece representing user / computer side
        '''
        radius = Draw.SQUARE / 2
        self.turt.begin_fill()
        self.turt.pendown()
        self.turt.color(color, color)
        self.turt.circle(radius)
        self.turt.penup()
        self.turt.end_fill()

    def draw_row(self, corner, row, color):
        '''
            Method -- draw_row
                Draws pieces on every row of the checkboard.
            Parameters:
                self -- The current Draw object
                corner -- bottom left of the checkboard
                row -- every row of checkboard (total 8 rows)
                color -- color of pieces to be drawn
        '''
        X = corner + Draw.SQUARE / 2
        Y = corner
        for col in range(Draw.NUM_SQUARES):
            if (row + col) % 2 == 1:
                set_x = X + col * Draw.SQUARE
                set_y = Y + row * Draw.SQUARE
                self.turt.setposition(set_x, set_y)
                self.draw_piece(color)

    def draw_orig_pieces(self, corner):
        '''
            Method -- draw_orig_pieces
                Draws two classes of pieces representing user
                and computer sides, by two different colors.
            Parameters:
                self -- The current Draw object
                corner -- bottom left of the checkboard
            Return:
                Nothing. Drawing all pieces at start of game.
        '''
        for row in range(Draw.NUM_SQUARES):
            if row <= 2:
                self.draw_row(corner, row, Draw.PIECE_COLOR[Draw.BLACK])
            elif row >= 5:
                self.draw_row(corner, row, Draw.PIECE_COLOR[Draw.RED])

    def outline_possible_move(self, pair, color):
        '''
            Method -- outline_possible_move
                Draws the outline of a possible move
            Parameters:
                self -- The current Draw object
                pair -- (x, y) pairs representing location to be outlined
                color -- The color to be outlined at certain locations
        '''
        self.turt.penup()
        self.turt.setposition(pair[0], pair[1])
        self.turt.pencolor(color)
        self.draw_square(Draw.SQUARE)

    def draw_empty_square(self, pair):
        '''
            Method -- draw_empty_square
                Draws an empty square after each move
            Parameters:
                self -- The current Draw object
                pair -- (x, y) pairs representing drawing locations
        '''
        self.turt.penup()
        self.turt.color("black", Draw.SQUARE_COLORS[0])
        self.turt.setposition(pair[0], pair[1])
        self.turt.begin_fill()
        self.draw_square(Draw.SQUARE)
        self.turt.end_fill()

    def draw_actual_move(self, pair, color, is_king):
        '''
            Method -- draw_actual_move
                Draws the piece after uncapture and capture move
            Parameters:
                self -- The current Draw object
                pair -- (x, y) pair indicating drawing location
                color -- color representing current player
                is_king -- Boolean whether the piece is king or not
        '''
        self.turt.penup()
        self.turt.setposition(pair[0] + Draw.SQUARE / 2, pair[1])
        self.draw_piece(Draw.PIECE_COLOR[color])

        if is_king:
            self.add_king_sign(pair)

    def add_king_sign(self, pair):
        '''
            Method -- add_king_sign
                If the piece becomes King piece, adds a sign on the piece
                representing King state
            Parameters:
                self -- The current Draw object
                pair -- (x, y) pair representing King piece location
        '''
        self.turt.penup()
        self.turt.pencolor(Draw.SQUARE_COLORS[1])
        set_x = pair[0] + Draw.SQUARE / 2
        set_y = pair[1] + Draw.SQUARE / 4
        self.turt.setposition(set_x, set_y)
        self.turt.pendown()
        self.turt.circle(Draw.SQUARE / 4)
        self.turt.penup()

    def claim_winner(self, winner):
        '''
            Method -- claim_winner
                Declare the winner when game is over.
                Prints winner in the UI
            Parameters:
                self -- The current Draw object
                winner -- User or computer player
        '''
        self.turt.penup()
        self.turt.color("Green")
        self.turt.setposition(0, 0)
        self.turt.pendown()
        if winner == Piece.BLACK:
            arg = "Game Over! \n\n You Win"
        else:
            arg = "Game Over! \n\n You Lose"
        self.turt.write(
            arg, False, align="center", font=("Comic Sans MS", 32, "bold")
            )
        self.turt.penup()
