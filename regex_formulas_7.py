import re


def has_internal_formula(formula_str: str) -> bool:
    """Check if the formula has another formula inside the arguments
    """
    pattern = r'\w+\('
    first_parenthesis_inside = formula_str.find('(') + 1
    inside_formula = formula_str[first_parenthesis_inside:-1]
    resp = re.search(pattern, inside_formula)

    return resp is not None


def clean_formulas_dict(formulas_dict: dict) -> dict:
    """ Clean recursevely the formulas that are inside another formula
    """
    was_updated = False
    formulas_resp = formulas_dict.copy()

    for key, value in formulas_dict.items():
        if has_internal_formula(value):
            print(f"Key: {key}, Value: {value} has internal formula")
            for key2, value2 in formulas_dict.items():
                if value2 in value:
                    print("Dict before: ", formulas_resp)
                    formulas_resp[key] = formulas_dict[key].replace(value2, f"|Formula_{key2}|")
                    print("Dict after: ", formulas_resp)
                    was_updated = True

    if not was_updated:
        return formulas_dict

    return clean_formulas_dict(formulas_resp)


test_dict = {
    '001': """iif(InList(EmpEsqLiq(),1),Max(SMVM()/200*iif(EmpJorParc()>0,EmpJorParc()/100,1),
           Monto(SDOBAS)*(1+(iif(EmpEsqLiq()=29,Monto(AANTUT),Monto(AANTIG))*Monto(PORANT)+
           iif(EmpEsqLiq()=33,10,0))/100)*iif(EmpEsqLiq()=24,1.2,1))*iif(EmpEmpresa()=40,Cant(),
           iif(InList(EmpEsqLiq(),1,22),1,iif(EmpEmpresa()=89,1.1,1))*iif(Cant(HSFERI)>0,
           iif(Cant(HSFERI)<1,Cant(HSFERI)*8*iif(Between(MONTO(JORPAR),1,100),MONTO(JORPAR)/100,1),
           Cant(HSFERI)),iif(pTipoLiq()=1,nFeri1q(),nFeri2q())*iif(InList(EmpEmpresa(),3,80,88,92),1.1,1)*
           iif(Between(EmpJorParc(),1,100),EmpJorParc()/100,1)*iif(EmpFormaLiq()=Q,8,1))),0)""",
    '002': 'InList(EmpEsqLiq(),1)',
    '003': 'EmpEsqLiq()',
    '004': 'Max(SMVM()/200*iif(EmpJorParc()>0,EmpJorParc()/100,1),Monto(SDOBAS)*(1+(iif(EmpEsqLiq()=29,Monto(AANTUT),Monto(AANTIG))*Monto(PORANT)+iif(EmpEsqLiq()=33,10,0))/100)*iif(EmpEsqLiq()=24,1.2,1))',
    '005': 'SMVM()',
    '006': 'iif(EmpJorParc()>0,EmpJorParc()/100,1)',
    '007': 'EmpJorParc()',
    '008': 'Monto(SDOBAS)',
    '009': 'iif(EmpEsqLiq()=29,Monto(AANTUT),Monto(AANTIG))',
    '010': 'Monto(AANTUT)',
    '011': 'Monto(AANTIG)',
    '012': 'Monto(PORANT)',
    '013': 'iif(EmpEsqLiq()=33,10,0)',
    '014': 'iif(EmpEsqLiq()=24,1.2,1)',
    '015': 'iif(EmpEmpresa()=40,Cant(),iif(InList(EmpEsqLiq(),1,22),1,iif(EmpEmpresa()=89,1.1,1))*iif(Cant(HSFERI)>0,iif(Cant(HSFERI)<1,Cant(HSFERI)*8*iif(Between(MONTO(JORPAR),1,100),MONTO(JORPAR)/100,1),Cant(HSFERI)),iif(pTipoLiq()=1,nFeri1q(),nFeri2q())*iif(InList(EmpEmpresa(),3,80,88,92),1.1,1)*iif(Between(EmpJorParc(),1,100),EmpJorParc()/100,1)*iif(EmpFormaLiq()=Q,8,1)))',
    '016': 'EmpEmpresa()',
    '017': 'Cant()',
    '018': 'iif(InList(EmpEsqLiq(),1,22),1,iif(EmpEmpresa()=89,1.1,1))',
    '019': 'InList(EmpEsqLiq(),1,22)',
    '020': 'iif(EmpEmpresa()=89,1.1,1)',
    '021': 'iif(Cant(HSFERI)>0,iif(Cant(HSFERI)<1,Cant(HSFERI)*8*iif(Between(MONTO(JORPAR),1,100),MONTO(JORPAR)/100,1),Cant(HSFERI)),iif(pTipoLiq()=1,nFeri1q(),nFeri2q())*iif(InList(EmpEmpresa(),3,80,88,92),1.1,1)*iif(Between(EmpJorParc(),1,100),EmpJorParc()/100,1)*iif(EmpFormaLiq()=Q,8,1))',
    '022': 'Cant(HSFERI)',
    '023': 'iif(Cant(HSFERI)<1,Cant(HSFERI)*8*iif(Between(MONTO(JORPAR),1,100),MONTO(JORPAR)/100,1),Cant(HSFERI))',
    '024': 'iif(Between(MONTO(JORPAR),1,100),MONTO(JORPAR)/100,1)',
    '025': 'Between(MONTO(JORPAR),1,100)',
    '026': 'MONTO(JORPAR)',
    '027': 'iif(pTipoLiq()=1,nFeri1q(),nFeri2q())',
    '028': 'pTipoLiq()',
    '029': 'nFeri1q()',
    '030': 'nFeri2q()',
    '031': 'iif(InList(EmpEmpresa(),3,80,88,92),1.1,1)',
    '032': 'InList(EmpEmpresa(),3,80,88,92)',
    '033': 'iif(Between(EmpJorParc(),1,100),EmpJorParc()/100,1)',
    '034': 'Between(EmpJorParc(),1,100)',
    '035': 'iif(EmpFormaLiq()=Q,8,1)',
    '036': 'EmpFormaLiq()'
}

test_dict_2 = {
    '001': 'Max(SMVM()/200*iif(EmpJorParc()>0,EmpJorParc()/100,1),Monto(SDOBAS)*(1+(iif(EmpEsqLiq()=29,Monto(AANTUT),Monto(AANTIG))*Monto(PORANT)+iif(EmpEsqLiq()=33,10,0))/100)*iif(EmpEsqLiq()=24,1.2,1))',
    '002': 'SMVM()',
    '003': 'iif(EmpJorParc()>0,EmpJorParc()/100,1)',
    '004': 'EmpJorParc()',
    '005': 'Monto(SDOBAS)',
    '006': 'iif(EmpEsqLiq()=29,Monto(AANTUT),Monto(AANTIG))',
    '007': 'EmpEsqLiq()',
    '008': 'Monto(AANTUT)',
    '009': 'Monto(AANTIG)',
    '010': 'Monto(PORANT)',
    '011': 'iif(EmpEsqLiq()=33,10,0)',
    '012': 'iif(EmpEsqLiq()=24,1.2,1)'
}

test_dict_base = {
    '001': 'Formula1(1,Formula2(Si(Formula()=3,4,Formula3(3,4)),Formula3(3,4)),3)',
    '002': 'Formula2(Si(Formula()=3,4,Formula3(3,4))',
    '003': 'Formula3(3,4)',
    '004': 'Si(Formula()=3,4,Formula3(3,4)'
}

cleaned_dict = clean_formulas_dict(test_dict_base)
print(cleaned_dict)
