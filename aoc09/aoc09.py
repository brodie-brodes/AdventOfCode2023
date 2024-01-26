def get_diffs(sequence):
    return [sequence[i] - sequence[i - 1] for i in range(1, len(sequence))]

def get_diff_sets(sequences):
    while not all([i == 0 for i in sequences[-1]]):
        sequences = sequences + [get_diffs(sequences[-1])]

    return sequences

def get_next_num_in_sequence(sequence):
    diff_sets = get_diff_sets([sequence])
    for idx in range(len(diff_sets) - 2, -1, -1):
        end_set1 = diff_sets[idx][-1]
        end_set2 = diff_sets[idx + 1][-1]

        diff_sets[idx].append(end_set1 + end_set2)

    return diff_sets[0][-1]

def p1():
    with open("input.txt") as f:
        sequences = [[int(i) for i in line.strip().split(" ")] for line in f.read().split("\n")]

    next_nums = [get_next_num_in_sequence(s) for s in sequences]

    print(f"Solution (p1) - {sum(next_nums)}")

if __name__ == "__main__":
    p1()