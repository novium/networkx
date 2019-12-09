import unittest
import networkx as nx

try:
    import numpy as np
    numpy = True
except:
    numpy = False
    print('not testing numpy!')

class TestDigraph(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        G = nx.DiGraph()
        self.assertIsNotNone(G)

        G = nx.DiGraph(name = 'test_create')
        self.assertIsNotNone(G)
        self.assertEqual(G.name, 'test_create')

    def test_add_node_1(self):
        G = nx.DiGraph()
        self.assertIsNotNone(G)

        # New graph
        self.assertEqual(G.number_of_nodes(), 0)
        G.add_node(0) # Add a node, check if added
        self.assertEqual(G.number_of_nodes(), 1)
        G.add_node(0) # Check that same node can't be added twice (branch)
        self.assertEqual(G.number_of_nodes(), 1)
        G.add_node(1) # Add >1 node
        self.assertEqual(G.number_of_nodes(), 2)

    def test_add_nodes_from_1(self):
        G = nx.DiGraph()
        self.assertIsNotNone(G)

        nodes = [0,2,3,5,7,11,13,17]
        self.assertEqual(G.number_of_nodes(), 0)
        G.add_nodes_from(nodes)
        self.assertEqual(G.number_of_nodes(), len(nodes))
        nodes_p = nodes[0:2]
        G.add_nodes_from(nodes_p)
        self.assertEqual(G.number_of_nodes(), len(nodes))

    def test_add_nodes_from_numpy_1(self):
        """ Tests importing graph from random numpy matrix
        """
        if not numpy:
            return
        
        a = np.random.randint(0, 2, size=(20, 20))
        G = nx.DiGraph(a)
        
        self.assertEqual(G.number_of_nodes(), 20)