# Ajuste de curvas

Metodos implementados:

- minimos quadrados com funcoes base gerais;
- ajuste linear `P1(x) = a*x + b`;
- ajuste polinomial;
- regressao exponencial linearizada;
- regressao hiperbolica linearizada;
- regressao geometrica linearizada.

Dataset principal:

- `datasets/04_trafego_rede_mmq.csv`

Objetivo do exemplo:

- encontrar a reta `P1(x) = ax + b`;
- prever o trafego para `x = 13 h`.

Comando principal:

```bash
python -m src.ajuste_curvas.executar_ajuste_curvas
```

Testes:

```bash
python -m unittest discover -s tests -v
```
