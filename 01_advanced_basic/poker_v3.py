#!/usr/bin/env python
# -*- coding: utf-8 -*-

# use python3 

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокерва.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertoolsю
# Можно свободно определять свои функции и т.п.
# -----------------


import itertools as it
from collections import Counter

# good  
def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему """
    card_ranks_dict = {'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
    list_ranks = [card_ranks_dict[item[0]]  if item[0] in card_ranks_dict.keys() else int(item[0]) for item in hand]
    return sorted(list_ranks)

# good
def straight(ranks):
    pointer = ranks[0]
    counter = 0 
    for item in ranks[1:]:
        if int(item) - 1 == pointer:
            counter = counter + 1
        elif int(item) == pointer:
            pass
        else:
            counter = 0
        pointer = item
    if counter >= 4:
        return True
    else:
        return False    

# good
def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается 
    в данной руке.
    Возвращает None, если ничего не найдено
    """
    temp = Counter(ranks)
    output = []
    for k, v in temp.items():
        if v == n:
            output.append(k) 
    try:
        return max(output)   
    except ValueError:
        return None
    
# good
def flush(hand):    
    container = Counter(list(map(lambda x: x[-1], hand)))
    for v in container.values():
        if v >= 5:
            return True
    return False

# good
def two_pair(ranks):
    """Если есть две пары, то возврщает два 
    соответствующих ранга,
    иначе возвращает None"""
    # counter = 0
    container = Counter(ranks)
    output = []
    for k, v in container.items(): 
        if v == 2:
            output.append(k)
    if len(output) >= 2:
        output = sorted(output, reverse=True)
        return output[:2]

# 
def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
 
    if straight_flush(hand):
        return (8, max(card_ranks(find_str_flush(hand))))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, card_ranks(find_flush(hand))) 
    elif straight(ranks):
        return (4, max(card_ranks(find_straight(hand)))) 
    elif kind(3, ranks):
        return (3, kind(3, ranks), card_ranks(find_kind_1(hand, ranks[1])))
    
    elif two_pair(ranks):
        return (2, two_pair(ranks), card_ranks(find_two_pair( hand, two_pair(ranks), ranks )))
    
    elif kind(2, ranks):
        return (1, kind(2, ranks), card_ranks(find_kind_1(hand, ranks[1])))
    else:
        return (0, card_ranks(find_zero(hand)))

# my functions------------------------------------------------
# good    
def rang_2_num(s):
    card_ranks_dict = {'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
    try:
        if type(int(s)) is int:
            return int(s)
    except ValueError:
        return card_ranks_dict[s]

#good
def num_2_rang(num):
    card_ranks_dict = {10: 'T', 11:'J', 12:'Q', 13:'K', 14:'A'}
    if num in card_ranks_dict:
        return card_ranks_dict[num]
    else:
        return str(num)

# good
def list_to_tuples(some_list):
    new = []
    for item in some_list:
        new.append((rang_2_num(item[0]), item[1]))
    return sorted(new)

# good
def tuple_nums_to_list_ranks(list_tuples):
    sorted(list_tuples)
    temp = []
    for item in list_tuples:
        temp.append(tuple_to_string((num_2_rang(item[0]), item[1])) )
    return temp


# good
def straight_flush(hand):
    temp = list_to_tuples(hand)
    pointer = temp[0]
    set_suits  = set()
    set_suits.add(pointer[1])
    bingo = {'S':0, 'H':0, 'D':0, 'C':0} 
    for item in temp[1:]:
        if (item[0] - 1 == pointer[0]) and item[1] in set_suits:
            bingo[item[1]] += 1
        elif (item[0] == pointer[0]) and item[1] in set_suits:
            bingo[item[1]] += 1
        pointer = item
    for v in bingo.values(): 
        if v >= 4:
            return True
    return False

def tuple_to_string(some_tuple):
    return str(some_tuple[0])+str(some_tuple[1])


def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    #ToDo
    rank = hand_rank(hand)
    if rank[0] == 8:
        return find_str_flush(hand) #done
    elif rank[0] == 7:
        return find_kind(hand, rank[1], rank[2]) #done
    elif rank[0] == 6:
        return find_kind(hand, rank[1], rank[2]) #done
    elif rank[0] == 5:
        return find_flush(hand) #done
    elif rank[0] == 4:
        return find_straight(hand) #done
    elif rank[0] == 3:
        return find_kind_1(hand, rank[1]) #done
    elif rank[0] == 2:
        return find_two_pair(hand, rank[1], rank[2]) #done
    elif rank[0] == 1:
        return find_kind_1(hand, rank[1]) #done
    elif rank[0] == 0:
        return find_zero(hand)# done


#ok
def find_str_flush(hand):
    selected = []
    temp = list_to_tuples(hand)
    pointer = temp[0]
    set_suits  = set()
    set_suits.add(pointer[1])
    bingo = {'S':0, 'H':0, 'D':0, 'C':0} 
    for item in temp[1:]:
        if (item[0] - 1 == pointer[0]) and item[1] in set_suits:
            bingo[item[1]] += 1
            if len(selected) == 0: selected.append(pointer)
            selected.append(item)
        elif item[0] == pointer[0] and item[1] in set_suits:
            bingo[item[1]] += 1
            selected.append(item)
        pointer = item
    for v in bingo.values(): 
        if v >= 4:
            foo = sorted(selected, reverse=True)
            final = tuple_nums_to_list_ranks(sorted(foo[:5]))
            return final
    return None

#ok
def find_kind(hand, a, b):
    temp  = list_to_tuples(hand)
    output = []
    for item in temp:
        if item[0] == a or item[0] == b:
            output.append(item)
    return tuple_nums_to_list_ranks(sorted(output))

#ok
def find_kind_1(hand, a):
    temp  = list_to_tuples(hand)
    sorted(temp, reverse=True)
    output = []
    for item in temp:
        if item[0] == a:
            output.append(item)
        elif len(output) < 5:
            output.append(item)
    return tuple_nums_to_list_ranks(sorted(output))

#ok
def find_flush_suit(hand):    
    container = Counter(list(map(lambda x: x[-1], hand)))
    for k, v in container.items():
        if v >= 5:
            return k
    return False

#ok
def find_flush(hand):
    temp  = list_to_tuples(hand)
    output = []
    key = find_flush_suit(hand)
    for item in sorted(temp, reverse=True):
        if item[1] == key and len(output) < 5:
            output.append(item)    
    return tuple_nums_to_list_ranks(sorted(output))

#ok
def find_straight(hand):
    temp  = list_to_tuples(hand)
    output = []
    pointer = temp[0]
    counter = 0
    for item in temp[1:]:
        if item[0] - 1 == pointer[0]:
            if len(output) == 0: output.append(pointer) 
            output.append(item)
            counter += 1
        elif item[0] == pointer[1]:
            pass
        pointer = item
    if counter >= 4:
        return tuple_nums_to_list_ranks(sorted(output))

# ok
def find_max_excl(small, long):
    output = []
    for item in long:
        if item not in small:
            output.append(item)
    return max(output)

#ok
def find_two_pair(hand, ranks, long_list):
    temp  = list_to_tuples(hand)
    output = []

    for item in sorted(temp, reverse=True):
        if (item[0] in ranks) or (item[0] == find_max_excl(ranks, long_list)):
            output.append(item)
            if len(output) == 5: break
    return tuple_nums_to_list_ranks(sorted(output))


#ok
def find_zero(hand):
    temp  = list_to_tuples(hand)
    output = sorted(temp, reverse=True)
    return tuple_nums_to_list_ranks(sorted(output[:5]))


# ok
def list_jokers(hand):
    list_jokers = []
    for item in hand:
        if item[0] == '?': list_jokers.append(item[1])
    return list_jokers

#ok
def create_products(hand, suit):
    db = {'B': 'SC', 'R':'DH'}
    if list_jokers(hand) is not None:
        for joker_suit in list_jokers(hand): 
            if joker_suit == suit:
                return list(it.product(range(2,15), db[suit]))


# ok
def best_wild_hand(hand):
    """best_hand но с джокерами"""
    if len(list_jokers(hand)) == 1:
        products = create_products(hand, list_jokers(hand)[0]) #ToDo
        counter = {}
        for item in sorted(hand, reverse=True):
            if item.startswith('?'):
                hand.remove(item)
        hand_tuples = list_to_tuples(hand)

        for elem in products:
            if elem not in hand_tuples:
                new_elem = str(num_2_rang(elem[0])) + elem[1]
                new_hand = hand
                new_hand.append(new_elem)    
                counter[new_elem] = hand_rank(new_hand)
                new_hand.remove(new_elem)        
        best_item = sorted(counter.items(), key=lambda x: x[1] )[-1][0]
        best_elem = str(best_item[0] + best_item[1])
        final_hand = hand
        final_hand.append(best_elem)
        return best_hand(final_hand)

    elif len(list_jokers(hand)) == 2:
        black = create_products(hand, "B")
        red = create_products(hand, "R")
        big_counter = {}
        hand2 = hand

        for item in sorted(hand, reverse=True):
            if item.startswith('?'):
                hand2.remove(item)
        hand_tuples = list_to_tuples(hand2)

        for black_card in black:
            if black_card not in hand_tuples:
                new_black_element = str(num_2_rang(black_card[0])) + black_card[1]
                new_outer_hand = hand2
                new_outer_hand.append(new_black_element)
                for red_card in red:
                    if red_card not in hand_tuples:
                        new_red_element = str(num_2_rang(red_card[0])) + red_card[1]
                        new_inner_hand = new_outer_hand
                        new_inner_hand.append(new_red_element)                        
                        big_counter[(new_black_element, new_red_element)] = hand_rank(new_inner_hand)
                        new_inner_hand.remove(new_red_element)
                new_outer_hand.remove(new_black_element)

        # print(big_counter)
        list_values = list(big_counter.values())
        best_item = sorted(big_counter.items(), key=lambda x: x[1] )[-1][0]
        best_elem1 = str(best_item[0][0] + best_item[0][1])
        best_elem2 = str(best_item[1][0] + best_item[1][1])
        final_hand = hand2
        final_hand.append(best_elem1)
        final_hand.append(best_elem2)
        return best_hand(final_hand)

    elif len(list_jokers(hand)) == 0:
        return best_hand(hand)
#-------------------------------------------------------

def test_best_hand():
    print("test_best_hand...")
    assert (sorted(best_hand( "6C 7C 8C 9C TC 5C JS".split()  ))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


def test_best_wild_hand():
    print("test_best_wild_hand...")
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


if __name__ == '__main__':

    test_best_hand()
    test_best_wild_hand()
