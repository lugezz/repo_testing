
def binary_search(arr, target):
    """ Binary search algorithm to find the target in the given array sorted in ascending order.

    Args:
        arr: A list of integers sorted in ascending order.
        target: An integer to search in the array.

    Returns:
        The index of the target in the array if found, otherwise -1.
    """
    left, right = 0, len(arr)

    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


this_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

print(binary_search(this_list, 5))  # 4
