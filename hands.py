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
        self.__hand = hand

    def getName(self):
        return self.__name

    def receiveCard(self, new_card):
        if isinstance(new_card, Card):
            self.__hand.append(new_card)

    def receive_cards(self, cards):
        self.__hand = cards

    def showHand(self):
        hand_str = []
        for card in self.__hand:
            hand_str.append(card)
        print(hand_str)

    def __get_three(self, hand):
        value_list = []
        for i in hand:
            value_list.append(i.getValue().value)
            res = value_list.count(i.getValue().value)
            if res == 3:
                three_cards = [x for x in value_list if value_list.count(x) == 3]
                other_cards = [x for x in value_list if x not in three_cards]
                new_hand = three_cards + sorted(other_cards, reverse=True)
                return HandRank.THREE, new_hand[:5]
        return None

    def __get_pair(self, __hand):
        # search for any card pair that has a duplicate, sort rest of the cards
        # return pair with largest 3 values of cards left
        seen_cards = []
        pair_cards = []
        for hand_card in __hand:
            for seen_card in seen_cards:
                if hand_card == seen_card:
                    pair_cards.extend([hand_card, seen_card])
                    left_cards = [x for x in __hand if x not in pair_cards]
                    left_cards.sort()
                    return_hand = pair_cards + left_cards
                    return HandRank.PAIR, return_hand[0:5]
            seen_cards.append(hand_card)
        return None

    def __get_two_pairs(self, hnd):
        values = []
        unique = []
        pair = 0
        paired_crds = []
        notpaired_crds = []
        for value in hnd:
            values.append(value.getValue().value)
            if value.getValue().value not in values:
                unique.append(value.getValue().value)
        for a in unique:
            if values.count(a) == 2:
                pair += 1
                for b in hnd:
                    if a == b.getValue().value:
                        paired_crds.append(b)
                    else:
                        notpaired_crds.append(b)
        if pair == 2:
            returnhand = paired_crds + notpaired_crds
            return HandRank.TWO_PAIRS, returnhand[0:5]
        else:
            return None

    def __get_flush(self, l):
        list_of_hearts = [card for card in l if card.getSuit().name == "HEARTS"]
        list_of_diamonds = [card for card in l if card.getSuit().name == "DIAMONDS"]
        list_of_clubs = [card for card in l if card.getSuit().name == "CLUBS"]
        list_of_spades = [card for card in l if card.getSuit().name == "SPADES"]
        checking_list = [list_of_clubs, list_of_diamonds, list_of_spades, list_of_hearts]
        for cards in checking_list:
            if len(cards) == 5:
                return HandRank.FLUSH, cards.sort(reverse=True)
        return None

    def __get_royal_flush(self, l):
        list_of_hearts = [card for card in l if card.getSuit().name == "HEARTS"]
        list_of_diamonds = [card for card in l if card.getSuit().name == "DIAMONDS"]
        list_of_clubs = [card for card in l if card.getSuit().name == "CLUBS"]
        list_of_spades = [card for card in l if card.getSuit().name == "SPADES"]
        checking_list = [list_of_clubs, list_of_diamonds, list_of_spades, list_of_hearts]
        for cards in checking_list:
            if len(cards) == 5:
                suited = sorted(cards, reverse=True)
                cheking = []
                for i in range(5):
                    cheking.append(suited[i].getValue().name)
                if cheking == ["ACE", "KING", "QUEEN", "JACK", "TEN"]:
                    return HandRank.ROYAL_FLUSH, suited
        return None

    def __get_straight_flush(self, cards_on_hand: list):
        cardsBySuit = {}
        if len(cards_on_hand) < 7:
            raise BaseException("There should be 7 cards on hand!")

        for card in cards_on_hand:
            if card.getSuit() not in cardsBySuit:
                cardsBySuit[card.getSuit()] = []
            cardsBySuit[card.getSuit()].append(card)

        cardsBySuitSorted = dict(sorted(cardsBySuit.items(), key=lambda item: len(item[1]), reverse=True))
        longest_list = next(iter(cardsBySuitSorted.items()))[1]
        if not len(longest_list) >= 5:
            return None

        longest_list.sort(reverse=True)
        last_card = None
        for card in longest_list:
            if not last_card:
                last_card = card
                continue
            if (last_card.getValue().value - card.getValue().value != 1):
                return None
            else:
                last_card = card
        else:
            return (HandRank.STRAIGHT_FLUSH, longest_list[:5])

        cardsBySuitSorted = dict(sorted(cardsBySuit.items(), key=lambda item: len(item[1]), reverse=True))
        longest_list = next(iter(cardsBySuitSorted.items()))[1]
        if not len(longest_list) >= 5:
            return None

    def __get_straight(self, hand):
        # l = hand
        straight = False
        hand.sort()
        for i in range(0, len(hand) - 1):
            if hand[i].getValue().value is hand[i + 1].getValue().value + 1:
                straight = True
        if straight:
            return HandRank.STRAIGHT, hand
        else:
            return None

    def __get_highest_card(self, hand):
        hand.sort(reverse=True)
        return HandRank.HIGHEST_CARD, hand[0:6]

    def __get_four(self, hand):
        value_list = []
        for i in hand:
            value_list.append(i.getValue().value)
            res = value_list.count(i.getValue().value)
            if res == 4:
                four_cards = [x for x in value_list if value_list.count(x) == 4]
                other_cards = [x for x in value_list if x not in four_cards]
                new_hand = four_cards + sorted(other_cards, reverse=True)
                return HandRank.FOUR, new_hand[:5]
        return None

    def __get_full_house(self, hand):
        three_of_a_kind = self.__get_three(hand)
        pair = self.__get_pair(hand)
        if three_of_a_kind and pair:
            three = three_of_a_kind[1][0:3]
            two = pair[1][0:2]
            returnhand = three + two
            return HandRank.FULL_HOUSE, returnhand
        return None

    def getHighestRank(self):
        ret = None
        ret = self.__get_royal_flush(self.__hand)
        if ret:
            return ret

        ret = self.__get_straight_flush(self.__hand)
        if ret:
            return ret

        ret = self.__get_four(self.__hand)
        if ret:
            return ret

        ret = self.__get_full_house(self.__hand)
        if ret:
            return ret

        ret = self.__get_flush(self.__hand)
        if ret:
            return ret

        ret = self.__get_straight(self.__hand)
        if ret:
            return ret

        ret = self.__get_three(self.__hand)
        if ret:
            return ret

        ret = self.__get_two_pairs(self.__hand)
        if ret:
            return ret

        ret = self.__get_pair(self.__hand)
        if ret:
            return ret

        return self.__get_highest_card(self.__hand)



from card import *

values = list(CardRank)
suits = list(Suit)

card1 = Card(values[12], suits[0])
card2 = Card(values[12], suits[1])
card3 = Card(values[12], suits[2])
card4 = Card(values[12], suits[3])
card5 = Card(values[11], suits[0])
card6 = Card(values[2], suits[2])
card7 = Card(values[2], suits[2])

hand = Hand("mi")
hand1 = [card1, card2, card3, card4, card5, card6, card7]
hand.receive_cards(hand1)
ret = hand.getHighestRank()

hand1 = HandRank.FOUR
some_hand_rank = HandRank.FULL_HOUSE

# Compare two HandRank values
if HandRank.THREE.value > HandRank.PAIR.value:
    print("Three of a kind beats a pair")

# Use a HandRank value in a conditional statement
if some_hand_rank.value == HandRank.FULL_HOUSE.value:
    print("You have a full house!")

# Convert an integer value back to a HandRank value
hand_rank_value = 3
hand_rank = HandRank(hand_rank_value)
print(hand_rank == HandRank.THREE)  # prints True


print()
print(ret[0])
print(ret[1])

