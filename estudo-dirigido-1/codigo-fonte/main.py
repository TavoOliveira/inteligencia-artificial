from tabuleiro import criar_tabuleiro
from bfs import busca_largura
from dfs import busca_profundidade
from guloso import busca_gulosa
from a_estrela import busca_a_estrela
from hill_climbing import hill_climbing_com_reinicios


TAMANHOS = [2, 3, 5, 7]
TEMPO_MAX_S = 600.0
MEMORIA_MAX_MB = 4096
EXECUCOES_HC = 10

CORTE = {"tempo_max": TEMPO_MAX_S, "memoria_max_mb": MEMORIA_MAX_MB}


def imprimir_linha(nome, r):
    if r.get("corte"):
        print(f"  {nome:<16} | CORTE  | {r['corte']:<15} | "
              f"t={r['tempo']:.2f}s  mem_pico={r['memoria_kb']:.0f}KB")
        return
    achou = "Sim" if r["encontrou"] else "Nao"
    print(f"  {nome:<16} | {achou:<6} | {r['numero_cliques']:<7} | "
          f"{r['nos_expandidos']:<8} | {r['tempo']:<9.4f} | {r['memoria_kb']:<9.2f}")


def rodar_deterministicos(tabuleiro):
    print(f"  {'Algoritmo':<16} | {'Achou?':<6} | {'Cliques':<7} | "
          f"{'Nos exp.':<8} | {'Tempo(s)':<9} | {'Mem(KB)':<9}")
    print("  " + "-" * 72)
    imprimir_linha("BFS",           busca_largura(tabuleiro, **CORTE))
    imprimir_linha("DFS",           busca_profundidade(tabuleiro, limite_profundidade=15, **CORTE))
    imprimir_linha("Gulosa",        busca_gulosa(tabuleiro, **CORTE))
    imprimir_linha("A*",            busca_a_estrela(tabuleiro, **CORTE))
    imprimir_linha("Hill Climbing", hill_climbing_com_reinicios(tabuleiro, **CORTE))


def rodar_bulk_hc(tabuleiro, execucoes):
    sucessos = 0
    cortados = 0
    tempos = []
    cliques_ok = []

    for i in range(execucoes):
        r = hill_climbing_com_reinicios(tabuleiro, semente=100 + i, **CORTE)
        tempos.append(r["tempo"])
        if r.get("corte"):
            cortados += 1
        elif r["encontrou"]:
            sucessos += 1
            cliques_ok.append(r["numero_cliques"])

    taxa = sucessos * 100 // execucoes
    t_min, t_med, t_max = min(tempos), sum(tempos) / len(tempos), max(tempos)

    if cliques_ok:
        c_str = f"{min(cliques_ok)}/{sum(cliques_ok)/len(cliques_ok):.1f}/{max(cliques_ok)}"
    else:
        c_str = "-"

    linha_resumo = f"  Execucoes: {execucoes}  |  Sucessos: {sucessos}  |  Taxa: {taxa}%"
    if cortados > 0:
        linha_resumo += f"  |  Cortados: {cortados}"
    print(linha_resumo)
    print(f"  Cliques (min/med/max): {c_str}")
    print(f"  Tempo   (min/med/max): {t_min:.4f} / {t_med:.4f} / {t_max:.4f} s")


def rodar_cenario(tamanho):
    tabuleiro = criar_tabuleiro(tamanho)
    titulo = f" Tabuleiro {tamanho}x{tamanho} "
    print("=" * 78)
    print(titulo.center(78, "="))
    print("=" * 78)

    print("\n[1] Algoritmos deterministicos (1 execucao cada)")
    rodar_deterministicos(tabuleiro)

    print(f"\n[2] Hill Climbing estocastico ({EXECUCOES_HC} execucoes com sementes distintas)")
    rodar_bulk_hc(tabuleiro, EXECUCOES_HC)
    print()


if __name__ == "__main__":
    print(f"Criterios de corte: tempo_max = {TEMPO_MAX_S:.0f}s | memoria_max = {MEMORIA_MAX_MB} MB")
    print()
    for tamanho in TAMANHOS:
        rodar_cenario(tamanho)
    print("=" * 78)
    print(" Experimentos finalizados ".center(78, "="))
    print("=" * 78)
