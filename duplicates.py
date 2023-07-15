a = {(1, 2, 3), (4, 5, 6)}
a.add((7, 8, 9))
a.add((4, 5, 6))
a.add((1, 2, 4))
a.add((1, 2, 3))
a.add((10, 11, 12))

print(a)

b = (1, 2, 3)

if b not in a:
    print('No Está!')
else:
    print('Está!!')
