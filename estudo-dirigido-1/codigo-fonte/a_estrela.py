import heapq

from tabuleiro import (
    criar_tabuleiro,
    meu_objetivo,
    gerar_vizinhos,
    imprimir_tabuleiro,
    medir,
    mostrar_fluxo_resolucao,
    verificar_corte,
)


def heuristica(tabuleiro):
    n = len(tabuleiro)
    apagadas_pos = [(i, j) for i in range(n) for j in range(n) if tabuleiro[i][j] == 0]
    a = len(apagadas_pos)
    if a == 0:
        return 0

    bound1 = (a + 4) // 5

    independentes = []
    for p in apagadas_pos:
        if all((abs(p[0] - q[0]) + abs(p[1] - q[1])) > 2 for q in independentes):
            independentes.append(p)
    bound2 = len(independentes)

    return max(bound1, bound2)


def a_estrela(tabuleiro_inicial):
    if meu_objetivo(tabuleiro_inicial):
        return {"caminho": [], "numero_cliques": 0, "nos_expandidos": 0, "encontrou": True}

    contador = 0
    fila = [(heuristica(tabuleiro_inicial), contador, 0, tabuleiro_inicial, [])]
    melhor_g = {tabuleiro_inicial: 0}
    nos = 0

    while fila:
        verificar_corte()
        _, _, g, atual, caminho = heapq.heappop(fila)
        nos += 1

        if meu_objetivo(atual):
            return {
                "caminho": caminho,
                "numero_cliques": len(caminho),
                "nos_expandidos": nos,
                "encontrou": True,
            }

        if g > melhor_g.get(atual, g):
            continue

        for novo, acao in gerar_vizinhos(atual):
            novo_g = g + 1
            if novo_g < melhor_g.get(novo, 10**9):
                melhor_g[novo] = novo_g
                contador += 1
                f = novo_g + heuristica(novo)
                heapq.heappush(fila, (f, contador, novo_g, novo, caminho + [acao]))

    return {"caminho": [], "numero_cliques": -1, "nos_expandidos": nos, "encontrou": False}


def busca_a_estrela(tabuleiro_inicial, tempo_max=60.0, memoria_max_mb=1024):
    return medir(a_estrela, tabuleiro_inicial, tempo_max=tempo_max, memoria_max_mb=memoria_max_mb)


if __name__ == "__main__":
    print("Teste do Algoritmo A* - tabuleiro 3x3 apagado\n")
    inicial = criar_tabuleiro(3)
    imprimir_tabuleiro(inicial)

    r = busca_a_estrela(inicial)
    print(f"Encontrou: {r['encontrou']}")
    print(f"Cliques: {r['numero_cliques']}")
    print(f"Nos expandidos: {r['nos_expandidos']}")
    print(f"Tempo: {r['tempo']:.4f}s")
    print(f"Memoria: {r['memoria_kb']:.2f} KB")
    print(f"Caminho: {r['caminho']}\n")

    if r["encontrou"]:
        mostrar_fluxo_resolucao(inicial, r["caminho"])
