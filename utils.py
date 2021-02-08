import constant
from spot import SPOT


def init_board(rows, columns, null_value=SPOT.EMPTY):
    board = []
    for i in range(rows):
        row_to_add = []
        for j in range(columns):
            row_to_add.append(null_value)
        board.append(row_to_add)

    return board


# Returns the output of the board in the console.
def print_board(board, column_labels=True):
    for row in board:
        line = ''
        for cell in row:
            line += str(cell)
            line += ' '
        print(line)
    if column_labels:
        labels = ''
        if len(board) != 0:
            for i in range(len(board[0])):
                labels += '{} '.format(i)
        print(labels)
    print('\n')


def opposite_player(player):
    if player == SPOT.RED:
        return SPOT.YELLOW
    else:
        return SPOT.RED


# Returns:
# True, SPOT.RED if red has won
# True, SPOT.YELLOW is yellow has won
# True, None if the game has ended in a tie
# False, None if the game has not been won yet
def has_game_ended(board, win_number=4):
    if check_for_full_board(board):
        return True, None

    for player in [SPOT.RED, SPOT.YELLOW]:
        if check_for_win_rows(board, player, win_number) \
                or check_for_win_columns(board, player, win_number) \
                or check_for_win_diagonals(board, player, win_number):

            return True, player
    return False, None


def check_for_win_rows(board, player, win_number):
    for row in board:
        if check_for_win_row(row, player, win_number=win_number):
            return True
    return False


def check_for_win_row(row, player, win_number):
    count = 0
    index = 0
    prev_player_index = -1
    while count < win_number and index < len(row):
        if row[index] == player and prev_player_index == index - 1:
            count += 1
            prev_player_index = index
        elif row[index] == player:
            count = 1
            prev_player_index = index
        else:
            count = 0
        index += 1

    if count >= win_number:
        return True
    return False


def check_for_win_columns(board, player, win_number):
    num_rows = len(board[0])
    num_columns = len(board)
    transposed = [[board[j][i] for j in range(num_columns)] for i in range(num_rows)]
    return check_for_win_rows(transposed, player, win_number=win_number)


# Checks if there is a winner in either diagonal of the board.
# Both diagonals are checked by inverting the rows of the board, and then calling the same helper function on both
# transformed boards.
def check_for_win_diagonals(board, player, win_number):
    flipped_board = []
    i = len(board) - 1
    while i >= 0:
        flipped_board.append(board[i])
        i -= 1
    return check_for_win_diagonal(board,
                                  player,
                                  win_number) or check_for_win_diagonal(flipped_board,
                                                                        player,
                                                                        win_number)


# Checks for a winner in the positive-sloping diagonals.
# i.e. if the board is:
# a b c d
# e f g h
# i j k l
# this function will check diagonals:
# a
# eb
# ifc
# jgd
# kh
# l
def check_for_win_diagonal(board, player, win_number):
    num_rows = len(board)
    num_cols = len(board[0])
    k = 0
    while k <= num_rows + num_cols - 2:
        diag_as_row = []
        j = 0
        while j <= k:
            i = k - j
            if i < num_rows and j < num_cols:
                diag_as_row.append(board[i][j])
            j += 1
        if len(diag_as_row) >= win_number:
            if check_for_win_row(diag_as_row, player, win_number):
                return True
        k += 1
    return False


def check_for_full_board(board):
    for row in board:
        number_of_filled_cells = 0
        for cell in row:
            if cell != SPOT.EMPTY:
                number_of_filled_cells += 1
        if number_of_filled_cells != len(row):
            return False

    return True


def handle_win(winner):
    if winner is SPOT.RED:
        print('Red Wins!')
    elif winner is SPOT.YELLOW:
        print('Yellow Wins!')
    else:
        print('The game has ended in tie.')


def check_number_of_streaks(board, streak_num, player):
    streaks = 0
    streaks += (check_num_streaks_rows(board, player, streak_num) +
                check_num_streaks_columns(board, player, streak_num) +
                check_num_streaks_diagonals(board, player, streak_num))

    return streaks


def check_num_streaks_rows(board, player, streak_num):
    score = 0
    for row in board:
        score += check_num_streaks_row(row, player, streak_num)
    return score


def check_num_streaks_columns(board, player, streak_num):
    num_rows = len(board[0])
    num_columns = len(board)
    transposed = [[board[j][i] for j in range(num_columns)] for i in range(num_rows)]
    return check_num_streaks_rows(transposed, player, streak_num)


def check_num_streaks_diagonals(board, player, streak_num):
    flipped_board = []
    i = len(board) - 1
    while i >= 0:
        flipped_board.append(board[i])
        i -= 1
    return check_num_streaks_diagonal(board,
                                      player,
                                      streak_num) + check_num_streaks_diagonal(flipped_board,
                                                                               player,
                                                                               streak_num)


def check_num_streaks_diagonal(board, player, streak_num):
    score = 0
    num_rows = len(board)
    num_cols = len(board[0])
    k = 0
    while k <= num_rows + num_cols - 2:
        diag_as_row = []
        j = 0
        while j <= k:
            i = k - j
            if i < num_rows and j < num_cols:
                diag_as_row.append(board[i][j])
            j += 1
        if len(diag_as_row) >= streak_num:
            score += check_for_win_row(diag_as_row, player, streak_num)
        k += 1
    return False


def check_num_streaks_row(row, player, streak_num):
    score = 0
    consecutive_player_occurrences = 0
    for cell in row:
        if cell == player:
            consecutive_player_occurrences += 1
        else:
            if consecutive_player_occurrences >= streak_num:
                score += 1
                consecutive_player_occurrences = 0
    return score


def make_action(board, player, column_number):
    new_board = [row[:] for row in board]
    if column_number >= len(new_board[0]) or column_number < 0:
        raise IndexError('Column {} is not in the board.'.format(column_number))

    for i in reversed(range(len(new_board))):
        current_cell = new_board[i][column_number]
        if current_cell == SPOT.EMPTY:
            new_board[i][column_number] = player
            return new_board

    raise IndexError('Column {} is full.'.format(column_number))


def get_valid_column_moves(board):
    valid_columns = []
    for i, cell in enumerate(board[0]):
        if cell == SPOT.EMPTY:
            valid_columns.append(i)
    return valid_columns


def evaluate_game_state(board, player):
    game_ended, winner = has_game_ended(board)
    if game_ended:
        if winner is None:
            return 0
        if winner == player:
            return 1000000
        if winner == opposite_player(player):
            return -10000000000
    else:
        score = 0
        score += check_number_of_streaks(board, 3, player)
        score -= check_number_of_streaks(board, 3, opposite_player(player)) * 2

        score += check_number_of_streaks(board, 2, player)
        score -= check_number_of_streaks(board, 2, opposite_player(player)) * 2

        # print(score)
        return score


def make_minimax_move(board, player_who_wants_to_win, depth=10):
    return minimax_2(board, player_who_wants_to_win,
                       alpha=constant.NINF,
                       beta=constant.INF,
                       depth=depth)

def make_expectimax_move(board, player_who_wants_to_win, depth=10):
    return expectimax(board, player_who_wants_to_win, depth=depth)

def minimax_max(board, player, alpha, beta, depth):
    game_ended, winner = has_game_ended(board)
    if game_ended or depth == 0:
        return None, evaluate_game_state(board, player)
    valid_columns = get_valid_column_moves(board)
    next_move = valid_columns[-1]
    utility = constant.NINF
    for col_num in valid_columns:
        new_board = make_action(board, player, col_num)
        updated_move, updated_score = minimax_min(new_board, player,
                                                  alpha, beta, depth-1)
        if updated_score > utility and updated_move is not None:
            utility = updated_score
            next_move = updated_move

        alpha = max(utility, alpha)
        if alpha >= beta:
            # means that we don't need to evaluate this branch
            break
    return next_move, utility


def minimax_min(board, player, alpha, beta, depth):
    game_ended, winner = has_game_ended(board)
    if game_ended or depth == 0:
        return None, evaluate_game_state(board, player)
    valid_columns = get_valid_column_moves(board)
    next_move = valid_columns[0]
    utility = constant.INF
    for col_num in valid_columns:
        new_board = make_action(board, opposite_player(player), col_num)
        updated_move, updated_score = minimax_max(new_board, player,
                                                  alpha, beta, depth-1)

        if updated_score > utility and updated_move is not None:
            utility = updated_score
            next_move = updated_move

        beta = min(utility, beta)
        if alpha >= beta:
            # means that we don't need to evaluate this branch
            break
    return next_move, utility


def minimax_2(board, player, depth, alpha=constant.NINF, beta=constant.INF, max_player=True):
    valid_locations = get_valid_column_moves(board)
    is_end, winner = has_game_ended(board)

    if depth == 0:
        return None, evaluate_game_state(board, player)
    if is_end:
        if winner == player:
            return None, 9999999999999999
        elif winner == opposite_player(player):
            return None, -9999999999999999999999999
        else:
            return None, 0

    if max_player:
        utility = constant.NINF
        column = valid_locations[0]
        for col in valid_locations:
            new_board = make_action(board, player, col)
            new_score = minimax_2(new_board, player, depth-1, alpha, beta, False)[1]
            if new_score > utility:
                utility = new_score
                column = col

            alpha = max(alpha, utility)
            if alpha >= beta:
                break
        return column, utility

    else:
        utility = constant.INF
        column = valid_locations[0]
        for col in valid_locations:
            new_board = make_action(board, opposite_player(player), col)
            new_score = minimax_2(new_board, player, depth - 1, alpha, beta, True)[1]
            if new_score < utility:
                utility = new_score
                column = col

            beta = min(beta, utility)
            if alpha >= beta:
                break
        return column, utility

def expectimax(board, player, depth, max_player=True): 
    valid_locations = get_valid_column_moves(board)
    is_end, winner = has_game_ended(board)

    if depth == 0:
        return None, evaluate_game_state(board, player)
    if is_end:
        if winner == player:
            return None, 99999
        elif winner == opposite_player(player):
            return None, -99999
        else:
            return None, 0

    if max_player:
        utility = constant.NINF
        column = valid_locations[0]

        for col in valid_locations:
            new_board = make_action(board, player, col)
            new_score = expectimax(new_board, player, depth - 1, False)[1]
            if new_score > utility:
                utility = new_score
                column = col

        return column, utility

    else: 
        utility = 0
        column = valid_locations[0]
        for col in valid_locations: 
            new_board = make_action(board, player, col)
            utility += expectimax(new_board, player, depth - 1, True)[1]

        avg_utility = utility/len(valid_locations)
        return None, avg_utility

            
                

