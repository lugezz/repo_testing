# [1, 2, 3]
# [(1, 1), (2, 4), (3, 9)]


import unittest


def my_func(param1: list, another_func) -> list:
    resp = []

    for item in param1:
        resp.append((item, another_func(item)))

    return resp


list1 = [1, 2, 3]
list_resp = [(1, 1), (2, 8), (3, 27)]
another_func = lambda x: x ** 3

temp = my_func(list1, another_func)
print(temp, list_resp)


class MyTest(unittest.TestCase):

    def test_calc(self):
        self.assertEqual(temp, list_resp)


if __name__ == '__main__':
    unittest.main()
