from card import Card
from enum import Enum, auto, unique


class HandRank(Enum):
    HIGHEST_CARD = auto()
    PAIR = auto()
    TWO_PAIRS = auto()
    THREE = auto()
    STRAIGHT = auto()
    FLUSH = auto()
    FULL_HOUSE = auto()
    FOUR = auto()
    STRAIGHT_FLUSH = auto()
    ROYAL_FLUSH = auto()


class Hand:
    def __init__(self, hand):
        self.hand = hand
        self.hand_rank = self.getHighestRank()

    def get_hand_rank(self):
        return self.hand_rank

    def sort_hand(self):
        self.hand = sorted(self.hand, reverse=True)

    def receiveCard(self, new_card):
        if isinstance(new_card, Card):
            self.hand.append(new_card)

    def receive_cards(self, cards):
        self.hand = cards

    def showHand(self):
        hand_str = []
        for card in self.hand:
            hand_str.append(card)
        print(hand_str)

    def __get_royal_flush(self, l):
        list_of_hearts = [card for card in l if card.getSuit().name == "HEARTS"]
        list_of_diamonds = [card for card in l if card.getSuit().name == "DIAMONDS"]
        list_of_clubs = [card for card in l if card.getSuit().name == "CLUBS"]
        list_of_spades = [card for card in l if card.getSuit().name == "SPADES"]
        checking_list = [list_of_clubs, list_of_diamonds, list_of_spades, list_of_hearts]
        for cards in checking_list:
            suited = sorted(cards, reverse=True)
            suited_cards = suited[:5]
            if len(suited_cards) == 5:
                cheking = []
                for i in range(5):
                    cheking.append(suited[i].getValue().name)
                if cheking == ["ACE", "KING", "QUEEN", "JACK", "TEN"]:
                    return HandRank.ROYAL_FLUSH, suited
        return None

    def __get_straight_flush(self, cards_on_hand: list):
        cards_by_suit = {}
        if len(cards_on_hand) < 7:
            raise ValueError("There should be 7 cards on hand!")

        for card in cards_on_hand:
            if card.getSuit() not in cards_by_suit:
                cards_by_suit[card.getSuit()] = []
            cards_by_suit[card.getSuit()].append(card)

        for suit, cards in cards_by_suit.items():
            if len(cards) >= 5:
                cards.sort(reverse=True)
                last_value = cards[0].getValue().value
                straight_flush = [cards[0]]
                count = 1

                for i in range(1, len(cards)):
                    if cards[i].getValue().value == last_value - 1:
                        straight_flush.append(cards[i])
                        last_value = cards[i].getValue().value
                        count += 1

                        if count == 5:
                            return HandRank.STRAIGHT_FLUSH, straight_flush

                    elif cards[i].getValue().value != last_value:
                        straight_flush = [cards[i]]
                        last_value = cards[i].getValue().value
                        count = 1

        return None

        cardsBySuitSorted = dict(sorted(cardsBySuit.items(), key=lambda item: len(item[1]), reverse=True))
        longest_list = next(iter(cardsBySuitSorted.items()))[1]
        if not len(longest_list) >= 5:
            return None

    def __get_four(self, hand):
        value_list = []
        for card in hand:
            value_list.append(card)
            res = value_list.count(card)
            if res == 4:
                four_cards = [card] * 4
                other_cards = [x for x in hand if x != card]
                other_cards.sort(reverse=True)
                new_hand = four_cards + other_cards[:1]
                return HandRank.FOUR, new_hand[:5]
        return None

    def __get_full_house(self, hand):
        three_of_a_kind = self.__get_three(hand)
        if three_of_a_kind:
            remaining_cards = [card for card in hand if card not in three_of_a_kind[1][:3]]
            pair = self.__get_pair(remaining_cards)
            if pair:
                three = three_of_a_kind[1][0:3]
                two = pair[1][0:2]
                returnhand = three + two
                return HandRank.FULL_HOUSE, returnhand[:5]  # Return 5 cards of the full house
        return None

    def __get_flush(self, l):
        list_of_hearts = [card for card in l if card.getSuit().name == "HEARTS"]
        list_of_diamonds = [card for card in l if card.getSuit().name == "DIAMONDS"]
        list_of_clubs = [card for card in l if card.getSuit().name == "CLUBS"]
        list_of_spades = [card for card in l if card.getSuit().name == "SPADES"]
        checking_list = [list_of_clubs, list_of_diamonds, list_of_spades, list_of_hearts]
        for cards in checking_list:
            if len(cards) >= 5:
                sorted_cards = sorted(cards, reverse=True)
                return HandRank.FLUSH, sorted_cards[:5]
        return None

    def __get_straight(self, hand):
        hand.sort()
        straight_count = 1
        max_straight_count = 1
        max_straight_index = 0

        for i in range(len(hand) - 1):
            if hand[i].getValue().value == hand[i + 1].getValue().value - 1:
                straight_count += 1
                if straight_count > max_straight_count:
                    max_straight_count = straight_count
                    max_straight_index = i + 1
            elif hand[i].getValue().value != hand[i + 1].getValue().value:
                straight_count = 1

        if max_straight_count >= 5:
            straight_hand = hand[max_straight_index - max_straight_count + 1: max_straight_index + 1]
            return HandRank.STRAIGHT, straight_hand[-5:]  # Return the highest 5 cards
        else:
            return None

    def __get_three(self, hand):
        value_list = []
        for i in hand:
            value_list.append(i.getValue().value)
        for value in value_list:
            if value_list.count(value) == 3:
                three_cards = [x for x in hand if x.getValue().value == value]
                other_cards = [x for x in hand if x not in three_cards]
                new_hand = three_cards + sorted(other_cards, key=lambda x: x.getValue().value, reverse=True)
                return HandRank.THREE, new_hand[:5]
        return None

    def __get_two_pairs(self, hand):
        res1 = self.__get_pair(hand)
        if res1 is not None and res1[0] == HandRank.PAIR:
            hand2 = []
            for c in hand:
                if c not in res1[1][:2]:
                    hand2.append(c)
            res2 = self.__get_pair(hand2)
            if res2 is not None and res2[0] == HandRank.PAIR:
                return_hand = res1[1][:2] + res2[1][:3]
                return HandRank.TWO_PAIRS, return_hand

        return None

    def __get_pair(self, __hand):
        # search for any card pair that has a duplicate, sort the rest of the cards
        # return the pair with the largest 3 values of cards left
        seen_cards = []
        pair_cards = []
        for hand_card in __hand:
            for seen_card in seen_cards:
                if hand_card == seen_card:
                    pair_cards.extend([hand_card, seen_card])
                    left_cards = [x for x in __hand if x not in pair_cards]
                    left_cards.sort(reverse=True)
                    return_hand = pair_cards + left_cards[:3]
                    return HandRank.PAIR, return_hand
            seen_cards.append(hand_card)
        return None

    def __get_highest_card(self, hand):
        hand = sorted(hand, reverse=True)
        return HandRank.HIGHEST_CARD, hand[0:5]

    def getHighestRank(self):
        ret = None
        self.sort_hand()
        ret = self.__get_royal_flush(self.hand)
        if ret:
            return ret

        ret = self.__get_straight_flush(self.hand)
        if ret:
            return ret

        ret = self.__get_four(self.hand)
        if ret:
            return ret

        ret = self.__get_full_house(self.hand)
        if ret:
            return ret

        ret = self.__get_flush(self.hand)
        if ret:
            return ret

        ret = self.__get_straight(self.hand)
        if ret:
            return ret

        ret = self.__get_three(self.hand)
        if ret:
            return ret

        ret = self.__get_two_pairs(self.hand)
        if ret:
            return ret

        ret = self.__get_pair(self.hand)
        if ret:
            return ret

        return self.__get_highest_card(self.hand)