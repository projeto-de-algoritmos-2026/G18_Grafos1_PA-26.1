# solver.py — Algoritmos BFS e DFS para resolver o labirinto

from collections import deque


def bfs(maze, start: tuple, end: tuple):
    """Busca em Largura (BFS): garante o caminho de menor número de passos.

    Retorna:
        path       — lista de células do início ao fim (caminho ótimo)
        exploration — células na ordem em que foram descobertas (animação)
    """
    visitados = {start}
    pai = {start: None}
    fila = deque([start])
    exploracao = []

    while fila:
        atual = fila.popleft()
        exploracao.append(atual)

        if atual == end:
            break

        r, c = atual
        for vizinho in maze._neighbors(r, c):
            if vizinho not in visitados and maze.has_passage(atual, vizinho):
                visitados.add(vizinho)
                pai[vizinho] = atual
                fila.append(vizinho)

    return _reconstruir_caminho(pai, end), exploracao


def dfs(maze, start: tuple, end: tuple):
    """Busca em Profundidade (DFS) iterativa: explora fundo antes de retroceder.

    Retorna:
        path       — lista de células do início ao fim
        exploration — células na ordem em que foram visitadas (animação)
    """
    visitados: set = set()
    pai = {start: None}
    pilha = [start]
    exploracao = []

    while pilha:
        atual = pilha.pop()

        # Lazy visited: ignora se já processado (pode ser empurrado várias vezes)
        if atual in visitados:
            continue

        visitados.add(atual)
        exploracao.append(atual)

        if atual == end:
            break

        r, c = atual
        for vizinho in maze._neighbors(r, c):
            if vizinho not in visitados and maze.has_passage(atual, vizinho):
                # Define pai apenas na primeira descoberta
                if vizinho not in pai:
                    pai[vizinho] = atual
                pilha.append(vizinho)

    return _reconstruir_caminho(pai, end), exploracao


# ------------------------------------------------------------------
# Utilitário interno
# ------------------------------------------------------------------

def _reconstruir_caminho(pai: dict, end: tuple) -> list:
    """Percorre o dicionário de pais do destino até a origem e inverte."""
    if end not in pai:
        return []  # destino não alcançado (não ocorre num labirinto perfeito)

    caminho = []
    atual = end
    while atual is not None:
        caminho.append(atual)
        atual = pai[atual]

    caminho.reverse()
    return caminho
