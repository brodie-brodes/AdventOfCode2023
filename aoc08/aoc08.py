import math


def p1():
    with open("input.txt") as f:
        text = f.read()

    instructions, network = text.split("\n\n")
    network = {l.split(" = ")[0]: [c for c in l.split(" = ")[1][1:-1].split(", ")] for l in network.split("\n")}

    steps = 0
    current_node = "AAA"
    instruction_idx = 0

    while not current_node.endswith("Z"):
        instruction = instructions[instruction_idx]

        current_node = network[current_node][0] if instruction == "L" else network[current_node][1]

        instruction_idx = instruction_idx + 1 if instruction_idx < len(instructions) - 1 else 0
        steps += 1

    print(f"Solution (p1) - {steps}")


def p2():
    with open("input.txt") as f:
        text = f.read()

    instructions, network = text.split("\n\n")

    network = {l.split(" = ")[0]: [c for c in l.split(" = ")[1][1:-1].split(", ")] for l in network.split("\n")}

    start_nodes = [node for node in network.keys() if node.endswith("A")]

    # Get number of steps required to reach a Z node for each start node
    steps_to_reach_z_node = []
    for node in start_nodes:
        instruction_idx = 0
        steps = 0
        current_node = node

        while not current_node.endswith("Z"):
            instruction = instructions[instruction_idx]

            current_node = network[current_node][0] if instruction == "L" else network[current_node][1]

            instruction_idx = instruction_idx + 1 if instruction_idx < len(instructions) - 1 else 0
            steps += 1

        steps_to_reach_z_node.append(steps)

    # Then take the lowest common multiple for each path
    print(f"Solution (p2) - {math.lcm(*steps_to_reach_z_node)}")


if __name__ == "__main__":
    p1()
    p2()