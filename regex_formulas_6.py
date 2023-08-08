import re

formula_easy = '(formula(1,2,3) + formula2(1,2,3) - formula3(1,2,3)) * formula(1,2,3)'
formula_complex = 'Monto() + Suma(1,2,3) + Si(3>Suma(1,2),2,3) - Suma(1,2)'
formula_real = 'Si(EnLista(EmpleadoEmpresa(), 34, 88, 89),TotalHaberes() * 0.01, 0)'
formulas_real_compleja = """iif (InList (EmpEsqLiq(), 1), Monto ('CONFIJ') / 192 * Cant (), 0)
        + iif (InList (EmpEsqLiq(), 1), Max (SMVM () / 200 * iif (EmpJorParc() > 0, EmpJorParc() / 100, 1),
        Monto ('SDOBAS') * (1 + (iif (EmpEsqLiq() = 29, Monto ('AANTUT'), Monto ('AANTIG')) * Monto ('PORANT')
        + iif (EmpEsqLiq() = 33,10, 0)) / 100) * iif (EmpEsqLiq() = 24, 1.2, 1)) * iif (EmpEmpresa() = 40,
        Cant (), iif (InList (EmpEsqLiq(), 1, 22), 1,
        iif (EmpEmpresa() = 89, 1.1, 1)) * iif (Cant ('HSFERI') > 0,
        iif (Cant ('HSFERI') < 1, Cant ('HSFERI') * 8 * iif (Between (MONTO ('JORPAR'), 1, 100),
        MONTO('JORPAR') / 100, 1), Cant ('HSFERI')), iif (pTipoLiq()='1', nFeri1q() ,  nFeri2q()) *
        iif (InList (EmpEmpresa(), 3, 80, 88, 92), 1.1, 1) * iif (Between (EmpJorParc(), 1, 100),
        EmpJorParc() / 100, 1) * iif (EmpFormaLiq() = 'Q',  8, 1))), 0) * iif (InList (EmpEmpresa(), 114),
        9 / 8, 1)"""
formula_6 = """iif(InList(EmpEsqLiq(),1),Max(SMVM()/200*iif(EmpJorParc()>0,EmpJorParc()/100,1),
            Monto(SDOBAS)*(1+(iif(EmpEsqLiq()=29,Monto(AANTUT),Monto(AANTIG))*Monto(PORANT)+
            iif(EmpEsqLiq()=33,10,0))/100)*iif(EmpEsqLiq()=24,1.2,1))*iif(EmpEmpresa()=40,Cant(),
            iif(InList(EmpEsqLiq(),1,22),1,iif(EmpEmpresa()=89,1.1,1))*iif(Cant(HSFERI)>0,
            iif(Cant(HSFERI)<1,Cant(HSFERI)*8*iif(Between(MONTO(JORPAR),1,100),MONTO(JORPAR)/100,1),
            Cant(HSFERI)),iif(pTipoLiq()=1,nFeri1q(),nFeri2q())*iif(InList(EmpEmpresa(),3,80,88,92),1.1,1)*
            iif(Between(EmpJorParc(),1,100),EmpJorParc()/100,1)*iif(EmpFormaLiq()=Q,8,1))),0)"""
formula_18 = """iif(EmpEmpresa()=40,Cant(),iif(InList(EmpEsqLiq(),1,22),1,iif(EmpEmpresa()=89,1.1,1))*
                iif(Cant(HSFERI)>0,iif(Cant(HSFERI)<1,Cant(HSFERI)*8*iif(Between(MONTO(JORPAR),1,100),
                MONTO(JORPAR)/100,1),Cant(HSFERI)),iif(pTipoLiq()=1,nFeri1q(),nFeri2q())*iif(InList(EmpEmpresa(),
                3,80,88,92),1.1,1)*iif(Between(EmpJorParc(),1,100),EmpJorParc()/100,1)*iif(EmpFormaLiq()=Q,8,1)))"""
formula_18_x = "iif(Between(EmpJorParc(),1,100),EmpJorParc()/100,1)*iif(EmpFormaLiq()=Q,8,1))"


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


def clean_formula_str(input_string: str) -> str:
    """Remove everything different [a-zA-Z0-9] or any of these values ["(", ")", ",", "+", "/", ".", "* "]
    """
    # Define the regular expression pattern
    pattern = r"[^a-zA-Z0-9(),+/*.=<>\-]"

    # Use the 're.sub' function to replace all occurrences of unwanted characters with an empty string
    cleaned_string = re.sub(pattern, "", input_string)

    return cleaned_string


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
    # 0. Clean formula_str
    formula_str = clean_formula_str(formula_str)
    # 1. Get the formulas from the string to dict
    # 1a. Get the formulas from the string to list
    formulas_list = get_list_formulas(formula_str)
    # 1b. Create a dictionary with the formulas in the list
    formulas_dict = create_formulas_dict(formulas_list)
    # 1c. Remove the formulas that are inside another formula
    print("Formulas dict 1", formulas_dict)
    formulas_dict_2 = clean_formulas_dict(formulas_dict)
    print("Formulas dict", formulas_dict_2)
    # 2. Replace the formulas in the string
    formula_resp = replace_formulas(formula_str, formulas_dict_2)

    # 2a. Lastly check if formula_resp has is in the formulas_dict_2
    for key, value in formulas_dict_2.items():
        if formula_resp == value:
            formula_resp = f"|Formula_{key}|"
            break

    # 3. Return the string and the dictionary in a tuple
    return formula_resp, formulas_dict_2


# test_formula = update_formula_str(formula_easy)
# print("*" * 40 + " Easy formula " + "*" * 40)
# print("Formula string updated", test_formula[0])
# print("Formulas dictionary", test_formula[1])
# print("*" * 100)

# test_formula = update_formula_str(formula_complex)
# print("*" * 40 + " complex formula " + "*" * 40)
# print("Formula string updated", test_formula[0])
# print("Formulas dictionary", test_formula[1])
# print("*" * 100)

# test_formula = update_formula_str(formula_real)
# print("*" * 40 + " real formula " + "*" * 40)
# print("Original formula", formula_real)
# print("Formula string updated", test_formula[0])
# print("Formulas dictionary", test_formula[1])
# print("*" * 100)

formula_pr = """Max(SMVM()/200*iif(EmpJorParc()>0,EmpJorParc()/100,1),Monto(SDOBAS)*
                (1+(iif(EmpEsqLiq()=29,Monto(AANTUT),Monto(AANTIG))*Monto(PORANT)+
                iif(EmpEsqLiq()=33,10,0))/100)*iif(EmpEsqLiq()=24,1.2,1))"""


formula_to_test = formula_pr
test_formula = update_formula_str(formula_to_test)
print("*" * 40 + " real formula " + "*" * 40)
print("Original formula", formula_to_test)
print("Cleaned formula", clean_formula_str(formula_to_test))
print("Formula string updated", test_formula[0])
print("Formulas dictionary", test_formula[1])
print("*" * 100)
