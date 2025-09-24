import heapq
class MaxPQ:
    def __init__(self):
        self.h = []
    def push(self, priority, item):
        heapq.heappush(self.h, (-priority, item))
    def pop(self):
        p, it = heapq.heappop(self.h)
        return -p, it
    def __len__(self):
        return len(self.h)
