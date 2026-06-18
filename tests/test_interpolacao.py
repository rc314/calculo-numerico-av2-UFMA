import unittest

from src.interpolacao import (
    coeficientes_spline_cubica_natural,
    diferencas_divididas,
    diferencas_finitas,
    gregory_newton,
    lagrange,
    newton,
    segundas_derivadas_spline_cubica_natural,
    spline_cubica_natural,
    spline_linear,
)


class TestInterpolacao(unittest.TestCase):
    def test_lagrange_e_newton_reproduzem_exemplo_da_aula(self):
        pontos = [(-1.0, 4.0), (0.0, 1.0), (2.0, -1.0)]

        for x in [-1.0, 0.0, 1.0, 2.0]:
            esperado = (2.0 / 3.0) * x**2 - (7.0 / 3.0) * x + 1.0
            self.assertAlmostEqual(lagrange(pontos, x), esperado)
            self.assertAlmostEqual(newton(pontos, x), esperado)

    def test_diferencas_divididas_do_exemplo_da_aula(self):
        pontos = [(-1.0, 4.0), (0.0, 1.0), (2.0, -1.0)]
        tabela = diferencas_divididas(pontos)

        self.assertAlmostEqual(tabela[0][0], 4.0)
        self.assertAlmostEqual(tabela[0][1], -3.0)
        self.assertAlmostEqual(tabela[0][2], 2.0 / 3.0)

    def test_gregory_newton_bate_com_newton_em_pontos_equidistantes(self):
        pontos = [(10.0, 45.0), (20.0, 52.0), (30.0, 60.0), (40.0, 71.0)]

        self.assertAlmostEqual(gregory_newton(pontos, 25.0), 55.75)
        self.assertAlmostEqual(gregory_newton(pontos, 25.0), newton(pontos, 25.0))

    def test_tabela_de_diferencas_finitas(self):
        pontos = [(10.0, 45.0), (20.0, 52.0), (30.0, 60.0), (40.0, 71.0)]
        tabela = diferencas_finitas(pontos)

        self.assertEqual([tabela[i][0] for i in range(4)], [45.0, 52.0, 60.0, 71.0])
        self.assertEqual([tabela[i][1] for i in range(3)], [7.0, 8.0, 11.0])
        self.assertEqual([tabela[i][2] for i in range(2)], [1.0, 3.0])
        self.assertEqual(tabela[0][3], 2.0)

    def test_spline_linear_reproduz_exemplo_da_aula(self):
        pontos = [(1.0, 1.0), (2.0, 2.0), (5.0, 3.0), (7.0, 2.5)]

        self.assertAlmostEqual(spline_linear(pontos, 1.5), 1.5)
        self.assertAlmostEqual(spline_linear(pontos, 3.5), 2.5)
        self.assertAlmostEqual(spline_linear(pontos, 6.0), 2.75)

    def test_splines_resolvem_dataset_do_laser(self):
        pontos = [(0.0, 2.5), (1.0, 4.5), (2.0, 3.0), (3.0, 6.0)]

        self.assertAlmostEqual(spline_linear(pontos, 1.5), 3.75)
        self.assertAlmostEqual(spline_cubica_natural(pontos, 1.5), 3.675)
        segundas = segundas_derivadas_spline_cubica_natural(pontos)
        for obtido, esperado in zip(segundas, [0.0, -7.4, 8.6, 0.0]):
            self.assertAlmostEqual(obtido, esperado)

    def test_spline_cubica_natural_mantem_suavidade_nos_nos(self):
        pontos = [(0.0, 2.5), (1.0, 4.5), (2.0, 3.0), (3.0, 6.0)]
        trechos = coeficientes_spline_cubica_natural(pontos)

        for i in range(len(trechos) - 1):
            esquerda = trechos[i]
            direita = trechos[i + 1]
            x_no = esquerda.x_final

            self.assertAlmostEqual(esquerda.avaliar(x_no), direita.avaliar(x_no))
            self.assertAlmostEqual(esquerda.derivada_primeira(x_no), direita.derivada_primeira(x_no))
            self.assertAlmostEqual(esquerda.derivada_segunda(x_no), direita.derivada_segunda(x_no))

        self.assertAlmostEqual(trechos[0].derivada_segunda(trechos[0].x_inicial), 0.0)
        self.assertAlmostEqual(trechos[-1].derivada_segunda(trechos[-1].x_final), 0.0)


if __name__ == "__main__":
    unittest.main()
