from pprint import pprint

situaciones_revista_1 = [
    {
        'inicio': 1,
        'fin': 3,
        'situacion': 10,
    },
    {
        'inicio': 5,
        'fin': 7,
        'situacion': 2,
    },
    {
        'inicio': 19,
        'fin': 30,
        'situacion': 3,
    },
]

situaciones_revista_2 = [
    {
        'inicio': 10,
        'fin': 25,
        'situacion': 10,
    },
]

situaciones_revista_3 = [
    {
        'inicio': 10,
        'fin': 30,
        'situacion': 10,
    },
]

situaciones_revista_4 = [
    {'inicio': 10, 'fin': 12, 'situacion': 19},
    {'inicio': 28, 'fin': 29, 'situacion': 12},
]


def fill_gaps(resp, index=0):
    if index == len(resp) - 1:
        return resp

    if resp[index]['fin'] + 1 != resp[index + 1]['inicio']:
        resp.insert(index + 1, {
            'inicio': resp[index]['fin'] + 1,
            'fin': resp[index + 1]['inicio'] - 1,
            'situacion': 1,
        })
        return fill_gaps(resp, index + 1)
    else:
        return fill_gaps(resp, index + 1)


def agrega_situaciones_revista(situaciones_revista: list) -> list:
    # Fill the gaps between the situations
    resp = sorted(situaciones_revista, key=lambda x: x['inicio'])

    # If the first situation doesn't start at 1, add a new situation
    if resp[0]['inicio'] != 1:
        resp.insert(0, {
            'inicio': 1,
            'fin': resp[0]['inicio'] - 1,
            'situacion': 1,
        })

    # Fill the gaps between the situations
    resp = fill_gaps(resp)

    # If the last situation doesn't end at 30, add a new situation
    if resp[-1]['fin'] != 30:
        resp.append({
            'inicio': resp[-1]['fin'] + 1,
            'fin': 30,
            'situacion': 1,
        })

    return sorted(resp, key=lambda x: x['inicio'])


fixed_sr1 = agrega_situaciones_revista(situaciones_revista_1)
fixed_sr2 = agrega_situaciones_revista(situaciones_revista_2)
fixed_sr3 = agrega_situaciones_revista(situaciones_revista_3)
fixed_sr4 = agrega_situaciones_revista(situaciones_revista_4)


print("-" * 100)
print("Situaciones Revista 1")
pprint(fixed_sr1)
print("-" * 100)

print("-" * 100)
print("Situaciones Revista 2")
pprint(fixed_sr2)
print("-" * 100)

print("-" * 100)
print("Situaciones Revista 3")
pprint(fixed_sr3)
print("-" * 100)

print("-" * 100)
print("Situaciones Revista 4")
pprint(fixed_sr4)
print("-" * 100)


def depura_situaciones_revista(situaciones_revista: list) -> list:
    # Merge the continued situations that have the same situation number
    resp = sorted(situaciones_revista, key=lambda x: x['inicio'])

    i = 0
    while i < len(resp) - 1:
        if resp[i]['situacion'] == resp[i + 1]['situacion']:
            resp[i]['fin'] = resp[i + 1]['fin']
            resp.pop(i + 1)
        else:
            i += 1

    return resp


situaciones_revista_50 = [
    {
        'inicio': 1,
        'fin': 3,
        'situacion': 10,
    },
    {
        'inicio': 4,
        'fin': 7,
        'situacion': 10,
    },
    {
        'inicio': 19,
        'fin': 30,
        'situacion': 3,
    },
]


fixed_sr50 = depura_situaciones_revista(situaciones_revista_50)

print("=" * 100)
print("-" * 100)
print("Situaciones Revista 50")
pprint(fixed_sr50)
print("-" * 100)
