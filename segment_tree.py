class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.st = [0]*(4*self.n)
        self._build(arr, 1, 0, self.n-1)

    def _build(self, arr, idx, l, r):
        if l == r:
            self.st[idx] = arr[l]
            return
        m = (l+r)//2
        self._build(arr, idx*2, l, m)
        self._build(arr, idx*2+1, m+1, r)
        self.st[idx] = self.st[idx*2] + self.st[idx*2+1]

    def query(self, ql, qr):
        return self._query(1, 0, self.n-1, ql, qr)

    def _query(self, idx, l, r, ql, qr):
        if qr < l or r < ql:
            return 0
        if ql <= l and r <= qr:
            return self.st[idx]
        m = (l+r)//2
        return self._query(idx*2, l, m, ql, qr) + self._query(idx*2+1, m+1, r, ql, qr)
