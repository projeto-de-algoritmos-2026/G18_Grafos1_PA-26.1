# maze.py — Geração de labirinto usando Recursive Backtracker (DFS iterativo)

import random


class Maze:
    """Labirinto procedural gerado por Recursive Backtracker.

    Representa as passagens como um conjunto de pares ordenados de células
    adjacentes, formando uma árvore geradora (labirinto perfeito):
    exatamente um caminho entre quaisquer duas células.
    """

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        # Cada passagem é uma tupla (célula_menor, célula_maior) para
        # normalizar a representação e evitar duplicatas.
        self.passages: set = set()
        self._generate()

    # ------------------------------------------------------------------
    # Geração
    # ------------------------------------------------------------------

    def _generate(self):
        """Gera o labirinto com DFS iterativo (Recursive Backtracker).

        Partindo de (0, 0), visita todas as células escolhendo aleatoriamente
        um vizinho não visitado e abrindo passagem até ele. Quando não há
        vizinhos livres, retrocede na pilha (backtrack).
        """
        visitados: set = set()
        inicio = (0, 0)
        pilha = [inicio]
        visitados.add(inicio)

        while pilha:
            atual = pilha[-1]
            r, c = atual

            # Vizinhos válidos ainda não visitados
            livres = [
                (nr, nc)
                for nr, nc in self._neighbors(r, c)
                if (nr, nc) not in visitados
            ]

            if livres:
                # Escolhe próxima célula aleatoriamente e abre passagem
                proximo = random.choice(livres)
                self.passages.add(self._passagem(atual, proximo))
                visitados.add(proximo)
                pilha.append(proximo)
            else:
                # Sem vizinhos livres → retrocede
                pilha.pop()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _neighbors(self, r: int, c: int) -> list:
        """Retorna células vizinhas válidas nas 4 direções cardeais."""
        resultado = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                resultado.append((nr, nc))
        return resultado

    @staticmethod
    def _passagem(a: tuple, b: tuple) -> tuple:
        """Cria representação normalizada (menor, maior) de uma passagem."""
        return (min(a, b), max(a, b))

    def has_passage(self, a: tuple, b: tuple) -> bool:
        """Retorna True se existe passagem aberta entre as células a e b."""
        return self._passagem(a, b) in self.passages
