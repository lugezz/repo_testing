
def largest_range(list_to_process):
    numbers = {x: 0 for x in list_to_process}
    left = right = 0

    for number in list_to_process:
        # just if it is not previously marked as processed
        if numbers[number] == 0:
            left_count = number - 1
            right_count = number + 1

            while left_count in list_to_process:
                numbers[left_count] = 1
                left_count -= 1
            left_count += 1

            while right_count in list_to_process:
                numbers[right_count] = 1
                right_count += 1
            right_count -= 1

            if (right - left) < (right_count - left_count):
                right = right_count
                left = left_count

    return [left, right]


test_list1 = [11, 7, 2, 1, 4, 3, 0]
test_list2 = [11, 7, 13, 1, 4, 12, 0]
test_list3 = [8, 7, 2, 1, 4, 9, 0]
test_list4 = [11, 7, 8, 10, 9, 3, 0]

print(f'The largest range for {test_list1} is {largest_range(test_list1)}')
print(f'The largest range for {test_list2} is {largest_range(test_list2)}')
print(f'The largest range for {test_list3} is {largest_range(test_list3)}')
print(f'The largest range for {test_list4} is {largest_range(test_list4)}')
