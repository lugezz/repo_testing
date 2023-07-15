import random

results = []
for i in range(10):
    a = random.randint(50, 100)
    b = random.randint(1, 50)
    results.append((a,b))

print(results)
