# Integração numérica

Esta pasta reúne as implementações de integração numérica da AV2. Todas as
fórmulas foram programadas diretamente com a biblioteca padrão do Python, sem
NumPy ou SciPy.

## Métodos implementados

- regra do trapézio simples;
- regra dos trapézios repetidos;
- regra 1/3 de Simpson simples e repetida;
- regra 3/8 de Simpson simples e repetida;
- quadratura de Gauss-Legendre com 1, 2 e 3 pontos;
- transformação automática de um intervalo `[a, b]` para `[-1, 1]` em Gauss.

As regras de Newton-Cotes podem receber uma função ou uma tabela de pontos
igualmente espaçados. As funções validam as restrições de cada método: Simpson
1/3 exige número par de subintervalos e Simpson 3/8 exige múltiplo de três.

## Datasets utilizados

- `datasets/05_transferencia_simpson_3_8.csv`;
- `datasets/06_carro_eletrico_integracao.csv`;
- `datasets/07_torque_motor_gauss.csv`.

## Execução

Na raiz do projeto:

```bash
python -m src.integracao.executar_integracao
python -m unittest discover -s tests -p "test_integracao.py" -v
```

O executor mostra os pontos, o passo, o resultado de cada dataset e conferências
com integrais analíticas conhecidas.
