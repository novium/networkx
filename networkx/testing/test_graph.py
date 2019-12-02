import unittest
from networkx.classes.graph import Graph
import networkx as nx

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

