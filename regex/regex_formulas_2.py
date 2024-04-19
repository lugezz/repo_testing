import re


def find_expression_positions(text):
    # Define the pattern for finding expressions
    expression_pattern = r'(?<=[a-z])\('

    # Find all matches of the pattern in the text
    matches = re.finditer(expression_pattern, text, flags=re.IGNORECASE)

    # Get the positions of the matches
    positions = [match.start() for match in matches]

    return positions


# Example usage:
text = "(lala(a,b,c)+baba(x,y,z)+dada(x,lala(a,b))"
positions = find_expression_positions(text)
print(positions)
