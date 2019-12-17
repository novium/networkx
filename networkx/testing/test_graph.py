import unittest
from networkx.classes.graph import Graph
import networkx as nx

class WeirdClass:
   '''
   There are a lot of cases in graph.py that looks something like this:
   try:
      return n in self._node
   except TypeError:
      return False

   But we don't know how to make the TypeError to get raised.
   There is not a trace in the source code for dictionaries that this
   could ever happen. So to get 100% coverage this weird class is
   needed. It makes sure that a KeyError will always get raised.
   '''
   def __init__(self, err=KeyError):
      self.err = err
   def __hash__(self):
      raise self.err()
   def __eq__(self, _other):
      raise self.err()

class TestGraph(unittest.TestCase):

   # test name getters and setters
   def test_name(self):
      g = Graph()
      g.name = "testing testing! 1, 2, 3, 1, 2, 3"
      self.assertEqual(g.name, "testing testing! 1, 2, 3, 1, 2, 3")
      self.assertEqual(str(g), "testing testing! 1, 2, 3, 1, 2, 3")

   def test_nodes(self):
      # test various ways of node existence
      g = Graph()
      self.assertEqual(len(g), 0)
      self.assertEqual(len(g.nodes), 0)
      self.assertEqual(len(g.nodes()), 0)

      g.add_node(1)
      self.assertEqual(len(g), 1)
      self.assertTrue(1 in g)
      self.assertTrue(1 in iter(g))
      self.assertTrue(g.has_node(1))

      # to get 100% coverage
      self.assertFalse(g.has_node(WeirdClass(TypeError)))
      self.assertFalse(WeirdClass(TypeError) in g)

      g.add_node(2)
      self.assertTrue(1 in g)
      self.assertTrue(2 in g)
      self.assertEqual(len(g), 2)
      self.assertEqual(list(g), [1, 2])

      g.add_nodes_from([1,"hej"])
      self.assertTrue("hej" in g)
      self.assertEqual(len(g), 3)

      g.remove_node(2)
      self.assertFalse(2 in g)
      self.assertEqual(len(g), 2)

   def test_remove_nodes(self):
      g = Graph()
      g.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 11])

      # remove node
      g.remove_node(2)
      self.assertFalse(2 in g)

      # remove node that doesn't exist
      with self.assertRaises(nx.NetworkXError):
         g.remove_node(400020232)

      # remove several nodes
      g.remove_nodes_from([5, 6, 934982374])
      self.assertFalse(5 in g)
      self.assertFalse(6 in g)

      self.assertEqual(g.number_of_nodes(), 7)
      self.assertEqual(g.order(), 7)

   def test_node_data(self):
      g = Graph()
      # add node with data
      g.add_node(1, weight=2)
      self.assertEqual(g.nodes()[1], {"weight": 2})

      # update an existing node's data
      g.add_node(1, color="blue")
      self.assertEqual(g.nodes()[1], {"color": "blue", "weight": 2})

      # change value of existing node's data
      g.add_node(1, weight=3)
      self.assertEqual(g.nodes()[1], {"color": "blue", "weight": 3})

      # remove node data
      del g.nodes()[1]["weight"]
      self.assertEqual(g.nodes()[1], {"color": "blue"})

      # add new node with data
      g.add_nodes_from([(3, {"color": "blanc"})])
      self.assertEqual(g.nodes()[3], {"color": "blanc"})

      # test update existing node's data
      g.add_nodes_from([(3, {"color": "vert"})])
      self.assertEqual(g.nodes()[3], {"color": "vert"})

   def test_add_edge(self):
      g = Graph()

      # when no nodes exists
      g.add_edge(1, 2)
      self.assertTrue(g.has_edge(1, 2)) # should exist
      self.assertTrue(g.has_edge(2, 1)) # both ways
      # when the left node exists
      g.add_edge(2, 3)
      self.assertTrue(g.has_edge(2, 3))
      # when the right node exists
      g.add_edge(4, 3)
      self.assertTrue(g.has_edge(4, 3))

      # check nodes were added
      for x in [1, 2, 3, 4]:
         self.assertTrue(x in g)

      # when both existed from before
      g.add_node(10)
      g.add_node(11)
      g.add_edge(10, 11)
      self.assertTrue(g.has_edge(10, 11))

      # add edge that already exists
      before = len(g.edges())
      g.add_edge(10, 11)
      self.assertEqual(before, len(g.edges()))

      # test add_edges_from
      g.add_edges_from([(10, 11), (4, 5)])
      self.assertTrue(g.has_edge(4, 5))

      # a tuple that is too big
      with self.assertRaises(nx.NetworkXError):
         g.add_edges_from([(123, 123, 12, 312, 312, 3)])

      # add self loop
      g.add_edge(1, 1)
      self.assertTrue(g.has_edge(1, 1))

      # make sure to get 100% coverage
      self.assertFalse(g.has_edge(WeirdClass(), None))

   def test_add_edge_data(self):
      g = Graph()

      # add edge with data
      g.add_edge(1, 2, omg=3)
      self.assertTrue(g.edges[1, 2]["omg"], 3)
      self.assertTrue(g.edges()[1, 2]["omg"], 3)
      self.assertTrue(g.get_edge_data(1, 2)["omg"], 3)

      # get with default value
      self.assertEqual(g.get_edge_data(100, 100, default={"def": 100})["def"], 100)

      # override data and append more
      g.add_edge(1, 2, omg=2, xXx=42)
      self.assertTrue(g.edges[1, 2]["omg"], 2)
      self.assertTrue(g.edges[1, 2]["xXx"], 42)

      # test add_edges_from with triple tuple
      g.add_edges_from([(123, 712737, {828: 99})])
      self.assertTrue(g.edges[123, 712737][828], 99)

      g.add_weighted_edges_from([(4, 5, 2)])
      self.assertTrue(g.has_edge(4, 5))
      self.assertTrue(g.edges[4, 5]["weight"], 2)

   def test_edge_remove(self):
      g = Graph()
      g.add_edges_from([(1, 2), (2, 3, {"data": 9}), (3, 1)])

      # remove an edge
      self.assertTrue(g.has_edge(1, 2))
      g.remove_edge(1, 2)
      self.assertFalse(g.has_edge(1, 2))

      # remove a node that has edges
      self.assertTrue(g.has_edge(3, 1))
      g.remove_node(1)
      self.assertFalse(g.has_edge(3, 1))

      # test remove_nodes_from
      self.assertTrue(g.has_edge(2, 3))
      g.remove_nodes_from([3])
      self.assertFalse(g.has_edge(2, 3))

      # remove one that doesn't exist
      with self.assertRaises(nx.NetworkXError):
         g.remove_edge(2, 3)

      # remove a self-loop
      g.add_edge(1, 1)
      g.remove_edge(1, 1)
      self.assertFalse(g.has_edge(1, 1))

      # add a bunch of edges for remove_edges_from
      g.add_edges_from([(1, 1), (2, 1), (4, 5, {"asd": 2})])
      # remove self-loops, tuple with data (that is ignored) and an
      # edge that doesn't exis
      g.remove_edges_from([(1, 1), (1, 2, {"wat", 3}), (42, 54)])
      self.assertTrue(g.has_edge(4, 5))
      self.assertFalse(g.has_edge(1, 1))
      self.assertFalse(g.has_edge(1, 2))

   def test_adjacency(self):
      g = Graph()
      g.add_edges_from([(1, 2), (1, 3), (1, 4),
                        (4, 5), (4, 7),
                        (3, 2)])

      # test degree
      self.assertEqual(g.degree[1], 3)
      self.assertEqual(g.degree[7], 1)

      # test Graph.adjacency and Graph.neighbors
      for n, adj in g.adjacency():
         neigh = g.neighbors(n)
         self.assertEqual(set(neigh), adj.keys())

      # test two different ways of getting neighbors
      self.assertEqual(set(g[1]), {2, 3, 4})
      self.assertEqual(set(g.adj[1]), {2, 3, 4})

      # getting neighbor of something that doesn't exist
      with self.assertRaises(nx.NetworkXError):
         g.neighbors(100)

   def test_update(self):
      def check_if_updated_nodes(g):
         self.assertTrue(1 in g)
         self.assertTrue(2 in g)
         self.assertTrue(3 in g)
         self.assertTrue(4 in g)
         self.assertTrue(6 in g)
         self.assertTrue(7 in g)
      def check_if_updated_edges(g):
         self.assertTrue(g.has_edge(1, 2))
         self.assertTrue(g.has_edge(3, 4))
         self.assertTrue(g.has_edge(1, 3))
         self.assertTrue(g.has_edge(6, 7))

      g1 = Graph()
      g1.add_edges_from([(1, 2), (3, 4)])

      g2 = Graph()
      g2.add_edges_from([(1, 3), (6, 7)])

      # test update with graph as argument
      tmp = g1.copy()
      tmp.update(g2)
      check_if_updated_edges(tmp)
      check_if_updated_nodes(tmp)

      # test only new edges
      tmp = g1.copy()
      tmp.update(edges=g2.edges())
      check_if_updated_edges(tmp)
      check_if_updated_nodes(tmp)

      # test only nodes
      tmp = g1.copy()
      tmp.update(nodes=g2.nodes())
      check_if_updated_nodes(tmp)

      # add both explicitly
      tmp = g1.copy()
      tmp.update(nodes=g2.nodes(), edges=g2.edges())
      check_if_updated_edges(tmp)
      check_if_updated_nodes(tmp)

      tmp = g1.copy()
      with self.assertRaises(nx.NetworkXError):
         tmp.update()

   def test_to_undirected(self):
      g1 = Graph()
      g1.add_edges_from([(1, 2, {"asd": {"shared": True}}), (3, 4)])
      g2 = g1.to_undirected()
      # check that they are two completely different things
      self.assertFalse(g1 is g2)
      self.assertFalse(g1.edges[1, 2]["asd"] is g2.edges[1, 2]["asd"])

      # make sure the copy contains all nodes and edges of the
      # original
      for n in g1.nodes():
         self.assertTrue(n in g2)
      for u, v in g1.edges():
         self.assertTrue(g2.has_edge(u, v))

      # test views
      view = g1.to_undirected(as_view=True)
      for n in g1.nodes():
         self.assertTrue(n in view)
      for u, v in g1.edges():
         self.assertTrue(view.has_edge(u, v))

      # try to modify the read-only view
      with self.assertRaises(nx.NetworkXError):
         view.add_node("hej")

      # make sure that the copy is really independent
      g1.clear()
      self.assertEqual(len(g1), 0)
      self.assertEqual(len(g2), 4)

   def test_copy(self):
      g1 = Graph()
      g1.add_edges_from([(1, 2, {"asd": {"shared": True}}), (3, 4)])
      g2 = g1.copy()
      # check that they are two different things, except for the dict
      # in the attributes. The copy method is only doing shallow copy.
      self.assertFalse(g1 is g2)
      self.assertTrue(g1.edges[1, 2]["asd"] is g2.edges[1, 2]["asd"])

      # make sure the copy contains all nodes and edges of the
      # original
      for n in g1.nodes():
         self.assertTrue(n in g2)
      for u, v in g1.edges():
         self.assertTrue(g2.has_edge(u, v))

      # test views
      view = g1.copy(as_view=True)
      for n in g1.nodes():
         self.assertTrue(n in view)
      for u, v in g1.edges():
         self.assertTrue(view.has_edge(u, v))

      # try to modify the read-only view
      with self.assertRaises(nx.NetworkXError):
         view.add_node("hej")

      # make sure that the copy is really independent
      g1.clear()
      self.assertEqual(len(g1), 0)
      self.assertEqual(len(g2), 4)

   def test_number_edges(self):
      g = Graph()
      g.add_weighted_edges_from([(1, 2, 3.14), (3, 4, 2.718)])

      # simply test size method
      self.assertEqual(g.size(), 2)
      self.assertEqual(g.size(weight="weight"), 3.14 + 2.718)

      # simple test number_of_edges method
      self.assertEqual(g.number_of_edges(), 2)
      self.assertEqual(g.number_of_edges(u=1, v=2), 1)
      self.assertEqual(g.number_of_edges(u=1, v=6), 0)

   def test_misc(self):
      # these just return classes to use for empty copies, and we want
      # 100% coverage
      g = Graph()
      g.to_directed_class()
      g.to_undirected_class()
