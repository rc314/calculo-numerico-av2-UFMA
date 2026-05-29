"""Executa os exemplos de interpolacao usados na AV2."""

from __future__ import annotations

from pathlib import Path

from src.interpolacao.metodos import (
    diferencas_divididas,
    diferencas_finitas,
    erro_maximo_nos_pontos,
    gregory_newton,
    lagrange,
    ler_pontos_csv,
    newton,
)

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
DATASETS = RAIZ_PROJETO / "datasets"


def formatar_numero(valor: float) -> str:
    """Formata floats mantendo a saida curta e estavel."""
    return f"{valor:.10f}".rstrip("0").rstrip(".")


def formatar_tabela_triangular(tabela: list[list[float]]) -> str:
    """Converte uma tabela triangular em linhas legiveis."""
    linhas = []
    n = len(tabela)

    for i, linha in enumerate(tabela):
        valores_validos = linha[: n - i]
        linhas.append("  " + " | ".join(f"{valor:>12.6f}" for valor in valores_validos))

    return "\n".join(linhas)


def executar_lagrange_newton() -> str:
    """Resolve o problema do drone usando Lagrange e Newton."""
    caminho = DATASETS / "01_drone_altitude_interpolacao.csv"
    pontos = ler_pontos_csv(caminho)
    x_alvo = 3.5
    grau = len(pontos) - 1

    valor_lagrange = lagrange(pontos, x_alvo)
    valor_newton = newton(pontos, x_alvo)
    diferenca = abs(valor_lagrange - valor_newton)
    erro_lagrange = erro_maximo_nos_pontos(pontos, lagrange)
    erro_newton = erro_maximo_nos_pontos(pontos, newton)
    tabela = diferencas_divididas(pontos)
    coeficientes = tabela[0]

    return f"""1. INTERPOLACAO - LAGRANGE E NEWTON
Dataset: datasets/01_drone_altitude_interpolacao.csv
Pontos usados: {len(pontos)} pontos, polinomio de grau {grau}
Alvo: x = {formatar_numero(x_alvo)} s

Tabela de diferencas divididas:
{formatar_tabela_triangular(tabela)}

Coeficientes de Newton:
  {", ".join(formatar_numero(valor) for valor in coeficientes)}

Resultado por Lagrange: {formatar_numero(valor_lagrange)} m
Resultado por Newton:   {formatar_numero(valor_newton)} m
Diferenca absoluta entre os metodos: {diferenca:.12f}
Maior erro de Lagrange nos nos conhecidos: {erro_lagrange:.12f}
Maior erro de Newton nos nos conhecidos:   {erro_newton:.12f}
"""


def executar_gregory_newton() -> str:
    """Resolve o problema do servidor usando Gregory-Newton."""
    caminho = DATASETS / "02_servidor_temperatura_gregory_newton.csv"
    pontos = ler_pontos_csv(caminho)
    x_alvo = 25.0
    h = pontos[1][0] - pontos[0][0]

    valor_gregory = gregory_newton(pontos, x_alvo)
    valor_newton = newton(pontos, x_alvo)
    diferenca = abs(valor_gregory - valor_newton)
    erro_gregory = erro_maximo_nos_pontos(pontos, gregory_newton)
    tabela = diferencas_finitas(pontos)

    return f"""2. INTERPOLACAO - GREGORY-NEWTON
Dataset: datasets/02_servidor_temperatura_gregory_newton.csv
Pontos igualmente espacados: h = {formatar_numero(h)}
Alvo: x = {formatar_numero(x_alvo)} min

Tabela de diferencas finitas:
{formatar_tabela_triangular(tabela)}

Resultado por Gregory-Newton: {formatar_numero(valor_gregory)} C
Conferencia com Newton:       {formatar_numero(valor_newton)} C
Diferenca absoluta entre os metodos: {diferenca:.12f}
Maior erro de Gregory-Newton nos nos conhecidos: {erro_gregory:.12f}
"""


def main() -> None:
    """Ponto de entrada do script."""
    print(executar_lagrange_newton())
    print("=" * 70)
    print(executar_gregory_newton())


if __name__ == "__main__":
    main()
