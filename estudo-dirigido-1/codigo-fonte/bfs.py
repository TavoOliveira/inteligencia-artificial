from collections import deque

from tabuleiro import (
    criar_tabuleiro,
    meu_objetivo,
    gerar_vizinhos,
    imprimir_tabuleiro,
    medir,
    mostrar_fluxo_resolucao,
    verificar_corte,
)


def bfs(tabuleiro_inicial):
    if meu_objetivo(tabuleiro_inicial):
        return {"caminho": [], "numero_cliques": 0, "nos_expandidos": 0, "encontrou": True}

    fila = deque([(tabuleiro_inicial, [])])
    visitados = {tabuleiro_inicial}
    nos = 0

    while fila:
        verificar_corte()
        atual, caminho = fila.popleft()
        nos += 1
        for novo, acao in gerar_vizinhos(atual):
            if novo in visitados:
                continue
            novo_caminho = caminho + [acao]
            if meu_objetivo(novo):
                return {
                    "caminho": novo_caminho,
                    "numero_cliques": len(novo_caminho),
                    "nos_expandidos": nos,
                    "encontrou": True,
                }
            visitados.add(novo)
            fila.append((novo, novo_caminho))

    return {"caminho": [], "numero_cliques": -1, "nos_expandidos": nos, "encontrou": False}


def busca_largura(tabuleiro_inicial, tempo_max=60.0, memoria_max_mb=1024):
    return medir(bfs, tabuleiro_inicial, tempo_max=tempo_max, memoria_max_mb=memoria_max_mb)


if __name__ == "__main__":
    print("Teste da Busca em Largura (BFS) - tabuleiro 3x3 apagado\n")
    inicial = criar_tabuleiro(3)
    imprimir_tabuleiro(inicial)

    r = busca_largura(inicial)
    print(f"Encontrou: {r['encontrou']}")
    print(f"Cliques: {r['numero_cliques']}")
    print(f"Nos expandidos: {r['nos_expandidos']}")
    print(f"Tempo: {r['tempo']:.4f}s")
    print(f"Memoria: {r['memoria_kb']:.2f} KB")
    print(f"Caminho: {r['caminho']}\n")

    if r["encontrou"]:
        mostrar_fluxo_resolucao(inicial, r["caminho"])
