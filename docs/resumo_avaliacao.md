# Resumo da avaliação 2

A 2ª avaliação de Cálculo Numérico será feita como um projeto em repositório no
GitHub. A entrega vai crescer aos poucos, acompanhando os conteúdos vistos em sala.

## O que o professor destacou

- O repositório deve ser incremental.
- Cada aula deve gerar uma nova parte do projeto.
- O histórico de commits faz parte da avaliação.
- A linguagem é livre.
- Não pode usar bibliotecas prontas de cálculo numérico, como `numpy` e `scipy`.
- O código deve mostrar o retorno da resposta do algoritmo.
- A organização do código também será avaliada.

## Problemas previstos

1. Interpolação por Lagrange e Newton usando o log de altitude de um drone.
2. Interpolação por Gregory-Newton usando temperaturas de um servidor.
3. Splines linear e cúbica natural para movimento de uma cortadora a laser.
4. Ajuste linear por mínimos quadrados para tráfego de rede no DEINF.
5. Integração por Newton-Cotes, regra 3/8 de Simpson, para transferência de dados.
6. Integração por trapézios repetidos e Simpson 1/3 para distância de um carro elétrico.
7. Quadratura de Gauss para calcular o trabalho total de uma curva de torque.

## Situação atual do repositório

O projeto contém os sete problemas previstos, organizados por assunto:

- datasets separados por problema;
- interpolação polinomial e splines;
- ajuste de curvas por mínimos quadrados;
- integração por Newton-Cotes e quadratura de Gauss;
- executores que exibem os cálculos e resultados;
- testes automatizados para conferir propriedades e valores conhecidos;
- resultados registrados em `docs/resultados_codigo.txt`.

Todos os algoritmos usam apenas estruturas nativas e a biblioteca padrão do Python.
