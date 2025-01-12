import datetime
from enum import Enum
import unittest


def safe_eval(expression: str) -> tuple:
    """ Basic evaluation for simple expressions including '+', '-', '*', '/' and numbers
        It is supposed to have just one operator for expression
        if any other operator is used, it will return 0

        Returns a tuple with:
        - The result of the expression
        - A message with the error if any
    """
    allowed_operators = ['+', '-', '*', '/']
    operators_found = set()
    for operator in allowed_operators:
        if operator in expression:
            operators_found.add(operator)

    if len(operators_found) > 1:
        return 0, "Error: More than one operator in expression"

    result = 0
    error_msg = ""
    try:
        if '+' in expression:
            adders = expression.split('+')
            for adder in adders:
                result += float(adder)
        elif '-' in expression:
            substractors = expression.split('-')
            result = float(substractors[0])
            for substractor in substractors[1:]:
                result -= float(substractor)
        elif '*' in expression:
            multipliers = expression.split('*')
            result = float(multipliers[0])
            for multiplier in multipliers[1:]:
                result *= float(multiplier)
        elif '/' in expression:
            dividers = expression.split('/')
            result = float(dividers[0])
            for divider in dividers[1:]:
                result /= float(divider)
        else:
            result = float(expression)
    except ZeroDivisionError:
        result = 0
        error_msg = "Error: Division by zero"
    except Exception as e:
        result = 0
        error_msg = f"Error: {e}"
    return result, error_msg


class CType(Enum):
    REMUNERATIVO = "Remunerativo"
    NO_REMUNERATIVO = "No Remunerativo"
    DESCUENTO = "Descuento"
    AUXILIAR = "Auxiliar"


class Concepto:
    def __init__(self, name: str, ctype: CType, formula: str, validity: tuple, amount: float = None):
        # ctype can be 'Remunerativo', 'No Remunerativo', 'Descuento' or 'Auxiliar'.
        # The 2 first cases are added to the total and 'Descuento' is subtracted.
        self.name = name
        self.ctype = ctype
        self.formula = formula
        self.amount = amount
        self.validity_from = validity[0]
        self.validity_to = validity[1]

    def get_amount(self):
        if self.amount:
            return self.amount
        else:
            return safe_eval(self.formula)[0]


class Empleado:
    def __init__(self, name: str, concepts: list):
        self.name = name
        self.concepts = concepts
        self.liquidaciones = []

    def add_liquidacion(self, liquidacion):
        self.liquidaciones.append(liquidacion)

    def calculate(self, liquidacion) -> dict:
        """ Calculate concepts for a given liquidacion
            It should return a dictionary with the calculated concepts.
            and a total like this:
            {
                'concepts: {
                    'concept_1': 100
                    'concept_2': 200
                }
                'total': 300
            }
        """
        total = 0
        calculated_concepts = {}
        for concept in liquidacion.concepts:
            if concept.validity_from <= liquidacion.date <= concept.validity_to:
                # If formula concepto is like 'Monto(NombreConcepto)' I should get the amount of the concepto
                amount = 0
                if 'Monto' in concept.formula:
                    concept_name = concept.formula.split('(')[1].split(')')[0]
                    for c in liquidacion.concepts:
                        if c.name == concept_name:
                            amount = c.get_amount()
                else:
                    amount = concept.get_amount()

                if concept.ctype == CType.DESCUENTO:
                    total -= amount
                elif concept.ctype in [CType.REMUNERATIVO, CType.NO_REMUNERATIVO]:
                    total += amount
                if concept.ctype in [CType.REMUNERATIVO, CType.NO_REMUNERATIVO, CType.DESCUENTO]:
                    calculated_concepts[concept.name] = amount
        return {'concepts': calculated_concepts, 'total': total}


class Liquidacion:
    def __init__(self, date: datetime.date, concepts: list):
        self.date = date
        self.net_amount = 0
        self.concepts = concepts


# Test case
class TestLiquidacion(unittest.TestCase):
    def test_calculate(self):
        sueldo = Concepto('sueldo', CType.REMUNERATIVO, '100000', (datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)))
        auxiliar = Concepto('auxiliar', CType.AUXILIAR, '50000/5', (datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)))
        no_remunerativo = Concepto(
            name='no_remunerativo',
            ctype=CType.NO_REMUNERATIVO,
            formula='Monto(auxiliar)',
            validity=(datetime.date(2025, 1, 1), datetime.date(2025, 12, 31))
        )
        aportes = Concepto('descuento', CType.DESCUENTO, '0', (datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)), 5000)

        empleado = Empleado('Juan', [sueldo, auxiliar, no_remunerativo, aportes])
        liquidacion = Liquidacion(datetime.date(2025, 1, 1), empleado.concepts)
        empleado.add_liquidacion(liquidacion)
        result = empleado.calculate(liquidacion)

        self.assertEqual(result['total'], 105000)
        self.assertEqual(len(result['concepts']), 3)

    def test_validity(self):
        sueldo = Concepto('sueldo', CType.REMUNERATIVO, '100000', (datetime.date(2025, 1, 1), datetime.date(2025, 1, 31)))
        auxiliar = Concepto('auxiliar', CType.AUXILIAR, '50000/5', (datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)))
        no_remunerativo = Concepto(
            name='no_remunerativo',
            ctype=CType.NO_REMUNERATIVO,
            formula='Monto(auxiliar)',
            validity=(datetime.date(2025, 1, 1), datetime.date(2025, 12, 31))
        )
        aportes = Concepto('descuento', CType.DESCUENTO, '0', (datetime.date(2025, 7, 1), datetime.date(2025, 12, 31)), 5000)

        empleado = Empleado('Juan', [sueldo, auxiliar, no_remunerativo, aportes])
        liquidacion = Liquidacion(datetime.date(2025, 6, 1), empleado.concepts)
        empleado.add_liquidacion(liquidacion)
        result = empleado.calculate(liquidacion)

        self.assertEqual(result['total'], 10000)
        self.assertEqual(len(result['concepts']), 1)

    def test_safe_eval_ok(self):
        expression1 = '100+200'
        result, error_msg = safe_eval(expression1)
        self.assertEqual(result, 300)
        self.assertEqual(error_msg, "")

    def test_safe_eval_2_same_operators(self):
        expression1 = '100+200+300'
        result, error_msg = safe_eval(expression1)
        self.assertEqual(result, 600)
        self.assertEqual(error_msg, "")

    def test_safe_eval_2_diff_operators(self):
        expression1 = '100+200-300'
        result, error_msg = safe_eval(expression1)
        self.assertEqual(result, 0)
        self.assertEqual(error_msg, "Error: More than one operator in expression")


# Run the tests
if __name__ == "__main__":
    unittest.main()
