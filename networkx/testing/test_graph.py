import unittest
import networkx as nx

class TestGraph(unittest.TestCase):
    def setUp(self):
        pass

    def test_1(self):
        G = nx.Graph()

        self.assertIsNotNone(G)

        G.add_node(1)

        self.assertEqual(len(G), 1)
