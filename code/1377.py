class Solution:
    def frogPosition(self, n, edges, t, target):
        if n == 1:
            return 1.0

        graph = [[] for _ in range(n + 1)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        from collections import deque
        queue = deque()
        queue.append((1, 0, 1.0))
        visited = [False] * (n + 1)
        visited[1] = True

        while queue:
            node, time, prob = queue.popleft()
            children = [nb for nb in graph[node] if not visited[nb]]

            if node == target:
                if (not children and t >= time) or (time == t):
                    return prob
                return 0.0

            if not children or time == t:
                continue

            for child in children:
                visited[child] = True
                queue.append((child, time + 1, prob / len(children)))

        return 0.0