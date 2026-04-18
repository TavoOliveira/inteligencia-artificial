import heapq

from tabuleiro import (
    contar_apagadas,
    criar_tabuleiro,
    meu_objetivo,
    gerar_vizinhos,
    imprimir_tabuleiro,
    medir,
    mostrar_fluxo_resolucao,
    verificar_corte,
)


def gulosa(tabuleiro_inicial):
    if meu_objetivo(tabuleiro_inicial):
        return {"caminho": [], "numero_cliques": 0, "nos_expandidos": 0, "encontrou": True}

    contador = 0
    fila = [(contar_apagadas(tabuleiro_inicial), contador, tabuleiro_inicial, [])]
    visitados = {tabuleiro_inicial}
    nos = 0

    while fila:
        verificar_corte()
        _, _, atual, caminho = heapq.heappop(fila)
        nos += 1

        if meu_objetivo(atual):
            return {
                "caminho": caminho,
                "numero_cliques": len(caminho),
                "nos_expandidos": nos,
                "encontrou": True,
            }

        for novo, acao in gerar_vizinhos(atual):
            if novo in visitados:
                continue
            visitados.add(novo)
            contador += 1
            heapq.heappush(fila, (contar_apagadas(novo), contador, novo, caminho + [acao]))

    return {"caminho": [], "numero_cliques": -1, "nos_expandidos": nos, "encontrou": False}


def busca_gulosa(tabuleiro_inicial, tempo_max=60.0, memoria_max_mb=1024):
    return medir(gulosa, tabuleiro_inicial, tempo_max=tempo_max, memoria_max_mb=memoria_max_mb)


if __name__ == "__main__":
    print("Teste da Busca Gulosa - tabuleiro 3x3 apagado\n")
    inicial = criar_tabuleiro(3)
    imprimir_tabuleiro(inicial)

    r = busca_gulosa(inicial)
    print(f"Encontrou: {r['encontrou']}")
    print(f"Cliques: {r['numero_cliques']}")
    print(f"Nos expandidos: {r['nos_expandidos']}")
    print(f"Tempo: {r['tempo']:.4f}s")
    print(f"Memoria: {r['memoria_kb']:.2f} KB")
    print(f"Caminho: {r['caminho']}\n")

    if r["encontrou"]:
        mostrar_fluxo_resolucao(inicial, r["caminho"])
