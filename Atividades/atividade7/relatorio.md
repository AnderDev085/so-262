# Relatório de Execução — Atividade 07

**Disciplina:** Sistemas Operacionais (SO-262)  
**Tema:** Algoritmo do Banqueiro (Dijkstra)  
**Dupla:** Camilla Peixoto e Anderson Leite

## 1. Objetivo

Executar e analisar o Algoritmo do Banqueiro para demonstrar a identificação de estados seguros, a concessão de solicitações válidas, o bloqueio por falta de recursos e a rejeição de requisições que comprometeriam a segurança do sistema. Também foi incluído um teste para solicitações acima da necessidade declarada.

## 2. Ambiente e dados utilizados

O programa foi executado em Python 3, sem dependências externas. Os dados fornecidos pelo professor incluem cinco processos (P0 a P4) e três tipos de recursos (R0, R1 e R2), com vetor total `E = [10, 5, 7]`.

A soma dos recursos inicialmente alocados é `[7, 2, 5]`. Portanto, o vetor de recursos disponíveis inicial é `A = E - soma(C) = [3, 3, 2]`.

A necessidade restante de cada processo é calculada por `Need = Max - Allocation`:

| Processo | Allocation (C) | Max | Need |
|---|---|---|---|
| P0 | `[0, 1, 0]` | `[7, 5, 3]` | `[7, 4, 3]` |
| P1 | `[2, 0, 0]` | `[3, 2, 2]` | `[1, 2, 2]` |
| P2 | `[3, 0, 2]` | `[9, 0, 2]` | `[6, 0, 0]` |
| P3 | `[2, 1, 1]` | `[2, 2, 2]` | `[0, 1, 1]` |
| P4 | `[0, 0, 2]` | `[4, 3, 3]` | `[4, 3, 1]` |

## 3. Testes executados

### Teste 01 — Estado inicial seguro

**Objetivo:** verificar se existe uma sequência de execução capaz de concluir todos os processos, considerando o estado inicial.

**Execução:** `python3 testes.py 01`

**Saída observada:** o programa calculou `A = [3, 3, 2]`, identificou que o sistema está em estado **seguro** e exibiu a sequência `P1 -> P3 -> P0 -> P2 -> P4`.

**Explicação:** cada processo escolhido tem uma necessidade restante menor ou igual aos recursos temporariamente disponíveis. Ao simular sua conclusão, o algoritmo adiciona seus recursos alocados ao vetor de trabalho. Todos os cinco processos puderam ser concluídos.

**Evidências:** [saída em texto](resultados/teste-01.txt) · [print da execução](prints/teste-01.png)

### Teste 02 — Solicitação válida e segura de P1

**Objetivo:** verificar se a requisição `[1, 0, 2]` feita por P1 pode ser concedida.

**Execução:** `python3 testes.py 02`

**Saída observada:** a solicitação foi **concedida** e o estado permaneceu **seguro**. Os recursos disponíveis passaram de `[3, 3, 2]` para `[2, 3, 0]`. A alocação de P1 passou a `[3, 0, 2]` e sua necessidade restante a `[0, 2, 0]`.

**Explicação:** a requisição não ultrapassa a necessidade declarada nem a disponibilidade inicial. A simulação encontra uma sequência segura mesmo após a alocação provisória, autorizando a concessão definitiva.

**Evidências:** [saída em texto](resultados/teste-02.txt) · [print da execução](prints/teste-02.png)

### Teste 03 — Requisição bloqueada por recursos indisponíveis (caso original do professor)

**Objetivo:** reproduzir a segunda solicitação do exemplo do professor, depois da concessão do Teste 02.

**Execução:** `python3 testes.py 03`

**Saída observada:** P4 solicitou `[3, 3, 0]`, mas havia apenas `[2, 3, 0]` disponíveis. A resposta foi **PROCESSO BLOQUEADO**, porque, para o recurso R0, `3 > 2`. A requisição de P4 não alterou o estado do sistema.

**Explicação:** a solicitação está dentro da necessidade de P4, mas excede a disponibilidade atual. O algoritmo encerra o atendimento antes da alocação provisória, e P4 precisa aguardar.

**Evidências:** [saída em texto](resultados/teste-03.txt) · [print da execução](prints/teste-03.png)

### Teste 04 — Requisição que levaria a estado inseguro (caso complementar)

**Objetivo:** demonstrar uma solicitação que cabe nos recursos disponíveis, mas que não pode ser concedida por comprometer a segurança.

**Execução:** `python3 testes.py 04`

**Saída observada:** no estado inicial, P4 solicitou `[3, 3, 0]` e o algoritmo realizou uma **tentativa provisória**. O vetor disponível provisório passou a `[0, 0, 2]`. Nenhum processo conseguiu satisfazer sua necessidade restante nesse estado; o algoritmo apontou **ESTADO INSEGURO**, negou o pedido e realizou **rollback**, retornando o vetor disponível a `[3, 3, 2]`.

**Explicação:** ter recursos suficientes no momento não garante segurança. O Algoritmo do Banqueiro testa se a alocação deixaria uma sequência completa possível; como não deixou, ela foi desfeita. Um estado inseguro representa risco de deadlock, mas não significa necessariamente que já ocorreu um deadlock.

**Evidências:** [saída em texto](resultados/teste-04.txt) · [print da execução](prints/teste-04.png)

### Teste 05 — Solicitação acima da necessidade declarada

**Objetivo:** verificar a recusa de um pedido que excede a necessidade restante do processo.

**Execução:** `python3 testes.py 05`

**Saída observada:** P1 solicitou `[2, 0, 0]`, embora sua necessidade restante fosse `[1, 2, 2]`. O pedido foi **negado**, porque, em R0, `2 > 1`, sem modificar o estado do sistema.

**Explicação:** o algoritmo verifica primeiro se a requisição respeita a necessidade máxima declarada. Como essa condição foi violada, não há tentativa provisória de alocação.

**Evidências:** [saída em texto](resultados/teste-05.txt) · [print da execução](prints/teste-05.png)

## 4. Síntese dos resultados

| Teste | Resultado | Efeito da operação testada |
|---|---|---|
| 01 | Estado inicial seguro | Nenhuma alteração permanente |
| 02 | Requisição concedida | Recursos alocados a P1 |
| 03 | P4 bloqueado | Pedido de P4 não altera o estado |
| 04 | Estado inseguro | Estado restaurado após rollback |
| 05 | Requisição acima de Need | Pedido negado sem alterações |

## 5. Conclusão

Os testes demonstraram que o Algoritmo do Banqueiro considera não apenas a quantidade de recursos disponíveis, mas também a possibilidade de concluir todos os processos sem perder a segurança. Uma requisição pode ser aceita (Teste 02), aguardar devido à falta de disponibilidade (Teste 03), ser negada porque geraria um estado inseguro (Teste 04), ou ser rejeitada imediatamente por exceder a necessidade declarada (Teste 05). Os testes confirmam ainda que solicitações negadas não devem modificar permanentemente a alocação.

A diferença entre os Testes 03 e 04 é especialmente importante: uma mesma requisição de P4 tem resultados distintos conforme o estado inicial considerado. Essa distinção esclarece o comportamento do código fornecido pelo professor.

## 6. Referência

TANENBAUM, Andrew S.; BOS, Herbert. *Sistemas Operacionais Modernos*. Capítulo 6, conforme material de aula indicado pelo professor.

---

**Dupla:** Camilla Peixoto e Anderson Leite