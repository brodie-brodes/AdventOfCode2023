puzzle_input = [line.strip() for line in open("input.txt")]


def count_winning_numbers(card):
    nums = card.split(":")[1].strip()
    winning_nums = [int(i) for i in nums.split(" | ")[0].strip().replace("  ", " ").split(" ")]
    my_nums = [int(i) for i in nums.split(" | ")[1].strip().replace("  ", " ").split(" ")]
    my_winning_nums = [i for i in my_nums if i in winning_nums]
    return len(my_winning_nums)
    
    
def calc_points(num_winning_nums):
    return 2 ** (num_winning_nums - 1) if num_winning_nums else 0
    
def count_all_points(main_card):
    total_points = 0
    for card in main_card:
        num_winning_nums = count_winning_numbers(card)
        points = calc_points(num_winning_nums)
        total_points += points
    
    return total_points

def p1(cards):
    total_points = count_all_points(cards)

    print(f"Solution (p1) - {total_points}")


def p2(cards):
    card_copy_counts = {idx: 1 for idx in range(len(cards))}
    all_cards = []
    
    # Generate all copies of each card, iterating down the list
    for card_idx, card in enumerate(cards):
        num_winning_nums = count_winning_numbers(card)
        for _ in range(card_copy_counts[card_idx]):
            all_cards.extend(cards[card_idx + 1: card_idx + 1 + num_winning_nums])
            for iter_idx in range(card_idx + 1, card_idx + 1 + num_winning_nums):
                card_copy_counts[iter_idx] += 1

    # Add in the original copies of each card
    all_cards.extend(cards)

    print(f"Solution (p2) - {len(all_cards)}")

p1(puzzle_input)
p2(puzzle_input)