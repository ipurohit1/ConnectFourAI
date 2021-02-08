from spot import SPOT
from utils import has_game_ended, init_board, check_for_win_row


def test_empty_row():
    row = []
    assert not check_for_win_row(row, SPOT.RED, 4)


def test_one_red_row():
    row = [SPOT.RED]
    assert not check_for_win_row(row, SPOT.RED, 4)

    for i in range(5):
        row.append(SPOT.YELLOW)
    assert not check_for_win_row(row, SPOT.RED, 4)


def test_winning_red_row():
    row = []
    for i in range(4):
        row.append(SPOT.RED)
    assert check_for_win_row(row, SPOT.RED, 4)
    assert not check_for_win_row(row, SPOT.YELLOW, 4)
    row.append(SPOT.RED)
    assert check_for_win_row(row, SPOT.RED, 4)
    row.append(SPOT.YELLOW)
    assert check_for_win_row(row, SPOT.RED, 4)
    assert not check_for_win_row(row, SPOT.YELLOW, 4)


def test_3_red_row():
    row = [SPOT.RED, SPOT.RED, SPOT.RED]
    assert not check_for_win_row(row, SPOT.RED, 4)


def test_empty_board():
    board = init_board(6, 7, SPOT.EMPTY)
    assert not has_game_ended(board)[0]


def test_full_red_board():
    board = init_board(6, 7, SPOT.RED)
    assert has_game_ended(board)[0]


def test_full_yellow_board():
    board = init_board(6, 7, SPOT.YELLOW)
    assert has_game_ended(board)[0]


def test_bottom_row():
    board = init_board(6, 7, SPOT.EMPTY)
    assert not has_game_ended(board)[0]
    for player in [SPOT.RED, SPOT.YELLOW]:
        for i in range(4):
            board[5][i] = player
        assert has_game_ended(board)[0]


def test_top_row():
    board = init_board(6, 7, SPOT.EMPTY)
    assert not has_game_ended(board)[0]
    for player in [SPOT.RED, SPOT.YELLOW]:
        for i in range(4):
            board[0][i+1] = player
        assert has_game_ended(board)[0]


def test_first_column():
    board = init_board(5, 5, SPOT.EMPTY)
    for i in range(5):
        board[i][0] = SPOT.RED
    assert has_game_ended(board)[0]


def test_last_column():
    board = init_board(5, 5, SPOT.EMPTY)
    for i in range(5):
        board[i][-1] = SPOT.RED
    assert has_game_ended(board)[0]


def test_last_column_almost_win():
    board = init_board(5, 5, SPOT.EMPTY)
    for i in range(3):
        board[i][-1] = SPOT.RED
    assert not has_game_ended(board)[0]


def test_positive_diagonal_1():
    x = SPOT.EMPTY
    r = SPOT.RED
    board = [
        [x, x, x, x, x],
        [x, x, x, r, x],
        [x, x, r, x, x],
        [x, r, x, x, x],
        [r, x, x, x, x]
    ]
    assert has_game_ended(board)[0]


def test_positive_diagonal_2():
    x = SPOT.EMPTY
    r = SPOT.RED
    board = [
        [x, x, x, x, r],
        [x, x, x, r, x],
        [x, x, r, x, x],
        [x, r, x, x, x],
        [x, x, x, x, x]
    ]
    assert has_game_ended(board)[0]


def test_positive_diagonal_3():
    x = SPOT.EMPTY
    r = SPOT.RED
    board = [
        [x, x, x, x, x],
        [x, x, x, x, r],
        [x, x, x, r, x],
        [x, x, r, x, x],
        [x, r, x, x, x]
    ]
    assert has_game_ended(board)[0]


def test_positive_diagonal_4():
    x = SPOT.EMPTY
    r = SPOT.RED
    board = [
        [x, x, x, r, x],
        [x, x, r, x, x],
        [x, r, x, x, x],
        [r, x, x, x, x],
        [x, x, x, x, x]
    ]
    assert has_game_ended(board)[0]


def test_negative_diagonal_1():
    x = SPOT.EMPTY
    r = SPOT.RED
    board = [
        [r, x, x, x, x],
        [x, r, x, x, x],
        [x, x, r, x, x],
        [x, x, x, r, x],
        [x, x, x, x, r]
    ]
    assert has_game_ended(board)[0]


def test_negative_diagonal_2():
    x = SPOT.EMPTY
    r = SPOT.RED
    board = [
        [x, x, x, x, x],
        [x, r, x, x, x],
        [x, x, r, x, x],
        [x, x, x, r, x],
        [x, x, x, x, r]
    ]
    assert has_game_ended(board)[0]


def test_negative_diagonal_3():
    x = SPOT.EMPTY
    r = SPOT.RED
    board = [
        [x, r, x, x, x],
        [x, x, r, x, x],
        [x, x, x, r, x],
        [x, x, x, x, r],
        [x, x, x, x, x]
    ]
    assert has_game_ended(board)[0]


def test_negative_diagonal_4():
    x = SPOT.EMPTY
    r = SPOT.RED
    board = [
        [x, x, x, x, x],
        [r, x, x, x, x],
        [x, r, x, x, x],
        [x, x, r, x, x],
        [x, x, x, r, x]
    ]
    assert has_game_ended(board)[0]

