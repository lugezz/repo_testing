import datetime
import unittest


def vacaciones_en_meses(start: datetime.date, end: datetime.date, months: list) -> dict:
    """ Calculate the vacations in months.
    Args:
        start: The start date.
        end: The end date.
        months: A list of the months to calculate. Example: [1, 2]

        The calculation is based on the following rules:
            - Base 30 days per month. It prioritizes the start date over the end date.
            - if end date is less than start date, it should return and empty dictionary.
            - All duplicates should be removed from the list of months.
            - All invalid months should be removed from the list of months. Not numeric or not in the range of 1 to 12.
            - The result should be sorted by month.
    Returns:
        A dictionary with the vacations in months.
        Example:
            {
                1: 30,
                2: 2,
            }
    """
    if end < start:
        return {}

    # Remove invalid months
    clean_months = [month for month in months if isinstance(month, int) and 1 <= month <= 12]

    # Remove duplicates
    clean_months = list(set(clean_months))

    # Sort the months
    clean_months.sort()

    vacations = {}
    for month in clean_months:
        if start.month == month:
            days = min(30 - start.day + 1, (end - start).days + 1)
        elif end.month == month:
            days = min(end.day, 30)
        elif start.month < month < end.month:
            days = 30
        else:
            days = 0

        vacations[str(month)] = days

    return vacations


# Test case
class TestVacations(unittest.TestCase):
    def test_vacaciones_ok(self):
        start = datetime.date(2025, 1, 1)
        end = datetime.date(2025, 2, 2)
        months = [1, 2]
        self.assertEqual(vacaciones_en_meses(start, end, months), {'1': 30, '2': 2})

    def test_vacaciones_invalid_months(self):
        start = datetime.date(2025, 1, 1)
        end = datetime.date(2025, 2, 2)
        months = [1, 2, 2, 1, '3', -1, 13, []]
        self.assertEqual(vacaciones_en_meses(start, end, months), {'1': 30, '2': 2})

    def test_vacaciones_empty(self):
        start = datetime.date(2025, 1, 1)
        end = datetime.date(2025, 2, 2)
        months = []
        self.assertEqual(vacaciones_en_meses(start, end, months), {})
        months_2 = ['lala']
        self.assertEqual(vacaciones_en_meses(start, end, months_2), {})

    def test_no_vacations_found(self):
        start = datetime.date(2025, 1, 1)
        end = datetime.date(2025, 2, 2)
        months = [3]
        self.assertEqual(vacaciones_en_meses(start, end, months), {'3': 0})
        months_2 = [3, 2]
        self.assertEqual(vacaciones_en_meses(start, end, months_2), {'2': 2, '3': 0})

    def test_long_vacations(self):
        start = datetime.date(2025, 2, 1)
        end = datetime.date(2025, 4, 2)
        months = [1, 2, 3, 4]
        self.assertEqual(vacaciones_en_meses(start, end, months), {'1': 0, '2': 30, '3': 30, '4': 2})


# Run the tests
if __name__ == "__main__":
    unittest.main()
