from move import Move


def test_constructor():
    non_cap = Move((3, 1), (2, 0), False, None)
    cap_move = Move((0, 0), (2, 2), True, (1, 1))
    assert(non_cap.start == (3, 1))
    assert(non_cap.end == (2, 0))
    assert(not non_cap.is_capture)
    assert(non_cap.captured_location is None)
    assert(cap_move.start == (0, 0))
    assert(cap_move.end == (2, 2))
    assert(cap_move.is_capture)
    assert(cap_move.captured_location == (1, 1))