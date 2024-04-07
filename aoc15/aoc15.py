def hash_str(string):
    current_val = 0

    for c in string:
        current_val += ord(c)
        current_val *= 17
        current_val %= 256

    return current_val


def p1():
    input_txt = open("input.txt").read().strip()

    total = 0
    for elem in input_txt.split(","):
        total += hash_str(elem)

    print(f"Solution (p1) - {total}")


def p2():
    input_txt = open("input.txt").read().strip()

    boxes = {}
    for i in range(256):
        boxes[i] = []

    for instruction in input_txt.split(","):

        # Handle dash (-) case
        if instruction.endswith("-"):
            label = instruction[:-1]
            box_num = hash_str(label)

            for item in boxes[box_num]:
                if item.startswith(f"{label} "):
                    boxes[box_num].remove(item)

        # Handle equals (=) case
        else:
            label, focal_len = instruction.split("=")
            box_num = hash_str(label)
            placed = False

            # Check if box contains lens with same label and replace if yes
            for idx, lens in enumerate(boxes[box_num]):
                if lens.startswith(f"{label} "):
                    boxes[box_num][idx] = f"{label} {focal_len}"
                    placed = True

            # Otherwise, add lens to the end of the box
            if not placed:
                boxes[box_num].append(f"{label} {focal_len}")

    # Calculate focal power
    focal_power = 0
    for box_num, box in boxes.items():
        box_focal_power = sum([(box_num + 1) * (slot_number + 1) * int(lens.split(" ")[1]) for slot_number, lens in enumerate(box)])
        focal_power += box_focal_power

    print(f"Solution (p2) - {focal_power}")


if __name__ == "__main__":
    p1()
    p2()
