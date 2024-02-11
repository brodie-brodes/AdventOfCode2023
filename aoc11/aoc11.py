import itertools

def get_input():
    return [i.strip() for i in open("input.txt")]

def row_is_empty(grid, row_idx):
    return all([c == '.' for c in grid[row_idx]])

def col_is_empty(grid, col_idx):
    return all([grid[row_idx][col_idx] == '.' for row_idx, _ in enumerate(grid)])

def calc_dist_between(g0, g1, empty_rows, empty_cols, expansion_dist = 2):
    dist = 0

    # Sort rows and cols numerically
    row1, row2 = min([g0[0], g1[0]]), max([g0[0], g1[0]])
    col1, col2 = min([g0[1], g1[1]]), max([g0[1], g1[1]])

    # Add distance by rows
    for row_idx in range(row1, row2):
        dist += expansion_dist if row_idx in empty_rows else 1

    # Add distance by cols
    for col_idx in range(col1, col2):
        dist += expansion_dist if col_idx in empty_cols else 1

    return dist

def main():
    # Get the input
    lines = get_input()

    # Get all positions of galaxies
    galaxy_positions = []
    for row_idx, row in enumerate(lines):
        for col_idx, ch in enumerate(row):
            if ch == "#":
                galaxy_positions.append((row_idx, col_idx))

    # Get lists of empty rows and columns
    empty_rows = [row_idx for row_idx, row in enumerate(lines) if row_is_empty(lines, row_idx)]
    empty_cols = [col_idx for col_idx, col in enumerate(lines[0]) if col_is_empty(lines, col_idx)]

    # Calculate distances between galaxies in pairwise fashion
    total_p1, total_p2 = 0, 0
    for g0, g1 in list(itertools.combinations(galaxy_positions, 2)):
        path_dist_p1 = calc_dist_between(g0, g1, empty_rows, empty_cols)
        path_dist_p2 = calc_dist_between(g0, g1, empty_rows, empty_cols, expansion_dist=1000000)

        total_p1 += path_dist_p1
        total_p2 += path_dist_p2

    print(f"Solution (p1) - {total_p1}")
    print(f"Solution (p2) - {total_p2}")

if __name__ == "__main__":
    main()