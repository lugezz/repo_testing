import re

# TODO: Need some hard work

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


def get_key_from_dict(formula_dict: dict, value: str) -> str:
    """ Get the key from the dictionary for the given value
    """
    for key, value2 in formula_dict.items():
        if value2 == value:
            return key

    return None


def get_formula_dict_2(formula_str: str, formula_dict: dict = {}) -> dict:
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

    # formula_dict = {}
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
            this_key = get_key_from_dict(formula_dict, this_formula)
            if this_key is None:
                this_key = f'{len(formula_dict)+1:03d}'
                formula_dict[this_key] = this_formula
            if has_internal_formula(this_formula):
                this_formula_args = this_formula[this_formula.find('(')+1:-1]   
                formula_dict = get_formula_dict_2(this_formula_args, formula_dict)

        # restart the idx if this is a separator
        if formula_str[i-1] in separators:
            idx = i + 1
        i += 1

    return formula_dict


def get_formula_dict_3(formula_str: str, formula_dict: dict = {}) -> dict:
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

    # formula_dict = {}
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
                formula_dict = get_formula_dict_3(this_formula_args, formula_dict)
                # Now I need to replace the formula with the key 'Formula_00x'
                for key, value in formula_dict.items():
                    this_formula = this_formula.replace(value, f"|Formula_{key}|")

                if has_internal_formula(this_formula):
                    return get_formula_dict_3(this_formula, formula_dict)
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


def get_formula_dict(formula_str: str, level: int = 0, parent: str = '') -> dict:
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
            if f'level_{level:02d}' not in formula_dict:
                formula_dict[f'level_{level:02d}'] = {}

            end = find_closing_parenthesis_position(formula_str, i)
            i = end
            this_formula = formula_str[idx-1:end+1]
            this_key = f'{parent}{len(formula_dict[f"level_{level:02d}"])+1:03d}'
            if has_internal_formula(this_formula):
                this_formula_args = this_formula[this_formula.find('(')+1:-1]
                child_dict = get_formula_dict(this_formula_args, level + 1, this_key)
                # Let's update formula_dict with the child_dict for any level
                for key, value in child_dict.items():
                    if key not in formula_dict:
                        formula_dict[key] = value
                    else:
                        formula_dict[key].update(value)
            formula_dict[f'level_{level:02d}'][this_key] = this_formula

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
            cd_key_str = str(i).zfill(3) + str(len(cleaned_dict) + 1).zfill(3)
            cleaned_dict[cd_key_str] = value
            for key2, value2 in formulas_dict[f'level_{i-1:02d}'].items():
                cd_key_str = str(i-1).zfill(3) + str(len(cleaned_dict) + 1).zfill(3)
                cleaned_dict[cd_key_str] = value2

                if has_internal_formula(value2):
                    if value in value2:
                        formulas_dict[f'level_{i-1:02d}'][key2] = formulas_dict[f'level_{i-1:02d}'][key2].replace(
                           value, f"|Formula_{cd_key_str}|")

    return cleaned_dict


def clean_formulas_dict_2(formulas_dict: dict) -> dict:
    """ Clean the formulas that are inside another formula the function will replace the formulas
    """
    cleaned_dict = {
        'Original_dict': formulas_dict,
        'final_dict': {}
    }
    for key, value in formulas_dict.items():
        if has_internal_formula(value):
            while True:
                this_formula = value
                this_formula_args = this_formula[this_formula.find('(')+1:-1]
                new_dict = get_formula_dict_2(this_formula_args)
                # Add new formulas to the final_dict if it's not in it
                for key2, value2 in new_dict.items():
                    if get_key_from_dict(cleaned_dict['final_dict'], value2) is None:
                        cleaned_dict['final_dict'][f"{key}_{key2}"] = value

                if value2 in this_formula:
                    this_formula = this_formula.replace(value2, f"|Formula_{key}_{key2}|")

                if not has_internal_formula(this_formula):
                    cleaned_dict['final_dict'][key] = this_formula
                    break
            for key2, value2 in cleaned_dict['final_dict'].items():
                cleaned_dict['final_dict'][f"{key}_{key2}"] = value
                if value2 in this_formula:
                    this_formula = this_formula.replace(value2, f"|Formula_{key}_{key2}|")

        else:
            cleaned_dict['final_dict'][key] = value

    return cleaned_dict


def clean_formula_str(input_string: str) -> str:
    """Remove everything different [a-zA-Z0-9] or any of these values ["(", ")", ",", "+", "/", ".", "* "]
    """
    # Define the regular expression pattern
    pattern = r"[^a-zA-Z0-9(),+/*.=<>\-]"

    # Use the 're.sub' function to replace all occurrences of unwanted characters with an empty string
    cleaned_string = re.sub(pattern, "", input_string)

    return cleaned_string


def remove_duplicated_values_in_dict(formulas_dict: dict) -> dict:
    """Remove duplicated values in a dictionary
       But after that I should change each value in the dictionary |Formulaxxx|
       to the correct value
    """
    resp = {}
    # formulas show a reverse dict where the key is the value and the value is the key
    formulas = {}
    # formula_replace_by show the key to replace by the value
    formula_replace_by = {}
    # 1. Loop through the dictionary descending ways
    for key in sorted(formulas_dict.keys(), reverse=True):
        value = formulas_dict[key]
        if value in formulas:
            formula_replace_by[key] = formulas[value]
        else:
            formulas[value] = key
            resp[key] = value

    # print("Formula Replace By", formula_replace_by)
    # Replace the values in the dictionary
    # For example I have:
    # formula_replace_by = {'001': '002', '102': '003'}
    # I have replace |Formula_001| by |Formula_002| and |Formula_102| by |Formula_003|

    for key, value in formula_replace_by.items():
        for key2, value2 in resp.items():
            resp[key2] = value2.replace(f'|Formula_{key}|', f'|Formula_{value}|')

    return resp


def replace_formula_string(formula_str: str, formula_dict: dict) -> str:
    """Replace the formulas inside the string with the key of the dictionary
    """
    for key in sorted(formula_dict.keys(), reverse=True):
        value = formula_dict[key]
        formula_str = formula_str.replace(value, f"|Formula_{key}|")

    return formula_str


test_formula = formula_real_complex
cleaned_test_formula = clean_formula_str(test_formula)
test_formula_dict = get_formula_dict_3(cleaned_test_formula)
print("Formula Dict", test_formula_dict)
print("*" * 100)
# test_formula_cleaned_dict = clean_formulas_dict_2(test_formula_dict)
# print("Cleaned dict", test_formula_cleaned_dict['final_dict'])
# print("*" * 100)
# no_duplicated_test_formula_cleaned_dict = remove_duplicated_values_in_dict(test_formula_cleaned_dict)
# print("No duplicated dict", no_duplicated_test_formula_cleaned_dict)
# Finally translate the formula from the dictionary replacing the values with |Formula_key|
step2_formula = replace_formula_string(cleaned_test_formula, test_formula_dict)
print("Step2 Formula", step2_formula)
print("*" * 100)
step2_dict = get_formula_dict_3(step2_formula, test_formula_dict)
final_formula = replace_formula_string(step2_formula, step2_dict)
print("Final Formula", final_formula)
print("*" * 100)
print("Final dict", step2_dict)
print("*" * 100)
final2_dict = get_formula_dict_3(final_formula, step2_dict)
print("Step3 dict", final2_dict)
final2_formula = replace_formula_string(final_formula, final2_dict)

print("Has internal formula - Final 1", has_internal_formula(final_formula))
print("Has internal formula - Final 2", has_internal_formula(final2_formula))
