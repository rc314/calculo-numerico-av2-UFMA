# Interpolação

Esta pasta reúne os métodos de interpolação da avaliação.

Implementações disponíveis:

- Lagrange;
- Newton por diferenças divididas;
- Gregory-Newton por diferenças finitas;
- spline linear;
- spline cúbica natural.

Comando principal:

```bash
python -m src.interpolacao.executar_interpolacao
```

Testes:

```bash
python -m unittest discover -s tests -v
```

Os métodos de integração numérica estão organizados separadamente em
`src/integracao/`.
