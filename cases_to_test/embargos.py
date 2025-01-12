import datetime


class Embargo:
    def __init__(
        self,
        amount: float,
        start_date: datetime.date,
        end_date: datetime.date,
        calc_variable: float = 0.0,
        calc_fixed: float = 0.0,
        is_cuota_alimentaria: bool = False,
        percentage_rules: dict = None
    ):
        """
            percentage_rules: A dictionary with the percentage rules.
            rules_format:
                {'from': 0, 'to': 100, 'percentage': 10}
                {'from': 101, 'to': 200, 'percentage': 20}
        """
        self.amount = amount
        self.start_date = start_date
        self.end_date = end_date
        self.calc_variable = calc_variable
        self.calc_fixed = calc_fixed
        self.is_cuota_alimentaria = is_cuota_alimentaria
        self.balance = amount

        # Default percentage rules:
        if percentage_rules is None:
            self._percentage_rules = [
                {'from': 0, 'to': 500000, 'percentage': 10},
                {'from': 500000, 'to': 99999999999, 'percentage': 20},
            ]
        else:
            self._percentage_rules = percentage_rules

    def get_percentage_rules(self):
        return self._percentage_rules

    def set_percentage_rules(self, percentage_rules: dict):
        self._percentage_rules = percentage_rules

    def set_percentage_rule_from_smvm(self, smvm):
        """ Set the percentage rules based on the "Salario Minimo """
        self._percentage_rules = [
            {'from': 0, 'to': smvm * 2, 'percentage': 10},
            {'from': smvm * 2, 'to': 99999999999, 'percentage': 20},
        ]

    def subtract(self, amount):
        self.balance -= amount

    def add(self, amount):
        self.balance += amount

    def calculate(self, date, remuneracion, max_amount, to_subtract) -> float:
        """ Calculate the embargo amount based on the date and the rules.
        Args:
            date: The date for which the embargo should be calculated.
            max_amount: The maximum amount that can be embargoed.
            to_subtract: The amount that should be subtracted from the embargo.

        Returns:
            The embargo amount.
        """
        # Check if the date is within the embargo period:
        if not self.start_date <= date <= self.end_date:
            return 0

        # Cuota alimentaria are always calculated:
        if self.is_cuota_alimentaria:
            result = remuneracion * self.calc_variable + self.calc_fixed
        else:
            # Embargo comercial
            # Get the percentage:
            percentage = 0
            for rule in self._percentage_rules:
                if rule['from'] <= remuneracion <= rule['to']:
                    percentage = rule['percentage']
                    break

            # Calculate the embargo amount:
            embargo_amount = (remuneracion - to_subtract) * percentage / 100
            result = max(0, min(embargo_amount, max_amount, self.balance))

        print("°°°°°°")
        print(self._percentage_rules)

        return result


class Empleado:
    def __init__(self, remuneracion: float, embargos: list):
        self.remuneracion = remuneracion
        self.embargos = embargos
        self.saldo_embargos = 0

    def has_cuota_alimentaria(self) -> bool:
        """ Check if the employee has a cuota alimentaria. """
        return any(embargo.is_cuota_alimentaria for embargo in self.embargos)

    def update_saldo_embargos(self):
        """ Update the total embargo amount for the employee. """
        self.saldo_embargos = 0
        for embargo in self.embargos:
            self.saldo_embargos += embargo.balance

    def calculate_embargos(self, date, to_subtract) -> tuple:
        """ Calculate the total embargo amount for the employee.
        Args:
            date: The date for which the embargo should be calculated.
            to_subtract: The amount that should be subtracted from the embargo.
        Returns:
            Tuple with the total embargo amount and the cuota alimentaria amount.
        """
        if self.saldo_embargos == 0 and not self.has_cuota_alimentaria():
            return 0, 0

        total_embargo = 0
        total_cuota_alimentaria = 0

        for embargo in self.embargos:
            if total_embargo >= self.saldo_embargos and not self.has_cuota_alimentaria():
                break
            embargado = embargo.calculate(
                date=date,
                remuneracion=self.remuneracion,
                max_amount=self.saldo_embargos - total_embargo,
                to_subtract=to_subtract,
            )
            if embargo.is_cuota_alimentaria:
                total_cuota_alimentaria += embargado
            else:
                total_embargo += embargado

        return total_embargo, total_cuota_alimentaria
