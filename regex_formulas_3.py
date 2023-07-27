from cgi import test
import re

formula_1 = "lala(1,2,3)+baba(3,2,1)/dada(3,2,1)"
formula_2 = "lala(1,2,3)+baba(3,lala(1,3),1)/dada(3,2,lala(1,2))"


def find_expression_positions(text):
    # Define the pattern for finding expressions
    # En este caso el inicio de una formula es una letra seguida de un parentesis
    # expression_pattern = r'(?<=[a-z])\('
    formula_pattern = r'\w+\('

    # Find all matches of the pattern in the text
    matches = re.finditer(formula_pattern, text, flags=re.IGNORECASE)

    # Get the positions of the matches
    positions = [match.start() for match in matches]

    return positions


def find_closing_parenthesis_position(text: str, start_pos: int) -> int:
    """ Function find where the parenthesis closes, adding (open) and
        substracting (close). The parenthesis closes when it reachs to zero.
        The function returns the position of the closing parenthesis

        example = "(kaka(aalal(lla,2,3)))
        Expected result = 22

    Args:
        text (_type_): Text to search for the closing parenthesis
        start_pos (_type_): Position where the parenthesis starts

    Returns:
        int: Position of the closing parenthesis
    """
    count = 0

    for idx in range(start_pos, len(text)):
        if text[idx] == '(':
            count += 1
        elif text[idx] == ')':
            count -= 1
            if count == 0:
                return idx

    # Returns -1 if the closing parenthesis is not found
    return -1


def get_formulas_to_dict(formula_str: str, start_pos: int = 0, dict_len: int = 0) -> dict:
    """ Function to get the formulas from a string and return them as a
        dictionary like this:
        {'0': 'lala(1,2,3)', '1': 'baba(3,2,1)', '2': 'dada(3,2,1)'}

    Args:
        formula_str (str): String with the formulas

    Returns:
        dict: Dictionary with the formulas
    """
    # Take into account start_pos
    formula_str = formula_str[start_pos:]

    # Get the positions of the expressions
    positions = find_expression_positions(formula_str)

    # Get the formulas
    child_dict = {}
    formulas = {}

    # If no positions are found, return an empty dictionary
    if len(positions) == 0:
        return formulas

    last_character_position = 0
    for idx in range(len(positions)):
        if last_character_position > positions[idx]:
            continue
        # Get the position of the closing parenthesis
        closing_pos = find_closing_parenthesis_position(formula_str, positions[idx])
        last_character_position = closing_pos + 1

        # Get the formula
        formula = formula_str[positions[idx]:closing_pos + 1]

        # Recursively call the function to get the formulas inside the formula
        expressions_in_formula = find_expression_positions(formula)
        if expressions_in_formula != [0]:
            child_dict = get_formulas_to_dict(
                formula,
                start_pos=expressions_in_formula[1],
                dict_len=len(formulas)+1
                )
            # Update the formula with the formulas inside
            # Like this lala(1,2,dada(3,2,1)) -> lala(1,2,|formula_001|)
            for key, value in child_dict.items():
                formula = formula.replace(value, f"|formula_{key}|")

        # Add the formula to the dictionary
        formulas[str(len(formulas)+1+dict_len).zfill(3)] = formula

        # Add the formulas inside the formula to the dictionary
        formulas.update(child_dict)

    return formulas


def get_formulas_str_updated(formulas_str: str) -> tuple:
    """ Function to get the formulas from a string and follow these steps:
        1. Get the formulas from the string to dict
        2. Replace the formulas in the string like this:
            lala(1,2,3) -> |formula_000|
            baba(3,2,1) -> |formula_001|
            dada(3,2,1) -> |formula_002|
        3. Return the string and the dictionary in a tuple        

    """
    # 1. Get the formulas from the string to dict
    formulas = get_formulas_to_dict(formulas_str)

    # 2. Replace the formulas in the string like this:
    # 2a. Sort the dictionary by key from highest to lowest
    formulas = dict(sorted(formulas.items(), key=lambda item: item[0], reverse=True))

    for key, value in formulas.items():
        formulas_str = formulas_str.replace(value, f"|formula_{key}|")

    # 3. Return the string and the dictionary in a tuple
    return formulas_str, formulas


# print("*" * 100)
# print("Original 1", formula_1)
# print("Formula 1", get_formulas_to_dict(formula_1))
# print("*" * 100)
# print("Original 2", formula_2)
# print("Formula 2", get_formulas_to_dict(formula_2))
# print("*" * 100)

print("Original Formula 2", formula_2)
resultado = get_formulas_str_updated(formula_2)
print("Resultado final Formula 2 a", resultado[0])
print("Resultado final Formula 2 b", resultado[1])
print("*" * 100)
print("*" * 100)
print("*" * 100)

# Execute formula -----------------------------------------------------------------------------------
formula_to_execute_1 = "|formula_001|"
formula_to_execute_2 = "(|formula_001| + 1"
formula_to_execute_complex = "(|formula_001| + |formula_002|) / |formula_003|"

formulas_dict = {
            '001': 'Monto()',
            '002': 'suma_basica(1,2,|formula_003|)',
            '003': 'funcion_si(3>2,4,5)',
            '004': 'funcion_si(1,2,3)',
        }


# Formulas Dict ------------------------------------------------------------------------------------
def monto(*args):
    # Monto de un concepto
    # TODO: Por el momento devuelve 100
    return 100


def suma_basica(*args) -> float:
    # Devuelve la suma de todos los argumentos
    return sum(args)


def funcion_si(option_yes, option_no, condition):
    # Básica función si.
    return option_yes if condition else option_no


FUNCIONES_DICT = {
    'Monto': monto,
}


# End of Formula Dict ----------------------------------------------------------------------------
def get_formulas_and_replace(formula_str: str, formulas_dict: dict) -> str:
    formulas = re.findall(r'\|([^|]+)\|', formula_str)
    for formula in formulas:
        formula_str = formula_str.replace(f"|{formula}|", str(execute_formula(formula, formulas_dict)))

    return formula_str


def execute_formula(formula_name: str, formulas_dict: dict) -> float:
    """Execute a formula and return the result
       For that I need to first replace the formulas with the values
       if there are other formulas within the formula

    Args:
        formula_str (str): Formula to execute
        formulas_dict (dict): Dictionary with the formulas to find in the formula_str

    Returns:
        float: Result of the formula
    """
    resp = 0.0

    # 1. Find if there are formulas inside formulas_str
    #    These have a format |formula_name|
    #    If there are formulas inside, replace them with their value recursively
    #    If there are no formulas inside, return the value of the formula
    formula_key = formula_name.replace('formula_', '')
    this_formula = formulas_dict[formula_key]
    formulas_internas = re.findall(r'\|([^|]+)\|', this_formula)
    if formulas_internas:
        print("formulas_internas", formulas_internas)

    return resp


test_case = get_formulas_and_replace(formula_to_execute_1, formulas_dict)
print(test_case)

test_case_complex = get_formulas_and_replace(formula_to_execute_complex, formulas_dict)
print(test_case_complex)
