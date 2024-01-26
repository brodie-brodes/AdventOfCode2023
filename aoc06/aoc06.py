def val_wins_race(val, race_time, best_dist):
    moving_time = race_time - val
    if moving_time * val > best_dist:
        return True

    return False


def count_ways_to_win(race_time, best_dist):
    ways_to_win = 0
    for val in range(1, race_time):
        if val_wins_race(val, race_time, best_dist):
            ways_to_win += 1

    return ways_to_win


def p1():
    with open("input.txt") as f:
        times, distances = f.read().strip().split("\n")
        times = [int(i) for i in times.split(" ")[1:] if i != ""]
        distances = [int(i) for i in distances.split(" ")[1:] if i != ""]

    print(times, distances)
    solution = 1
    for race_time, best_dist in zip(times, distances):
        solution *= count_ways_to_win(race_time, best_dist)

    print(f"Solution (p1) - {solution}")


def p2():
    with open("input.txt") as f:
        times, distances = f.read().strip().split("\n")
        times = [int(times.replace(" ", "").lstrip("Time:"))]
        distances = [int(distances.replace(" ", "").lstrip("Distance:"))]

    solution = 1
    for race_time, best_dist in zip(times, distances):
        print(solution)
        solution *= count_ways_to_win(race_time, best_dist)

    print(f"Solution (p2) - {solution}")


if __name__ == "__main__":
    p1()
    p2()