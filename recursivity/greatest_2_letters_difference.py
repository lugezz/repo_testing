
def find_any_letter_group_distance(text: str) -> int:
    """
    Find the greatest distance between any two letters in a text.
    It takes 2 letters groups and compares them to find the greatest distance.
    taking into account the position of the letters in the text.
    It returns -1 if no equals groups found
    """
    # Initialize the variables
    greatest_distance = -1
    dict_letters = {}
    # Iterate over the text
    for idx, letter in enumerate(text):
        # Get the next letter
        next_letter = text[idx:idx+2]
        # Check if it's in dictionary
        if next_letter in dict_letters:
            greatest_distance = max(greatest_distance, idx - dict_letters[next_letter])
        else:
            dict_letters[next_letter] = idx

    # Return the greatest distance
    return greatest_distance


# Test the function
text_1 = "pruebadeunapruebapr"
result_1 = find_any_letter_group_distance(text_1)
print(result_1)  # Output: 17

text_2 = "aaa"
result_2 = find_any_letter_group_distance(text_2)
print(result_2)  # Output: 1


def find_greatest_distance(text, group_size):
    positions = {}
    max_distance = -1

    for i in range(len(text) - group_size + 1):
        group = text[i:i+group_size]
        if group in positions:
            distance = i - positions[group]
            max_distance = max(max_distance, distance)
        else:
            positions[group] = i

    return max_distance


text1 = "pruebadeunapruebapr"
group_size1 = 2
result1 = find_greatest_distance(text1, group_size1)
print(f"Greatest distance in '{text1}' for groups of size {group_size1} is: {result1}")

text2 = "aaa"
group_size2 = 2
result2 = find_greatest_distance(text2, group_size2)
print(f"Greatest distance in '{text2}' for groups of size {group_size2} is: {result2}")
