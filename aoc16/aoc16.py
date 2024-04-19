class Grid():
    def __init__(self, input_path):
        self.tiles = {}

        # Load input and pad with a single layer of "." on all sides
        input_grid = ["." + l.strip() + "." for l in open(input_path)]
        input_grid = ["." * len(input_grid[0])] + input_grid + ["." * len(input_grid[0])]

        self.rows, self.cols = len(input_grid), len(input_grid[0])

        for row_idx, row in enumerate(input_grid):
            for col_idx, tile_char in enumerate(row.strip()):
                self.tiles[(row_idx, col_idx)] = Tile(self, tile_char, (row_idx, col_idx))

        self.beams = []
        self.beam_configs_seen = set()

    def add_new_beam(self, direction, starting_tile_pos):
        # Only add the beam if an identical beam configuration hasn't already been seen
        if not (direction, starting_tile_pos) in self.beam_configs_seen:
            starting_tile = self.tiles[starting_tile_pos]
            starting_tile.energized = True
            self.beams.append(Beam(self, starting_tile, direction))


    def move_beams(self):
        for beam in self.beams:
            beam.move()

            # Remove beam from list if it went off-grid
            if beam.tile is None:
                self.beams.remove(beam)
                del(beam)
            elif (beam.direction, beam.tile.pos) in self.beam_configs_seen:
                self.beams.remove(beam)
                del(beam)
            else:
                self.beam_configs_seen.add((beam.direction, beam.tile.pos))


    def count_energized_for_start_beam(self, start_beam_pos, start_beam_direction):
        self.add_new_beam(start_beam_direction, start_beam_pos)

        while self.beams:
            self.move_beams()

        return self.count_energized()

    def get_tile(self, pos):
        if pos in self.tiles:
            return self.tiles[pos]

    def count_energized(self):
        c = 0
        for pos, tile in self.tiles.items():
            if pos[0] in [0, self.rows - 1] or pos[1] in [0, self.cols - 1]:
                continue
            if tile.energized:
                c += 1

        return c


class Tile():
    def __init__(self, grid, char, pos):
        self.grid = grid
        self.char = char
        self.pos = pos

        self.energized = False


class Beam():
    def __init__(self, grid, starting_tile, direction):
        self.direction = direction
        self.tile = starting_tile
        self.grid = grid

    def move(self):
        next_pos = {
            "r": (self.tile.pos[0], self.tile.pos[1] + 1),
            "l": (self.tile.pos[0], self.tile.pos[1] - 1),
            "u": (self.tile.pos[0] - 1, self.tile.pos[1]),
            "d": (self.tile.pos[0] + 1, self.tile.pos[1]),
        }[self.direction]

        self.tile = self.grid.get_tile(next_pos)

        if self.tile is None:
            return None

        self.tile.energized = True

        if self.tile.char == "/":
            self.direction = {"r": "u", "l": "d", "u": "r", "d": "l"}[self.direction]

        elif self.tile.char == "\\":
            self.direction = {"r": "d", "l": "u", "u": "l", "d": "r"}[self.direction]

        elif self.tile.char == "|":
            if self.direction in ["r", "l"]:
                # only add new beams if identical beam doesn't already exist at position
                placed = False
                if not any([(b.tile.pos == self.tile.pos and b.direction) == "d" for b in self.grid.beams]):
                        placed = True
                        self.direction = "d"
                if not any([(b.tile.pos == self.tile.pos and b.direction) == "u" for b in self.grid.beams]):
                    if placed:
                        self.grid.add_new_beam("u", self.tile.pos)
                    else:
                        self.direction = "u"

        elif self.tile.char == "-":
            if self.direction in ["u", "d"]:
                # only add new beams if identical beam doesn't already exist at position
                placed = False
                if not any([(b.tile.pos == self.tile.pos and b.direction) == "r" for b in self.grid.beams]):
                    placed = True
                    self.direction = "r"
                if not any([(b.tile.pos == self.tile.pos and b.direction) == "l" for b in self.grid.beams]):
                    if placed:
                        self.grid.add_new_beam("l", self.tile.pos)
                    else:
                        self.direction = "l"


def main():
    # Do part 1
    grid = Grid("input.txt")
    p1_energized = grid.count_energized_for_start_beam((1, 0), 'r')
    print(f"Solution (p1) - {p1_energized}")

    # Do part 2
    p2_energized_max = 0
    start_positions_directions = \
        [((0, col), "d") for col in range(1, grid.cols - 1)] + \
        [((row, 0), "r") for row in range(1, grid.rows - 1)] + \
        [((grid.rows - 1, col), "u") for col in range(1, grid.cols - 1)] + \
        [((row, grid.cols - 1), "l") for row in range(1, grid.rows - 1)]

    for pos, direction in start_positions_directions:
        grid = Grid("input.txt")
        energized = grid.count_energized_for_start_beam(pos, direction)
        if energized > p2_energized_max:
            p2_energized_max = energized

    print(f"Solution (p2) - {p2_energized_max}")


if __name__ == "__main__":
    main()