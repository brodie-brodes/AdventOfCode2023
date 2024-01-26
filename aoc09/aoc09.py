def get_diffs(sequence):
    return [sequence[i] - sequence[i - 1] for i in range(1, len(sequence))]

def get_diff_sets(sequences):
    while not all([i == 0 for i in sequences[-1]]):
        sequences = sequences + [get_diffs(sequences[-1])]

    return sequences

def get_next_nums_in_sequence(sequence):
    diff_sets = get_diff_sets([sequence])
    for idx in range(len(diff_sets) - 2, -1, -1):
        end_set1 = diff_sets[idx][-1]
        end_set2 = diff_sets[idx + 1][-1]

        start_set1 = diff_sets[idx][0]
        start_set2 = diff_sets[idx + 1][0]

        diff_sets[idx].append(end_set1 + end_set2)
        diff_sets[idx] = [start_set1 - start_set2] + diff_sets[idx]

    return diff_sets[0][0], diff_sets[0][-1]

def main():
    with open("input.txt") as f:
        sequences = [[int(i) for i in line.strip().split(" ")] for line in f.read().split("\n")]

    right_end_nums = [get_next_nums_in_sequence(s)[1] for s in sequences]
    left_end_nums = [get_next_nums_in_sequence(s)[0] for s in sequences]

    print(f"Solution (p1) - {sum(right_end_nums)}")
    print(f"Solution (p2) - {sum(left_end_nums)}")

if __name__ == "__main__":
    main()