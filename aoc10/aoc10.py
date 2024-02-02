import numpy as np

connection_type_directions_neighbour = {
    "|": ["north", "south"],
    "-": ["east", "west"],
    "L": ["south", "west"],
    "J": ["south", "east"],
    "7": ["north", "east"],
    "F": ["north", "west"],
    ".": [],
    "S": []
}


connection_type_directions_self = {
    "|": ["north", "south"],
    "-": ["east", "west"],
    "L": ["north", "east"],
    "J": ["north", "west"],
    "7": ["south", "west"],
    "F": ["south", "east"],
    ".": [],
    "S": ["north", "south", "east", "west"]
}

empty_tile = np.array([
    np.array([".", ".", "."]),
    np.array([".", ".", "."]),
    np.array([".", ".", "."])
])

s_tile = np.array([
    np.array(["S", "S", "S"]),
    np.array(["S", "S", "S"]),
    np.array(["S", "S", "S"]),
])

char_to_line_mapping = {
    "F": [[2, 1], [1, 2]],
    "L": [[0, 1], [1, 2]],
    "|": [[0, 1], [2, 1]],
    "-": [[1, 0], [1, 2]],
    "J": [[0, 1], [1, 0]],
    "7": [[2, 1], [1, 0]]
}


def get_direction_pos(direction, x, y):
    direction_offsets = {
        "north": [x, y - 1],
        "south": [x, y + 1],
        "east": [x + 1, y],
        "west": [x - 1, y]
    }

    return direction_offsets[direction]


def get_distances_from_point(grid, distance_grid, queue, mapping):
    x, y = queue[0]
    current_point_character = grid[y][x]
    current_point_dist = distance_grid[y][x]
    neighbors_for_queue = []
    mapping[y][x] = current_point_character

    for direction in connection_type_directions_self[current_point_character]:
        neighbour_x, neighbour_y = get_direction_pos(direction, x, y)

        # Ensure neighbour position exists in grid
        if neighbour_x < 0 or neighbour_x >= len(grid[neighbour_y]) or neighbour_y < 0 or neighbour_y >= len(grid):
            continue

        # Get the pipe type at neighbor position
        neighbour_type = grid[neighbour_y][neighbour_x]

        # Check if neighbour is connected
        connected = direction in connection_type_directions_neighbour[neighbour_type]
        if not connected:
            continue

        # Check if neighbour already has distance associated with it
        neighbor_dist = distance_grid[neighbour_y][neighbour_x]

        # If it does not, or if its current distance value is larger than
        # current dist + 1, set it to current_dist + 1 and add it to the queue
        if neighbor_dist == "." or neighbor_dist > current_point_dist + 1:
            distance_grid[neighbour_y][neighbour_x] = current_point_dist + 1
            neighbors_for_queue.append([neighbour_x, neighbour_y])

    # Prepend any relevant neighbours to the queue and return
    return neighbors_for_queue + queue[1:]


def get_enclosed_area(grid):
    # Convert all instances of "." into "-" if they are not enclosed
    # (i.e. if they can connect to the grid's edge without crossing the main loop)
    # the enclosed area can then be measured by counting the total number of "." remaining

    # Get list of coordinates of all outside edge positions
    num_rows, num_cols = len(grid), len(grid[0])
    top_edge = [[0, i] for i in range(num_cols - 1)]
    bottom_edge = [[num_rows - 1, i] for i in range(num_cols - 1)]
    left_edge = [[i, 0] for i in range(num_rows - 1)]
    right_edge = [[i, num_cols - 1] for i in range(num_rows - 1)]
    queue = top_edge + bottom_edge + left_edge + right_edge
    c = 0
    while queue:
        c += 1
        y, x = queue[0]

        queue = queue[1:]
        if grid[y][x] == ".":
            grid[y][x] = "-"

            for neighbour_y, neighbour_x in [[y, x + 1], [y, x - 1], [y - 1, x], [y + 1, x]]:
                if neighbour_y < 0 or neighbour_y >= len(grid) or neighbour_x < 0 or neighbour_x >= len(grid[0]):
                    continue

                if grid[neighbour_y][neighbour_x] == ".":
                    queue = [[neighbour_y, neighbour_x]] + queue

    return grid

def convert_char_map_to_line_map(char_map):
    line_map = None
    for line in char_map:
        line_map_line = None
        for c in line:
            tile = empty_tile.copy()
            if c in char_to_line_mapping:
                tile[1][1] = "+"
                (p1y, p1x), (p2y, p2x) = char_to_line_mapping[c]
                tile[p1y][p1x] = "+"
                tile[p2y][p2x] = "+"
            else:
                if c not in ["S", "."]:
                    raise ValueError()

            if c == "S":
                tile = s_tile.copy()

            line_map_line = np.concatenate((line_map_line, tile), axis=1) if line_map_line is not None else tile

        line_map = np.concatenate((line_map, line_map_line), axis=0) if line_map is not None else line_map_line

    return line_map

def count_center_dots(line_map):
    row, col = 1, 1
    count = 0
    while row < line_map.shape[0]:
        while col < line_map.shape[1]:
            center_char = line_map[row][col]
            if center_char == ".":
                count += 1

            col += 3

        col = 1
        row += 3

    return count

def main():
    # Get the input
    grid = [line.strip() for line in open("input.txt")]
    distance_grid = []
    mapping = []

    # Compute the start position and create a distance grid
    for y in range(len(grid)):
        distance_line = []
        mapping_line = []
        for x in range(len(grid[y])):
            distance_line.append(".")
            mapping_line.append(".")
            if grid[y][x] == "S":
                start_x, start_y = x, y
        distance_grid.append(distance_line)
        mapping.append(mapping_line)

    distance_grid[start_y][start_x] = 0

    # We will use a queue-based system, as the grid is too large for a recursive approach
    queue = [[start_x, start_y]]

    # Populate the distance grid by branching out from the start position
    while queue:
        queue = get_distances_from_point(grid, distance_grid, queue, mapping)

    line_map = convert_char_map_to_line_map(mapping)

    # Compute the max distance to the starting point from any position
    max_dist = 0
    for y in range(len(distance_grid)):
        for x in range(len(distance_grid[y])):
            dist = distance_grid[y][x]
            if dist != "." and dist > max_dist:
                max_dist = dist

    area_enclosed = get_enclosed_area(line_map)
    size_area_enclosed = count_center_dots(area_enclosed)

    print(f"Solution (p1) - {max_dist}")
    print(f"Solution (p2) - {size_area_enclosed}")

if __name__ == "__main__":
    main()