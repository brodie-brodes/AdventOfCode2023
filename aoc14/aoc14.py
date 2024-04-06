import numpy as np


def apply_movement_north(grid, row, col):
    """Apply movement from northward tilt to a single object in a grid"""
    if not grid[row][col] == "O":
        return 0

    swap_row = row

    while swap_row - 1 >= 0 and grid[swap_row - 1][col] == ".":
        swap_row -= 1

    if swap_row != row:
        grid[swap_row][col] = "O"
        grid[row][col] = "."


def do_cycle(grid):
    """Perform a single part 2 cycle"""
    g = grid.copy()

    for i in range(4):
        for row_idx, row in enumerate(g):
            for col_idx, col in enumerate(row):
                apply_movement_north(g, row_idx, col_idx)

        g = np.rot90(g, k = 3)

    return g


def count_load_north(grid):
    """Quantify northward load on the grid"""
    total_load = 0
    for row_idx, row in enumerate(grid):
        # Count rocks in row
        num_rocks = dict(zip(*np.unique(row, return_counts=True)))["O"] if "O" in row else 0

        total_load += num_rocks * (len(grid) - row_idx)

    return total_load


def identify_loop(seq):
    """Identify whether a loop exists in sequence of values"""
    seq = np.array(seq)
    last_val = seq[-1]

    matching_value_indices = np.flip(np.where(seq[:-1] == last_val)[0])

    if len(matching_value_indices) < 2:
        return None

    # Check if perfect loop exists
    sub_seqs = [seq[matching_value_indices[idx + 1]: matching_value_indices[idx]] for idx, _ in enumerate(matching_value_indices[:-1])]
    if not all([np.array_equal(ss, sub_seqs[0]) for ss in sub_seqs[1:2]]):
        return None

    return sub_seqs[0]


def p1():
    grid = [list(line.strip()) for line in open("input.txt")]

    # Roll all rocks northward
    total_load = 0
    for row_idx, row in enumerate(grid):
        for col_idx, col in enumerate(row):
            apply_movement_north(grid, row_idx, col_idx)

    print(f"Solution (P1) - {count_load_north(grid)}")


def p2():
    grid = [list(line.strip()) for line in open("input.txt")]
    grid = np.array([np.array([np.array(char) for char in line]) for line in grid])

    # Keep track of the sequence of load values as cycles progress
    load_value_seq = {}

    total_load, cycle = 0, 0
    while True:
        grid = do_cycle(grid)
        load_value_seq[cycle] = count_load_north(grid)
        cycle += 1

        # Check if current sequence contains a repeating subsequence
        loop = identify_loop(list(load_value_seq.values()))

        if loop is not None:
            break

    idx_load_at_finish = (1_000_000_000 - len(list(load_value_seq.values()))) % len(loop)
    load_at_finish = loop[idx_load_at_finish]

    print(f"Solution (p2) - {load_at_finish}")


if __name__ == "__main__":
    p1()
    p2()