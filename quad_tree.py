class QuadTreeNode:
    def __init__(self, bbox, capacity=8, depth=0, max_depth=10):
        self.bbox = bbox
        self.capacity = capacity
        self.depth = depth
        self.max_depth = max_depth
        self.points = []
        self.children = None

    def _subdivide(self):
        minx,miny,maxx,maxy = self.bbox
        mx = (minx+maxx)/2; my = (miny+maxy)/2
        self.children = [
            QuadTreeNode((minx,my,mx,maxy), self.capacity, self.depth+1, self.max_depth),
            QuadTreeNode((mx,my,maxx,maxy), self.capacity, self.depth+1, self.max_depth),
            QuadTreeNode((minx,miny,mx,my), self.capacity, self.depth+1, self.max_depth),
            QuadTreeNode((mx,miny,maxx,my), self.capacity, self.depth+1, self.max_depth)
        ]

    def insert(self, x, y, payload):
        minx,miny,maxx,maxy = self.bbox
        if not (minx <= x <= maxx and miny <= y <= maxy):
            return False
        if self.children is None and (len(self.points) < self.capacity or self.depth >= self.max_depth):
            self.points.append((x,y,payload))
            return True
        if self.children is None:
            self._subdivide()
        for ch in self.children:
            if ch.insert(x,y,payload):
                return True
        return False

    def query_range(self, bbox):
        res = []
        def overlaps(a,b):
            return not (a[2] < b[0] or a[0] > b[2] or a[3] < b[1] or a[1] > b[3])
        if not overlaps(self.bbox, bbox):
            return res
        for x,y,p in self.points:
            if bbox[0] <= x <= bbox[2] and bbox[1] <= y <= bbox[3]:
                res.append((x,y,p))
        if self.children:
            for ch in self.children:
                res.extend(ch.query_range(bbox))
        return res
