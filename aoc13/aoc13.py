import numpy as np


def is_mirror_row(grid, line_idx, smudges=0):
    idx1, idx2 = line_idx - 1, line_idx
    smudges_seen = 0
    while True:
        smudges_seen += (grid[idx1] != grid[idx2]).sum()

        if smudges_seen > smudges:
            return False

        idx1 -= 1
        idx2 += 1

        if idx1 < 0 or idx2 >= len(grid):
            return smudges == smudges_seen


def is_mirror_col(grid, line_idx, smudges=0):
    idx1, idx2 = line_idx - 1, line_idx
    smudges_seen = 0

    while True:
        smudges_seen += (grid[:, idx1] != grid[:, idx2]).sum()

        if smudges_seen > smudges:
            return False

        idx1 -= 1
        idx2 += 1

        if idx1 < 0 or idx2 >= len(grid[0]):
            return smudges == smudges_seen


def do_part(part=1):
    with open("input.txt") as f:
        input_txt = f.read()

    grids = [np.array([np.array(list(l)) for l in grid.split("\n")]) for grid in input_txt.split("\n\n")]

    total = 0
    smudges = 0 if part == 1 else 1
    for idx, grid in enumerate(grids):
        for row_idx in range(1, len(grid)):
            if is_mirror_row(grid, row_idx, smudges=smudges):
                total += (row_idx) * 100

        for col_idx in range(1, len(grid[1])):
            if is_mirror_col(grid, col_idx, smudges=smudges):
                total += col_idx

    print(f"Solution (part {part}) - {total}")


if __name__ == "__main__":
    do_part(1)
    do_part(2)
