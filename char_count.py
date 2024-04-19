def count_char(string_to_count: str) -> dict:
    resp = {}
    my_str = string_to_count.lower()

    for letter in my_str:
        resp[letter] = resp.get(letter, 0) + 1

    return resp


print(count_char('Cachula es cachula la loca amorosa'))
