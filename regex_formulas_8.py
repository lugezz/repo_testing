import re

# TODO: Need some hard work

formula_easy = '(formula(1,2,3) + formulax(1,2,3) - formulaz(1,suma(1,2),3)) * formula(1,2,3)'
formula_complex = 'Monto() + Suma(1,2,3) + Si(3>Suma(1,2),2,3) - Suma(1,2)'
formula_real = 'Si(EnLista(EmpleadoEmpresa(), 34, 88, 89),TotalHaberes() * 0.01, 0)'
formula_real_complex = """Max(SMVM()/200*iif(EmpJorParc()>0,EmpJorParc()/100,1),Monto(SDOBAS)*
                (1+(iif(EmpEsqLiq()=29,Monto(AANTUT),Monto(AANTIG))*Monto(PORANT)+
                iif(EmpEsqLiq()=33,10,0))/100)*iif(EmpEsqLiq()=24,1.2,1))"""


def has_internal_formula(formula_str: str) -> bool:
    """Check if the formula has another formula inside the arguments
    """
    pattern = r'\w+\('
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


def get_formula_dict(formula_str: str, level: int = 0) -> dict:
    """ Function to get the formulas inside a string and return a dictionary
        this function read character by character and when it finds a letter + '('
        if a new letter + '(' is found, the level will be increased and the
        function will read until it finds the closing parenthesis ')', if the
        level is 0, the function will save the formula in a dictionary and
        replace the formula with the key of the dictionary
        The expected result is a dictionary with the formulas and the string
        like this:
        {
            'level_00': {
                '001': 'formula(1,2,3),
                '002': formula2(1,2,3),
                '003': formula3(1,2,3)',
                },
            'level_01': {
                '001': 'formula(1,2,3)',
                },
        }
    """

    formula_dict = {}
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
                child_dict = get_formula_dict(this_formula_args, level + 1)
                formula_dict.update(child_dict)
            if f'level_{level:02d}' not in formula_dict:
                formula_dict[f'level_{level:02d}'] = {}
            formula_dict[f'level_{level:02d}'][f'{len(formula_dict[f"level_{level:02d}"])+1:03d}'] = this_formula

        # restart the idx if this is a separator
        if formula_str[i-1] in separators:
            idx = i + 1
        i += 1

    return formula_dict


def clean_formulas_dict(formulas_dict: dict) -> dict:
    """ Clean the formulas that are inside another formula
        Starting from the last level, the function will replace the formulas
    """
    levels = len(formulas_dict) - 1
    cleaned_dict = {}
    for i in range(levels, 0, -1):
        for key, value in formulas_dict[f'level_{i:02d}'].items():
            for key2, value2 in formulas_dict[f'level_{i-1:02d}'].items():
                if has_internal_formula(value2):
                    if value in value2:
                        formulas_dict[f'level_{i-1:02d}'][key2] = formulas_dict[f'level_{i-1:02d}'][key2].replace(
                           value, f"|Formula_{key}|")
                else:
                    cd_key = len(cleaned_dict) + 1
                    cleaned_dict[cd_key] = value2

            cd_key = len(cleaned_dict) + 1
            cleaned_dict[cd_key] = value

    return cleaned_dict


def clean_formula_str(input_string: str) -> str:
    """Remove everything different [a-zA-Z0-9] or any of these values ["(", ")", ",", "+", "/", ".", "* "]
    """
    # Define the regular expression pattern
    pattern = r"[^a-zA-Z0-9(),+/*.=<>\-]"

    # Use the 're.sub' function to replace all occurrences of unwanted characters with an empty string
    cleaned_string = re.sub(pattern, "", input_string)

    return cleaned_string


test_formula = formula_real_complex
cleaned_test_formula = clean_formula_str(test_formula)
test_formula_dict = get_formula_dict(cleaned_test_formula)
print("Formula Dict", test_formula_dict)
test_formula_cleaned_dict = clean_formulas_dict(test_formula_dict)
print("Cleaned dict", test_formula_cleaned_dict)
