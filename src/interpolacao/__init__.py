"""Metodos de interpolacao polinomial."""

from .metodos import (
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

__all__ = [
    "TrechoSpline",
    "coeficientes_spline_cubica_natural",
    "coeficientes_spline_linear",
    "diferencas_divididas",
    "diferencas_finitas",
    "erro_maximo_nos_pontos",
    "gregory_newton",
    "lagrange",
    "ler_pontos_csv",
    "newton",
    "segundas_derivadas_spline_cubica_natural",
    "spline_cubica_natural",
    "spline_linear",
]
