def check_winner(board, size_x, size_y, win_length):
    def check_line(line):
        count = 0
        last = None
        for cell in line:
            if cell == last and cell is not None:
                count += 1
                if count == win_length:
                    return last
            else:
                count = 1
                last = cell
        return 0

    for row in board:
        result = check_line(row)
        if result:
            return result

    for col in range(size_x):
        column = [board[row][col] for row in range(size_y)]
        result = check_line(column)
        if result:
            return result

    for row in range(size_y - win_length + 1):
        for col in range(size_x - win_length + 1):
            diagonal = [board[row + i][col + i] for i in range(win_length)]
            result = check_line(diagonal)
            if result:
                return result

    for row in range(size_y - win_length + 1):
        for col in range(win_length - 1, size_x):
            diagonal = [board[row + i][col - i] for i in range(win_length)]
            result = check_line(diagonal)
            if result:
                return result

    if all(all(cell != 0 for cell in row) for row in board):
        return 'Draw'

    return None


def checking_the_created_field(all_players, size_x, size_y, condition_win):
    size_min = size_x if size_x < size_y else size_y
    if condition_win > size_min:
        return "'Condition Win' should be in the range from 3 to the size of the minimum side"

    if all_players > 2:
        if all_players == 3 and size_min < 6:
            return "For 3 players, the dimensions of the field should be at least 6 by 6"
        elif all_players == 4 and size_min < 8:
            return "For 4 players, the dimensions of the field should be at least 8 by 8"
        elif all_players == 5 and size_min < 10:
            return "For 5 players, the dimensions of the field should be at least 10 by 10"

    return None
