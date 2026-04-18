import random

from tabuleiro import (
    clicar,
    contar_apagadas,
    criar_tabuleiro,
    meu_objetivo,
    gerar_vizinhos,
    imprimir_tabuleiro,
    medir,
    mostrar_fluxo_resolucao,
    verificar_corte,
)


def subir(tabuleiro_inicial, maximo_passos):
    atual = tabuleiro_inicial
    caminho = []

    for passos in range(maximo_passos):
        verificar_corte()
        if meu_objetivo(atual):
            return atual, caminho, passos, True

        h_atual = contar_apagadas(atual)
        melhor_h = h_atual
        melhor_viz = None
        melhor_acao = None

        for viz, acao in gerar_vizinhos(atual):
            h_viz = contar_apagadas(viz)
            if h_viz < melhor_h:
                melhor_h = h_viz
                melhor_viz = viz
                melhor_acao = acao

        if melhor_viz is None:
            return atual, caminho, passos, False

        atual = melhor_viz
        caminho.append(melhor_acao)

    return atual, caminho, maximo_passos, False


def hill_climbing(tabuleiro_inicial, numero_reinicios, maximo_passos, semente):
    random.seed(semente)
    n = len(tabuleiro_inicial)
    total_passos = 0
    partida = tabuleiro_inicial

    for tentativa in range(1, numero_reinicios + 1):
        _, caminho, passos, achou = subir(partida, maximo_passos)
        total_passos += passos

        if achou:
            return {
                "caminho": caminho,
                "numero_cliques": len(caminho),
                "nos_expandidos": total_passos,
                "encontrou": True,
                "reinicios": tentativa,
                "tabuleiro_partida": partida,
            }

        partida = tabuleiro_inicial
        for _ in range(random.randint(1, n * n)):
            partida = clicar(partida, random.randint(0, n - 1), random.randint(0, n - 1))

    return {
        "caminho": [],
        "numero_cliques": -1,
        "nos_expandidos": total_passos,
        "encontrou": False,
        "reinicios": numero_reinicios,
        "tabuleiro_partida": tabuleiro_inicial,
    }


def hill_climbing_com_reinicios(tabuleiro_inicial, numero_reinicios=30, maximo_passos=500, semente=42, tempo_max=60.0, memoria_max_mb=1024):
    return medir(hill_climbing, tabuleiro_inicial, numero_reinicios, maximo_passos, semente,
                 tempo_max=tempo_max, memoria_max_mb=memoria_max_mb)


if __name__ == "__main__":
    print("Teste do Hill Climbing com reinicios aleatorios - tabuleiro 3x3 apagado\n")
    inicial = criar_tabuleiro(3)
    imprimir_tabuleiro(inicial)

    r = hill_climbing_com_reinicios(inicial)
    print(f"Encontrou: {r['encontrou']}")
    print(f"Cliques: {r['numero_cliques']}")
    print(f"Passos totais: {r['nos_expandidos']}")
    print(f"Reinicios: {r['reinicios']}")
    print(f"Tempo: {r['tempo']:.4f}s")
    print(f"Memoria: {r['memoria_kb']:.2f} KB")
    print(f"Caminho: {r['caminho']}\n")

    if r["encontrou"]:
        partida = r["tabuleiro_partida"]
        if partida != inicial:
            print("Obs: o Hill Climbing fez reinicios aleatorios.")
            print("O fluxo abaixo parte do tabuleiro apos os cliques aleatorios.\n")
        mostrar_fluxo_resolucao(partida, r["caminho"])
