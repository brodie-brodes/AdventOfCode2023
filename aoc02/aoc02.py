import numpy as np

puzzle_input = [line.strip() for line in open("input.txt")]

print(puzzle_input)

def main():
    available_balls = {"red": 12, "green": 13, "blue": 14}

    sum_possible_ids = 0
    sum_powers = 0
    for line in puzzle_input:
        game_id = int(line.split(":")[0].split(" ")[1])

        ball_sets = [i.strip() for i in line.split(":")[1].replace(";", ",").split(",")]
        game_balls_req = {color: 0 for color in ["red", "green", "blue"]}
        game_color_max = game_balls_req.copy()
        game_possible = True
        for ball_set in ball_sets:
            num = int(ball_set.split(" ")[0])
            color = ball_set.split(" ")[1]

            game_balls_req[color] += num
            if num > game_color_max[color]:
                game_color_max[color] = num

            if num > available_balls[color]:
                game_possible = False

        if game_possible:
            sum_possible_ids += game_id

        power = np.prod(list(game_color_max.values()))
        sum_powers += power

    print(f"Solution (p1) - {sum_possible_ids}")
    print(f"Solution (p2) - {sum_powers}")






if __name__ == "__main__":
    main()