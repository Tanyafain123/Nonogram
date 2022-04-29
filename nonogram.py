

# constants

EMPTY = 0
COLORED = 1
UNDEFINED_CELL = -1


def append_list(base_str):
    """"""
    new_list = []
    for i in base_str:
        num = eval(i)
        new_list.append(num)
    return new_list


# 1
def constraint_satisfactions(n, blocks):
    """The function provides all valid combinations for a row with len n and given constructions"""
    valid_combinations = []
    base_str = ''
    if n >= sum(blocks) + len(blocks) - 1:
        constraint_sat_helper(valid_combinations, base_str, n, blocks)
    return valid_combinations


def constraint_sat_helper(valid_combinations, base_str, n, blocks):
    """The helper function for the constraint_satisfactions function"""
    if n == len(base_str):
        valid_combinations.append(append_list(base_str))
        return
    if not blocks:
        base_str += '0' * (n - len(base_str))
        valid_combinations.append(append_list(base_str))
        return
    if n - len(base_str) == sum(blocks) + len(blocks) - 1:
        valid_combinations.append(
            append_list(complete_left_spaces(base_str, blocks)))
        return
    constraint_sat_helper(valid_combinations, base_str + "0", n, blocks)
    base_str += "1" * blocks[0]
    base_str += "0"
    constraint_sat_helper(valid_combinations, base_str, n, blocks[1:])


def check_row_validity(constraints):
    """"""
    row_len = len(constraints[1])
    col_len = len(constraints[0])

    row_constraints_len = 0
    col_constraints_len = 0

    for r_block in constraints[0]:
        row_constraints_len += sum(r_block)
        if sum(r_block) > row_len:
            return False
    for c_block in constraints[1]:
        col_constraints_len += sum(c_block)
        if sum(c_block) > col_len:
            return False
    if row_constraints_len != col_constraints_len:
        return False
    return True


def complete_left_spaces(base_str, blocks):
    """"""
    for index, constraint in enumerate(blocks):
        base_str += "1" * constraint
        if not index + 1 == len(blocks):
            base_str += "0"
    return base_str


# 2

def row_variations(row, blocks):
    """The function provides all valid combinations for a partially coloured row and given constructions"""
    valid_combinations = []
    combination_lst = row[:]
    lst_index_counter = 0
    block_counter = 0
    cells_to_color = possible_counter(row)
    if not cells_to_color < sum(blocks):
        row_variations_helper(valid_combinations, combination_lst, row,
                              lst_index_counter, blocks, block_counter,
                              cells_to_color)

    return valid_combinations


def possible_counter(row):
    """"""
    count = 0
    for i in row:
        if i != EMPTY:
            count += 1
    return count


def row_variations_helper(valid_combinations, combination_lst, row,
                          lst_index, blocks, block_counter, cells_to_color):
    """The helper function for the row_variations function"""
    if block_counter == len(blocks):
        no_more_blocks(valid_combinations, combination_lst, blocks)
        return
    for temp_index in range(lst_index, len(combination_lst)):
        if temp_index + blocks[block_counter] > len(combination_lst):
            return
        if valid_cell_checker(row, temp_index, blocks, block_counter, cells_to_color):
            combination_lst[temp_index:temp_index + blocks[block_counter]] = [
                                                                                 1] * \
                                                                             blocks[
                                                                                 block_counter]

            row_variations_helper(valid_combinations, combination_lst, row,
                                  temp_index + blocks[block_counter] + 1,
                                  blocks, block_counter + 1,
                                  cells_to_color - blocks[block_counter])

            combination_lst[
            temp_index:temp_index + blocks[block_counter]] = row[
                                                             temp_index:temp_index +
                                                                        blocks[
                                                                            block_counter]]


def valid_cell_checker(row, lst_index_counter, blocks, block_counter,
                       cells_to_color):
    """"""
    if cells_to_color <= 0:
        return False
    if lst_index_counter != 0:
        if row[lst_index_counter - 1] == 1:
            return False
    if lst_index_counter + blocks[block_counter] < len(row):
        if row[lst_index_counter + blocks[block_counter]] == COLORED:
            return False
    if EMPTY in row[lst_index_counter:lst_index_counter + blocks[block_counter]]:
        return False

    return True


def no_more_blocks(valid_combinations, combination_lst, blocks):
    """"""
    counter = 0
    lst_copy = combination_lst[:]
    if combination_lst.count(1) == sum(blocks):
        while UNDEFINED_CELL in lst_copy:
            if combination_lst[counter] == UNDEFINED_CELL:
                lst_copy[counter] = EMPTY
            counter += 1
        valid_combinations.append(lst_copy)
    return


def check_recursion_end(cells_to_color, combination_lst, lst_index, blocks, block_counter,
                        valid_combinations):
    """
    Check if reached the end of a recursion.
    """
    if cells_to_color == 0:
        if block_counter == len(blocks) and combination_lst.count(1) == sum(blocks):
            row_copy_copy = [EMPTY if square == UNDEFINED_CELL or square == EMPTY else COLORED for square
                             in combination_lst]

            valid_combinations.append(row_copy_copy)
        return True

    if cells_to_color < 0:
        return True

    elif lst_index >= len(combination_lst) or block_counter >= len(blocks):
        return True


# 3

def intersection_row(rows):
    """The function thar receives list of rows and returns it's common elements witch a certain logic.If two similar
    numbers meet the number doe not change. If -1 meets 1 it
    changes to -1. If -1 meets 0 it changes to -1 if 0 meets 1 or 1 meets 0 the number changes to -1"""
    if not rows:
        return rows
    cut_row = []
    new_rows = rows[:]
    for index_to_check in range(len(rows[0])):
        checker = True
        for row in range(len(rows) - 1):
            if not rows[row][index_to_check] == rows[row + 1][index_to_check]:
                if rows[row][index_to_check] == EMPTY and rows[row + 1][index_to_check] == UNDEFINED_CELL:
                    answer = -1
                    checker = False
                if rows[row][index_to_check] == UNDEFINED_CELL and rows[row + 1][index_to_check] == EMPTY:
                    answer = -1
                    checker = False
                if rows[row][index_to_check] == COLORED and rows[row + 1][index_to_check] == UNDEFINED_CELL:
                    answer = -1
                    checker = False
                if rows[row][index_to_check] == UNDEFINED_CELL and rows[row + 1][index_to_check] == COLORED:
                    answer = -1
                    checker = False
                else:
                    answer = -1
                    checker = False
        if checker:
            cut_row.append(rows[0][index_to_check])
        else:
            cut_row.append(answer)
    return cut_row


# 4


def init_board(constraints):
    """"""
    len_row = len(constraints[1])
    board = []
    for constraint in constraints[0]:
        row = intersection_row(constraint_satisfactions(len_row, constraint))
        if not row:
            board = None
            return board
        board.append(row)
    return board


def is_nono_done(board):
    """"""
    for row in board:
        if UNDEFINED_CELL in row:
            return False
    return True


def transpose_row_and_col(rows):
    """"""
    transpose_list = list(map(list, zip(*rows)))
    return transpose_list

#4
def solve_easy_nonogram(constraints):
    """This function receives constraints and returns a solved board or a maximum that is possible to solve"""
    if not check_row_validity(constraints):
        return None
    row_list = init_board(constraints)
    return solve_easy_helper(constraints, row_list)


def solve_easy_helper(constraints, row_list):
    """The solve easy nonogram helper function"""
    if is_nono_done(row_list):
        return row_list
    temp_col = transpose_row_and_col(row_list)
    new_col = []
    for index, col in enumerate(temp_col):
        if UNDEFINED_CELL not in col:
            new_col.append(col)
        else:
            temp = intersection_row(row_variations(col, constraints[1][index]))
            if not temp:
                return None
            new_col.append(temp)
    temp_row = transpose_row_and_col(new_col)
    new_row = []
    for index, row in enumerate(temp_row):
        if UNDEFINED_CELL not in row:
            new_row.append(row)
        else:
            temp = intersection_row(row_variations(row, constraints[0][index]))
            if not temp:
                return None
            new_row.append(temp)
    if new_row == row_list:
        return row_list
    else:
        return solve_easy_helper(constraints, new_row)


# 5


def solve_easy_nonogram1(constraints):
    """This function receives constraints and returns a solved board or a maximum that is possible to solve"""
    if not check_row_validity(constraints):
        return None
    row_list = init_board(constraints)
    return solve_easy_helper1(constraints, row_list)


def solve_easy_helper1(constraints, row_list):
    """The solve easy nonogram helper function"""
    if is_nono_done(row_list):
        return row_list
    temp_col = transpose_row_and_col(row_list)
    new_col = []
    for index, col in enumerate(temp_col):
        if UNDEFINED_CELL not in col:
            new_col.append(col)
        else:
            temp = intersection_row(row_variations(col, constraints[1][index]))
            if not temp:
                return None
            new_col.append(temp)
            break
    temp_row = transpose_row_and_col(new_col)
    new_row = []
    for index, row in enumerate(temp_row):
        if UNDEFINED_CELL not in row:
            new_row.append(row)
        else:
            temp = intersection_row(row_variations(row, constraints[0][index]))
            if not temp:
                return None
            new_row.append(temp)
            break
    if new_row == row_list:
        return row_list
    else:
        return solve_easy_helper1(constraints, new_row)


def check_undefined_in_board(board):
    for row in board:
        if not UNDEFINED_CELL in row:
            continue
        else:
            return False
    return True


def get_index(board, row_len):
    index = row_len
    for r_index, row in enumerate(board):
        for c_index, square in enumerate(row):
            if c_index < index and square == UNDEFINED_CELL:
                index = c_index
    return index


def col_mahher(board, index):
    """"""
    col = []
    for row in board:
        col.append(row[index])
    return col


def update_board(option, board, col_index):
    """"""
    for row_index in range(len(option)):
        board[row_index][col_index] = option[row_index]


def if_valid_row(constraints_for_rows, board, col_len):
    """"""
    for index in range(col_len):
        if not row_variations(board[index], constraints_for_rows[index]):
            return False
    return True


def solve_nonogram(constraints):
    """This function receives constraints and returns a solved board"""
    constraints_for_rows = constraints[0]
    constraints_for_cols = constraints[1]
    possible_solutions = []
    row_len = len(constraints[1])
    col_len = len(constraints[0])
    board = solve_easy_nonogram1(constraints)
    if board is None:
        return possible_solutions
    if check_undefined_in_board(board):
        possible_solutions.append(board)
        return possible_solutions
    else:
        solve_nonogram_helper(board, constraints_for_rows, constraints_for_cols, possible_solutions, row_len, col_len)
        return possible_solutions


def solve_nonogram_helper(board, constraints_for_rows, constraints_for_cols, possible_solutions, row_len, col_len):
    """The solve_nonogram helper function"""
    col_index = get_index(board, row_len)

    if col_index == row_len:
        board_solution = copy.deepcopy(board)
        possible_solutions.append(board_solution)
        return

    col = col_mahher(board, col_index)
    col_options = row_variations(col, constraints_for_cols[col_index])
    for option in col_options:
        update_board(option, board, col_index)
        if if_valid_row(constraints_for_rows, board, col_len):
            solve_nonogram_helper(board, constraints_for_rows,
                                  constraints_for_cols, possible_solutions,
                                  row_len, col_len)
        update_board(col, board, col_index)


# print(solve_easy_nonogram([[[1], [2], [1], [1]], [[2, 1], [2], [1], [1]]]))

# import time
#
# tower = [[[1, 8], [3, 11], [1, 14], [5, 17], [7, 15], [1, 1, 1, 1, 9], [1, 1, 1, 1, 3], [9], [1, 1, 1, 1, 4],
#           [1, 1, 1, 1, 12],
#           [8, 17], [6, 14], [1, 7, 1, 12], [11, 9], [9, 7], [9, 4], [8, 2], [7], [7], [1, 5], [1, 5], [1, 7, 1],
#           [11], [6, 3], [5, 2], [4, 1], [7], [7], [1, 5], [1, 5], [1, 5], [7, 2], [4, 1, 2], [5, 13], [5, 14],
#           [22], [2, 19], [2, 20], [23], [11, 2, 1, 3], [11, 2, 1, 2], [23], [28], [30], [30]],
#          [[2], [3], [2, 3, 3], [4, 3, 3, 12], [4, 1, 33], [2, 1, 9, 7, 5, 7], [1, 42], [5, 1, 35], [1, 20, 6, 10],
#           [2, 1, 13, 6, 10], [4, 35], [3, 4, 3, 12], [2, 2, 3, 12], [4, 3, 12], [4, 3, 8, 4], [4, 3, 8, 4],
#           [4, 4, 12], [4, 3, 12], [4, 4, 6, 4], [5, 4, 6, 4], [5, 4, 12], [4, 5, 6, 4], [5, 5, 6, 4], [5, 6, 11],
#           [5, 6, 10], [5, 5, 3, 4], [5, 6, 3], [4, 6, 3], [4, 7, 3], [4, 7, 3]]]
# start = time.time()
# solve_nonogram([[[6], [2, 2], [1, 6, 1], [1, 13], [1, 3, 2, 2], [3, 1, 5, 3, 1], [1, 1, 1, 9, 3, 1],
#                  [1, 2, 2, 2, 2, 1], [1, 3, 2, 7, 3, 2, 1], [1, 3, 1, 5, 3, 2, 3, 2],
#                  [1, 3, 1, 4, 3, 3, 3, 1], [1, 3, 2, 4, 3, 2, 3, 1], [1, 4, 3, 2, 3, 2, 3, 1],
#                  [3, 3, 6, 2, 3, 2, 1], [1, 2, 3, 8, 3, 2, 1], [1, 4, 4, 3, 3, 2, 1]
#                     , [1, 4, 8, 1, 2, 2, 1], [1, 5, 4, 1, 1, 2, 1], [1, 2, 2, 2, 1, 1, 2, 1],
#                  [1, 2, 1, 4, 2, 3, 1], [1, 2, 2, 3, 3, 1], [1, 2, 9, 1, 2], [1, 1, 5, 1, 2],
#                  [2, 2, 2, 1], [5, 1], [2, 2], [2, 4, 2], [2, 1, 1, 3], [2, 1, 4, 1, 3],
#                  [1, 2, 1, 8, 4], [1, 4, 10, 4], [1, 6, 2, 3, 7], [2, 1, 6, 2, 9], [2, 3, 3, 3, 13],
#                  [2, 2, 2, 2, 13], [5, 4, 2, 13], [7, 2, 13], [13, 2, 13], [13, 2, 13], [13, 2, 13]],
#                 [[1, 11], [2, 1, 8], [6, 1, 1, 5], [2, 4, 2, 1, 5], [1, 5, 4, 2, 2, 5],
#                  [2, 6, 5, 1, 1, 1, 4], [3, 8, 6, 1, 3, 1, 4], [1, 2, 4, 1, 2, 1, 3, 1, 3],
#                  [1, 3, 4, 2, 1, 1, 1, 4, 1, 3], [1, 2, 2, 3, 2, 1, 2, 1, 4, 1, 3],
#                  [1, 3, 2, 2, 2, 2, 1, 2, 1, 3, 1, 3], [1, 2, 2, 3, 3, 2, 1, 2, 1, 1, 2, 3],
#                  [1, 2, 2, 4, 2, 2, 1, 2, 1, 4, 2, 3], [1, 2, 2, 4, 2, 2, 1, 2, 10],
#                  [1, 2, 2, 2, 4, 2, 1, 2, 3, 10], [1, 2, 2, 1, 2, 3, 1, 3, 1, 2, 6],
#                  [1, 2, 1, 3, 3, 1, 2, 1, 1, 1], [1, 2, 1, 8, 1, 3, 1, 1, 3, 7],
#                  [2, 3, 6, 1, 2, 1, 1, 4, 7], [1, 1, 2, 2, 1, 2, 1, 4, 7], [1, 2, 3, 8, 1, 1, 3, 7],
#                  [1, 1, 9, 2, 1, 1, 3, 8], [1, 2, 5, 3, 1, 1, 1, 8], [1, 3, 4, 1, 2, 9], [1, 9, 2, 1, 9],
#                  [1, 6, 2, 9], [1, 3, 2, 11], [1, 2, 13], [1, 2, 15], [1, 17]]])
# end = time.time()
# print(end - start)
