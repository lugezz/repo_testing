my_list = ['primero', 'cachula', 1221, 1224, 'ultimo']

for i, line in enumerate(my_list):
    if i == 0:
        print("Primero", line)

    if i == len(my_list) - 1:
        print("Último", line)


a = 3
b = 4

print(max(a, b))
