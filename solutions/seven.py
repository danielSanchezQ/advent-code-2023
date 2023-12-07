from utils import input_stream
from collections import Counter

CARDS_VALUES = dict(zip('23456789TJQKA', range(13)))
JOKERIZE_CARDS_VALUES = dict(zip('J23456789TQKA', range(13)))


class Hand:
    __slots__ = ["hand", "bet", "suit", "points"]

    def __init__(self, data, cards_values=CARDS_VALUES):
        hand, bet = data.split()
        self.hand = hand
        self.bet = int(bet)
        self.suit = self._suit(self.hand)
        self.points = tuple(cards_values[c] for c in self.hand)

    def __repr__(self):
        return f"({self.hand}, {self.suit}, {self.points}, {self.bet})"

    @staticmethod
    def _suit(hand):
        count = Counter(hand)
        match len(count):
            case 1:
                # 5
                return 6
            case 2:
                # 4+1
                if any(s == 4 for s in count.values()):
                    return 5
                # 3+2
                return 4
            case 3:
                # 3
                if any(s == 3 for s in count.values()):
                    return 3
                # 2+2+1
                return 2
            case 4:
                # 2
                return 1
            case 5:
                # nothing
                return 0


class JokerizeHand(Hand):
    def __init__(self, hand):
        super().__init__(hand, cards_values=JOKERIZE_CARDS_VALUES)

    @staticmethod
    def _suit(hand):
        count = Counter(hand)
        jokers = count.pop('J') if 'J' in count else 0
        if jokers == 5:
            return 6
        max_key = max(count.keys(), key=lambda k: count[k])
        count[max_key] += jokers
        return Hand._suit("".join(c*v for c, v in count.items()))


def solve(data_stream, hand_cls):
    hands = [hand_cls(l) for l in data_stream]
    hands.sort(key=lambda c: (c.suit, c.points))
    return sum(i*c.bet for i, c in enumerate(hands, start=1))


if __name__ == "__main__":
    print(f"First: {solve(input_stream('../inputs/007.txt'), Hand)}")
    print(f"Second: {solve(input_stream('../inputs/007.txt'), JokerizeHand)}")