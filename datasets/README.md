# Datasets da AV2

Os arquivos desta pasta foram montados a partir dos dados do PDF da avaliação.
Cada dataset guarda só as entradas do problema, evitando copiar valores direto do
enunciado na hora de programar.

| Arquivo | Tema | O que calcular |
| --- | --- | --- |
| `01_drone_altitude_interpolacao.csv` | Interpolação por Lagrange e Newton | Altitude em `x = 3.5 s` |
| `02_servidor_temperatura_gregory_newton.csv` | Gregory-Newton | Temperatura no minuto `25` |
| `03_laser_splines.csv` | Splines linear e cúbica natural | Posição em `t = 1.5 s` |
| `04_trafego_rede_mmq.csv` | Mínimos quadrados | Reta de tendência e previsão para `x = 13 h` |
| `05_transferencia_simpson_3_8.csv` | Newton-Cotes, regra 3/8 de Simpson | Total transferido em MB |
| `06_carro_eletrico_integracao.csv` | Trapézios repetidos e Simpson 1/3 | Distância total percorrida |
| `07_torque_motor_gauss.csv` | Quadratura de Gauss | Integral de `f(x) = 5x^3 + x^2 - 12x + 4` em `[-1, 1]` |

O arquivo `metadados_av2.csv` funciona como um índice simples dos problemas.

## Padrão usado

- Nomes das colunas em português, com unidades quando faz sentido.
- Valores numéricos com ponto decimal para facilitar a leitura pelo código.
- Um arquivo por problema, para evitar misturar assuntos diferentes.
