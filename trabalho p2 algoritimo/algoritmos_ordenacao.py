"""
Trabalho: Algoritmos de Ordenação em Python
- Lista aleatória de 100.000 elementos
- 9 algoritmos implementados
- Vantagens e desvantagens descritas em comentários
"""

import random
import time

TAMANHO = 100_000        # quantidade de elementos da lista
VALOR_MAXIMO = 100_000   # valores aleatórios entre 0 e VALOR_MAXIMO


# ---------------------------------------------------------------------------
# 1) SELECTION SORT (ordenação por seleção) - O(n²)
# Vantagens:    simples; faz poucas trocas (no máximo n-1); usa pouca memória O(1).
# Desvantagens: sempre O(n²), mesmo com lista já ordenada; muito lento para
#               listas grandes; não é estável.
# ---------------------------------------------------------------------------
def selection_sort(lista):
    n = len(lista)
    for i in range(n - 1):
        menor = i
        for j in range(i + 1, n):
            if lista[j] < lista[menor]:
                menor = j
        lista[i], lista[menor] = lista[menor], lista[i]
    return lista


# ---------------------------------------------------------------------------
# 2) BUBBLE SORT - O(n²) (melhor caso O(n) com a verificação de "trocou")
# Vantagens:    muito simples; estável; detecta lista já ordenada (melhor caso O(n)).
# Desvantagens: faz muitas comparações e trocas; é o mais lento dos algoritmos
#               comuns; inviável para listas grandes.
# ---------------------------------------------------------------------------
def bubble_sort(lista):
    n = len(lista)
    for i in range(n - 1):
        trocou = False
        for j in range(n - 1 - i):
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                trocou = True
        if not trocou:  # nenhuma troca: a lista já está ordenada
            break
    return lista


# ---------------------------------------------------------------------------
# 3) INSERTION SORT (ordenação por inserção) - O(n²) (melhor caso O(n))
# Vantagens:    estável; ótimo para listas pequenas ou quase ordenadas;
#               in-place (memória O(1)); mais rápido que Bubble e Selection.
# Desvantagens: O(n²) no pior caso e no caso médio; lento para listas grandes
#               e aleatórias.
# ---------------------------------------------------------------------------
def insertion_sort(lista):
    for i in range(1, len(lista)):
        chave = lista[i]
        j = i - 1
        while j >= 0 and lista[j] > chave:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = chave
    return lista


# ---------------------------------------------------------------------------
# 4) MERGE SORT (ordenação por intercalação) - O(n log n)
# Vantagens:    sempre O(n log n) (pior, médio e melhor caso); estável;
#               desempenho previsível.
# Desvantagens: usa memória extra O(n); é um pouco mais lento que o Quick Sort
#               na prática por causa das cópias de listas.
# ---------------------------------------------------------------------------
def merge_sort(lista):
    if len(lista) <= 1:
        return lista
    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio])
    direita = merge_sort(lista[meio:])

    resultado = []
    i = j = 0
    while i < len(esquerda) and j < len(direita):
        if esquerda[i] <= direita[j]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado


# ---------------------------------------------------------------------------
# 5) QUICK SORT (ordenação rápida) - O(n log n) médio, O(n²) no pior caso
# Vantagens:    geralmente o mais rápido na prática; in-place (pouca memória
#               extra); boa localidade de cache.
# Desvantagens: pior caso O(n²) com pivôs ruins (aqui reduzido com pivô
#               aleatório); não é estável; recursão pode ficar profunda.
# ---------------------------------------------------------------------------
def quick_sort(lista):
    _quick(lista, 0, len(lista) - 1)
    return lista


def _quick(lista, baixo, alto):
    while baixo < alto:
        # pivô aleatório evita o pior caso em listas já ordenadas
        indice_pivo = random.randint(baixo, alto)
        lista[indice_pivo], lista[alto] = lista[alto], lista[indice_pivo]
        pivo = lista[alto]

        i = baixo - 1
        for j in range(baixo, alto):
            if lista[j] <= pivo:
                i += 1
                lista[i], lista[j] = lista[j], lista[i]
        lista[i + 1], lista[alto] = lista[alto], lista[i + 1]
        p = i + 1

        # recursão na parte menor, laço na maior (limita a profundidade)
        if p - baixo < alto - p:
            _quick(lista, baixo, p - 1)
            baixo = p + 1
        else:
            _quick(lista, p + 1, alto)
            alto = p - 1


# ---------------------------------------------------------------------------
# 6) HEAP SORT - O(n log n)
# Vantagens:    sempre O(n log n); in-place (memória O(1)); não tem pior caso
#               quadrático.
# Desvantagens: não é estável; na prática costuma ser mais lento que Quick Sort
#               e Merge Sort; acessos à memória pouco sequenciais.
# ---------------------------------------------------------------------------
def heap_sort(lista):
    n = len(lista)

    def peneirar(tamanho, raiz):
        while True:
            maior = raiz
            esq = 2 * raiz + 1
            dir_ = 2 * raiz + 2
            if esq < tamanho and lista[esq] > lista[maior]:
                maior = esq
            if dir_ < tamanho and lista[dir_] > lista[maior]:
                maior = dir_
            if maior == raiz:
                return
            lista[raiz], lista[maior] = lista[maior], lista[raiz]
            raiz = maior

    # constrói o heap máximo
    for i in range(n // 2 - 1, -1, -1):
        peneirar(n, i)
    # extrai o maior elemento repetidamente
    for fim in range(n - 1, 0, -1):
        lista[0], lista[fim] = lista[fim], lista[0]
        peneirar(fim, 0)
    return lista


# ---------------------------------------------------------------------------
# 7) COUNTING SORT (ordenação por contagem) - O(n + k), k = amplitude dos valores
# Vantagens:    não usa comparações; muito rápido quando k é pequeno em relação
#               a n; estável.
# Desvantagens: só funciona com inteiros (ou chaves inteiras); gasta memória
#               O(k), inviável se a amplitude dos valores for muito grande.
# ---------------------------------------------------------------------------
def counting_sort(lista):
    if not lista:
        return lista
    menor, maior = min(lista), max(lista)
    contagem = [0] * (maior - menor + 1)
    for x in lista:
        contagem[x - menor] += 1
    # soma acumulada: posição final de cada valor
    for i in range(1, len(contagem)):
        contagem[i] += contagem[i - 1]
    saida = [0] * len(lista)
    for x in reversed(lista):  # percorrer de trás para frente mantém a estabilidade
        contagem[x - menor] -= 1
        saida[contagem[x - menor]] = x
    return saida


# ---------------------------------------------------------------------------
# 8) RADIX SORT (LSD, base 10) - O(d · (n + b)), d = nº de dígitos, b = base
# Vantagens:    não usa comparações; muito eficiente para inteiros com poucos
#               dígitos; estável.
# Desvantagens: limitado a inteiros/strings (aqui, não negativos); usa memória
#               extra; depende do nº de dígitos dos valores.
# ---------------------------------------------------------------------------
def radix_sort(lista):
    if not lista:
        return lista
    maior = max(lista)
    exp = 1
    while maior // exp > 0:
        lista = _counting_por_digito(lista, exp)
        exp *= 10
    return lista


def _counting_por_digito(lista, exp):
    contagem = [0] * 10
    for x in lista:
        contagem[(x // exp) % 10] += 1
    for i in range(1, 10):
        contagem[i] += contagem[i - 1]
    saida = [0] * len(lista)
    for x in reversed(lista):
        d = (x // exp) % 10
        contagem[d] -= 1
        saida[contagem[d]] = x
    return saida


# ---------------------------------------------------------------------------
# 9) BUCKET SORT (ordenação por baldes) - O(n + k) médio, O(n²) no pior caso
# Vantagens:    muito rápido quando os valores são bem distribuídos
#               (uniformes); fácil de paralelizar.
# Desvantagens: desempenho cai se muitos elementos caírem no mesmo balde; usa
#               memória extra; depende da distribuição e da escolha dos baldes.
# ---------------------------------------------------------------------------
def bucket_sort(lista):
    if not lista:
        return lista
    menor, maior = min(lista), max(lista)
    qtd_baldes = max(1, len(lista) // 10)
    amplitude = (maior - menor + 1) / qtd_baldes
    baldes = [[] for _ in range(qtd_baldes)]
    for x in lista:
        baldes[int((x - menor) / amplitude)].append(x)

    resultado = []
    for balde in baldes:
        insertion_sort(balde)  # cada balde é pequeno, então Insertion Sort é eficiente
        resultado.extend(balde)
    return resultado


# ---------------------------------------------------------------------------
# TESTES
# ---------------------------------------------------------------------------
def main():
    random.seed(42)  # resultado reprodutível (pode remover)
    original = [random.randint(0, VALOR_MAXIMO) for _ in range(TAMANHO)]
    esperado = sorted(original)
    print(f"Lista aleatória com {TAMANHO:,} elementos criada.\n".replace(",", "."))

    algoritmos = [
        ("Selection Sort", selection_sort),
        ("Bubble Sort", bubble_sort),
        ("Insertion Sort", insertion_sort),
        ("Merge Sort", merge_sort),
        ("Quick Sort", quick_sort),
        ("Heap Sort", heap_sort),
        ("Counting Sort", counting_sort),
        ("Radix Sort", radix_sort),
        ("Bucket Sort", bucket_sort),
    ]

    print(f"{'Algoritmo':<16}{'Tempo (s)':>12}   Ordenou corretamente?")
    print("-" * 52)
    for nome, funcao in algoritmos:
        copia = original.copy()  # cada algoritmo recebe a mesma lista
        inicio = time.perf_counter()
        resultado = funcao(copia)
        tempo = time.perf_counter() - inicio
        correto = "Sim" if resultado == esperado else "NAO"
        print(f"{nome:<16}{tempo:>12.4f}   {correto}")


if __name__ == "__main__":
    main()
