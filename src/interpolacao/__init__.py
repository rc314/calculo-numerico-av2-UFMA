"""Metodos de interpolacao polinomial."""

from .metodos import (
    diferencas_divididas,
    diferencas_finitas,
    erro_maximo_nos_pontos,
    gregory_newton,
    lagrange,
    ler_pontos_csv,
    newton,
)

__all__ = [
    "diferencas_divididas",
    "diferencas_finitas",
    "erro_maximo_nos_pontos",
    "gregory_newton",
    "lagrange",
    "ler_pontos_csv",
    "newton",
]
