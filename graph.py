import heapq, math
class Graph:
    def __init__(self):
        self.adj = {}

    def add_edge(self, u, v, w, undirected=True):
        self.adj.setdefault(u, []).append((v,w))
        if undirected:
            self.adj.setdefault(v, []).append((u,w))

    def dijkstra(self, src, dst):
        dist = {node: math.inf for node in self.adj.keys()}
        prev = {}
        dist[src] = 0.0
        pq = [(0.0, src)]
        seen = set()
        while pq:
            d,u = heapq.heappop(pq)
            if u in seen: continue
            seen.add(u)
            if u == dst: break
            for v,w in self.adj.get(u, []):
                if d + w < dist.get(v, math.inf):
                    dist[v] = d + w
                    prev[v] = u
                    heapq.heappush(pq, (dist[v], v))
        if dist.get(dst, math.inf) == math.inf:
            return math.inf, []
        path = [dst]
        while path[-1] != src:
            path.append(prev[path[-1]])
        path.reverse()
        return dist[dst], path
