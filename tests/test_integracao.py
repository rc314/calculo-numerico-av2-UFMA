import math
import unittest

from src.integracao import (
    nos_e_pesos_gauss,
    quadratura_gauss,
    simpson_1_3,
    simpson_1_3_pontos,
    simpson_3_8,
    simpson_3_8_pontos,
    trapezio,
    trapezios_repetidos,
    trapezios_repetidos_pontos,
)


class TestIntegracao(unittest.TestCase):
    def test_trapezio_integra_funcao_linear_exatamente(self):
        self.assertAlmostEqual(trapezio(lambda x: 3.0 * x + 2.0, 0.0, 4.0), 32.0)

    def test_trapezios_repetidos_reproduzem_exemplo_do_enunciado(self):
        obtido = trapezios_repetidos(math.exp, 0.0, 1.0, 10)
        valor_exato = math.e - 1.0
        limite_teorico = math.e / 1200.0

        self.assertAlmostEqual(obtido, 1.7197134914)
        self.assertLessEqual(abs(obtido - valor_exato), limite_teorico)

    def test_trapezios_resolvem_dataset_do_carro(self):
        pontos = [(0.0, 0.0), (0.5, 40.0), (1.0, 65.0), (1.5, 80.0), (2.0, 90.0)]
        self.assertAlmostEqual(trapezios_repetidos_pontos(pontos), 115.0)

    def test_simpson_1_3_e_exato_para_polinomio_cubico(self):
        funcao = lambda x: x**3 - 2.0 * x + 1.0
        self.assertAlmostEqual(simpson_1_3(funcao, -1.0, 2.0, 2), 3.75)

    def test_simpson_1_3_resolve_dataset_do_carro(self):
        pontos = [(0.0, 0.0), (0.5, 40.0), (1.0, 65.0), (1.5, 80.0), (2.0, 90.0)]
        self.assertAlmostEqual(simpson_1_3_pontos(pontos), 350.0 / 3.0)

    def test_simpson_3_8_resolve_dataset_de_transferencia(self):
        pontos = [(0.0, 10.0), (2.0, 15.0), (4.0, 12.0), (6.0, 8.0)]
        self.assertAlmostEqual(simpson_3_8_pontos(pontos), 74.25)

    def test_simpson_3_8_e_exato_para_polinomio_cubico(self):
        funcao = lambda x: 2.0 * x**3 - x**2 + 4.0
        self.assertAlmostEqual(simpson_3_8(funcao, 0.0, 3.0, 3), 43.5)

    def test_gauss_de_dois_pontos_e_exato_ate_grau_tres(self):
        funcao = lambda x: 5.0 * x**3 + x**2 - 12.0 * x + 4.0
        obtido = quadratura_gauss(funcao, -1.0, 1.0, n_pontos=2)
        self.assertAlmostEqual(obtido, 26.0 / 3.0)

    def test_gauss_faz_mudanca_para_intervalo_geral(self):
        # Tres pontos de Gauss integram exatamente polinomios de grau ate cinco.
        self.assertAlmostEqual(
            quadratura_gauss(lambda x: x**5, 1.0, 3.0, n_pontos=3),
            (3.0**6 - 1.0) / 6.0,
        )

    def test_nos_e_pesos_de_gauss_possuem_as_somas_corretas(self):
        for ordem in (1, 2, 3):
            nos, pesos = nos_e_pesos_gauss(ordem)
            self.assertEqual(len(nos), ordem)
            self.assertAlmostEqual(sum(pesos), 2.0)

    def test_rejeita_quantidades_incompativeis_com_simpson(self):
        with self.assertRaises(ValueError):
            simpson_1_3(lambda x: x, 0.0, 1.0, n=3)
        with self.assertRaises(ValueError):
            simpson_3_8(lambda x: x, 0.0, 1.0, n=4)

    def test_rejeita_tabela_nao_equidistante(self):
        pontos = [(0.0, 1.0), (1.0, 2.0), (2.1, 3.0)]
        with self.assertRaises(ValueError):
            trapezios_repetidos_pontos(pontos)


if __name__ == "__main__":
    unittest.main()
