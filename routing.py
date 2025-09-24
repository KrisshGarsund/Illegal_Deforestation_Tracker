# backend/app/services/routing.py
from typing import List, Tuple, Any
from graph import Graph
import math

def build_waypoint_graph(points: List[Tuple[float, float]]) -> 'Graph':
    g = Graph()
    def dist(a: Tuple[float, float], b: Tuple[float, float]) -> float:
        return math.hypot(a[0]-b[0], a[1]-b[1])
    k = min(6, max(1, len(points)-1))
    for i in range(len(points)):
        dists = sorted([(dist(points[i], points[j]), j) for j in range(len(points)) if j!=i])[:k]
        for d,j in dists:
            g.add_edge(i, j, d, undirected=True)
    return g

def nearest_node(points: List[Tuple[float, float]], p: Tuple[float, float]) -> int:
    best = (1e18, -1)
    for i,pt in enumerate(points):
        d = math.hypot(pt[0]-p[0], pt[1]-p[1])
        if d < best[0]: best = (d,i)
    return best[1]

def route(points: List[Tuple[float, float]], start: Tuple[float, float], goal: Tuple[float, float]) -> Tuple[Any, Any]:
    g = build_waypoint_graph(points)
    s = nearest_node(points, start)
    t = nearest_node(points, goal)
    dist, path = g.dijkstra(s, t)
    return dist, path
