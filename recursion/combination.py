"""
You might have heard about permutations and combinations in mathematics.
In this example, let’s see how we can find out combinations using Python recursive functions.

Here is the equation for finding the combination:

nCr = n! / r! (n-r)!
Here, n is the total number of items and r is the number of combinations needed.

For example, consider taking combinations of 2 values from A, B, C, D.


4C2 = 4! / 2! (4-2)! = 24/2(2) = 24/4 = 6

The Python code for implementing combinations is given below:
"""


def fact(n):
    if n == 1:
        return n
    else:
        return n*(fact(n-1))


def combination(n, r):
    return fact(n)/(fact(r)*fact(n-r))


n = int(input("Enter n: "))
r = int(input("Enter r: "))
print(int(combination(n, r)))
