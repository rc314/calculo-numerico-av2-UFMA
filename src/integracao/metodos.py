"""Metodos de integracao numerica estudados na AV2.

As formulas foram implementadas diretamente, sem NumPy ou SciPy. O modulo
aceita tanto funcoes matematicas quanto tabelas de pontos igualmente espacados.
"""

from __future__ import annotations

import csv
from collections.abc import Callable
from math import sqrt
from pathlib import Path

Ponto = tuple[float, float]
Funcao = Callable[[float], float]


def ler_pontos_csv(caminho: str | Path) -> list[Ponto]:
    """Le as duas primeiras colunas de um CSV como pares ``(x, f(x))``."""
    pontos: list[Ponto] = []

    with Path(caminho).open(newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        colunas = leitor.fieldnames
        if colunas is None or len(colunas) < 2:
            raise ValueError("O CSV precisa ter pelo menos duas colunas.")

        coluna_x, coluna_y = colunas[0], colunas[1]
        for linha in leitor:
            pontos.append((float(linha[coluna_x]), float(linha[coluna_y])))

    passo_pontos_equidistantes(pontos)
    return pontos


def validar_numero_subintervalos(n: int, multiplo: int = 1) -> None:
    """Valida a quantidade de subintervalos exigida por uma formula."""
    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        raise ValueError("O numero de subintervalos deve ser um inteiro positivo.")
    if n % multiplo != 0:
        raise ValueError(f"O numero de subintervalos deve ser multiplo de {multiplo}.")


def passo_pontos_equidistantes(pontos: list[Ponto]) -> float:
    """Valida uma tabela ordenada e devolve seu espacamento constante ``h``."""
    if len(pontos) < 2:
        raise ValueError("Sao necessarios pelo menos dois pontos.")

    h = pontos[1][0] - pontos[0][0]
    if h <= 0.0:
        raise ValueError("Os valores de x devem estar em ordem crescente.")

    for i in range(1, len(pontos) - 1):
        passo_atual = pontos[i + 1][0] - pontos[i][0]
        tolerancia = 1e-12 * max(1.0, abs(h), abs(passo_atual))
        if passo_atual <= 0.0 or abs(passo_atual - h) > tolerancia:
            raise ValueError("Os pontos devem estar em ordem e igualmente espacados.")

    return h


def trapezio(funcao: Funcao, a: float, b: float) -> float:
    """Aproxima a integral em um unico subintervalo pela regra do trapezio."""
    h = b - a
    return (h / 2.0) * (funcao(a) + funcao(b))


def trapezios_repetidos(funcao: Funcao, a: float, b: float, n: int) -> float:
    """Aplica a regra dos trapezios em ``n`` subintervalos iguais."""
    validar_numero_subintervalos(n)
    h = (b - a) / n
    soma_interna = sum(funcao(a + i * h) for i in range(1, n))
    return (h / 2.0) * (funcao(a) + 2.0 * soma_interna + funcao(b))


def trapezios_repetidos_pontos(pontos: list[Ponto]) -> float:
    """Aplica trapezios repetidos aos valores de uma tabela equidistante."""
    h = passo_pontos_equidistantes(pontos)
    valores_internos = sum(y for _, y in pontos[1:-1])
    return (h / 2.0) * (pontos[0][1] + 2.0 * valores_internos + pontos[-1][1])


def simpson_1_3(funcao: Funcao, a: float, b: float, n: int = 2) -> float:
    """Aplica Simpson 1/3 repetida; ``n`` deve ser par."""
    validar_numero_subintervalos(n, multiplo=2)
    h = (b - a) / n
    soma_impares = sum(funcao(a + i * h) for i in range(1, n, 2))
    soma_pares = sum(funcao(a + i * h) for i in range(2, n, 2))
    return (h / 3.0) * (
        funcao(a) + 4.0 * soma_impares + 2.0 * soma_pares + funcao(b)
    )


def simpson_1_3_pontos(pontos: list[Ponto]) -> float:
    """Aplica Simpson 1/3 aos valores de uma tabela equidistante."""
    h = passo_pontos_equidistantes(pontos)
    n = len(pontos) - 1
    validar_numero_subintervalos(n, multiplo=2)
    soma_impares = sum(pontos[i][1] for i in range(1, n, 2))
    soma_pares = sum(pontos[i][1] for i in range(2, n, 2))
    return (h / 3.0) * (
        pontos[0][1] + 4.0 * soma_impares + 2.0 * soma_pares + pontos[-1][1]
    )


def simpson_3_8(funcao: Funcao, a: float, b: float, n: int = 3) -> float:
    """Aplica Simpson 3/8 repetida; ``n`` deve ser multiplo de tres."""
    validar_numero_subintervalos(n, multiplo=3)
    h = (b - a) / n
    soma_multiplos_de_tres = sum(funcao(a + i * h) for i in range(3, n, 3))
    soma_demais = sum(funcao(a + i * h) for i in range(1, n) if i % 3 != 0)
    return (3.0 * h / 8.0) * (
        funcao(a)
        + 3.0 * soma_demais
        + 2.0 * soma_multiplos_de_tres
        + funcao(b)
    )


def simpson_3_8_pontos(pontos: list[Ponto]) -> float:
    """Aplica Simpson 3/8 aos valores de uma tabela equidistante."""
    h = passo_pontos_equidistantes(pontos)
    n = len(pontos) - 1
    validar_numero_subintervalos(n, multiplo=3)
    soma_multiplos_de_tres = sum(pontos[i][1] for i in range(3, n, 3))
    soma_demais = sum(pontos[i][1] for i in range(1, n) if i % 3 != 0)
    return (3.0 * h / 8.0) * (
        pontos[0][1]
        + 3.0 * soma_demais
        + 2.0 * soma_multiplos_de_tres
        + pontos[-1][1]
    )


def nos_e_pesos_gauss(n_pontos: int) -> tuple[tuple[float, ...], tuple[float, ...]]:
    """Devolve nos e pesos de Gauss-Legendre para uma, duas ou tres ordens."""
    if n_pontos == 1:
        return (0.0,), (2.0,)
    if n_pontos == 2:
        no = 1.0 / sqrt(3.0)
        return (-no, no), (1.0, 1.0)
    if n_pontos == 3:
        no = sqrt(3.0 / 5.0)
        return (-no, 0.0, no), (5.0 / 9.0, 8.0 / 9.0, 5.0 / 9.0)

    raise ValueError("A quadratura de Gauss foi implementada para 1, 2 ou 3 pontos.")


def quadratura_gauss(
    funcao: Funcao,
    a: float = -1.0,
    b: float = 1.0,
    n_pontos: int = 2,
) -> float:
    """Integra por Gauss-Legendre, incluindo a mudanca de ``[a,b]`` para ``[-1,1]``."""
    nos, pesos = nos_e_pesos_gauss(n_pontos)
    ponto_medio = (a + b) / 2.0
    meia_largura = (b - a) / 2.0

    # x(t) faz a mudanca de variavel; meia_largura e o Jacobiano dx/dt.
    soma_ponderada = sum(
        peso * funcao(ponto_medio + meia_largura * no)
        for no, peso in zip(nos, pesos)
    )
    return meia_largura * soma_ponderada
