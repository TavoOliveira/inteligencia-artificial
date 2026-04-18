from tabuleiro import (
    criar_tabuleiro,
    meu_objetivo,
    gerar_vizinhos,
    imprimir_tabuleiro,
    medir,
    mostrar_fluxo_resolucao,
    verificar_corte,
)


def dfs(tabuleiro_inicial, limite_profundidade):
    if meu_objetivo(tabuleiro_inicial):
        return {"caminho": [], "numero_cliques": 0, "nos_expandidos": 0, "encontrou": True}

    pilha = [(tabuleiro_inicial, [])]
    visitados = {tabuleiro_inicial}
    nos = 0

    while pilha:
        verificar_corte()
        atual, caminho = pilha.pop()
        nos += 1
        if len(caminho) >= limite_profundidade:
            continue

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
            pilha.append((novo, novo_caminho))

    return {"caminho": [], "numero_cliques": -1, "nos_expandidos": nos, "encontrou": False}


def busca_profundidade(tabuleiro_inicial, limite_profundidade=20, tempo_max=60.0, memoria_max_mb=1024):
    return medir(dfs, tabuleiro_inicial, limite_profundidade,
                 tempo_max=tempo_max, memoria_max_mb=memoria_max_mb)


if __name__ == "__main__":
    print("Teste da Busca em Profundidade (DFS) - tabuleiro 3x3 apagado\n")
    inicial = criar_tabuleiro(3)
    imprimir_tabuleiro(inicial)

    r = busca_profundidade(inicial, limite_profundidade=15)
    print(f"Encontrou: {r['encontrou']}")
    print(f"Cliques: {r['numero_cliques']}")
    print(f"Nos expandidos: {r['nos_expandidos']}")
    print(f"Tempo: {r['tempo']:.4f}s")
    print(f"Memoria: {r['memoria_kb']:.2f} KB")
    print(f"Caminho: {r['caminho']}\n")

    if r["encontrou"]:
        mostrar_fluxo_resolucao(inicial, r["caminho"])
