"""Executa os exemplos de interpolacao usados na AV2."""

from __future__ import annotations

from pathlib import Path

from src.interpolacao.metodos import (
    TrechoSpline,
    coeficientes_spline_cubica_natural,
    coeficientes_spline_linear,
    diferencas_divididas,
    diferencas_finitas,
    erro_maximo_nos_pontos,
    gregory_newton,
    lagrange,
    ler_pontos_csv,
    newton,
    segundas_derivadas_spline_cubica_natural,
    spline_cubica_natural,
    spline_linear,
)

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
DATASETS = RAIZ_PROJETO / "datasets"


def formatar_numero(valor: float) -> str:
    """Formata floats mantendo a saida curta e estavel."""
    return f"{valor:.10f}".rstrip("0").rstrip(".")


def formatar_termo_sinal(coeficiente: float, termo: str) -> str:
    """Formata um termo com sinal explicito para polinomios."""
    sinal = "+" if coeficiente >= 0.0 else "-"
    return f"{sinal} {formatar_numero(abs(coeficiente))}*{termo}"


def formatar_tabela_triangular(tabela: list[list[float]]) -> str:
    """Converte uma tabela triangular em linhas legiveis."""
    linhas = []
    n = len(tabela)

    for i, linha in enumerate(tabela):
        valores_validos = linha[: n - i]
        linhas.append("  " + " | ".join(f"{valor:>12.6f}" for valor in valores_validos))

    return "\n".join(linhas)


def formatar_trechos_spline(trechos: list[TrechoSpline], grau: int) -> str:
    """Converte os polinomios por partes em texto curto."""
    linhas = []

    for i, trecho in enumerate(trechos, start=1):
        a, b, c, d = trecho.coeficientes
        deslocamento = f"(x - {formatar_numero(trecho.x_inicial)})"

        if grau == 1:
            expressao = (
                f"{formatar_numero(a)} "
                f"{formatar_termo_sinal(b, deslocamento)}"
            )
        else:
            expressao = (
                f"{formatar_numero(a)} "
                f"{formatar_termo_sinal(b, deslocamento)} "
                f"{formatar_termo_sinal(c, deslocamento + '^2')} "
                f"{formatar_termo_sinal(d, deslocamento + '^3')}"
            )

        linhas.append(
            f"  S{i}(x) = {expressao}, x em "
            f"[{formatar_numero(trecho.x_inicial)}, {formatar_numero(trecho.x_final)}]"
        )

    return "\n".join(linhas)


def medir_suavidade_spline(trechos: list[TrechoSpline]) -> tuple[float, float, float]:
    """Mede saltos de S, S' e S'' nos nos internos da spline cubica."""
    saltos_valor = []
    saltos_derivada_1 = []
    saltos_derivada_2 = []

    for i in range(len(trechos) - 1):
        esquerda = trechos[i]
        direita = trechos[i + 1]
        x_no = esquerda.x_final

        saltos_valor.append(abs(esquerda.avaliar(x_no) - direita.avaliar(x_no)))
        saltos_derivada_1.append(abs(esquerda.derivada_primeira(x_no) - direita.derivada_primeira(x_no)))
        saltos_derivada_2.append(abs(esquerda.derivada_segunda(x_no) - direita.derivada_segunda(x_no)))

    return (
        max(saltos_valor, default=0.0),
        max(saltos_derivada_1, default=0.0),
        max(saltos_derivada_2, default=0.0),
    )


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


def executar_splines() -> str:
    """Resolve o problema do laser usando splines linear e cubica natural."""
    caminho = DATASETS / "03_laser_splines.csv"
    pontos = ler_pontos_csv(caminho)
    x_alvo = 1.5

    trechos_linear = coeficientes_spline_linear(pontos)
    trechos_cubica = coeficientes_spline_cubica_natural(pontos)
    segundas = segundas_derivadas_spline_cubica_natural(pontos)
    valor_linear = spline_linear(pontos, x_alvo)
    valor_cubica = spline_cubica_natural(pontos, x_alvo)
    erro_linear = erro_maximo_nos_pontos(pontos, spline_linear)
    erro_cubica = erro_maximo_nos_pontos(pontos, spline_cubica_natural)
    salto_s, salto_s1, salto_s2 = medir_suavidade_spline(trechos_cubica)

    return f"""3. SPLINES LINEAR E CUBICA NATURAL
Dataset: datasets/03_laser_splines.csv
Alvo: x = {formatar_numero(x_alvo)} s

Trechos da spline linear no formato a + b*(x - xi):
{formatar_trechos_spline(trechos_linear, grau=1)}

Segundas derivadas M_i da spline cubica natural:
  {", ".join(formatar_numero(valor) for valor in segundas)}

Trechos da spline cubica natural no formato a + b*(x - xi) + c*(x - xi)^2 + d*(x - xi)^3:
{formatar_trechos_spline(trechos_cubica, grau=3)}

Resultado por spline linear:          {formatar_numero(valor_linear)} cm
Resultado por spline cubica natural:  {formatar_numero(valor_cubica)} cm
Maior erro da spline linear nos nos conhecidos:         {erro_linear:.12f}
Maior erro da spline cubica natural nos nos conhecidos: {erro_cubica:.12f}
Maior salto em S nos nos internos:    {salto_s:.12f}
Maior salto em S' nos nos internos:   {salto_s1:.12f}
Maior salto em S'' nos nos internos:  {salto_s2:.12f}
"""


def main() -> None:
    """Ponto de entrada do script."""
    print(executar_lagrange_newton())
    print("=" * 70)
    print(executar_gregory_newton())
    print("=" * 70)
    print(executar_splines())


if __name__ == "__main__":
    main()
