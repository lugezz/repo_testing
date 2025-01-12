from .embargos import Embargo, Empleado


def test_multiples_embargos():
    smvm = 300000
    embargo1 = Embargo(
        amount=1000,
        start_date='2025-01-01',
        end_date='2025-12-31',
        percentage_rules=[
            {'from': 0, 'to': 100000, 'percentage': 10},
            {'from': 100000, 'to': 999999999, 'percentage': 20},
        ],
    )
    embargo2 = Embargo(
        amount=1000000,
        start_date='2025-01-01',
        end_date='2025-12-31',
    )
    embargo2.set_percentage_rule_from_smvm(smvm)

    empleado = Empleado(
        remuneracion=3000000,
        embargos=[embargo1, embargo2],
    )
    empleado.update_saldo_embargos()
    assert empleado.saldo_embargos == 1001000

    this_date = '2025-06-01'
    embargos, cuotas_alimentarias = empleado.calculate_embargos(this_date, smvm)
    assert embargos == 541000
    assert cuotas_alimentarias == 0
