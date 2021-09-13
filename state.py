'''
Class representing and recording game states.
'''

from piece import Piece
from move import Move


class GameState:
    '''
        Class -- GameState
            Reports current state of each piece in a game
        Attributes:
            squares -- Current square the piece was located
            current_player -- The player who's currently making a move
        Methods:
            load_current_piece_location -- Helper function
            is_in_bound -- Check if piece is in bound
            get_moved_location -- A tuple representing location after move
            get_square_by_location -- Find square at certain location
            update_square -- Update square attributes while moving
            find_possible_moves -- Find all possible moves given start location
            and return a list of possible moves
            get_move_by_end_location -- Check if the chosen piece matches with
            end location of any possible move
            is_valid_move -- Valid capturing and noncapturing moves
            has_capturing_move -- Check whether any capturing move available
            move -- move a piece
            who_wins -- Return the winner of the game
            get_enemy_color -- Find opposite player / color
            next_round -- Update & initialize game state
    '''
    INITIAL_STATE = 0
    MOVE_STATE = 1

    def __init__(self, current_player, state):
        '''
            Constructor -- Creates a new instance of GameState
            Parameters:
                self -- The current GameState object
                current_player -- current player of the game; User or Computer
                state -- current game state
        '''
        self.squares = []
        self.current_player = current_player
        self.state = state
        self.possible_moves = []
        self.piece_locations_by_player = {Piece.BLACK: set(), Piece.RED: set()}

    def load_current_piece_locations(self):
        '''
            Method -- load_current_piece_location
                Collect locations of pieces of same colors.
                Each color was collected into sets and stored as values
                related with players(keys).
            Parameter:
                self -- The current GameState object
        '''
        piece_locations_by_player = {Piece.BLACK: set(), Piece.RED: set()}
        for row in self.squares:
            for square in row:
                if square is not None:
                    piece_locations_by_player[square.color].add(
                        square.location)
        self.piece_locations_by_player = piece_locations_by_player

    def is_in_bounds(self, location):
        '''
            Method -- is_in_bounds:
                Check if the location is within checkboard.
            Parameters:
                self -- Current GameState object
                location -- Current piece location, a pair of indices
        '''
        for index in location:
            if index >= len(self.squares) or index < 0:
                return False
        return True

    def get_moved_location(self, start_location, direction):
        '''
            Method -- get_moved_location:
                Get destination location from starting location
                by specified direction moving rule
            Parameters:
                self -- Current object of GameState
                start_location -- a pair of indices
                direction -- diagonal moving direction determined by
                current player
            Return:
                End location of the piece after move, an index tuple.
        '''
        return (start_location[0] + direction[0],
                start_location[1] + direction[1])

    def get_square_by_location(self, location):
        '''
            Method -- get_square_by_location:
                Map a valid location coordinate (tuple pair) to
                a square (None or an object of Piece)
            Parameters:
                self -- Current object of GameState
                location -- An index pair indicating location
            Return:
                A square (None or an object of Piece)
        '''
        return self.squares[location[0]][location[1]]

    def update_square(self, location, square):
        '''
            Method -- update_square:
                Helper function when moving pieces.
                Update a piece with location, its allowed moving direction;
                Also updates the target square on the board.
            Parameters:
                self -- Current GameState object
                location -- Location to be updated, with regards with
                piece(object of Piece) and square(Attribute of GameState)
        '''
        if square is not None:
            # Update location in Piece if it's not None
            square.location = location

            # Update to King if qualified
            top = len(self.squares) - 1
            if location[0] == top and square.color == Piece.BLACK:
                square.is_king = True
            elif location[0] == 0 and square.color == Piece.RED:
                square.is_king = True

            # Update directions
            square.find_direction()

        self.squares[location[0]][location[1]] = square

    def find_possible_moves(self, start_location):
        '''
            Method -- find_possible_moves
                Find all possible moves given a valid location
            Parameters:
                self -- The current GameState object
                start_location -- Current square the piece located
            Return:
                All possible moves -- a list of tuples
        '''
        start_square = self.get_square_by_location(start_location)
        moves = []

        for direction in start_square.find_direction():
            end_location = self.get_moved_location(start_location, direction)
            if self.is_in_bounds(end_location):
                end_square = self.get_square_by_location(end_location)
                if end_square is None:
                    # Uncapturing move
                    possible_move = Move(
                        start_square.location, end_location, False, None)
                    moves.append(possible_move)
                elif end_square.color != start_square.color:
                    next_location = \
                        self.get_moved_location(end_location, direction)
                    if self.is_in_bounds(next_location) and \
                            self.get_square_by_location(next_location) is None:
                        # Capturing move
                        possible_move = Move(
                            start_square.location,
                            next_location, True, end_location)
                        moves.insert(0, possible_move)
        return moves

    def get_move_by_end_location(self, current_location):
        '''
            Method -- get_move_by_end_location
                If the clicked square is within the list of
                possible moves' end locations, return those moves;
                Otherwise, return None.
            Parameters:
                self -- The current GameState object
                current_location -- Clicked square by user;
                Or AI selected square
            Return:
                Qualified chosen moves
        '''
        for move in self.possible_moves:
            if current_location == move.end:
                return move
        return None

    def is_valid_move(self, move):
        '''
            Method -- is_valid_move
                Determine if select move is valid.
                A move is valid if: capturing move; OR a non-capture move
                when there is no capturing move available.
            Parameters:
                self -- The current GameState object
                move -- a move
            Return:
                Boolean value of whether the move made is valid.
        '''
        if move.is_capture:
            return True
        else:
            # invalid if the selected move is non-capturing
            # and there is a capturing move in possible moves
            return not self.has_capturing_move()

    def has_capturing_move(self):
        '''
            Method -- has_capturing_move
                Determine if there is any capturing move in possible moves
        '''
        return len(self.possible_moves) > 0 \
            and self.possible_moves[0].is_capture

    def move(self, move):
        '''
            Method -- move
                Move piece and to update State and Piece attributes.
            Parameters:
                self -- The current GameState object
                move -- Current moving piece
        '''
        start_location = move.start
        end_location = move.end
        start_piece = self.get_square_by_location(start_location)
        self.update_square(end_location, start_piece)
        self.update_square(start_location, None)

        # Update piece location set
        self.piece_locations_by_player[start_piece.color].remove(
            start_location)
        self.piece_locations_by_player[start_piece.color].add(end_location)

        if move.is_capture:
            # remove captured piece
            self.update_square(move.captured_location, None)
            enemy_color = self.get_enemy_color(start_piece.color)
            self.piece_locations_by_player[enemy_color].remove(
                move.captured_location)

        self.state = GameState.MOVE_STATE

    def who_wins(self):
        '''
            Method -- who_wins
                Determine which side wins
            Parameter:
                self -- The current GameState object
        '''
        for player in self.piece_locations_by_player.keys():
            piece_location_set = self.piece_locations_by_player[player]
            # win condition 1: no remaining enemy pieces
            if len(piece_location_set) == 0:
                return self.get_enemy_color(player)

            # win condition 2: no possible moves for enemy
            all_possible_moves = []
            for piece_location in piece_location_set:
                all_possible_moves.extend(
                    self.find_possible_moves(piece_location))
            if len(all_possible_moves) == 0:
                return self.get_enemy_color(player)

        # No one wins if none of win conditions matches
        return None

    def get_enemy_color(self, player):
        '''
            Method -- get_enemy_color
                Find opposite color / player
            Parameters:
                self -- The current GameState object
                player -- Current player
            Returns:
                Opposite color / player
        '''
        if player == Piece.BLACK:
            return Piece.RED
        else:
            return Piece.BLACK

    def next_round(self):
        '''
            Method -- next_round
                Initialize after each round. Change current player.
        '''
        self.state = GameState.INITIAL_STATE
        self.possible_moves = []
        self.current_player = self.get_enemy_color(self.current_player)
