def read_input(path: str):
    """
    Read game board file from path.
    Return list of str.
    """
    with open(path, "r", encoding="utf-8") as f:
        lst = list(f.readlines())
        board = []
        for els in lst:
            board += [els[:7]]
    return board


def left_to_right_check(input_line: str, pivot: int):
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible looking to the right,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    """
    if pivot == "*":
        return True
    else:
        pivot = int(pivot)
    new_line = input_line[1:6]
    numb = new_line[0]
    result = 1
    for i in range(5):
        try:
            if numb < new_line[i+1]:
                result += 1
                numb = new_line[i+1]
            else:
                continue
        except IndexError:
            break
    if result == pivot:
        return True
    else:
        return False


def check_not_finished_board(board: list):
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5', '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    new_lst = board[1:]
    for els in new_lst:
        if els.find("?") == -1:
            continue
        else:
            return False
    return True


def check_uniqueness_in_rows(board: list):
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    new_board = board[1:6]
    new_lst = []
    for els in new_board:
        new_lst += [els[1:6]]
    for elo in new_lst:
        for i in range(5):
            if elo.count(elo[i]) > 1:
                return False
    return True


def check_horizontal_visibility(board: list):
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    new_board = board[1:6]
    for els in new_board:
        if left_to_right_check(els, els[0]) == False:
            return False
    revers_new_board = []
    for elo in new_board:
        revers_new_board += [elo[::-1]]
    for eles in revers_new_board:
        if left_to_right_check(eles, eles[0]) == False:
            return False
    return True


def check_columns(board: list):
    """
    Check column-wise compliance of the board for uniqueness (buildings of unique height) and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    new_board = []
    for i in range(1, 6):
        columns = ""
        for j in range(7):
            columns += board[j][i]
        new_board += [columns]
    return check_horizontal_visibility(new_board) and check_uniqueness_in_rows(new_board)


def check_skyscrapers(input_path: str):
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.
    """
    path = read_input(input_path)
    check_rows = check_horizontal_visibility(path) and check_uniqueness_in_rows(path)
    return check_columns(path) and check_rows and check_not_finished_board(path)
