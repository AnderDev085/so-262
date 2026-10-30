#!/usr/bin/env python3
"""Testes individuais da Atividade 07 - Camilla Peixoto e Anderson Leite."""

import argparse
import copy
import io
from contextlib import redirect_stdout

from banqueiro import BankersAlgorithm


DUPLA = "Camilla Peixoto e Anderson Leite"


def criar_sistema():
    """Devolve um sistema novo, para que os testes sejam independentes."""
    processos = ["P0", "P1", "P2", "P3", "P4"]
    recursos_totais = [10, 5, 7]
    alocacao = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2],
    ]
    maximo = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3],
    ]
    return BankersAlgorithm(processos, recursos_totais, alocacao, maximo)


def estado_snapshot(banqueiro):
    return (
        list(banqueiro.available),
        copy.deepcopy(banqueiro.allocation),
        copy.deepcopy(banqueiro.need),
    )


def cabecalho(numero, descricao):
    print("=" * 74)
    print("ATIVIDADE 07 - ALGORITMO DO BANQUEIRO")
    print(f"DUPLA: {DUPLA}")
    print(f"TESTE {numero} - {descricao}")
    print("=" * 74)


def rodape():
    print("\n" + "=" * 74)
    print(f"EXECUÇÃO CONCLUÍDA - DUPLA: {DUPLA}")
    print("=" * 74)


def teste_01():
    """Confere disponibilidade e sequência segura do estado inicial."""
    cabecalho("01", "Estado inicial seguro")
    banco = criar_sistema()
    banco.display_state()
    seguro, sequencia = banco.is_safe_state(verbose=True)
    assert banco.available == [3, 3, 2]
    assert seguro is True
    assert sequencia == ["P1", "P3", "P0", "P2", "P4"]
    print("RESULTADO DO TESTE 01: APROVADO - Estado inicial seguro.")
    rodape()


def teste_02():
    """Confere a concessão de [1,0,2] a P1 e a nova disponibilidade."""
    cabecalho("02", "Requisição válida e segura de P1")
    banco = criar_sistema()
    concedida = banco.request_resources(1, [1, 0, 2])
    banco.display_state()
    assert concedida is True
    assert banco.available == [2, 3, 0]
    assert banco.allocation[1] == [3, 0, 2]
    assert banco.need[1] == [0, 2, 0]
    print("RESULTADO DO TESTE 02: APROVADO - Solicitação concedida a P1.")
    rodape()


def teste_03():
    """Repete o segundo pedido do professor, após o pedido aceito de P1."""
    cabecalho("03", "Requisição de P4 após P1: recursos indisponíveis")
    banco = criar_sistema()

    # Prepara o estado da demonstração original, sem poluir o print com outra execução.
    with redirect_stdout(io.StringIO()):
        concedida_p1 = banco.request_resources(1, [1, 0, 2])
    assert concedida_p1 is True
    print("PREPARAÇÃO: P1 recebeu [1, 0, 2], conforme o teste anterior.")
    print(f"Recursos disponíveis antes do pedido de P4: {banco.available}")
    antes = estado_snapshot(banco)
    concedida_p4 = banco.request_resources(4, [3, 3, 0])
    print(f"Recursos disponíveis após o pedido de P4: {banco.available}")
    assert concedida_p4 is False
    assert estado_snapshot(banco) == antes
    print("RESULTADO DO TESTE 03: APROVADO - P4 aguarda por falta do recurso R0.")
    rodape()


def teste_04():
    """Mostra um pedido disponível inicialmente, mas que torna o estado inseguro."""
    cabecalho("04", "Requisição de P4 em estado inseguro: rollback")
    banco = criar_sistema()
    print(f"Recursos disponíveis antes do pedido: {banco.available}")
    antes = estado_snapshot(banco)
    concedida = banco.request_resources(4, [3, 3, 0])
    print(f"Recursos disponíveis após o rollback: {banco.available}")
    assert concedida is False
    assert estado_snapshot(banco) == antes
    print("RESULTADO DO TESTE 04: APROVADO - Pedido negado; estado original restaurado.")
    rodape()


def teste_05():
    """Confere a recusa de um pedido acima da necessidade declarada."""
    cabecalho("05", "Requisição acima da necessidade máxima de P1")
    banco = criar_sistema()
    print(f"Necessidade inicial de P1: {banco.need[1]}")
    antes = estado_snapshot(banco)
    concedida = banco.request_resources(1, [2, 0, 0])
    assert concedida is False
    assert estado_snapshot(banco) == antes
    print("RESULTADO DO TESTE 05: APROVADO - Pedido acima de Need negado.")
    rodape()


TESTES = {
    "01": teste_01,
    "02": teste_02,
    "03": teste_03,
    "04": teste_04,
    "05": teste_05,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Executa um teste da Atividade 07.")
    parser.add_argument("teste", choices=[*TESTES, "todos"], help="01, 02, 03, 04, 05 ou todos")
    args = parser.parse_args()
    if args.teste == "todos":
        for funcao in TESTES.values():
            funcao()
            print()
    else:
        TESTES[args.teste]()
