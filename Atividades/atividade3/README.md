# Atividade 03
Elaborar a especificação de projeto de um gerenciador de processos para um simulador de Sistema Operacional, com base nos conceitos de gerenciamento de processos e threads abordados na disciplina de Sistemas Operacionais (SO-262).
## Descrição
Nesta atividade foram realizadas as seguintes etapas:
* Definição da visão geral e da arquitetura do simulador, considerando uma CPU virtual com registradores básicos, contador de programa e relógio lógico;
* Especificação do Bloco de Controle de Processo (PCB) e da tabela de processos, contendo informações como PID, estado atual, registradores, prioridade, tempo de CPU e tempo de espera;
* Modelagem do ciclo de vida dos processos e das transições entre os estados Pronto, Em Execução e Bloqueado;
* Definição das transições provocadas pela criação de processos, expiração de quantum, solicitações e conclusões de operações de entrada/saída e término de processos;
* Especificação de dois algoritmos de escalonamento de CPU: Round Robin e escalonamento por prioridades;
* Definição de mecanismos para prevenção de inanição (starvation) no escalonamento por prioridades;
* Definição do formato do arquivo de tarefas utilizado como entrada do simulador;
* Especificação das saídas esperadas, incluindo logs de transições de estados, gráficos de Gantt textuais e estatísticas de utilização da CPU;
* Definição de casos de teste para validar o funcionamento do simulador;
* Organização da especificação em formato Markdown para posterior utilização como entrada na geração do código por meio de um Harness, como Claude Code ou Open Code.
A especificação completa do projeto está disponível nesta pasta.