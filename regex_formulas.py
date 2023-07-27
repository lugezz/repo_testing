import re


text_1 = 'alala(1,2,3)+blbl(3, 2, 1)/blbl(3, 2, 1)'
text_2 = 'Nothing found here'
text_3 = "I'm at the end of the line(lalal())"
text_4 = 'I have a coma,alala(1,2,3)'
text_5 = 'Simple math calc (1+2+3)'

# Find the regex to find all the formulas with the following format: formula(lalala), formulas are
# separated by +, -, *, /, **, //, %, (, ), and formulas can have any number of parameters separated by ,
# Example: formula(1,2,3) + formula2(1,2,3) - formula3(1,2,3) * formula4(1,2,3) / formula5(1,2,3)
# ** formula6(1,2,3) // formula7(1,2,3) % formula8(1,2,3)
# Expected result is a list with all the formulas found in the text
# Example: ['formula(1,2,3)', 'formula2(1,2,3)', 'formula3(1,2,3)', 'formula4(1,2,3)', 'formula5(1,2,3)',
# 'formula6(1,2,3)', 'formula7(1,2,3)', 'formula8(1,2,3)']
# But if I have a formula inside a formula, I want this not affected
# Example: formula(1,formulax(1,2),3) + formula2(1,2,3) - formula3(1,2,3)
# Expected result is a list with all the formulas found in the text
# Example: ['formula(1,formulax(1,2),3)', 'formula2(1,2,3)', 'formula3(1,2,3)']

text = """formula(1,2,3) + formula2(1,2,3) - formula3(1,2,3) * formula4(1,2,3) /
formula5(1,2,3) ** formula6(1,2,3) // formula7(1,2,3) % formula8(1,2,3)"""
formula_en_formula = "formula(1,formulax(1,2),3) + formula2(1,2,3) - formula3(1,2,3)"

# pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\([^)]*\)'
# formulas = re.findall(pattern, text)
# formulas_complex = re.findall(pattern, formula_en_formula)
formula_pattern = r'formula\([^()]*+(?:(?R)[^()]*)*+\)'

# Find all matches of the pattern in the text
formulas = re.findall(formula_pattern, formula_en_formula, flags=re.IGNORECASE | re.VERBOSE)


print(formulas)
# print(formulas_complex)
