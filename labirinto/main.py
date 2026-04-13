# main.py — Ponto de entrada do solucionador de labirinto

from maze import Maze
from solver import bfs, dfs
from visualizer import animate


def main():
    # ── Escolha do tamanho ─────────────────────────────────────────────────
    print('\n=== Solucionador de Labirinto ===')
    try:
        n = int(input('Tamanho do labirinto (N×N, mínimo 5): ').strip())
        if n < 5:
            print('Tamanho mínimo é 5. Usando 5.')
            n = 5
    except ValueError:
        print('Entrada inválida. Usando 20.')
        n = 20

    labirinto = Maze(n, n)

    inicio = (0, 0)
    fim    = (labirinto.rows - 1, labirinto.cols - 1)

    # ── Escolha do algoritmo ───────────────────────────────────────────────
    print('Escolha o algoritmo de busca:')
    print('  1 → BFS  (Busca em Largura   — caminho mais curto garantido)')
    print('  2 → DFS  (Busca em Profundidade — explora fundo antes de retroceder)')
    escolha = input('\nDigite 1 ou 2: ').strip()

    if escolha == '1':
        caminho, exploracao = bfs(labirinto, inicio, fim)
        nome_algo = 'BFS'
    elif escolha == '2':
        caminho, exploracao = dfs(labirinto, inicio, fim)
        nome_algo = 'DFS'
    else:
        print('Opção inválida. Usando BFS por padrão.')
        caminho, exploracao = bfs(labirinto, inicio, fim)
        nome_algo = 'BFS'

    # ── Estatísticas no terminal ───────────────────────────────────────────
    print(f'\nAlgoritmo         : {nome_algo}')
    print(f'Tamanho do caminho : {len(caminho)} células')
    print(f'Células exploradas : {len(exploracao)}')
    print('\nAbrindo visualização… feche a janela para encerrar.')

    # ── Visualização animada ───────────────────────────────────────────────
    animate(labirinto, caminho, exploracao, nome_algo)


if __name__ == '__main__':
    main()
