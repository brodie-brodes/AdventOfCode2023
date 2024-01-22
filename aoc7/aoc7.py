from functools import cmp_to_key

def determine_hand(hand):
    """Determine what the hand type is for a single hand"""
    # 5- and 4-of-a-kind
    for n in [5, 4]:
        if any([hand.count(c) == n for c in hand]):
            return f"{n} of a kind"

    # 3-of-a-kind and full house
    pair = any([hand.count(c) == 2 for c in hand])
    kind3 = any([hand.count(c) == 3 for c in hand])
    if kind3 and pair:
        return "full house"
    elif kind3:
        return "3 of a kind"

    # check separately for 2-pair before returing pairf
    if [hand.count(c) == 2 for c in hand].count(True) == 4:
        return "2 pair"
    elif pair:
        return "pair"

    return "high card"

def sort_card_key(hand1, hand2):
    """Compare two hands based on part 1's rules"""
    hand1, hand2 = hand1.split(" ")[0], hand2.split(" ")[0]
    card_order = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    hand_order = ["5 of a kind", "4 of a kind", "full house", "3 of a kind", "2 pair", "pair", "high card"]

    hand1_type = determine_hand(hand1)
    hand2_type = determine_hand(hand2)

    # Determine which hand is higher based on specified ranking
    if hand_order.index(hand1_type) > hand_order.index(hand2_type):
        return -1
    if hand_order.index(hand1_type) < hand_order.index(hand2_type):
        return 1

    # If hands are the same, determine higher hand based on ordered high cards
    for idx in range(5):
        if card_order.index(hand1[idx]) > card_order.index(hand2[idx]):
            return -1
        if card_order.index(hand1[idx]) < card_order.index(hand2[idx]):
            return 1


def sort_card_key_p2(hand1, hand2):
    """Compare two hands based on part 2's rules"""
    hand1, hand2 = hand1.split(" ")[0], hand2.split(" ")[0]
    card_order = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
    hand_order = ["5 of a kind", "4 of a kind", "full house", "3 of a kind", "2 pair", "pair", "high card"]

    hand1_type = determine_hand(hand1)
    hand2_type = determine_hand(hand2)

    # Swap J in each hand for every possible card and take the best resulting hand
    for c in card_order:
        hand1_jswap = hand1.replace("J", c)
        hand1_jswap_type = determine_hand(hand1_jswap)
        if hand_order.index(hand1_jswap_type) < hand_order.index(hand1_type):
            hand1_type = hand1_jswap_type

        hand2_jswap = hand2.replace("J", c)
        hand2_jswap_type = determine_hand(hand2_jswap)
        if hand_order.index(hand2_jswap_type) < hand_order.index(hand2_type):
            hand2_type = hand2_jswap_type

    # Determine which hand is higher based on specified ranking
    if hand_order.index(hand1_type) > hand_order.index(hand2_type):
        return -1
    if hand_order.index(hand1_type) < hand_order.index(hand2_type):
        return 1

    # If hands are the same, determine higher hand based on ordered high cards
    for idx in range(5):
        if card_order.index(hand1[idx]) > card_order.index(hand2[idx]):
            return -1
        if card_order.index(hand1[idx]) < card_order.index(hand2[idx]):
            return 1


def p1():
    cards = [line.strip() for line in open("input.txt")]
    cards.sort(key=cmp_to_key(sort_card_key))

    solution = 0
    for idx, card in enumerate(cards):
        solution += (idx + 1) * int(card.split(" ")[1])

    print(f"Solution (p1) - {solution}")


def p2():
    cards = [line.strip() for line in open("input.txt")]
    cards.sort(key=cmp_to_key(sort_card_key_p2))

    solution = 0
    for idx, card in enumerate(cards):
        solution += (idx + 1) * int(card.split(" ")[1])

    print(f"Solution (p2) - {solution}")

if __name__ == "__main__":
    p1()
    p2()