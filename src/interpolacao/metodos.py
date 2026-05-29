"""Implementacoes dos metodos de interpolacao vistos em sala.

O projeto evita bibliotecas prontas de calculo numerico. Por isso, os metodos
abaixo usam apenas listas, lacos e a biblioteca padrao do Python.
"""

from __future__ import annotations

import csv
from math import factorial
from pathlib import Path

Ponto = tuple[float, float]


def ler_pontos_csv(caminho: str | Path) -> list[Ponto]:
    """Le um CSV com duas colunas numericas e devolve pares (x, y)."""
    pontos: list[Ponto] = []

    with Path(caminho).open(newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        colunas = leitor.fieldnames
        if colunas is None or len(colunas) < 2:
            raise ValueError("O CSV precisa ter pelo menos duas colunas.")

        coluna_x, coluna_y = colunas[0], colunas[1]
        for linha in leitor:
            pontos.append((float(linha[coluna_x]), float(linha[coluna_y])))

    validar_pontos(pontos)
    return pontos


def validar_pontos(pontos: list[Ponto]) -> None:
    """Confere se a lista de pontos permite interpolacao."""
    if len(pontos) < 2:
        raise ValueError("Sao necessarios pelo menos dois pontos.")

    valores_x = [x for x, _ in pontos]
    if len(set(valores_x)) != len(valores_x):
        raise ValueError("Os valores de x devem ser distintos.")


def lagrange(pontos: list[Ponto], x_alvo: float) -> float:
    """Calcula P(x_alvo) pela formula direta de Lagrange."""
    validar_pontos(pontos)
    resultado = 0.0

    for i, (xi, yi) in enumerate(pontos):
        base = 1.0

        # L_i(x) vale 1 no proprio no xi e 0 nos demais nos da tabela.
        for j, (xj, _) in enumerate(pontos):
            if i != j:
                base *= (x_alvo - xj) / (xi - xj)

        resultado += yi * base

    return resultado


def diferencas_divididas(pontos: list[Ponto]) -> list[list[float]]:
    """Monta a tabela triangular superior de diferencas divididas."""
    validar_pontos(pontos)
    n = len(pontos)
    tabela = [[0.0 for _ in range(n)] for _ in range(n)]

    for i, (_, yi) in enumerate(pontos):
        tabela[i][0] = yi

    for ordem in range(1, n):
        for linha in range(n - ordem):
            numerador = tabela[linha + 1][ordem - 1] - tabela[linha][ordem - 1]
            denominador = pontos[linha + ordem][0] - pontos[linha][0]
            tabela[linha][ordem] = numerador / denominador

    return tabela


def newton(pontos: list[Ponto], x_alvo: float) -> float:
    """Calcula P(x_alvo) pela formula de Newton."""
    tabela = diferencas_divididas(pontos)
    resultado = tabela[0][0]
    produto = 1.0

    for ordem in range(1, len(pontos)):
        produto *= x_alvo - pontos[ordem - 1][0]
        resultado += tabela[0][ordem] * produto

    return resultado


def diferencas_finitas(pontos: list[Ponto]) -> list[list[float]]:
    """Monta a tabela de diferencas finitas para pontos equidistantes."""
    validar_pontos(pontos)
    passo = pontos[1][0] - pontos[0][0]

    for i in range(1, len(pontos) - 1):
        passo_atual = pontos[i + 1][0] - pontos[i][0]
        if abs(passo_atual - passo) > 1e-12:
            raise ValueError("Gregory-Newton exige pontos igualmente espacados.")

    n = len(pontos)
    tabela = [[0.0 for _ in range(n)] for _ in range(n)]

    for i, (_, yi) in enumerate(pontos):
        tabela[i][0] = yi

    for ordem in range(1, n):
        for linha in range(n - ordem):
            tabela[linha][ordem] = tabela[linha + 1][ordem - 1] - tabela[linha][ordem - 1]

    return tabela


def gregory_newton(pontos: list[Ponto], x_alvo: float) -> float:
    """Calcula P(x_alvo) pela formula progressiva de Gregory-Newton."""
    tabela = diferencas_finitas(pontos)
    x0 = pontos[0][0]
    h = pontos[1][0] - pontos[0][0]
    s = (x_alvo - x0) / h
    resultado = tabela[0][0]
    produto_s = 1.0

    for ordem in range(1, len(pontos)):
        produto_s *= s - (ordem - 1)
        resultado += produto_s * tabela[0][ordem] / factorial(ordem)

    return resultado


def erro_maximo_nos_pontos(
    pontos: list[Ponto],
    avaliador,
) -> float:
    """Mede o maior erro ao reavaliar o polinomio nos proprios nos."""
    erros = [abs(avaliador(pontos, x) - y) for x, y in pontos]
    return max(erros)
