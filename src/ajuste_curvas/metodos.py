"""Implementacoes de minimos quadrados para ajuste de curvas.

O modulo usa apenas estruturas nativas do Python. A ideia central e montar as
equacoes normais do problema de minimos quadrados e resolver o sistema linear
resultante por eliminacao de Gauss com pivoteamento parcial.
"""

from __future__ import annotations

import csv
from collections.abc import Callable
from math import exp, log
from pathlib import Path

Ponto = tuple[float, float]
FuncaoBase = Callable[[float], float]


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


def validar_pontos(pontos: list[Ponto], quantidade_minima: int = 2) -> None:
    """Confere se ha pontos suficientes para ajustar um modelo."""
    if len(pontos) < quantidade_minima:
        raise ValueError(f"Sao necessarios pelo menos {quantidade_minima} pontos.")


def resolver_sistema_linear(matriz: list[list[float]], termos: list[float]) -> list[float]:
    """Resolve A*x = b por eliminacao de Gauss com pivoteamento parcial."""
    n = len(termos)

    if len(matriz) != n or any(len(linha) != n for linha in matriz):
        raise ValueError("A matriz do sistema deve ser quadrada.")

    a = [linha[:] for linha in matriz]
    b = termos[:]

    for coluna in range(n):
        linha_pivo = max(range(coluna, n), key=lambda linha: abs(a[linha][coluna]))

        if abs(a[linha_pivo][coluna]) < 1e-12:
            raise ValueError("Sistema singular; as funcoes base podem ser dependentes.")

        if linha_pivo != coluna:
            a[coluna], a[linha_pivo] = a[linha_pivo], a[coluna]
            b[coluna], b[linha_pivo] = b[linha_pivo], b[coluna]

        for linha in range(coluna + 1, n):
            fator = a[linha][coluna] / a[coluna][coluna]
            a[linha][coluna] = 0.0

            for j in range(coluna + 1, n):
                a[linha][j] -= fator * a[coluna][j]

            b[linha] -= fator * b[coluna]

    solucao = [0.0 for _ in range(n)]
    for linha in range(n - 1, -1, -1):
        soma = sum(a[linha][j] * solucao[j] for j in range(linha + 1, n))
        solucao[linha] = (b[linha] - soma) / a[linha][linha]

    return solucao


def montar_equacoes_normais(
    pontos: list[Ponto],
    funcoes_base: list[FuncaoBase],
) -> tuple[list[list[float]], list[float]]:
    """Monta a matriz e o vetor das equacoes normais de minimos quadrados."""
    validar_pontos(pontos, quantidade_minima=len(funcoes_base))

    if not funcoes_base:
        raise ValueError("Informe pelo menos uma funcao base.")

    n = len(funcoes_base)
    matriz = [[0.0 for _ in range(n)] for _ in range(n)]
    termos = [0.0 for _ in range(n)]

    for x, y in pontos:
        valores = [funcao(x) for funcao in funcoes_base]

        for i in range(n):
            termos[i] += y * valores[i]
            for j in range(n):
                matriz[i][j] += valores[i] * valores[j]

    return matriz, termos


def minimos_quadrados(
    pontos: list[Ponto],
    funcoes_base: list[FuncaoBase],
) -> list[float]:
    """Calcula os coeficientes alpha_i do ajuste por minimos quadrados."""
    matriz, termos = montar_equacoes_normais(pontos, funcoes_base)
    return resolver_sistema_linear(matriz, termos)


def avaliar_modelo(
    coeficientes: list[float] | tuple[float, ...],
    funcoes_base: list[FuncaoBase],
    x: float,
) -> float:
    """Avalia phi(x) = soma alpha_i*g_i(x)."""
    return sum(coeficiente * funcao(x) for coeficiente, funcao in zip(coeficientes, funcoes_base))


def ajuste_polinomial(pontos: list[Ponto], grau: int) -> list[float]:
    """Ajusta um polinomio a0 + a1*x + ... + an*x^n."""
    if grau < 0:
        raise ValueError("O grau do polinomio deve ser nao negativo.")

    funcoes_base = [lambda x, potencia=potencia: x**potencia for potencia in range(grau + 1)]
    return minimos_quadrados(pontos, funcoes_base)


def avaliar_polinomio(coeficientes: list[float] | tuple[float, ...], x: float) -> float:
    """Avalia um polinomio com coeficientes em ordem crescente de potencia."""
    return sum(coeficiente * x**potencia for potencia, coeficiente in enumerate(coeficientes))


def ajuste_reta(pontos: list[Ponto]) -> tuple[float, float]:
    """Ajusta P1(x) = a*x + b e devolve (a, b)."""
    b, a = ajuste_polinomial(pontos, grau=1)
    return a, b


def avaliar_reta(coeficientes: tuple[float, float], x: float) -> float:
    """Avalia P1(x) = a*x + b."""
    a, b = coeficientes
    return a * x + b


def ajuste_exponencial(pontos: list[Ponto]) -> tuple[float, float]:
    """Ajusta y ~= a1*e^(a2*x) usando ln(y) ~= ln(a1) + a2*x."""
    if any(y <= 0.0 for _, y in pontos):
        raise ValueError("O ajuste exponencial exige y > 0.")

    pontos_linearizados = [(x, log(y)) for x, y in pontos]
    a2, ln_a1 = ajuste_reta(pontos_linearizados)
    return exp(ln_a1), a2


def avaliar_exponencial(coeficientes: tuple[float, float], x: float) -> float:
    """Avalia y = a1*e^(a2*x)."""
    a1, a2 = coeficientes
    return a1 * exp(a2 * x)


def ajuste_hiperbolico(pontos: list[Ponto]) -> tuple[float, float]:
    """Ajusta y ~= 1/(a1 + a2*x) usando z = 1/y."""
    if any(y == 0.0 for _, y in pontos):
        raise ValueError("O ajuste hiperbolico exige y diferente de zero.")

    pontos_linearizados = [(x, 1.0 / y) for x, y in pontos]
    a2, a1 = ajuste_reta(pontos_linearizados)
    return a1, a2


def avaliar_hiperbolico(coeficientes: tuple[float, float], x: float) -> float:
    """Avalia y = 1/(a1 + a2*x)."""
    a1, a2 = coeficientes
    denominador = a1 + a2 * x

    if denominador == 0.0:
        raise ZeroDivisionError("O denominador do modelo hiperbolico ficou zero.")

    return 1.0 / denominador


def ajuste_geometrico(pontos: list[Ponto]) -> tuple[float, float]:
    """Ajusta y ~= a1*x^a2 usando ln(y) ~= ln(a1) + a2*ln(x)."""
    if any(x <= 0.0 or y <= 0.0 for x, y in pontos):
        raise ValueError("O ajuste geometrico exige x > 0 e y > 0.")

    pontos_linearizados = [(log(x), log(y)) for x, y in pontos]
    a2, ln_a1 = ajuste_reta(pontos_linearizados)
    return exp(ln_a1), a2


def avaliar_geometrico(coeficientes: tuple[float, float], x: float) -> float:
    """Avalia y = a1*x^a2."""
    a1, a2 = coeficientes

    if x <= 0.0:
        raise ValueError("O modelo geometrico exige x > 0.")

    return a1 * x**a2


def residuos(pontos: list[Ponto], avaliador: Callable[[float], float]) -> list[float]:
    """Calcula y_observado - y_estimado para cada ponto."""
    return [y - avaliador(x) for x, y in pontos]


def soma_quadrados_erros(pontos: list[Ponto], avaliador: Callable[[float], float]) -> float:
    """Calcula a soma dos quadrados dos residuos."""
    return sum(residuo**2 for residuo in residuos(pontos, avaliador))


def coeficiente_determinacao(pontos: list[Ponto], avaliador: Callable[[float], float]) -> float:
    """Calcula R^2 para medir a qualidade do ajuste."""
    validar_pontos(pontos)
    media_y = sum(y for _, y in pontos) / len(pontos)
    soma_total = sum((y - media_y) ** 2 for _, y in pontos)

    if soma_total == 0.0:
        return 1.0

    return 1.0 - soma_quadrados_erros(pontos, avaliador) / soma_total
