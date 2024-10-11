"""
What if somebody wants to check the parameters in a recursive function?
For example the factorial function.
Okay, please write a recursive version of factorial, which checks the
parameters. Maybe you did it in a perfect way, but maybe not.
Can you improve your version? Get rid of unnecessary tests?
"""


def factorial(n):
    """ Calculates the factorial of n,
        n should be an integer and n <= 0 """
    def inner_factorial(n):
        if n == 0:
            return 1
        else:
            return n * inner_factorial(n-1)
    if isinstance(n, int) and n >= 0:
        return inner_factorial(n)
    else:
        raise TypeError("n should be a positve int or 0")


print(factorial(10))
