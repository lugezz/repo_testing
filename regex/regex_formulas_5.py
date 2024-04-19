import re

formula_real = 'Si(EnLista(EmpleadoEmpresa(), 34, 88, 89),TotalHaberes() * 0.01, 0)'


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


def formula_update(formula_str: str, formula_dict: dict = {}) -> str:
    formula_pattern = r'\w+\('
    # Find the first match of the pattern in the text
    match = re.search(formula_pattern, formula_str)
    if not match:
        return formula_str, formula_dict

    start = match.start()
    end = find_closing_parenthesis_position(formula_str, start)
    this_formula = formula_str[start:end + 1]
    first_parenthesis_inside = this_formula.find('(') + 1
    inside_formula = this_formula[first_parenthesis_inside:-1]
    # Get the formula name
    if re.search(formula_pattern, inside_formula):
        print("Formula found", this_formula)
        return formula_update(formula_str, formula_dict)
    else:
        idx_str = f'{len(formula_dict) + 1:03}'
        formula_dict[idx_str] = this_formula
        new_formula_str = formula_str.replace(this_formula, f'|Formula_{idx_str}|')
        return formula_update(new_formula_str, formula_dict)


def get_list_formulas(formula_str: str) -> list:
    resp = []
    pattern = r'\w+\('
    # Find all matches of the pattern in the text
    matches = re.finditer(pattern, formula_str)
    if not matches:
        return formula_str

    for match in matches:
        start = match.start()
        end = find_closing_parenthesis_position(formula_str, start)
        this_formula = formula_str[start:end + 1]
        print(this_formula)
        resp.append(this_formula)

    # Remove duplicates from the list
    resp = list(dict.fromkeys(resp))

    return resp


def has_internal_formula(formula_str: str) -> bool:
    """Check if the formula has another formula inside the arguments
    """
    pattern = r'\w+\('
    first_parenthesis_inside = formula_str.find('(') + 1
    inside_formula = formula_str[first_parenthesis_inside:-1]
    resp = re.search(pattern, inside_formula)

    return resp is not None


def create_formulas_dict_ex(formulas_list: list) -> dict:
    """Create a dictionary with the formulas in the list
       Using this schema
       {
           'no_internal_formula': {
               '001': 'formula(1,2,3)',
               '002': 'formula2(1,2,3)',
           },
           internal_formula: {
               '001': 'formula(1,2,suma(1,2))',
           }
       }
    """
    resp = {
        'no_internal_formula': {},
        'internal_formula': {}
    }
    for formula in formulas_list:
        if has_internal_formula(formula):
            resp['internal_formula'][f'{len(resp["internal_formula"]) + 1:03}'] = formula
        else:
            resp['no_internal_formula'][f'{len(resp["no_internal_formula"]) + 1:03}'] = formula

    return resp


def create_formulas_dict(formulas_list: list) -> dict:
    """Create a dictionary with the formulas in the list
       Using this schema
       {
           '001': 'formula(1,2,3)',
           '002': 'formula2(1,2,3)',
           '003': 'formula3(1,2,3)',
       }
    """
    resp = {}

    for formula in formulas_list:
        resp[f'{len(resp) + 1:03}'] = formula

    return resp


def clean_formulas_dict(formulas_dict: dict) -> dict:
    """ Clean recursevely the formulas that are inside another formula
    """
    was_updated = False
    formulas_resp = formulas_dict.copy()

    for key, value in formulas_dict.items():
        if has_internal_formula(value):
            for key2, value2 in formulas_dict.items():
                if value2 in value:
                    formulas_resp[key] = formulas_dict[key].replace(value2, f"|Formula_{key2}|")
                    was_updated = True

    if not was_updated:
        return formulas_dict

    return clean_formulas_dict(formulas_resp)


def clean_formulas_dict_ex(formulas_dict: dict) -> dict:
    """Remove the formulas that are inside another formula
    """
    if not formulas_dict['internal_formula']:
        return formulas_dict['no_internal_formula']

    resp = {}

    for key, value in formulas_dict['no_internal_formula'].items():
        resp[key] = value
        for key2, value2 in formulas_dict['internal_formula'].items():
            if value in value2:
                resp[f"a{key2}"] = value2.replace(value, f"|Formula_{key}|")

    return resp


def replace_formulas(formula_str: str, formulas_dict: dict) -> str:
    """ Replace formulas with the formulas in the dictionary like this:
        formula_str = formula(1,2,3) + formula2(1,2,3) - formula3(1,2,3)
        formulas_dict = {
            '001': 'formula(1,2,3)',
            '002': 'formula2(1,2,3)',
            '003': 'formula3(1,2,3)'
        }
        It should return:
        formula_str = |Formula_001| + |Formula_002| - |Formula_003|
        It should check recursely if no other formula in the string
    """
    if not formulas_dict:
        return formula_str

    if not has_internal_formula(formula_str):
        return formula_str

    for key, value in formulas_dict.items():
        formula_str = formula_str.replace(value, f"|Formula_{key}|")

    return replace_formulas(formula_str, formulas_dict)


def update_formula_str(formula_str) -> tuple:
    """ Function to get the formulas from a string and follow these steps:
    1. Get the formulas from the string to dict
    2. Replace the formulas in the string like this:
        lala(1,2,3) -> |formula_000|
        baba(3,2,1) -> |formula_001|
        dada(3,2,1) -> |formula_002|
    3. Return the string and the dictionary in a tuple
    """
    # 1. Get the formulas from the string to dict
    # 1a. Get the formulas from the string to list
    formulas_list = get_list_formulas(formula_str)
    # 1b. Create a dictionary with the formulas in the list
    formulas_dict = create_formulas_dict(formulas_list)
    # 1c. Remove the formulas that are inside another formula
    formulas_dict_2 = clean_formulas_dict(formulas_dict)
    # 2. Replace the formulas in the string
    formula_resp = replace_formulas(formula_str, formulas_dict_2)

    # 3. Return the string and the dictionary in a tuple
    return formula_resp, formulas_dict_2


formulas_list = get_list_formulas(formula_real)
formulas_dict = create_formulas_dict(formulas_list)
formulas_dict_2 = clean_formulas_dict(formulas_dict)

print(formulas_dict_2)
