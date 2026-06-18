"""Executa os exemplos de ajuste de curvas usados na AV2."""

from __future__ import annotations

from pathlib import Path

from src.ajuste_curvas.metodos import (
    ajuste_reta,
    avaliar_reta,
    coeficiente_determinacao,
    ler_pontos_csv,
    montar_equacoes_normais,
    residuos,
    soma_quadrados_erros,
)

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
DATASETS = RAIZ_PROJETO / "datasets"


def formatar_numero(valor: float) -> str:
    """Formata floats mantendo a saida curta e estavel."""
    return f"{valor:.10f}".rstrip("0").rstrip(".")


def formatar_reta(a: float, b: float) -> str:
    """Formata P1(x) evitando sinais duplicados."""
    sinal = "+" if b >= 0.0 else "-"
    return f"P1(x) = {formatar_numero(a)}*x {sinal} {formatar_numero(abs(b))}"


def formatar_matriz(matriz: list[list[float]]) -> str:
    """Converte uma matriz pequena em texto alinhado."""
    linhas = []

    for linha in matriz:
        linhas.append("  " + " | ".join(f"{valor:>12.6f}" for valor in linha))

    return "\n".join(linhas)


def executar_ajuste_linear() -> str:
    """Resolve o problema de trafego usando ajuste linear por MMQ."""
    caminho = DATASETS / "04_trafego_rede_mmq.csv"
    pontos = ler_pontos_csv(caminho)
    x_alvo = 13.0

    coeficientes = ajuste_reta(pontos)
    a, b = coeficientes
    avaliador = lambda x: avaliar_reta(coeficientes, x)
    valor_previsto = avaliador(x_alvo)
    lista_residuos = residuos(pontos, avaliador)
    sse = soma_quadrados_erros(pontos, avaliador)
    r2 = coeficiente_determinacao(pontos, avaliador)
    soma_residuos = sum(lista_residuos)
    soma_x_residuos = sum(x * residuo for (x, _), residuo in zip(pontos, lista_residuos))
    matriz, termos = montar_equacoes_normais(
        pontos,
        [
            lambda _x: 1.0,
            lambda x: x,
        ],
    )

    linhas_residuos = []
    for (x, y), residuo in zip(pontos, lista_residuos):
        estimado = avaliador(x)
        linhas_residuos.append(
            "  "
            f"x={formatar_numero(x):>4} | y={formatar_numero(y):>6} | "
            f"estimado={formatar_numero(estimado):>8} | residuo={formatar_numero(residuo):>8}"
        )

    return f"""4. AJUSTE DE CURVAS - MINIMOS QUADRADOS
Dataset: datasets/04_trafego_rede_mmq.csv
Modelo: P1(x) = a*x + b
Alvo: x = {formatar_numero(x_alvo)} h

Equacoes normais:
Matriz:
{formatar_matriz(matriz)}
Termos independentes:
  {", ".join(formatar_numero(valor) for valor in termos)}

Coeficiente angular a: {formatar_numero(a)}
Coeficiente linear b:  {formatar_numero(b)}
Reta ajustada: {formatar_reta(a, b)}

Pontos, estimativas e residuos:
{chr(10).join(linhas_residuos)}

Previsao para x = {formatar_numero(x_alvo)} h: {formatar_numero(valor_previsto)} mil acessos
Soma dos quadrados dos erros: {formatar_numero(sse)}
Coeficiente de determinacao R^2: {formatar_numero(r2)}
Soma dos residuos: {soma_residuos:.12f}
Soma de x*residuo: {soma_x_residuos:.12f}
"""


def main() -> None:
    """Ponto de entrada do script."""
    print(executar_ajuste_linear())


if __name__ == "__main__":
    main()
