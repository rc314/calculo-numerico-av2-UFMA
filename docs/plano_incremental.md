# Plano incremental

Este plano serve para manter o projeto organizado e facilitar os commits da AV2.
Como a avaliação leva em conta o histórico do GitHub, o ideal é fazer commits
pequenos, cada um com um método ou avanço bem definido.

## Sequência sugerida

- [x] Organizar estrutura inicial do repositório, datasets e documentação.
- [ ] Implementar interpolação por Lagrange para o dataset do drone.
- [ ] Implementar interpolação por Newton para o dataset do drone.
- [ ] Implementar Gregory-Newton para pontos igualmente espaçados.
- [ ] Implementar spline linear.
- [ ] Implementar spline cúbica natural.
- [ ] Implementar ajuste linear por mínimos quadrados.
- [ ] Implementar regra 3/8 de Simpson.
- [ ] Implementar trapézios repetidos.
- [ ] Implementar regra 1/3 de Simpson.
- [ ] Implementar quadratura de Gauss para `n = 2` e `n = 3`.
- [ ] Registrar as saídas dos códigos em `docs/resultados_codigo.txt`.
- [ ] Revisar README, exemplos de execução e resultados finais.

## Organização dos commits

Sugestões de mensagens:

- `docs: organiza estrutura inicial da av2`
- `feat: implementa interpolacao de lagrange`
- `feat: implementa interpolacao de newton`
- `feat: implementa gregory newton`
- `feat: implementa splines`
- `feat: implementa ajuste linear por mmq`
- `feat: implementa integracao numerica`
- `docs: adiciona resultados finais da av2`

## Cuidados

- Conferir os resultados com contas manuais ou exemplos pequenos.
- Evitar misturar vários métodos no mesmo commit.
- Não adicionar bibliotecas externas sem necessidade.
- Deixar claro no README como executar cada parte do projeto.
