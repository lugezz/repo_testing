def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1


nums_squared_lc = [num**2 for num in range(5)]
nums_squared_gc = (num**2 for num in range(5))

print(nums_squared_lc)
print(type(nums_squared_lc))
print("-" * 30)

print(nums_squared_gc)
print(nums_squared_gc.__next__())
print(type(nums_squared_gc))
print("-" * 100)
