# Cálculo Numérico - AV2

Aluno: Richard Christopher Lima Mendes  
Curso: Ciência da Computação  
Disciplina: Cálculo Numérico  
Professor: Lucas Reis  
Instituição: UFMA

Este repositório reúne o material da 2ª avaliação de Cálculo Numérico. A atividade
será construída aos poucos, com os métodos sendo implementados conforme os assuntos
forem passados em sala.

Por enquanto, a estrutura inicial já está separada com datasets, documentação e
pastas para os códigos. A parte dos algoritmos fica para as próximas etapas, para
acompanhar a ordem das aulas e manter o histórico de commits organizado.

## Regras principais

- Não usar bibliotecas prontas para cálculo numérico, como `numpy` ou `scipy`.
- Implementar os algoritmos usando lógica de programação, laços de repetição e
  estruturas de dados nativas.
- Manter o histórico de commits organizado, já que ele faz parte da avaliação.
- Separar bem datasets, código-fonte e documentação.

## Estrutura do repositório

- `datasets/`: arquivos CSV com os dados dos problemas da avaliação.
- `docs/`: resumo da avaliação e plano incremental de implementação.
- `src/`: espaço reservado para os códigos dos métodos numéricos.

## Etapa inicial

O assunto visto até agora foi interpolação polinomial, principalmente a ideia de
aproximar uma função a partir de pontos conhecidos. Por isso, o primeiro código a
entrar no projeto deve ser o problema de altitude do drone, usando Lagrange e Newton.

Dataset inicial:

- `datasets/01_drone_altitude_interpolacao.csv`

Objetivo inicial:

- Interpolar a altitude no instante `x = 3.5 s`.

## Situação atual

O repositório ainda não contém as implementações dos métodos. A base está pronta
para receber os códigos conforme os conteúdos forem avançando nas aulas.
