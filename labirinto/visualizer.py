# visualizer.py — Visualização animada do labirinto com matplotlib

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import BoundaryNorm, ListedColormap

# ── Mapeamento de valores da grade para cores ──────────────────────────────
#   0.0  →  vermelho   (#e74c3c)  — início e fim
#   1.0  →  cinza claro(#f5f5f5)  — célula livre
#   1.5  →  azul claro (#85c1e9)  — célula explorada pelo algoritmo
#   2.5  →  amarelo    (#f4d03f)  — caminho final encontrado
_CORES  = ['#e74c3c', '#f5f5f5', '#85c1e9', '#f4d03f']
_LIMITES = [-0.5, 0.5, 1.25, 2.0, 3.0]   # fronteiras entre as 4 regiões de cor


def animate(maze, path: list, exploration: list, algorithm_name: str):
    """Anima a exploração e o caminho final do labirinto.

    Fase 1 — Exploração: pinta cada célula visitada em azul claro.
    Fase 2 — Caminho:    destaca o trajeto final em amarelo.

    Args:
        maze           — instância de Maze já gerado
        path           — sequência de células do caminho ótimo
        exploration    — sequência de células na ordem de visita
        algorithm_name — rótulo exibido no título ('BFS' ou 'DFS')

    Retorna o objeto FuncAnimation (mantém vivo até a janela ser fechada).
    """
    rows, cols = maze.rows, maze.cols

    # Grade numpy: inicializa tudo como "livre" (1.0)
    grade = np.ones((rows, cols))

    # Início (0,0) e fim (rows-1, cols-1) marcados em vermelho (0.0)
    grade[0][0] = 0.0
    grade[rows - 1][cols - 1] = 0.0

    # ── Configuração da figura ─────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(9, 9))
    ax.set_title(
        f'Labirinto {rows}×{cols}  —  {algorithm_name}',
        fontsize=14, fontweight='bold', pad=14
    )
    ax.set_aspect('equal')
    ax.axis('off')

    # Colormap com BoundaryNorm para mapear valores discretos a cores exatas
    cmap = ListedColormap(_CORES)
    norm = BoundaryNorm(_LIMITES, cmap.N)

    im = ax.imshow(grade, cmap=cmap, norm=norm, origin='upper')

    # Paredes desenhadas uma vez (ficam estáticas durante a animação)
    _desenhar_paredes(ax, maze)

    # Legenda de cores no canto superior direito
    _adicionar_legenda(ax)

    # Caixa de texto de progresso no canto inferior esquerdo
    texto = ax.text(
        0.02, 0.02, '',
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment='bottom',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffeaa7', alpha=0.9)
    )

    # ── Frames: exploração + caminho + pausa final ─────────────────────────
    total_frames = len(exploration) + len(path) + 30

    def atualizar(frame):
        if frame < len(exploration):
            # Fase 1: marca célula explorada (não sobrescreve início/fim)
            r, c = exploration[frame]
            if grade[r][c] == 1.0:
                grade[r][c] = 1.5
            texto.set_text(f'Explorando…  {frame + 1} / {len(exploration)}')

        elif frame < len(exploration) + len(path):
            # Fase 2: destaca célula do caminho final
            idx = frame - len(exploration)
            r, c = path[idx]
            if grade[r][c] != 0.0:   # preserva vermelho do início/fim
                grade[r][c] = 2.5
            texto.set_text(f'Caminho: {idx + 1} / {len(path)} células')

        else:
            # Animação concluída — exibe resumo
            texto.set_text(
                f'Concluído!   Caminho: {len(path)} cél.   '
                f'Exploradas: {len(exploration)} cél.'
            )

        im.set_data(grade)

    anim = FuncAnimation(
        fig, atualizar,
        frames=total_frames,
        interval=25,       # ms entre frames — aumente para animação mais lenta
        repeat=False
    )

    plt.tight_layout()
    plt.show()
    return anim   # mantém referência e evita coleta pelo garbage collector


# ── Helpers de desenho ─────────────────────────────────────────────────────

def _desenhar_paredes(ax, maze):
    """Desenha as paredes internas e a borda externa do labirinto.

    Cada célula sem passagem para o vizinho da direita gera um segmento
    vertical; sem passagem para baixo, um segmento horizontal.
    """
    rows, cols = maze.rows, maze.cols
    cor = '#2c3e50'

    for r in range(rows):
        for c in range(cols):
            # Parede vertical entre (r, c) e (r, c+1)
            if c + 1 < cols and not maze.has_passage((r, c), (r, c + 1)):
                ax.plot(
                    [c + 0.5, c + 0.5], [r - 0.5, r + 0.5],
                    color=cor, linewidth=1.0, solid_capstyle='round', zorder=3
                )
            # Parede horizontal entre (r, c) e (r+1, c)
            if r + 1 < rows and not maze.has_passage((r, c), (r + 1, c)):
                ax.plot(
                    [c - 0.5, c + 0.5], [r + 0.5, r + 0.5],
                    color=cor, linewidth=1.0, solid_capstyle='round', zorder=3
                )

    # Borda externa (linhas mais grossas)
    bordas = [
        ([-0.5, cols - 0.5], [-0.5,      -0.5]),          # topo
        ([-0.5, cols - 0.5], [rows - 0.5, rows - 0.5]),   # base
        ([-0.5,       -0.5], [-0.5,  rows - 0.5]),         # esquerda
        ([cols - 0.5, cols - 0.5], [-0.5, rows - 0.5]),    # direita
    ]
    for xs, ys in bordas:
        ax.plot(xs, ys, color=cor, linewidth=2.2, zorder=3)


def _adicionar_legenda(ax):
    """Adiciona pequena legenda de cores ao gráfico."""
    from matplotlib.patches import Patch
    itens = [
        Patch(facecolor='#e74c3c', label='Início / Fim'),
        Patch(facecolor='#85c1e9', label='Explorado'),
        Patch(facecolor='#f4d03f', label='Caminho'),
    ]
    ax.legend(
        handles=itens,
        loc='upper right',
        fontsize=9,
        framealpha=0.9,
        edgecolor='#cccccc'
    )
