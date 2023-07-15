import time

# lista = [20,14,10,7,4,3,2,0]
# search_nr = 7
# expected_output = 3

# def locate_card(cards, query):
#     pass

# result = locate_card(lista, search_nr)
# print (f'Result: {result}, It\'s expected: {result==expected_output}')

# def locate_card(cards, query):
#     position = 0
#     if len(cards) == 0:
#         return -1

#     while True:
#         if cards[position]==query:
#             return position
#         position += 1
    
#         if position == len(cards):
#             return -1

def locate_card_linear(cards, query):
    position = 0

    while position < len(cards):
        if cards[position]==query:
            return position
        position += 1

    return -1    


def locate_card_bin(cards, query):
    desde, hasta = 0, len(cards) - 1

    while desde <= hasta:
        middle = (desde + hasta) // 2
        mid_num = cards[middle]

        if mid_num == query:
            if middle == 0 or (mid_num != cards[middle - 1]):
                return middle
            else:
                i = middle - 1
                while mid_num == cards[i]:
                    i -= 1
                return i + 1
        elif mid_num > query:
            desde = middle + 1
        elif mid_num < query:
            hasta = middle -1

    return -1

def locate_card_mybin(cards, query, desde=0, hasta=-1):
    if not cards:
        return -1

    hasta = hasta if hasta >= 0 else len(cards) - 1
    if desde == hasta:
        if cards[desde] != query:
            return -1
        else:
            return desde

    middle = (hasta - desde)// 2 + desde
    if cards[middle] == query:
        return middle

    
    if query > cards[middle]:
        new_desde = desde
        new_hasta = middle - 1
    else:
        new_desde = middle + 1
        new_hasta = hasta
        
    return locate_card_mybin(cards, query, new_desde, new_hasta)

test = {
    'input': {
        'cards': [20,14,10,7,4,3,2,0],
        'query': 7
    },
    'output': 3
}

tests = [test]
tests.append({
    'input': {
        'cards': [20,14,10,7,4,3,2,0],
        'query': 20
    },
    'output': 0
})

tests.append({
    'input': {
        'cards': [20,14,10,7,4,3,2,0],
        'query': 0
    },
    'output': 7
})

tests.append({
    'input': {
        'cards': [20,14,10,-7,-14,-23,-32,-50],
        'query': -50
    },
    'output': 7
})

tests.append({
    'input': {
        'cards': [6],
        'query': 6
    },
    'output': 0
})

tests.append({
    'input': {
        'cards': [20,14,10,7,4,3,2,0],
        'query': 33
    },
    'output': -1
})

tests.append({
    'input': {
        'cards': [],
        'query': 0
    },
    'output': -1
})

tests.append({
    'input': {
        'cards': [20,14,14,14,4,3,2,0],
        'query': 4
    },
    'output': 4
})

tests.append({
    'input': {
        'cards': [20,20,14,14,14,14,3,3,0],
        'query': 14
    },
    'output': 2 #Should take the first
})

# n_test = 0
# for test in tests:
#     resp = locate_card_linear(**test['input'])
#     esperado = 'SI' if resp == test['output'] else 'No'

#     print (f'Test {n_test}: {resp}. El resultado {esperado} era el esperado')

#     n_test += 1

long_test = {
    'input': {
        'cards': list(range(1000000, 0, -1)),
        'query': 2
    },
    'output': 999998
}

start = time.time()
resp = locate_card_linear(**long_test['input'])
end = time.time()
print('Long Test:', resp, 'Time:', f'{round((end-start)*1000,2)}ms')

print ("-"*200)
print ("-"*200)
start = time.time()
resp = locate_card_bin(**long_test['input'])
end = time.time()
print('Long Test:', resp, 'Time:', f'{round((end-start)*1000,2)}ms')

n_test = 0
for test in tests:
    resp = locate_card_bin(**test['input'])
    esperado = 'SI' if resp == test['output'] else 'No'

    print (f'Test {n_test}: {resp}. El resultado {esperado} era el esperado')

    n_test += 1