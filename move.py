'''
Class tracing the moving of pieces
'''


class Move:
    '''
        Class -- Move
        Attributes:
            start -- Start location of the move
            end -- End location after the move
            is_capture -- Whether a capture move
            captured_location -- Location where a piece got captured
    '''

    def __init__(self, start, end, is_capture, captured_location):
        self.start = start
        self.end = end
        self.is_capture = is_capture
        self.captured_location = captured_location
