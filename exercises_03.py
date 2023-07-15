# importing random module
import random


"""
Exercise 10: Write a program in Python to remove duplicate items from a list.
Hint
Given num = [2,3,4,5,2,6,3,2]

Expected output
Result: [2, 3, 4, 5, 6]
"""

num = [2, 3, 4, 5, 2, 6, 3, 2]
x = []
for i in range(len(num)):
    if num[i] not in x:
        x.append(num[i])
    else:
        pass

# printing result
print(x)


"""
Exercise 11: Write a program in Python to choose a random item from a list.
Hint
Given num = [2,3,4,5,6,8,9]

Expected output
Result: 6
"""

num = [2, 3, 4, 5, 6, 8, 9]
result = random.choice(num)

# printing result
print(result)

"""
Exercise 12: Write a program to append data of the second list to the first list.
Hint
Given list1 = [23, 24, 25, 26] list2 = [27, 28, 29, 30]

Expected output
Result:
[23, 24, 25, 26, 27, 28, 29, 30]
"""

list1 = [23, 24, 25, 26]
list2 = [27, 28, 29, 30]

for i in range(len(list2)):
    list1.append(list2[i])

# printing list 1
print(list1)

"""
Exercise 13: Write a program in Python to filter odd and even number from a list.
Hint
Given [2, 23, 24, 51, 46, 67]

Expected output
Even [2, 24, 46] Odd [23, 51, 67]
"""

num = [2, 23, 24, 51, 46, 67]
even = []
odd = []

for i in range(len(num)):
    if num[i] % 2 == 0:
        even.append(num[i])
    else:
        odd.append(num[i])

print("Even elements are:", even)
print("Odd elements are:", odd)

"""
Exercise 14: Write a program to enter or append n numbers in a list.
Hint
Input: 2
Enter element at index 1: 2
Enter element at index 2: 4

Expected output
Result: [‘2’, ‘4’]
"""

num = []
n = int(input("How many elements you want to enter: "))
count = 1
for i in range(n):
    x = input(f"Enter element at index {count}: ")
    count += 1
    num.append(x)

# printing list after item insertion
print(num)

"""
Exercise 15: Write a program in Python to remove repetitive items from a list.
Hint
Given num = [2,3,4,5,2,6,3,2]

Expected output
Result: [2, 3, 4, 5, 6]
"""

num = [2, 3, 4, 5, 2, 6, 3, 2]
x = []
for i in range(len(num)):
    if num[i] not in x:
        x.append(num[i])
    else:
        pass

# printing result
print(x)
