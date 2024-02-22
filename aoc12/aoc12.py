def count_arrangements(char_string, nums, tracking):
    arrangements = 0
    num = nums[0]
    for idx, c in enumerate(char_string):
        substr = char_string[idx: idx + nums[0]]

        right_adjacent_char = char_string[idx + num] if len(char_string) > idx + num else ""

        if not all([(i in ["#", "?"]) for i in substr]):
            continue
        if len(substr) < num:
            continue
        if right_adjacent_char == "#":
            continue
        if "#" in char_string[:idx]:
            continue

        remainder = char_string[idx + nums[0] + 1:]

        if len(nums) == 1:
            if "#" not in remainder:
                arrangements += 1
        else:
            if not (remainder, nums[1:]) in tracking:
                tracking[(remainder, nums[1:])] = count_arrangements(remainder, nums[1:], tracking)

            arrangements_remainder = tracking[(remainder, nums[1:])]

            arrangements += arrangements_remainder

    return arrangements


def main():
    with open("input.txt") as f:
        txt_input = [i.strip() for i in f.readlines()]

    total_p1, total_p2 = 0, 0
    tracking_p1, tracking_p2 = {}, {}
    for line in txt_input:
        char_string = line.split(" ")[0]
        nums = tuple(int(i) for i in line.split(" ")[1].split(","))
        arrangements_p1 = count_arrangements(char_string, nums, tracking_p1)
        arrangements_p2 = count_arrangements("?".join([char_string] * 5), nums * 5, tracking_p2)

        total_p1 += arrangements_p1
        total_p2 += arrangements_p2

    print(f"Solution (p1) - {total_p1}")
    print(f"Solution (p2) - {total_p2}")


if __name__ == "__main__":
    main()
