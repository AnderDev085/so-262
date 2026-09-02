# Especificação de Projeto — Simulador de Gerenciamento de Processos

## 1. Introdução

Este documento apresenta a especificação de um simulador de gerenciamento de processos de um Sistema Operacional.

O objetivo do projeto é representar, de maneira simplificada, alguns dos principais conceitos relacionados ao gerenciamento de processos, escalonamento de CPU, transições de estados, operações de entrada e saída e interrupções de relógio.

O simulador será executado como um programa comum em modo usuário. Dessa forma, ele não será um Sistema Operacional real e não terá acesso direto ao hardware da máquina. Em vez disso, o programa irá simular o funcionamento de uma CPU e de alguns mecanismos existentes em um núcleo de Sistema Operacional.

O projeto deverá permitir a criação e execução de diferentes processos fictícios, possibilitando observar como eles são escalonados, bloqueados, interrompidos e finalizados durante a execução.

O escopo desta versão do simulador estará concentrado no gerenciamento de **processos**. Embora os conceitos estudados no capítulo também envolvam threads, threads individuais não serão simuladas nesta especificação.

---

# 2. Visão Geral e Arquitetura do Simulador

## 2.1 Objetivo do simulador

O simulador deverá representar o funcionamento básico de um gerenciador de processos.

Entre suas principais responsabilidades estarão:

- criar processos;
- armazenar informações sobre cada processo;
- controlar o estado atual dos processos;
- escolher qual processo utilizará a CPU;
- simular a execução dos processos;
- controlar interrupções de relógio;
- simular operações de entrada e saída;
- realizar trocas de contexto;
- finalizar processos;
- registrar todas as alterações realizadas durante a simulação;
- gerar estatísticas ao final da execução.

O simulador funcionará utilizando um relógio lógico.

Cada unidade desse relógio representará uma unidade de tempo da simulação.

Por exemplo:

```text
Tempo 0
Tempo 1
Tempo 2
Tempo 3
...

```

Essas unidades não precisam corresponder ao tempo real de execução do computador.

---

## 2.2 Componentes principais

O simulador deverá ser dividido conceitualmente nos seguintes componentes:

1. CPU virtual;
2. relógio lógico;
3. tabela de processos;
4. filas de processos;
5. escalonador;
6. gerenciador de entrada e saída;
7. gerenciador de interrupções;
8. sistema de logs e estatísticas.

O fluxo geral do sistema será:

```text
Arquivo de tarefas
        |
        v
Criação dos processos
        |
        v
Tabela de Processos
        |
        v
Fila de Prontos
        |
        v
Escalonador
        |
        v
CPU Virtual
   /         \
  v           v
E/S        Finalização
 |
 v
Fila de Bloqueados

```

---

# 3. CPU Virtual

O simulador deverá possuir uma representação simplificada de uma CPU.

A CPU virtual deverá armazenar informações referentes ao processo atualmente em execução.

A estrutura deverá possuir, no mínimo:

- identificador do processo em execução;
- contador de programa;
- registradores genéricos;
- quantidade de tempo executado no quantum atual;
- indicação de CPU livre ou ocupada.

Uma possível representação conceitual seria:

```c
CPU {
    pid_atual
    contador_programa
    registradores
    tempo_quantum
}

```

Não é necessário implementar instruções reais de uma arquitetura de processador.

Cada unidade de CPU representa apenas uma unidade fictícia de processamento.

---

# 4. Relógio Lógico

O simulador deverá utilizar um relógio lógico para controlar o avanço da simulação.

O relógio inicia no tempo:

```text
t = 0

```

A cada ciclo da simulação, o valor deverá aumentar em uma unidade:

```text
t = t + 1

```

O relógio será utilizado para:

- calcular o tempo de CPU;
- calcular o tempo de espera;
- controlar o quantum;
- determinar o término de operações de entrada e saída;
- registrar eventos;
- gerar o gráfico de Gantt;
- calcular as estatísticas finais.

---

# 5. Bloco de Controle de Processo — PCB

Cada processo deverá possuir um Bloco de Controle de Processo, chamado PCB, do inglês *Process Control Block*.

O PCB será responsável por armazenar todas as informações necessárias para controlar um processo.

## 5.1 Campos obrigatórios

Cada PCB deverá possuir, no mínimo:

| Campo                | Descrição                                        |
| -------------------- | ------------------------------------------------ |
| PID                  | Identificador textual único do processo (ex.: P1) |
| Estado               | Estado atual do processo                         |
| Prioridade           | Prioridade utilizada pelo escalonador            |
| Contador de Programa | Representa a posição atual da execução           |
| Registradores        | Valores fictícios armazenados durante a execução |
| Tempo de CPU         | Tempo total utilizado pela CPU                   |
| Tempo de Espera      | Tempo total aguardando na fila de prontos        |
| Tempo de Bloqueio    | Tempo utilizado em operações de E/S              |
| Quantum utilizado    | Tempo utilizado no quantum atual                 |
| Operação atual       | Operação que está sendo executada                |
| Índice da operação   | Posição atual dentro da sequência de operações   |
| Tempo restante       | Tempo restante da operação atual                 |

Uma possível representação seria:

```c
struct PCB {
    char pid[16];
    Estado estado;
    int prioridade;

    int pc;

    int registradores[4];

    int tempo_cpu;
    int tempo_espera;
    int tempo_bloqueado;

    int quantum_utilizado;

    int operacao_atual;
    int tempo_restante;
};

```

Nesta especificação, o PID será representado de forma textual, utilizando a letra `P` seguida de um número inteiro positivo, como `P1`, `P2` e `P3`. Isso mantém a identificação consistente no arquivo de tarefas, nos logs, na tabela de processos e no gráfico de Gantt.

A implementação final poderá utilizar estruturas diferentes, desde que todas as informações necessárias estejam presentes e a representação externa do PID permaneça consistente.

---

# 6. Tabela de Processos

O simulador deverá manter uma tabela contendo todos os processos existentes.

Essa tabela será utilizada para localizar rapidamente o PCB correspondente a cada processo.

Exemplo conceitual:

```text
Tabela de Processos

PID     Estado          Prioridade
1       PRONTO          2
2       EXECUTANDO      1
3       BLOQUEADO       3
4       PRONTO          2

```

Cada PID deverá ser único durante toda a execução do simulador.

Os processos finalizados poderão permanecer na tabela com o estado `TERMINADO`, permitindo posteriormente a geração das estatísticas.

---

# 7. Estados dos Processos

O simulador deverá trabalhar principalmente com os três estados clássicos de processos:

- PRONTO;
- EXECUTANDO;
- BLOQUEADO.

Também poderão ser utilizados os estados auxiliares:

- NOVO;
- TERMINADO.

## 7.1 Estado NOVO

Representa um processo que acabou de ser criado.

Após sua inicialização, deverá ocorrer a transição:

```text
NOVO -> PRONTO

```

---

## 7.2 Estado PRONTO

Representa um processo que está preparado para utilizar a CPU, porém ainda está aguardando sua vez.

Esses processos deverão permanecer na fila de prontos.

---

## 7.3 Estado EXECUTANDO

Representa o processo que está atualmente utilizando a CPU.

Como o simulador possui apenas uma CPU virtual, somente um processo poderá permanecer nesse estado por vez.

---

## 7.4 Estado BLOQUEADO

Representa um processo que está aguardando a conclusão de uma operação de entrada ou saída.

Enquanto estiver bloqueado, o processo não poderá utilizar a CPU.

---

## 7.5 Estado TERMINADO

Representa um processo que concluiu todas as suas operações ou executou uma chamada de término.

O processo não poderá retornar para nenhum outro estado depois de terminado.

---

# 8. Grafo de Transições de Estados

As principais transições serão:

```text
                  criação
                     |
                     v
                   NOVO
                     |
                     v
                  PRONTO
                     |
           escolhido pelo
             escalonador
                     |
                     v
                EXECUTANDO
                /    |    \
               /     |     \
     solicita E/S    |      \ finaliza
             /       |       \
            v        |        v
       BLOQUEADO     |    TERMINADO
            |        |
        E/S termina  |
            |        |
            v        |
          PRONTO <---+
               quantum
               expirou

```

---

# 9. Eventos e Transições

## 9.1 Criação de processo — simulação de `fork`

A criação de um processo representará, de maneira simplificada, o comportamento da chamada `fork` de um Sistema Operacional. O simulador **não** realizará uma cópia real do espaço de memória de um processo pai. A simulação de `fork` consistirá na criação de um novo PCB, atribuição de um PID único e inserção do novo processo no ciclo de vida do simulador.

Nesta versão, os processos serão descritos previamente no arquivo de tarefas e criados no início da simulação. Portanto, não será necessário incluir uma operação `FORK` na sequência de operações do arquivo de entrada.

Quando um processo for criado, será gerado um novo PID e um PCB correspondente.

Inicialmente:

```text
NOVO -> PRONTO

```

Em seguida, o processo deverá ser adicionado à fila de prontos.

---

## 9.2 Despacho de processo

Quando a CPU estiver disponível, o escalonador deverá selecionar um processo da fila de prontos.

A transição será:

```text
PRONTO -> EXECUTANDO

```

O estado da CPU deverá ser atualizado para indicar o processo selecionado.

---

## 9.3 Expiração do quantum

No algoritmo Round Robin, cada processo poderá utilizar a CPU durante uma quantidade máxima de tempo denominada quantum.

Por exemplo:

```text
quantum = 4

```

Se o processo ainda possuir trabalho a realizar após quatro unidades de CPU:

```text
EXECUTANDO -> PRONTO

```

Ele deverá ser colocado novamente ao final da fila de prontos.

---

## 9.4 Solicitação de Entrada/Saída

Quando um processo encontrar uma operação de entrada ou saída, deverá liberar a CPU.

A transição será:

```text
EXECUTANDO -> BLOQUEADO

```

O processo será inserido na lista ou fila de processos bloqueados.

---

## 9.5 Conclusão de Entrada/Saída

Cada operação de entrada e saída possuirá uma duração.

Quando essa duração terminar:

```text
BLOQUEADO -> PRONTO

```

O processo deverá retornar para a fila de prontos.

---

## 9.6 Término do processo

Quando todas as operações do processo forem concluídas:

```text
EXECUTANDO -> TERMINADO

```

O processo deverá liberar a CPU.

Seu PCB deverá permanecer disponível para o cálculo das estatísticas.

---

# 10. Troca de Contexto

Sempre que um processo deixar a CPU e outro processo assumir sua posição, deverá ser realizada uma troca de contexto.

Durante a troca de contexto, o simulador deverá:

1. salvar o contador de programa do processo atual;
2. salvar os valores dos registradores;
3. atualizar o PCB;
4. alterar o estado do processo anterior;
5. selecionar o próximo processo;
6. carregar os dados do novo processo;
7. atualizar o estado para `EXECUTANDO`.

A troca de contexto poderá ocorrer por:

- expiração do quantum;
- solicitação de E/S;
- término do processo;
- preempção provocada pelo escalonador de prioridade.

---

# 11. Escalonador de CPU

O simulador deverá possuir uma interface que permita utilizar diferentes algoritmos de escalonamento.

Serão implementados pelo menos dois algoritmos:

1. Round Robin;
2. Escalonamento por Prioridades.

O algoritmo poderá ser escolhido antes do início da simulação.

Exemplo:

```text
Algoritmo selecionado: ROUND_ROBIN

```

ou:

```text
Algoritmo selecionado: PRIORIDADE

```

---

# 12. Escalonamento Round Robin

O Round Robin deverá trabalhar com uma **fila circular de processos prontos**. O comportamento será circular: o processo será retirado do início da fila e, caso seu quantum expire antes de sua finalização ou bloqueio, será reinserido no final da fila.

A implementação poderá utilizar uma fila, deque ou outra estrutura equivalente, desde que preserve esse comportamento circular.

Exemplo:

```text
[P1] [P2] [P3]

```

O primeiro processo será escolhido:

```text
P1

```

Depois de utilizar seu quantum, caso ainda não tenha terminado, deverá retornar ao final da fila:

```text
[P2] [P3] [P1]

```

## 12.1 Quantum

O valor do quantum deverá ser configurável.

Exemplo:

```text
QUANTUM = 4

```

Um processo poderá utilizar no máximo quatro unidades consecutivas de CPU.

Caso termine ou solicite E/S antes do quantum acabar, a CPU deverá ser liberada imediatamente.

---

# 13. Escalonamento por Prioridade

Cada processo deverá possuir um valor de prioridade.

Neste projeto será adotada a seguinte convenção:

```text
menor número = maior prioridade

```

Exemplo:

```text
PID     Prioridade

P1          3
P2          1
P3          2

```

Nesse caso, a ordem de preferência será:

```text
P2 -> P3 -> P1

```

Caso dois processos possuam a mesma prioridade, deverá ser selecionado aquele que estiver esperando há mais tempo.

## 13.1 Comportamento preemptivo

O escalonamento por prioridade será **preemptivo**. Isso significa que, se um processo com prioridade superior à do processo atualmente em execução entrar na fila de prontos, o processo em execução deverá ser interrompido e retornar ao estado `PRONTO`.

Essa situação poderá ocorrer, por exemplo, quando:

- um processo de maior prioridade for criado;
- uma operação de E/S de um processo de maior prioridade for concluída;
- o mecanismo de aging elevar a prioridade de um processo que está aguardando.

A transição do processo preemptado será:

```text
EXECUTANDO -> PRONTO

```

Em seguida, o processo de maior prioridade será despachado para a CPU. Se as prioridades forem iguais, não ocorrerá preempção apenas por esse motivo; será mantido o processo que já está executando até que ele termine, bloqueie ou outra regra do algoritmo determine sua saída da CPU.

---

# 14. Prevenção de Starvation

O escalonamento por prioridade poderá causar starvation.

Starvation acontece quando um processo de baixa prioridade permanece aguardando por muito tempo enquanto processos de maior prioridade continuam sendo executados.

Para evitar esse problema, o simulador deverá utilizar o mecanismo de aging.

A cada determinado período de espera **na fila de prontos**, a prioridade de um processo poderá ser melhorada. O aging será aplicado somente aos processos no estado `PRONTO`; processos `EXECUTANDO`, `BLOQUEADO` ou `TERMINADO` não terão sua prioridade alterada por esse mecanismo.

Exemplo:

```text
Prioridade inicial = 5

```

Após determinado tempo aguardando:

```text
Prioridade = 4

```

Depois:

```text
Prioridade = 3

```

A prioridade mínima será:

```text
1

```

Dessa forma, um processo que aguarde por muito tempo eventualmente receberá prioridade suficiente para ser executado.

O intervalo de aging poderá ser configurável.

Exemplo:

```text
AGING_INTERVAL = 10

```

Isso significa que a prioridade poderá ser melhorada a cada dez unidades de espera.

---

# 15. Operações dos Processos

Cada processo será constituído por uma sequência de operações.

Inicialmente serão suportados os seguintes tipos:

```text
CPU
IO
EXIT

```

Uma sequência poderá ser:

```text
CPU 5
IO 3
CPU 4
EXIT

```

Isso significa:

1. utilizar a CPU durante 5 unidades;
2. realizar E/S durante 3 unidades;
3. utilizar a CPU durante mais 4 unidades;
4. terminar o processo.

---

# 16. Arquivo de Tarefas

O simulador deverá carregar seus processos a partir de um arquivo de texto.

Será utilizado um formato simples e legível.

Exemplo:

```text
P1 2 CPU:5 IO:3 CPU:4 EXIT
P2 1 CPU:8 EXIT
P3 3 CPU:2 IO:4 CPU:3 EXIT

```

O formato será:

```text
<PID> <PRIORIDADE> <OPERAÇÕES>

```

O campo `<PID>` deverá utilizar a forma `P` seguida de um número inteiro positivo, como `P1`, `P2` ou `P15`. Cada PID deverá ser único durante toda a simulação.

Exemplo:

```text
P1 2 CPU:5 IO:3 CPU:4 EXIT

```

Significa:

```text
Processo: P1
Prioridade: 2

CPU por 5 unidades
E/S por 3 unidades
CPU por 4 unidades
Finalização

```

---

# 17. Validação do Arquivo de Entrada

O simulador deverá detectar entradas inválidas.

Serão consideradas entradas inválidas:

- processo sem identificador;
- PID fora do formato definido;
- processo sem prioridade;
- operação desconhecida;
- duração igual ou inferior a zero;
- linha com formato incorreto;
- PID duplicado;
- ausência de operações.

Caso seja encontrado um erro, o simulador deverá informar:

```text
Erro na linha 3: operação inválida.

```

Sempre que possível, a mensagem deverá indicar o local e a causa do erro.

---

# 18. Regras Gerais da Simulação

Para evitar interpretações diferentes durante a implementação ou durante a geração de código por um Harness, serão adotadas as seguintes regras gerais:

1. Todos os processos descritos no arquivo de tarefas serão criados no tempo lógico `t = 0`, passando de `NOVO` para `PRONTO`.
2. A troca de contexto não consumirá unidades adicionais do relógio lógico nesta versão do simulador.
3. A cada unidade de tempo em que um processo permanecer no estado `EXECUTANDO`, seu tempo de CPU será incrementado em uma unidade e o tempo restante do surto de CPU atual será reduzido em uma unidade.
4. A cada unidade de tempo em que um processo permanecer no estado `PRONTO`, seu tempo total de espera será incrementado em uma unidade.
5. A cada unidade de tempo em que um processo permanecer no estado `BLOQUEADO`, seu tempo de bloqueio será incrementado em uma unidade e o tempo restante de sua operação de E/S será reduzido em uma unidade.
6. Nesta versão, as operações fictícias de E/S serão consideradas independentes entre si. Assim, mais de um processo poderá estar realizando E/S simultaneamente, sem disputa por um dispositivo físico específico.
7. Quando uma operação de E/S terminar, o processo deverá realizar a transição `BLOQUEADO -> PRONTO` e retornar à fila de prontos.
8. O valor de `quantum_utilizado` deverá ser zerado sempre que um processo deixar a CPU, seja por expiração do quantum, solicitação de E/S, término ou preempção por prioridade.
9. Quando nenhum processo estiver no estado `PRONTO`, a CPU permanecerá `IDLE`, mas o relógio lógico e as operações de E/S continuarão avançando normalmente.
10. No Round Robin, a preempção ocorrerá pela expiração do quantum. No escalonamento por prioridade, também poderá ocorrer preempção quando surgir um processo `PRONTO` com prioridade superior à do processo em execução.
11. Processos no estado `TERMINADO` não poderão retornar a nenhum outro estado e permanecerão disponíveis apenas para consulta e cálculo das estatísticas finais.

Essas regras constituem o comportamento padrão esperado do simulador e deverão ser preservadas independentemente da linguagem de programação escolhida.

---

# 19. Logs de Execução

O simulador deverá registrar os principais eventos ocorridos.

Cada evento deverá possuir o tempo lógico correspondente.

Exemplo:

```text
[t=0] Processo P1 criado.
[t=0] P1: NOVO -> PRONTO.
[t=0] P1: PRONTO -> EXECUTANDO.
[t=4] Quantum de P1 expirou.
[t=4] P1: EXECUTANDO -> PRONTO.
[t=4] P2: PRONTO -> EXECUTANDO.
[t=7] P2 solicitou operação de E/S.
[t=7] P2: EXECUTANDO -> BLOQUEADO.

```

Os logs deverão registrar pelo menos:

- criação de processo;
- início da execução;
- interrupção por quantum;
- operações de E/S;
- conclusão de E/S;
- alterações de prioridade;
- trocas de contexto;
- término dos processos.

---

# 20. Gráfico de Gantt

Ao final da simulação deverá ser apresentado um gráfico de Gantt textual representando a utilização da CPU.

Exemplo:

```text
Tempo: | 0 | 4 | 8 | 12 | 16 |

CPU:   |P1 |P2 |P3  |P1  |

```

Outra possibilidade será:

```text
0----4----8----12----16
| P1 | P2 | P3 | P1 |

```

Períodos em que nenhum processo estiver disponível para execução deverão ser identificados como `IDLE`.

Exemplo:

```text
| P1 | IDLE | P2 |

```

---

# 21. Estatísticas

Ao final da execução, o simulador deverá apresentar estatísticas globais e individuais.

## 21.1 Estatísticas individuais

Para cada processo deverão ser exibidos:

- PID;
- tempo total de CPU;
- tempo total de espera;
- tempo total bloqueado;
- tempo de conclusão;
- número de vezes em que utilizou a CPU;
- número de operações de E/S.

Exemplo:

```text
Processo P1

Tempo de CPU: 9
Tempo de espera: 6
Tempo bloqueado: 3
Tempo de conclusão: 18

```

---

## 21.2 Estatísticas globais

O simulador deverá apresentar:

- tempo total da simulação;
- tempo total de CPU ocupada;
- tempo total de CPU ociosa;
- utilização da CPU;
- número de processos executados;
- número de trocas de contexto;
- tempo médio de espera;
- tempo médio de conclusão.

A utilização da CPU deverá ser calculada por:

```text
Utilização da CPU =
Tempo de CPU ocupada / Tempo total da simulação

```

Multiplicado por 100 para obter o percentual.

---

# 22. Casos de Teste

O projeto deverá possuir diferentes casos de teste.

## 22.1 Teste 1 — Processo simples

Entrada:

```text
P1 1 CPU:5 EXIT

```

Objetivo:

Verificar se um único processo consegue ser criado, executado e finalizado corretamente.

Resultado esperado:

```text
P1: NOVO -> PRONTO
P1: PRONTO -> EXECUTANDO
P1: EXECUTANDO -> TERMINADO

```

---

## 22.2 Teste 2 — Round Robin

Configuração:

```text
Quantum = 2

```

Entrada:

```text
P1 1 CPU:5 EXIT
P2 1 CPU:4 EXIT

```

Comportamento esperado:

```text
P1 executa 2
P2 executa 2
P1 executa 2
P2 executa 2
P1 executa 1

```

O teste deverá verificar a correta rotação da fila de prontos.

---

## 22.3 Teste 3 — Entrada e Saída

Entrada:

```text
P1 1 CPU:2 IO:3 CPU:2 EXIT
P2 1 CPU:4 EXIT

```

Comportamento esperado:

1. P1 utiliza CPU;
2. P1 solicita E/S;
3. P1 passa para BLOQUEADO;
4. P2 utiliza a CPU;
5. após o término da E/S, P1 volta para PRONTO;
6. P1 volta a executar posteriormente.

---

# 23. Teste 4 — Prioridade

Entrada:

```text
P1 3 CPU:5 EXIT
P2 1 CPU:5 EXIT
P3 2 CPU:5 EXIT

```

Ordem esperada de preferência:

```text
P2
P3
P1

```

O teste deverá verificar se o escalonador sempre prioriza o processo com maior prioridade.

### Teste complementar de preempção por prioridade

Para verificar especificamente o comportamento preemptivo, poderá ser utilizada a seguinte entrada:

```text
P1 2 CPU:10 EXIT
P2 1 CPU:1 IO:3 CPU:2 EXIT

```

Comportamento esperado:

1. `P2`, por possuir maior prioridade, executa primeiro e depois solicita E/S;
2. enquanto `P2` está bloqueado, `P1` utiliza a CPU;
3. quando a E/S de `P2` termina, `P2` retorna ao estado `PRONTO`;
4. como `P2` possui prioridade superior à de `P1`, `P1` é preemptado;
5. ocorre `P1: EXECUTANDO -> PRONTO`;
6. `P2` volta a utilizar a CPU.

Esse caso deverá confirmar que a prioridade não é utilizada apenas no momento inicial do despacho, mas também pode provocar uma troca de contexto durante a execução.

---

# 24. Teste 5 — Aging

Entrada:

```text
P1 5 CPU:5 EXIT
P2 1 CPU:20 EXIT
P3 1 CPU:20 EXIT

```

O processo P1 começa com baixa prioridade.

O simulador deverá aumentar progressivamente sua prioridade conforme seu tempo de espera.

O teste deverá verificar se P1 consegue eventualmente utilizar a CPU, evitando starvation.

---

# 25. Teste 6 — CPU Ociosa

Entrada:

```text
P1 1 CPU:2 IO:5 CPU:2 EXIT

```

Após P1 solicitar E/S, nenhum outro processo estará pronto.

A CPU deverá permanecer ociosa.

O gráfico de Gantt deverá registrar esse período utilizando:

```text
IDLE

```

---

# 26. Estrutura Sugerida do Projeto

Uma possível organização do código seria:

```text
simulador/
|
|-- src/
|   |-- main
|   |-- cpu
|   |-- processo
|   |-- pcb
|   |-- scheduler
|   |-- round_robin
|   |-- prioridade
|   |-- io
|   |-- parser
|   |-- logger
|
|-- include/
|
|-- tarefas/
|   |-- teste1.txt
|   |-- teste2.txt
|   |-- teste3.txt
|
|-- README.md
|
|-- ESPECIFICACAO.md

```

A organização poderá variar de acordo com a linguagem de programação utilizada.

---

# 27. Requisitos Funcionais

O sistema deverá:

-  Ler um arquivo de tarefas;
-  Criar um PCB para cada processo;
-  simular a criação de processos de forma simplificada, representando o comportamento de `fork`;
-  armazenar os processos em uma tabela;
-  manter uma fila de processos prontos;
-  manter os processos bloqueados;
-  simular uma CPU;
-  possuir relógio lógico;
-  implementar Round Robin com comportamento de fila circular;
-  implementar escalonamento preemptivo por prioridade;
-  possuir mecanismo de aging;
-  simular operações de E/S;
-  realizar trocas de contexto;
-  registrar transições de estados;
-  gerar gráfico de Gantt;
-  calcular estatísticas;
-  detectar entradas inválidas.

---

# 28. Critérios de Aceitação

O projeto será considerado funcional quando:

1. os processos puderem ser carregados a partir de um arquivo;
2. cada processo possuir um PCB;
3. os estados forem atualizados corretamente;
4. apenas um processo utilizar a CPU por vez;
5. processos bloqueados não puderem utilizar a CPU;
6. processos cuja E/S terminou retornarem para a fila de prontos;
7. Round Robin respeitar o quantum e o comportamento circular da fila de prontos;
8. o escalonamento por prioridade respeitar as prioridades definidas e realizar preempção quando um processo de maior prioridade ficar pronto;
9. o aging impedir que processos permaneçam indefinidamente sem executar;
10. a criação de cada processo gerar um PID único e um PCB correspondente, representando a simulação simplificada de `fork`;
11. os processos terminados não retornarem para execução;
12. os logs representarem corretamente os eventos ocorridos;
13. o gráfico de Gantt representar a utilização da CPU;
14. as estatísticas finais serem calculadas corretamente;
15. os PIDs permanecerem consistentes entre arquivo de entrada, tabela de processos, logs e gráfico de Gantt.

---

# 29. Exemplo Completo de Execução

Arquivo:

```text
P1 2 CPU:4 IO:3 CPU:2 EXIT
P2 1 CPU:5 EXIT

```

Configuração:

```text
Algoritmo = ROUND_ROBIN
Quantum = 2

```

Possível sequência:

```text
[t=0] P1 criado.
[t=0] P2 criado.

[t=0] P1: NOVO -> PRONTO.
[t=0] P2: NOVO -> PRONTO.

[t=0] P1: PRONTO -> EXECUTANDO.

[t=2] Quantum de P1 expirou.
[t=2] P1: EXECUTANDO -> PRONTO.

[t=2] P2: PRONTO -> EXECUTANDO.

[t=4] Quantum de P2 expirou.
[t=4] P2: EXECUTANDO -> PRONTO.

[t=4] P1: PRONTO -> EXECUTANDO.

[t=6] P1 terminou seu primeiro surto de CPU.
[t=6] P1 solicitou E/S.
[t=6] P1: EXECUTANDO -> BLOQUEADO.

[t=6] P2: PRONTO -> EXECUTANDO.

```

A execução continuará até todos os processos atingirem o estado:

```text
TERMINADO

```

---

# 30. Considerações Finais

O simulador proposto tem como objetivo permitir a visualização prática dos principais conceitos relacionados ao gerenciamento de processos em Sistemas Operacionais.

Por meio do projeto será possível observar:

- criação e término de processos;
- funcionamento do PCB;
- filas de processos;
- escalonamento de CPU;
- Round Robin;
- escalonamento por prioridade;
- starvation;
- aging;
- interrupções;
- operações de entrada e saída;
- estados de processos;
- trocas de contexto;
- utilização da CPU.

A especificação foi desenvolvida de maneira independente da linguagem de programação e delimita seu escopo ao gerenciamento de processos, sem simulação individual de threads nesta versão.

Dessa forma, o documento poderá ser utilizado como entrada para ferramentas de geração de código através de Harness, como Claude Code ou Open Code, permitindo que a implementação seja desenvolvida posteriormente a partir dos requisitos apresentados neste documento.

---

# 31. Equipe

Componentes:

```text
Anderson de Oliveira Leite
Camilla Carvalhor Peixoto

```