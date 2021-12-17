import itertools
from collections import defaultdict

visited = defaultdict(int)
paths = []


# save path until this point
# can be visited more than once if uppercase
def dfs(g, multi_allowed, v='start', p=[]):
    visited[v] += 1
    p.append(v)

    for n in list(g[v]):
        if n == "end":
            p.append(n)
            global paths
            paths.append(p.copy())
            p.pop()
        if n.isupper() or visited[n] == 0 or (n == multi_allowed and visited[n] < 2):
            dfs(g, multi_allowed, n, p)
            visited[n] -= 1
            p.pop()


# ll = [x.split("-") for x in open("12.ex3").read().strip().split()]
ll = [x.split("-") for x in open("12.in").read().strip().split()]

# build graph: Adjacency list
graph = defaultdict(set)
for l in ll:
    if l[1] != "end" and l[0] != "start":
        graph[l[1]].add(l[0])
    if l[0] != "end" and l[1] != "start":
        graph[l[0]].add(l[1])

small_caves = [x for x in graph.keys() if x.islower() and x != "start" and x != "end"]
for cave in small_caves:
    dfs(graph, cave, v="start", p=[])
    visited = defaultdict(int)
paths.sort()
paths = list(k for k, _ in itertools.groupby(paths))
print(len(paths))
