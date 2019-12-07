import networkx as nx
import random
import math
import multiprocessing as MP

def path_dist(G, p):
   "Calculate the distance of following the path p on graph G."
   p_edges = set(zip(p, p[1:]))
   return sum(data["weight"] for u, v, data in G.edges(data=True) if (u, v) in p_edges)

# TODO: highlight shortest path
def draw_graph(G):
   "Draw the graph G for debugging."
   import matplotlib.pyplot as plt
   pos = nx.circular_layout(G)
   nx.draw(G, pos=pos, with_labels=True)
   nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "weight"))
   plt.show()

def graph_try_add(G, u, v, w):
   '''
   Try to add the edge (u, v) with weight w to G. If this edge
   happens to create a shorter path than the protected one, then it
   will not be added.
   If (u, v) is added, then will all "shortest"-attributes be updated
   on all affected edges.
   '''
   if G.has_edge(u, v):
      return False
   new_shortest = {}
   G.add_edge(u, v, weight=w)

   def getw(u):
      if u in new_shortest:
         return new_shortest[u]
      return G.nodes[u]["shortest"]

   # We don't want to visit neighbours of u that is not v because
   # those can't possible be affected, waste of CPU.
   def neigh(x):
      for n in G.neighbors(x):
         if x != u or (x == u and n == v):
            yield n

   # do some DFS thingy to update all "shortest"-attributes
   stack = [u]
   while stack:
      x = stack.pop()
      for n in neigh(x):
         news = getw(x) + G.edges[x, n]["weight"]
         if news <= getw(n) and G.nodes[n]["protected"]:
            G.remove_edge(u, v)
            return False

         if news < getw(n):
            stack.append(n)
            new_shortest[n] = news

   # do some dijkstra-like algorithm to update all "shortest"-attributes.
   # This didn't work :(
   # Leaving this here because it should work (I think) and because it
   # is more efficient than the DFS solution.

   # visited = set()
   # front = [(getw(u), u)]

   # while front:
   #    s, x = heapq.heappop(front)
   #    if x in visited:
   #       break
   #    visited.add(x)
   #    new_shortest[x] = s

   #    for n in neigh(x):
   #       if n in visited:
   #          continue
   #       news = s + G.edges[x, n]["weight"]
   #       if news <= getw(n) and G.nodes[n]["protected"]:
   #          G.remove_edge(u, v)
   #          return False

   #       if news < getw(n):
   #          heapq.heappush(front, (news, n))

   # write all new "shortest"-attributes
   for v, w in new_shortest.items():
      G.add_node(v, shortest=w)
   return True

def gen_graph(max_nodes=100, min_nodes=2, min_edge_weight=1, max_edge_weight=10, max_additional_edges=100):
   '''
   G, d, p = gen_graph()
   This will generate a random directed graph G that will have a
   shortest path p of distance d.
   '''
   num_nodes = random.randint(min_nodes, max_nodes)
   path_len = random.randint(2, num_nodes)
   path = random.sample(range(num_nodes), path_len)
   weights = [random.randint(min_edge_weight, max_edge_weight) for _ in range(path_len)]
   additional_edges = min(max_additional_edges, random.randint(0, num_nodes*(num_nodes - 1) - path_len))

   # create initial graph with one path
   G = nx.DiGraph()
   G.add_node(path[0], shortest=0)
   for u, v, w in zip(path, path[1:], weights):
      G.add_edge(u, v, weight=w)
      G.add_node(v, shortest=w+G.nodes[u]["shortest"], protected=True)

   for u in range(num_nodes):
      if u not in G:
         G.add_node(u, shortest=math.inf, protected=False)

   # try adding random edges and check whether they are allowed.
   for _ in range(additional_edges):
      [a, b] = random.sample(range(num_nodes), 2)
      w = random.randint(min_edge_weight, max_edge_weight)
      graph_try_add(G, a, b, w)

   return G, G.nodes[path[-1]]["shortest"], path

def test(*_args):
   "Generate a random graph and check whether networkx finds the correct shortest path."
   gen_G, gen_dist, gen_path = gen_graph()
   distance, path = nx.single_source_dijkstra(gen_G, gen_path[0], target=gen_path[-1])
   if gen_dist == distance and gen_path == path:
      return None
   else:
      return {
         "gen_G": gen_G,
         "gen_dist": gen_dist,
         "gen_path": gen_path,
         "nx_distance": distance,
         "nx_path": path
      }

def fuzz(times=10000, threads=None):
   "Run test a couple of times and collect the result."
   succ = 0
   fail = 0
   failed = []

   with MP.Pool(threads) as p:
      failed = [x for x in p.imap_unordered(test, range(times), 100) if x is not None]

   fail = len(failed)
   succ = times - fail
   return succ, fail, failed

def main():
   succ, fail, _failed = fuzz()
   # TODO: save failed somewhere for inspection
   print("{} succeded and {} failed".format(succ, fail))

if __name__ == "__main__":
   main()
