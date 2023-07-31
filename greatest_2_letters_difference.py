from collections import defaultdict


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


def find_any_letter_group_distance_2(text: str) -> int:
    """
    Find the greatest distance between any two letters in a text.
    It takes 2 letters groups and compares them to find the greatest distance.
    taking into account the position of the letters in the text.
    It returns -1 if no equal groups found.
    """
    greatest_distance = -1
    dict_letters = defaultdict(lambda: -1)

    for idx, letter in enumerate(text):
        next_letter = text[idx:idx+2]
        greatest_distance = max(greatest_distance, idx - dict_letters[next_letter])
        dict_letters[next_letter] = max(dict_letters[next_letter], idx)

    return greatest_distance - 2


# Test the function
result_1b = find_any_letter_group_distance_2(text_1)
print(result_1b)  # Output: 17

text_2 = "aaa"
result_2b = find_any_letter_group_distance_2(text_2)
print(result_2b)  # Output: 1
