# Interpolacao

Pasta para os metodos de interpolacao da avaliacao.

Implementacoes disponiveis:

- Lagrange;
- Newton por diferencas divididas;
- Gregory-Newton por diferencas finitas.

Comando principal:

```bash
python -m src.interpolacao.executar_interpolacao
```

Testes:

```bash
python -m unittest discover -s tests -v
```

Metodos que devem entrar depois:

- spline linear;
- spline cubica natural.
