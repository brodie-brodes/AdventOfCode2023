puzzle_input = [line.strip() for line in open("input.txt")]

def get_next_num(line, idx):
    if not any([c in line[idx:] for c in "0123456789"]):
        return None
    while line[idx] not in "0123456789" and idx < len(line) - 1:
        idx += 1

    num = ""
    start_idx = idx

    while line[idx] in "0123456789":
        num += line[idx]
        idx += 1
        if idx >= len(line):
            break

    return start_idx, idx

def get_adjacent_chars(grid, line_idx, start_idx, end_idx):
    adjacent_chars = []
    if start_idx > 0:
        adjacent_chars = adjacent_chars + [grid[line_idx][start_idx - 1]]

    if end_idx < len(grid[line_idx]) - 1:
        adjacent_chars = adjacent_chars + [grid[line_idx][end_idx]]


    if start_idx == 0:
        start_idx += 1
    if end_idx == len(grid[line_idx]):
        end_idx -= 1

    if line_idx > 0:
        adjacent_chars = adjacent_chars + [grid[line_idx - 1][start_idx - 1: end_idx + 1]]
    if line_idx < len(grid) - 1:
        adjacent_chars = adjacent_chars + [grid[line_idx + 1][start_idx - 1: end_idx + 1]]

    return "".join(adjacent_chars)


def p1():
    sum_part_nums = 0
    for line_idx, line in enumerate(puzzle_input):
        idx = 0
        while get_next_num(line, idx):
            start_idx, end_idx = get_next_num(line, idx)
            num = int(line[start_idx: end_idx])
            adjacent_chars = get_adjacent_chars(puzzle_input, line_idx, start_idx, end_idx)

            if not all([c in ".0123456789" for c in adjacent_chars]):
                sum_part_nums += num

            idx = end_idx

    print(sum_part_nums)



p1()