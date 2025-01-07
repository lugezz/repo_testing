"""
Create a function to find the max lenght in a subsequence for a list that has only 0s and 1s
A subsequence is a of a sequence that can be derived from another sequence by deleting some or
no elements without changing the order of the remaining elements.

"""


def max_length_subsequence(arr: list) -> int:
    if len(arr) < 2:
        return len(arr)

    max_length = 1
    current_length = 1

    for i in range(1, len(arr)):
        if arr[i] != arr[i-1]:  # Check if current element is different from the previous one
            current_length += 1
            max_length = max(max_length, current_length)
        else:
            current_length = 1  # Reset the current length if the sequence is not alternating

    return max_length


# Lists to test the function
list_1 = [0, 1, 0, 1, 0, 1, 0, 1]
list_2 = [0, 1, 1, 0]
list_3 = [0]
list_4 = [1, 1, 1, 1, 1, 1, 1, 1]
list_5 = [0, 0, 0, 0, 0, 0, 0, 0]
list_6 = [0, 1, 0, 1, 0]
list_7 = [0, 0, 0, 0, 1, 0, 0, 0]

# Testing the function
print(max_length_subsequence(list_1))  # Output: 8
print(max_length_subsequence(list_2))  # Output: 2
print(max_length_subsequence(list_3))  # Output: 1
print(max_length_subsequence(list_4))  # Output: 1
print(max_length_subsequence(list_5))  # Output: 1
print(max_length_subsequence(list_6))  # Output: 5
print(max_length_subsequence(list_7))  # Output: 3
