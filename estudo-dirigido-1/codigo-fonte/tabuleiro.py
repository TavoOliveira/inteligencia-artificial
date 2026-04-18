import time
import tracemalloc


def criar_tabuleiro(n):
    return tuple((0,) * n for _ in range(n))


def clicar(tabuleiro, linha, coluna):
    n = len(tabuleiro)
    novo = [list(l) for l in tabuleiro]
    vizinhos = [
        (linha, coluna),
        (linha - 1, coluna), (linha + 1, coluna),
        (linha, coluna - 1), (linha, coluna + 1),
    ]
    for li, co in vizinhos:
        if 0 <= li < n and 0 <= co < n:
            novo[li][co] = 1 - novo[li][co]
    return tuple(tuple(l) for l in novo)


def meu_objetivo(tabuleiro):
    return all(0 not in linha for linha in tabuleiro)


def gerar_vizinhos(tabuleiro):
    n = len(tabuleiro)
    return [(clicar(tabuleiro, i, j), (i, j)) for i in range(n) for j in range(n)]


def contar_apagadas(tabuleiro):
    return sum(linha.count(0) for linha in tabuleiro)


class CorteExcedido(Exception):
    def __init__(self, motivo):
        self.motivo = motivo
        super().__init__(motivo)


corte_inicio = None
corte_tempo_max = None
corte_memoria_max_bytes = None
corte_contador = 0


def verificar_corte():
    global corte_contador
    corte_contador += 1
    if corte_contador % 500 != 0:
        return
    if corte_inicio is None:
        return
    if corte_tempo_max is not None:
        if time.time() - corte_inicio > corte_tempo_max:
            raise CorteExcedido(f"tempo > {corte_tempo_max:.0f}s")
    if corte_memoria_max_bytes is not None and tracemalloc.is_tracing():
        memoria_atual, _ = tracemalloc.get_traced_memory()
        if memoria_atual > corte_memoria_max_bytes:
            mb = corte_memoria_max_bytes // (1024 * 1024)
            raise CorteExcedido(f"memoria > {mb}MB")


def medir(funcao, *args, tempo_max=60.0, memoria_max_mb=1024, **kwargs):
    global corte_inicio, corte_tempo_max, corte_memoria_max_bytes, corte_contador
    corte_tempo_max = tempo_max
    corte_memoria_max_bytes = memoria_max_mb * 1024 * 1024
    corte_contador = 0

    tracemalloc.start()
    corte_inicio = time.time()
    inicio = time.time()

    try:
        resultado = funcao(*args, **kwargs)
        resultado["corte"] = None
    except CorteExcedido as erro:
        resultado = {
            "caminho": [],
            "numero_cliques": -1,
            "nos_expandidos": -1,
            "encontrou": False,
            "corte": erro.motivo,
        }

    fim = time.time()
    _, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    corte_inicio = None

    resultado["tempo"] = fim - inicio
    resultado["memoria_kb"] = memoria_pico / 1024
    return resultado


def imprimir_tabuleiro(tabuleiro):
    for linha in tabuleiro:
        print(" ".join("O" if v else "." for v in linha))
    print()


def imprimir_tabuleiro_destacando(tabuleiro, linha_clique, coluna_clique):
    for i, linha in enumerate(tabuleiro):
        partes = []
        for j, v in enumerate(linha):
            simbolo = "O" if v else "."
            if i == linha_clique and j == coluna_clique:
                partes.append(f"[{simbolo}]")
            else:
                partes.append(f" {simbolo} ")
        print("".join(partes))
    print()


def mostrar_fluxo_resolucao(tabuleiro_inicial, caminho):
    print("Fluxo de resolucao:")
    print("-" * 40)
    print("Passo 0 - Estado inicial:")
    imprimir_tabuleiro(tabuleiro_inicial)

    atual = tabuleiro_inicial
    for indice, (linha, coluna) in enumerate(caminho, start=1):
        print(f"Passo {indice} - Clique em (linha={linha}, coluna={coluna}):")
        print("Antes:")
        imprimir_tabuleiro_destacando(atual, linha, coluna)
        atual = clicar(atual, linha, coluna)
        print("Depois:")
        imprimir_tabuleiro(atual)
        print("-" * 40)

    if meu_objetivo(atual):
        print("Objetivo alcancado! Todas as luzes estao ligadas.")
    else:
        print("Atencao: o caminho nao chegou no objetivo.")
