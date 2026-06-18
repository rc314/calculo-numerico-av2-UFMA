import math
import unittest

from src.ajuste_curvas import (
    ajuste_exponencial,
    ajuste_geometrico,
    ajuste_hiperbolico,
    ajuste_polinomial,
    ajuste_reta,
    avaliar_exponencial,
    avaliar_geometrico,
    avaliar_hiperbolico,
    avaliar_polinomio,
    avaliar_reta,
    coeficiente_determinacao,
    soma_quadrados_erros,
)


class TestAjusteCurvas(unittest.TestCase):
    def test_ajuste_linear_resolve_dataset_de_trafego(self):
        pontos = [(8.0, 2.1), (9.0, 2.8), (10.0, 3.1), (11.0, 4.0), (12.0, 4.8)]

        coeficientes = ajuste_reta(pontos)
        avaliador = lambda x: avaliar_reta(coeficientes, x)

        self.assertAlmostEqual(coeficientes[0], 0.66)
        self.assertAlmostEqual(coeficientes[1], -3.24)
        self.assertAlmostEqual(avaliador(13.0), 5.34)
        self.assertAlmostEqual(soma_quadrados_erros(pontos, avaliador), 0.096)
        self.assertAlmostEqual(coeficiente_determinacao(pontos, avaliador), 0.9784366577)

    def test_ajuste_reta_reproduz_dados_lineares_exatos(self):
        pontos = [(0.0, 1.0), (1.0, 3.0), (2.0, 5.0)]
        coeficientes = ajuste_reta(pontos)

        self.assertAlmostEqual(coeficientes[0], 2.0)
        self.assertAlmostEqual(coeficientes[1], 1.0)
        self.assertAlmostEqual(avaliar_reta(coeficientes, 4.0), 9.0)

    def test_ajuste_polinomial_reproduz_parabola_exata(self):
        pontos = [(x, 1.0 + 2.0 * x + 3.0 * x**2) for x in range(4)]
        coeficientes = ajuste_polinomial(pontos, grau=2)

        for obtido, esperado in zip(coeficientes, [1.0, 2.0, 3.0]):
            self.assertAlmostEqual(obtido, esperado)

        self.assertAlmostEqual(avaliar_polinomio(coeficientes, 5.0), 86.0)

    def test_modelo_exponencial_linearizado_reproduz_dados_exatos(self):
        pontos = [(x, 2.0 * math.exp(0.5 * x)) for x in [0.0, 1.0, 2.0]]
        coeficientes = ajuste_exponencial(pontos)

        self.assertAlmostEqual(coeficientes[0], 2.0)
        self.assertAlmostEqual(coeficientes[1], 0.5)
        self.assertAlmostEqual(avaliar_exponencial(coeficientes, 3.0), 2.0 * math.exp(1.5))

    def test_modelo_hiperbolico_linearizado_reproduz_dados_exatos(self):
        pontos = [(x, 1.0 / (2.0 + 3.0 * x)) for x in [0.0, 1.0, 2.0]]
        coeficientes = ajuste_hiperbolico(pontos)

        self.assertAlmostEqual(coeficientes[0], 2.0)
        self.assertAlmostEqual(coeficientes[1], 3.0)
        self.assertAlmostEqual(avaliar_hiperbolico(coeficientes, 4.0), 1.0 / 14.0)

    def test_modelo_geometrico_linearizado_reproduz_dados_exatos(self):
        pontos = [(x, 4.0 * x**1.5) for x in [1.0, 2.0, 3.0]]
        coeficientes = ajuste_geometrico(pontos)

        self.assertAlmostEqual(coeficientes[0], 4.0)
        self.assertAlmostEqual(coeficientes[1], 1.5)
        self.assertAlmostEqual(avaliar_geometrico(coeficientes, 4.0), 32.0)


if __name__ == "__main__":
    unittest.main()
