# Atividade 07

Evidenciar a execução do **Algoritmo do Banqueiro (Dijkstra)**, utilizando a linguagem Python para simular o gerenciamento e a alocação de recursos entre processos, referente à disciplina de Sistemas Operacionais (SO-262).

**Dupla:** Camilla Peixoto e Anderson Leite.

## Descrição

Nesta atividade foram realizadas as seguintes etapas:

* Execução do simulador do **Algoritmo do Banqueiro**, utilizando o código disponibilizado pelo professor;
* Análise das matrizes de alocação, necessidade máxima e recursos disponíveis no sistema;
* Verificação do estado inicial do sistema e identificação de uma sequência segura de execução dos processos;
* **Teste 01:** Verificação de um estado inicial seguro;
* **Teste 02:** Simulação de uma requisição válida e segura de recursos pelo processo P1;
* **Teste 03:** Verificação do bloqueio de uma requisição do processo P4 devido à insuficiência de recursos disponíveis;
* **Teste 04:** Identificação de um estado inseguro e execução do mecanismo de *rollback* para restaurar o estado original;
* **Teste 05:** Verificação da rejeição de uma requisição que ultrapassa a necessidade máxima declarada pelo processo P1;
* Registro das saídas geradas e das evidências de execução dos testes realizados.

As capturas de tela que evidenciam a execução dos cinco testes estão disponíveis na pasta `prints`, enquanto as saídas em texto estão armazenadas na pasta `resultados`. O código Python utilizado e o relatório com as explicações e os resultados de cada teste também estão disponíveis nesta pasta.