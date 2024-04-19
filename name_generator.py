import random

print([ord(char) - 96 for char in "eaiazal".lower()])
print(chr(26+96))


def get_random_name(len_first_name: int = 10, len_last_name: int = 10):
    first_name_list_rn = [random.randint(1, 26) for i in range(len_first_name)]
    first_name_list = [chr(randn+96) for randn in first_name_list_rn]
    first_name = ''.join(first_name_list)

    last_name_list_rn = [random.randint(1, 26) for i in range(len_last_name)]
    last_name_list = [chr(randn+96) for randn in last_name_list_rn]
    last_name = ''.join(last_name_list)

    return first_name.capitalize() + ' ' + last_name.capitalize()


print(get_random_name(12, 11))
