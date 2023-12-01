puzzle_input = [line.strip() for line in open("input.txt")]

def p1(puzzle_input):
    s = 0
    for line in puzzle_input:
        val = ""
        for c in line:
            if c in "0123456789":
                val += c
                break
        for c in line[::-1]:
            if c in "0123456789":
                val += c
                break
        
        s += int(val)
    
    print(f"Solution (p1) - {s}")


def get_n_p2(string, pos):
    if string[pos] in "0123456789":
        return string[pos]
    nums = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    nums_dict = {n: idx for idx, n in enumerate(nums)}
    for num in ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]:
        if string[pos:pos + len(num)] == num:
            return nums_dict[num]
    
def p2(puzzle_input):
    s = 0
    for line in puzzle_input:
        val = ""
        for idx in range(len(line)):
            n = get_n_p2(line, idx)
            if n:
                val += str(n)
                break
        for idx in range(len(line) - 1, -1, -1):
            n = get_n_p2(line, idx)
            if n:
                val += str(n)
                break
    

    
        s += int(val)

    print(f"Solution (p2) - {s}")


if __name__ == "__main__":
    p1(puzzle_input)
    p2(puzzle_input)