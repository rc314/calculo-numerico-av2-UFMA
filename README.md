# Cálculo Numérico - AV2

Aluno: Richard Christopher Lima Mendes  
Curso: Ciência da Computação  
Disciplina: Cálculo Numérico  
Professor: Lucas Reis  
Instituição: UFMA

Este repositório reúne o material da 2ª avaliação de Cálculo Numérico. O projeto
foi construído de forma incremental, com datasets, documentação, implementações
próprias dos métodos e testes automatizados.

## Regras principais

- Não usar bibliotecas prontas para cálculo numérico, como `numpy` ou `scipy`.
- Implementar os algoritmos usando lógica de programação, laços de repetição e
  estruturas de dados nativas.
- Manter o histórico de commits organizado, já que ele faz parte da avaliação.
- Separar bem datasets, código-fonte e documentação.

## Estrutura do repositório

- `datasets/`: arquivos CSV com os dados dos problemas da avaliação.
- `docs/`: resumo da avaliação, plano incremental e arquivo para registrar os resultados.
- `src/`: implementações dos métodos numéricos, separadas por assunto.

## Primeira etapa do desenvolvimento

A primeira etapa abordou interpolação polinomial, principalmente a ideia de
aproximar uma função a partir de pontos conhecidos. O primeiro problema implementado
foi o de altitude do drone, usando Lagrange e Newton.

Dataset inicial:

- `datasets/01_drone_altitude_interpolacao.csv`

Objetivo inicial:

- Interpolar a altitude no instante `x = 3.5 s`.

## Situação atual

As implementações atuais já contêm:

- Lagrange;
- Newton por diferenças divididas;
- Gregory-Newton por diferenças finitas;
- spline linear;
- spline cúbica natural;
- mínimos quadrados com ajuste linear, polinomial e modelos linearizados;
- regra 3/8 de Simpson;
- trapézios simples e repetidos;
- regra 1/3 de Simpson;
- quadratura de Gauss-Legendre com 1, 2 e 3 pontos.

Comandos principais:

```bash
python -m src.interpolacao.executar_interpolacao
python -m src.ajuste_curvas.executar_ajuste_curvas
python -m src.integracao.executar_integracao
python -m unittest discover -s tests -v
```

As saídas usadas para comprovar o funcionamento foram registradas em
`docs/resultados_codigo.txt`.
