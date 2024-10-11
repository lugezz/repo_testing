# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def separate_even_and_odd_balls(ball_list: list) -> tuple:
    """ Separate the ball_list in 2, even and odds
    """
    even_balls = [x for x in ball_list if x % 2 == 0]
    odd_balls = [x for x in ball_list if x % 2 != 0]

    return (even_balls, odd_balls)


def bucket_move(balls_list: list, empty_buckets_list: list) -> tuple:
    """ Function to make a move, return a empty tuple if not possible
        If it's possible, it returns a tuple with the lists after
        the move
        It checks the balls from the end and the spaces from the
        start
    """
    even_balls, odd_balls = separate_even_and_odd_balls(balls_list)
    # 1) Check if it's already done
    if not even_balls or not odd_balls:
        return ("Done", balls_list, empty_buckets_list)

    # 2) Check if the balls are more than the half of the len, it's not possible
    buckets_len = len(balls_list) + len(empty_buckets_list)
    if len(balls_list) * 2 > buckets_len + 1:
        return ("Not Possible", balls_list, empty_buckets_list)

    # Ready let's go for the move
    if len(odd_balls) > len(even_balls):
        even_numbers = [x for x in range(1, buckets_len + 1) if x % 2 == 0]
        positions_to_find = [x for x in even_numbers if x in empty_buckets_list]
        # Look for the ball move to convert it to even
        for ball in even_balls:
            if positions_to_find:
                move_to = positions_to_find.pop(0)
                balls_list.remove(ball)
                empty_buckets_list.remove(move_to)
                balls_list.append(move_to)
                empty_buckets_list.append(ball)
    else:
        odd_numbers = [x for x in range(1, buckets_len + 1) if x % 2 != 0]
        positions_to_find = [x for x in odd_numbers if x in empty_buckets_list]
        for ball in odd_balls:
            if positions_to_find:
                move_to = positions_to_find.pop(0)
                balls_list.remove(ball)
                empty_buckets_list.remove(move_to)
                balls_list.append(move_to)
                empty_buckets_list.append(ball)

    return ("Move Made", balls_list, empty_buckets_list)


def solution(buckets):
    """ Function to create a sequence for buckets that is a string
        of "B" and "." that place the "B" are just separated by
        one "."

        It returns the minimum of moves to place it correctly.
        If not possible, it returns -1
    """
    moves = 0
    # list of positions
    empty_buckets = []
    balls = []

    # Fill the position for each element in their lists
    for ix, bucket in enumerate(buckets):
        if bucket == '.':
            empty_buckets.append(ix)
        else:
            balls.append(ix)

    # Ok, let's order it one ball by one
    while True:
        status, balls, empty_buckets = bucket_move(balls, empty_buckets)
        if status == "Done":
            return moves
        elif status == "Not Possible":
            return -1
        else:
            moves += 1


# Test cases

case1 = "B.B.BB."

print(solution(case1))
