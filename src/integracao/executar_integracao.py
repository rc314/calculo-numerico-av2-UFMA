"""Executa os problemas de integracao numerica da AV2."""

from __future__ import annotations

import csv
from math import e, erf, exp, pi, sqrt
from pathlib import Path

from src.integracao.metodos import (
    ler_pontos_csv,
    nos_e_pesos_gauss,
    quadratura_gauss,
    simpson_1_3,
    simpson_1_3_pontos,
    simpson_3_8_pontos,
    trapezios_repetidos,
    trapezios_repetidos_pontos,
)

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
DATASETS = RAIZ_PROJETO / "datasets"


def formatar_numero(valor: float) -> str:
    """Formata numeros com precisao suficiente e sem zeros desnecessarios."""
    return f"{valor:.10f}".rstrip("0").rstrip(".")


def formatar_pontos(pontos: list[tuple[float, float]]) -> str:
    """Monta uma tabela curta com os pontos usados no calculo."""
    return "\n".join(
        f"  x={formatar_numero(x):>5} | f(x)={formatar_numero(y):>8}"
        for x, y in pontos
    )


def ler_polinomio_gauss(caminho: Path) -> tuple[float, float, int, tuple[float, ...]]:
    """Le limites, numero de pontos e coeficientes do problema de Gauss."""
    with caminho.open(newline="", encoding="utf-8") as arquivo:
        linha = next(csv.DictReader(arquivo))

    return (
        float(linha["a"]),
        float(linha["b"]),
        int(linha["n_pontos"]),
        (
            float(linha["coef_x3"]),
            float(linha["coef_x2"]),
            float(linha["coef_x1"]),
            float(linha["coef_x0"]),
        ),
    )


def avaliar_polinomio_grau_3(coeficientes: tuple[float, ...], x: float) -> float:
    """Avalia a*x^3 + b*x^2 + c*x + d pela forma de Horner."""
    a, b, c, d = coeficientes
    return ((a * x + b) * x + c) * x + d


def integral_exata_polinomio_grau_3(
    coeficientes: tuple[float, ...],
    a: float,
    b: float,
) -> float:
    """Calcula a primitiva do polinomio para conferir a quadratura."""
    c3, c2, c1, c0 = coeficientes

    def primitiva(x: float) -> float:
        return c3 * x**4 / 4.0 + c2 * x**3 / 3.0 + c1 * x**2 / 2.0 + c0 * x

    return primitiva(b) - primitiva(a)


def executar_simpson_3_8() -> str:
    """Calcula os dados transferidos pela regra 3/8 de Simpson."""
    caminho = DATASETS / "05_transferencia_simpson_3_8.csv"
    pontos = ler_pontos_csv(caminho)
    h = pontos[1][0] - pontos[0][0]
    resultado = simpson_3_8_pontos(pontos)

    return f"""5. INTEGRACAO - NEWTON-COTES 3/8 DE SIMPSON
Dataset: datasets/05_transferencia_simpson_3_8.csv
Subintervalos: {len(pontos) - 1}, h = {formatar_numero(h)} s

Pontos usados:
{formatar_pontos(pontos)}

Calculo: (3h/8) * [f(x0) + 3f(x1) + 3f(x2) + f(x3)]
Total transferido: {formatar_numero(resultado)} MB
"""


def executar_trapezios_e_simpson() -> str:
    """Calcula a distancia do carro pelos dois metodos compostos."""
    caminho = DATASETS / "06_carro_eletrico_integracao.csv"
    pontos = ler_pontos_csv(caminho)
    h = pontos[1][0] - pontos[0][0]
    distancia_trapezios = trapezios_repetidos_pontos(pontos)
    distancia_simpson = simpson_1_3_pontos(pontos)
    diferenca = abs(distancia_simpson - distancia_trapezios)

    return f"""6. INTEGRACAO - TRAPEZIOS E SIMPSON 1/3
Dataset: datasets/06_carro_eletrico_integracao.csv
Subintervalos: {len(pontos) - 1}, h = {formatar_numero(h)} h

Pontos usados:
{formatar_pontos(pontos)}

Distancia por trapezios repetidos: {formatar_numero(distancia_trapezios)} km
Distancia por Simpson 1/3:         {formatar_numero(distancia_simpson)} km
Diferenca absoluta:               {formatar_numero(diferenca)} km
"""


def executar_gauss() -> str:
    """Calcula o trabalho da curva de torque por Gauss-Legendre."""
    caminho = DATASETS / "07_torque_motor_gauss.csv"
    a, b, n_pontos, coeficientes = ler_polinomio_gauss(caminho)
    funcao = lambda x: avaliar_polinomio_grau_3(coeficientes, x)
    nos, pesos = nos_e_pesos_gauss(n_pontos)
    resultado = quadratura_gauss(funcao, a, b, n_pontos)
    valor_exato = integral_exata_polinomio_grau_3(coeficientes, a, b)
    erro = abs(resultado - valor_exato)

    linhas_nos = []
    for no, peso in zip(nos, pesos):
        x_transformado = (a + b) / 2.0 + (b - a) * no / 2.0
        linhas_nos.append(
            f"  t={no: .10f} | peso={peso:.10f} | "
            f"x(t)={x_transformado: .10f} | f(x)={funcao(x_transformado): .10f}"
        )

    return f"""7. INTEGRACAO - QUADRATURA DE GAUSS
Dataset: datasets/07_torque_motor_gauss.csv
Funcao: f(x) = 5x^3 + x^2 - 12x + 4
Intervalo: [{formatar_numero(a)}, {formatar_numero(b)}]
Pontos de Gauss: {n_pontos}

Nos, pesos e valores avaliados:
{chr(10).join(linhas_nos)}

Resultado por Gauss:       {formatar_numero(resultado)}
Integral analitica exata:  {formatar_numero(valor_exato)}
Erro absoluto:             {erro:.12f}
"""


def executar_exemplos_enunciado() -> str:
    """Confere os exemplos com valores analiticos conhecidos."""
    exata_exp = e - 1.0
    trapezios_exp = trapezios_repetidos(exp, 0.0, 1.0, 10)
    simpson_exp = simpson_1_3(exp, 0.0, 1.0, 10)
    limite_erro_trapezios = e / 1200.0

    gauss_normal = quadratura_gauss(lambda x: exp(-(x**2)), -1.0, 1.0, 2)
    exata_normal = sqrt(pi) * erf(1.0)

    return f"""CONFERENCIAS DOS EXEMPLOS DO ENUNCIADO
Integral de e^x em [0, 1], n = 10:
  Trapezios repetidos: {formatar_numero(trapezios_exp)}
  Simpson 1/3:         {formatar_numero(simpson_exp)}
  Valor exato e - 1:   {formatar_numero(exata_exp)}
  Erro dos trapezios:  {abs(trapezios_exp - exata_exp):.12f}
  Limite teorico ETR:  {limite_erro_trapezios:.12f}

Integral de e^(-x^2) em [-1, 1], Gauss com 2 pontos:
  Aproximacao:          {formatar_numero(gauss_normal)}
  Valor de referencia:  {formatar_numero(exata_normal)}
  Erro absoluto:        {abs(gauss_normal - exata_normal):.12f}
"""


def main() -> None:
    """Ponto de entrada do modulo."""
    secoes = [
        executar_simpson_3_8(),
        executar_trapezios_e_simpson(),
        executar_gauss(),
        executar_exemplos_enunciado(),
    ]
    print(("\n" + "=" * 70 + "\n").join(secoes))


if __name__ == "__main__":
    main()
