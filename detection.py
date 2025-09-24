# backend/app/services/detection.py
from typing import List, Tuple, Dict, Any
from union_find import UnionFind
from segment_tree import SegmentTree

def detect_changes(grid0: List[List[float]], grid1: List[List[float]], threshold: float=0.25) -> Tuple[List[List[float]], List[List[int]]]:
    n = len(grid0)
    loss = [[0.0]*n for _ in range(n)]
    mask = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            diff = grid0[i][j] - grid1[i][j]
            loss[i][j] = diff
            if diff >= threshold:
                mask[i][j] = 1
    return loss, mask

def cluster_incidents(mask: List[List[int]]) -> List[List[Tuple[int, int]]]:
    n = len(mask)
    idx = lambda x,y: x*n + y
    uf = UnionFind(n*n)
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    active = []
    for i in range(n):
        for j in range(n):
            if mask[i][j] == 1:
                active.append((i,j))
    for i,j in active:
        for di,dj in dirs:
            ni,nj = i+di, j+dj
            if 0 <= ni < n and 0 <= nj < n and mask[ni][nj] == 1:
                uf.union(idx(i,j), idx(ni,nj))
    groups: Dict[int, List[Tuple[int,int]]] = {}
    for i,j in active:
        r = uf.find(idx(i,j))
        groups.setdefault(r, []).append((i,j))
    return list(groups.values())

def incident_bbox(cells: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    xs = [i for i,_ in cells]; ys = [j for _,j in cells]
    return (min(xs), min(ys), max(xs), max(ys))

def incident_centroid(cells: List[Tuple[int, int]]) -> Tuple[float, float]:
    sx = sum(i for i,_ in cells)/len(cells); sy = sum(j for _,j in cells)/len(cells)
    return (sx, sy)

def range_stats(values: List[float], queries: List[Tuple[int, int]]) -> List[Any]:
    st = SegmentTree(values)
    return [st.query(l,r) for (l,r) in queries]
