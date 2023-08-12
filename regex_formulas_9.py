import re

formula_easy = '(formula(1,2,3) + formulax(1,2,3) - formulaz(1,suma(1,2),3)) * formula(1,2,3)'
formula_complex = 'Monto() + Suma(1,2,3) + Si(3>Suma(1,2),2,3) - Suma(1,2)'
formula_real = 'Si(EnLista(EmpleadoEmpresa(), 34, 88, 89),TotalHaberes() * 0.01, 0)'
formula_real_complex = """Max(SMVM()/200*iif(EmpJorParc()>0,EmpJorParc()/100,1),Monto(SDOBAS)*
                (1+(iif(EmpEsqLiq()=29,Monto(AANTUT),Monto(AANTIG))*Monto(PORANT)+
                iif(EmpEsqLiq()=33,10,0))/100)*iif(EmpEsqLiq()=24,1.2,1))"""


def is_formula(formula: str) -> bool:
    pattern = r'\w+\('
    match = re.match(pattern, formula)
    if not match or match.start() != 0:
        return False
    return True


def it_includes_a_formula(formula: str) -> bool:
    pattern = r'(?<=.)[a-zA-Z]+\('
    match = re.search(pattern, formula)
    if not match:
        return False
    return True


def has_internal_formula(formula_str: str) -> bool:
    """Check if the formula has another formula inside the arguments
    """
    pattern = r'\w+\('
    pattern = r'[a-zA-Z]+\('
    first_parenthesis_inside = formula_str.find('(') + 1
    inside_formula = formula_str[first_parenthesis_inside:-1]
    resp = re.search(pattern, inside_formula)

    return resp is not None


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


def get_key_from_dict(formula_dict: dict, value: str) -> str:
    """ Get the key from the dictionary for the given value
    """
    for key, value2 in formula_dict.items():
        if value2 == value:
            return key

    return None


def get_formula_dict(formula_str: str, formula_dict: dict = {}) -> dict:
    """ Function to get the formulas inside a string and return a dictionary
        this function read character by character and when it finds a letter + '('
        if a new letter + '(' is found, the level will be increased and the
        function will read until it finds the closing parenthesis ')', if the
        replace the formula with the key of the dictionary
        And recursively call the function to get the formulas inside the formula.
        For this example:
        example_formula = 'formula(1,2,3) + formula2(1,2,3) - formula3(1,suma(1, 4),3)'
        The expected result is a dictionary with the formulas and the string
        like this:
        {
            '001': 'formula(1,2,3)',
            '002': 'formula2(1,2,3)',
            '003': 'formula3(1,|Formula_004|,3)',
            '004': 'suma(1, 4)',
        }
    """
    # First clean the string
    # formula_str = clean_formula_str(formula_str)
    # idx shows where the formula starts
    idx = 1
    separators = ['+', '-', '*', '/', '(', ')', ',', ' ', '<', '>', '=']
    i = 1

    while i < len(formula_str):
        # Find a formula by the letter + '('
        if re.match(r'[a-zA-Z]\(', formula_str[i-1:i+1]):
            end = find_closing_parenthesis_position(formula_str, i)
            i = end
            this_formula = formula_str[idx-1:end+1]
            if has_internal_formula(this_formula):
                this_formula_args = this_formula[this_formula.find('(')+1:-1]
                formula_dict = get_formula_dict(this_formula_args, formula_dict)
                # Now I need to replace the formula with the key '|Formula_00x|'
                for key, value in formula_dict.items():
                    this_formula = this_formula.replace(value, f"|Formula_{key}|")

                if has_internal_formula(this_formula):
                    return get_formula_dict(this_formula, formula_dict)
                else:
                    return formula_dict
            else:
                this_key = get_key_from_dict(formula_dict, this_formula)
                if this_key is None:
                    this_key = f'{len(formula_dict)+1:03d}'
                    formula_dict[this_key] = this_formula

        # restart the idx if this is a separator
        if formula_str[i-1] in separators:
            idx = i + 1
        i += 1

    return formula_dict


def clean_formula_str(input_string: str) -> str:
    """Remove everything different [a-zA-Z0-9] or any of these values
    ["(", ")", ",", "+", "/", ".", "*", "-", "<", ">", "="]
    """
    # Define the regular expression pattern
    pattern = r"[^a-zA-Z0-9(),+/*.=<>\-]"

    # Use the 're.sub' function to replace all occurrences of unwanted characters with an empty string
    cleaned_string = re.sub(pattern, "", input_string)

    return cleaned_string


def replace_formula_string(formula_str: str, formula_dict: dict) -> str:
    """Replace the formulas inside the string with the key of the dictionary
    """
    for key in sorted(formula_dict.keys(), reverse=True):
        value = formula_dict[key]
        formula_str = formula_str.replace(value, f"|Formula_{key}|")

    return formula_str


def update_formula_string(formula_str: str, formula_dict: dict = {}) -> tuple:
    """Replace the formulas inside the string with the key of the dictionary
       It returns a tuple with the formula_str and the formula_dict
    """
    formula_dict_resp = get_formula_dict(formula_str, formula_dict)
    formula_resp = replace_formula_string(formula_str, formula_dict_resp)

    if is_formula(formula_resp) or has_internal_formula(formula_resp) or it_includes_a_formula(formula_resp):
        return update_formula_string(formula_resp, formula_dict_resp)
    return formula_resp, formula_dict_resp


test_formula = clean_formula_str(formula_real_complex)
result_formula, result_dict = update_formula_string(test_formula)
print("Final result: ", result_formula)
print("*"*200)
print("Final dict: ", result_dict)
