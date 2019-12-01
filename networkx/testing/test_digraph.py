import unittest
import networkx as nx

class TestDigraph(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        G = nx.DiGraph()
        self.assertIsNotNone(G)

        G = nx.DiGraph(name = 'test_create')
        self.assertEqual(G.name, 'test_create')

    def test_adj_1(self):
        pass
