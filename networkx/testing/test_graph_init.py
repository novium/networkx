import unittest
from networkx.classes.graph import Graph
import networkx as nx

# TODO: silence warning logs
class TestGraphInit(unittest.TestCase):
    # convert.py checks for a bunch of different kinds of input data,
    # basically all iterables. It checks explicitly for these cases:

    def test_init_empty(self):
        # test if can create empty Graph
        g = Graph()
        self.assertIsInstance(g, Graph)
        self.assertEqual(list(g.edges), [])
        self.assertEqual(list(g.nodes), [])
        self.assertFalse(g.is_directed())

    def test_init_dict_dict(self):
        # test creating a Graph from dict of dicts
        g = Graph({})
        self.assertEqual(list(g.edges), [])
        self.assertEqual(list(g.nodes), [])

        g = Graph({1: {2: None}})
        self.assertEqual(list(g.edges), [(1, 2)])
        self.assertEqual(list(g.nodes), [1, 2])

    def test_init_dict_list(self):
        # test creating a Graph from dict of lists
        g = Graph({1: [2]})
        self.assertEqual(list(g.edges), [(1, 2)])
        self.assertEqual(list(g.nodes), [1, 2])

        # test an invalid one
        with self.assertRaises(TypeError):
            g = Graph({1: 2})

    def test_init_edgelist(self):
        # Test creating a Graph from edgelists, i.e. iterables of 2-tuples.

        # list of tuples
        g = Graph([(1, 2)])
        self.assertEqual(list(g.edges), [(1, 2)])
        self.assertEqual(list(g.nodes), [1, 2])

        # tuple of tuples
        g = Graph(((1, 2),))
        self.assertEqual(list(g.edges), [(1, 2)])
        self.assertEqual(list(g.nodes), [1, 2])

        # generators of tuples
        g = Graph((t for t in [(1, 2)]))
        self.assertEqual(list(g.edges), [(1, 2)])
        self.assertEqual(list(g.nodes), [1, 2])

        # test invalid edgelists
        with self.assertRaises(nx.NetworkXError):
            g = Graph([1, 2])

        # to make the generator at convert.py:103 to finish
        with self.assertRaises(nx.NetworkXError):
            g = Graph(1)

        with self.assertRaises(nx.NetworkXError):
            g = Graph([(1, 2, 3)])
