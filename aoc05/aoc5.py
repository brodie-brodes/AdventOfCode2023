def map_vals_p1(src_val, src_to_dest_keys):
    """Map a single value for a single source-to-destination key set
    (e.g. seed-to-soil)"""
    for dest_key_start, src_key_start, key_length in src_to_dest_keys:
        diff = src_val - src_key_start

        # If source value is less than start of source key, value is unmappable
        if diff < 0:
            continue

        if diff <= key_length:
            return dest_key_start + diff

    # If value wasn't mappable, return it unchanged
    return src_val


def get_mappable_ranges(r1, r2):
    """Get the intersection of two ranges, defined as (start, length)
    Intersection is mappable, remainder is unmappable"""

    # Case where there is no overlap/intersection
    if (r1[0] + r1[1]) < r2[0] or (r1[0] > r2[0] + r2[1]):
        return [], [r1]  # Return empty mappable val list, full original range as unmappable


    # Case where r1 is entirely within r2
    if r1[0] >= r2[0] and (r1[0] + r1[1]) < (r2[0] + r2[1]):
        return [r1], []

    # Case where r2 is entirely within r1
    if r2[0] >= r1[0] and (r2[0] + r2[1]) <= (r1[0] + r1[1]):
        mappable = [r2]
        unmappable = [(r1[0], r2[0] - r1[0]), (r2[0] + r2[1], (r1[0] + r1[1]) - (r2[0] + r2[1]) - 1)]
        return [r for r in mappable if r[1] > 0], [r for r in unmappable if r[1] > 0]  # Avoid including length-0 ranges

    # Case where r1 intersects r2 on the left
    if r1[0] < r2[0] and r1[0] + r1[1] > r2[0]:
        mappable = [(r2[0], (r1[0] + r1[1]) - r2[0])]
        unmappable = [(r1[0], r2[0] - r1[0])]
        return mappable, unmappable

    # Case where r1 intersects r2 on the right
    if r1[0] > r2[0] and (r1[0] + r1[1]) + (r2[0] + r2[1]):
        mappable = [(r1[0], (r2[0] + r2[1] - r1[0]))]
        unmappable = [(r2[0] + r2[1], (r1[0] + r1[1]) - (r2[0] + r2[1]))]
        return mappable, unmappable

    raise ValueError("Unhandled case - ", r1, r2)


def map_ranges_p2(unmapped_ranges, src_to_dest_keys):
    """Map value ranges for a single source-to-destination key set
    (e.g. seed-to-soil)"""
    mapped_ranges = []
    for dest_key_start, src_key_start, key_length in src_to_dest_keys:
        new_unmapped_ranges = []
        diff = dest_key_start - src_key_start
        for unmapped_range in unmapped_ranges:
            mappable_ranges, unmappable_ranges = get_mappable_ranges(unmapped_range, (src_key_start, key_length))
            new_unmapped_ranges.extend(unmappable_ranges)
            for r in mappable_ranges:
                mapped_ranges.append((r[0] + diff, r[1]))

        unmapped_ranges = new_unmapped_ranges


    return mapped_ranges + unmapped_ranges



def p1():
    """Part 1"""

    # Parse the input
    key_sets = {}
    key_set_order = []
    with open("input.txt") as f:
        text = f.read()
        seeds = [int(i) for i in text.split("\n")[0].split(": ")[1].split(" ")]

        for key_set in text.split("\n\n")[1:]:
            key_set_name = key_set.split("\n")[0].split(" ")[0]
            key_set_order.append(key_set_name)
            key_set_vals = [[int(i) for i in key.split(" ")] for key in key_set.split("\n")[1:]]

            key_sets[key_set_name] = key_set_vals

    # Map the values
    result_values = []
    for value in seeds:
        for key_set_name in key_set_order:
                value = map_vals_p1(value, key_sets[key_set_name])

        result_values.append(value)

    print(f"Solution (p1) - {min(result_values)}")


def p2():
    """Part 2"""

    # Parse the input (slightly differently for part 2)
    key_sets = {}
    key_set_order = []
    with open("input.txt") as f:
        text = f.read()
        values = [int(i) for i in text.split("\n")[0].split(": ")[1].split(" ")]
        values = [(i, j) for i, j in zip(values[::2], values[1:][::2])]
        for key_set in text.split("\n\n"):
            key_set_name = key_set.split("\n")[0].split(" ")[0]
            key_set_order.append(key_set_name)
            key_set_vals = [[int(i) for i in key.split(" ")] for key in key_set.split("\n")[1:]]

            key_sets[key_set_name] = key_set_vals

    # Map the values
    for key_set_name in key_set_order:
        values = map_ranges_p2(values, key_sets[key_set_name])

    print(f"Solution (p2) - {min([r[0] for r in values])}")


if __name__ == "__main__":
    p1()
    p2()