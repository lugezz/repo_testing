import re

# Add value to set
a = {'Cachula'}
a.add('Jazchula')

print(a)

# ----- list comprenhension

list1 = [(1, 'a'), (2, 'b'), (3, 'c')]
list2 = [x[1] for x in list1]

print(list2)

# Remove duplicates
list3 = [1, 2, 3, 4, 4, 5, 5, 6, 6, 6]
list4 = list(set(list3))

print(list4)

# Loop vacía
lista_vacia = []

for item in lista_vacia:
    print(item)

# Caracteres especiales

string = "Hey! What's up bro?"
new_string = re.sub(r"[^a-zA-Z0-9 ]", "", string)
print(new_string)

# Lista
lista_trucha = []
lista_trucha[10] = 1

print(lista_trucha)
