import os

W = True
B = False
U = None
turn = W
no_capture_count = 0


def clear():
    os.system("cls" if os.name == "nt" else "clear")


board_position = [
    [W, B, W, B],
    [B, W, B, W],
    [W, B, W, B],
    [B, W, B, W]
]


def to_2d_coords(square):
    square = square.upper()
    if len(square) == 2 and square[0] in "ABCD" and square[1] in "1234":
        return [ord(square[0]) - 65, int(square[1]) - 1]
    return [None, None]


def to_algebraic_coords(coords):
    if len(coords) == 2 and 0 <= coords[0] <= 3 and 0 <= coords[1] <= 3:
        return chr(coords[0] + 65) + str(coords[1] + 1)
    return None


def position_to_text(position):
    text = "\n     1   2   3   4  \n   |---|---|---|---|\n"
    for row_index, row in enumerate(position):
        text += f" {chr(row_index + 65)} | "
        for col in row:
            if col is W:
                text += "○ | "
            elif col is B:
                text += "● | "
            else:
                text += "  | "
        text += "\n   |---|---|---|---|\n"
    return text


def remove_piece(player):
    repeat = False
    while True:
        if not repeat:
            square = input(
                f"\033[1m{player}:\033[0m Choose a piece to remove from the board,\n"
                "and enter the coordinate here (e.g. A1): "
            )
        else:
            square = input(
                f"\nThe piece you've chosen is not {player.lower()}. Pick again: "
            )
        row, col = to_2d_coords(square)
        if (
            col is not None
            and row is not None
            and board_position[row][col] == (W if player == "WHITE" else B)
        ):
            board_position[row][col] = U
            clear()
            print(position_to_text(board_position))
            break
        repeat = True


def get_valid_moves(square):
    row, col = to_2d_coords(square)
    color = board_position[row][col]
    potential_moves = [
        [row, col + 1],
        [row + 1, col],
        [row, col - 1],
        [row - 1, col],
        [row + 1, col + 1],
        [row - 1, col - 1],
        [row - 1, col + 1],
        [row + 1, col - 1],
    ]
    valid_moves = []
    for move in potential_moves:
        try:
            if (
                0 <= move[0] <= 3
                and 0 <= move[1] <= 3
            ):
                if board_position[move[0]][move[1]] is U:
                    valid_moves.append(move)
                elif board_position[move[0]][move[1]] is not color:
                    diff_r = 2 * (move[0] - row)
                    diff_c = 2 * (move[1] - col)
                    if board_position[row + diff_r][col + diff_c] is U:
                        valid_moves.append([row + diff_r, col + diff_c])
                    
        except IndexError:
            continue
    valid_moves = list(filter(lambda item: item is not None, valid_moves))
    return valid_moves


def move_piece():
    global turn, no_capture_count
    if turn == W:
        while True:
            square = input(
                f"\033[1mWHITE\033[0m: Enter the coordinates of the piece you want to move: "
            )
            row, col = to_2d_coords(square)
            if (row is not None or col is not None) and board_position[row][col] is W:
                break
            else:
                print("\nThe piece you've chosen is not white.")
    elif turn == B:
        while True:
            square = input(
                f"\033[1mBLACK\033[0m: Enter the coordinates of the piece you want to move: "
            )
            row, col = to_2d_coords(square)
            if (row is not None or col is not None) and board_position[row][col] is B:
                break
            else:
                print("\nThe piece you've chosen is not black.")
    moves = get_valid_moves(square)
    for index, move in enumerate(moves):
        moves[index] = to_algebraic_coords(move)
    while True:
        chosen_move = input(
            f"\nYour available moves are {moves}.\nPick one of them and enter it here: "
        )
        if chosen_move.upper() in moves:
            break
        else:
            print(
                f"\nThe piece you've chosen is not a valid move."
            )
    new_row, new_col = to_2d_coords(chosen_move)
    board_position[new_row][new_col] = board_position[row][col]
    board_position[row][col] = U
    no_capture_count += 1
    if abs(new_row - row) == 2 or abs(new_col - col) == 2:
        board_position[row + (new_row - row) // 2][col + (new_col - col) // 2] = U
        no_capture_count = 0
    clear()
    print(position_to_text(board_position))
    turn = not turn


print(position_to_text(board_position))
remove_piece("WHITE")
remove_piece("BLACK")
while True:
    move_piece()
    flattened = [i for row in board_position for i in row]
    if B not in flattened:
        print("\033[1mWHITE\033[0m wins")
        break
    elif W not in flattened:
        print("\033[1mBLACK\033[0m wins")
        break
    elif flattened.count(B) == 1 and flattened.count(W) == 1:
        print("Draw by insufficient pieces")
        break
    elif no_capture_count > 20:
        print("Draw by 20 moves without captures")
        break
