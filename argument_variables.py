

def test_argument(val_1: int = 0, val_2: int = 0, val_3: int = 0, val_4: int = 0):
    result = (val_1 + val_2 + val_3) * val_4

    return result


simple_test = test_argument(1, 2, 3, 4)
print(simple_test)

combined_test = test_argument(val_1=1, **{'val_4': 10})
print(combined_test)
