"""Implementacoes dos metodos de interpolacao vistos em sala.

O projeto evita bibliotecas prontas de calculo numerico. Por isso, os metodos
abaixo usam apenas listas, lacos e a biblioteca padrao do Python.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from math import factorial
from pathlib import Path

Ponto = tuple[float, float]


@dataclass(frozen=True)
class TrechoSpline:
    """Representa um polinomio de spline em um intervalo fechado.

    Os coeficientes seguem o formato:
    S(x) = a + b*(x - x_inicial) + c*(x - x_inicial)^2 + d*(x - x_inicial)^3
    """

    x_inicial: float
    x_final: float
    coeficientes: tuple[float, float, float, float]

    def avaliar(self, x: float) -> float:
        """Avalia o trecho usando a forma deslocada em relacao ao no inicial."""
        a, b, c, d = self.coeficientes
        dx = x - self.x_inicial
        return a + b * dx + c * dx**2 + d * dx**3

    def derivada_primeira(self, x: float) -> float:
        """Avalia S'(x) no trecho."""
        _, b, c, d = self.coeficientes
        dx = x - self.x_inicial
        return b + 2.0 * c * dx + 3.0 * d * dx**2

    def derivada_segunda(self, x: float) -> float:
        """Avalia S''(x) no trecho."""
        _, _, c, d = self.coeficientes
        dx = x - self.x_inicial
        return 2.0 * c + 6.0 * d * dx


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


def validar_pontos_ordenados(pontos: list[Ponto]) -> None:
    """Confere se os pontos estao em ordem crescente de x."""
    validar_pontos(pontos)

    for i in range(len(pontos) - 1):
        if pontos[i][0] >= pontos[i + 1][0]:
            raise ValueError("Splines exigem pontos em ordem crescente de x.")


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


def localizar_trecho_spline(trechos: list[TrechoSpline], x_alvo: float) -> TrechoSpline:
    """Encontra o trecho que contem x_alvo."""
    if not trechos:
        raise ValueError("A lista de trechos nao pode estar vazia.")

    primeiro = trechos[0]
    ultimo = trechos[-1]
    if x_alvo < primeiro.x_inicial or x_alvo > ultimo.x_final:
        raise ValueError("x_alvo esta fora do intervalo coberto pela spline.")

    for trecho in trechos:
        if trecho.x_inicial <= x_alvo <= trecho.x_final:
            return trecho

    return ultimo


def coeficientes_spline_linear(pontos: list[Ponto]) -> list[TrechoSpline]:
    """Monta os trechos da spline linear interpolante."""
    validar_pontos_ordenados(pontos)
    trechos: list[TrechoSpline] = []

    for i in range(len(pontos) - 1):
        x0, y0 = pontos[i]
        x1, y1 = pontos[i + 1]
        inclinacao = (y1 - y0) / (x1 - x0)

        # Forma local: S_i(x) = y_i + m_i*(x - x_i).
        trechos.append(TrechoSpline(x0, x1, (y0, inclinacao, 0.0, 0.0)))

    return trechos


def spline_linear(pontos: list[Ponto], x_alvo: float) -> float:
    """Avalia a spline linear interpolante em x_alvo."""
    trechos = coeficientes_spline_linear(pontos)
    return localizar_trecho_spline(trechos, x_alvo).avaliar(x_alvo)


def segundas_derivadas_spline_cubica_natural(pontos: list[Ponto]) -> list[float]:
    """Calcula as segundas derivadas M_i da spline cubica natural.

    A condicao natural fixa M_0 = M_n = 0. Os valores internos sao obtidos
    resolvendo o sistema tridiagonal classico das splines cubicas.
    """
    validar_pontos_ordenados(pontos)
    quantidade_pontos = len(pontos)

    if quantidade_pontos == 2:
        return [0.0, 0.0]

    h = [pontos[i + 1][0] - pontos[i][0] for i in range(quantidade_pontos - 1)]
    internos = quantidade_pontos - 2
    inferior = [0.0 for _ in range(internos)]
    diagonal = [0.0 for _ in range(internos)]
    superior = [0.0 for _ in range(internos)]
    termos = [0.0 for _ in range(internos)]

    for linha in range(internos):
        i = linha + 1
        inferior[linha] = h[i - 1] if linha > 0 else 0.0
        diagonal[linha] = 2.0 * (h[i - 1] + h[i])
        superior[linha] = h[i] if linha < internos - 1 else 0.0
        inclinacao_direita = (pontos[i + 1][1] - pontos[i][1]) / h[i]
        inclinacao_esquerda = (pontos[i][1] - pontos[i - 1][1]) / h[i - 1]
        termos[linha] = 6.0 * (inclinacao_direita - inclinacao_esquerda)

    # Metodo de Thomas: eliminacao progressiva seguida de substituicao reversa.
    for linha in range(1, internos):
        fator = inferior[linha] / diagonal[linha - 1]
        diagonal[linha] -= fator * superior[linha - 1]
        termos[linha] -= fator * termos[linha - 1]

    internas = [0.0 for _ in range(internos)]
    internas[-1] = termos[-1] / diagonal[-1]

    for linha in range(internos - 2, -1, -1):
        internas[linha] = (termos[linha] - superior[linha] * internas[linha + 1]) / diagonal[linha]

    return [0.0, *internas, 0.0]


def coeficientes_spline_cubica_natural(pontos: list[Ponto]) -> list[TrechoSpline]:
    """Monta os trechos da spline cubica natural interpolante."""
    validar_pontos_ordenados(pontos)
    segundas = segundas_derivadas_spline_cubica_natural(pontos)
    trechos: list[TrechoSpline] = []

    for i in range(len(pontos) - 1):
        x0, y0 = pontos[i]
        x1, y1 = pontos[i + 1]
        h = x1 - x0

        a = y0
        b = (y1 - y0) / h - h * (2.0 * segundas[i] + segundas[i + 1]) / 6.0
        c = segundas[i] / 2.0
        d = (segundas[i + 1] - segundas[i]) / (6.0 * h)

        trechos.append(TrechoSpline(x0, x1, (a, b, c, d)))

    return trechos


def spline_cubica_natural(pontos: list[Ponto], x_alvo: float) -> float:
    """Avalia a spline cubica natural interpolante em x_alvo."""
    trechos = coeficientes_spline_cubica_natural(pontos)
    return localizar_trecho_spline(trechos, x_alvo).avaliar(x_alvo)


def erro_maximo_nos_pontos(
    pontos: list[Ponto],
    avaliador,
) -> float:
    """Mede o maior erro ao reavaliar o polinomio nos proprios nos."""
    erros = [abs(avaliador(pontos, x) - y) for x, y in pontos]
    return max(erros)
