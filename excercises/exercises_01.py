"""
Print integers from 1 to 15
for multiples of 3 print "Fizz"
for multiples of 5 print "Buzz"
if it's multiple or both 3 and 5 "FizzBuzz" should be printed
"""

for i in range(1, 16):
    resp = i
    if i % 3 == 0:
        resp = 'Fizz'

    if i % 5 == 0:
        v_add = '' if resp == i else resp
        resp = v_add + 'Buzz'

    print(resp)
