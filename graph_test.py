from unittest import TestCase

from graph import Graph, GraphNode

class GraphTest(TestCase):
    def setUp(self):
        pass

        #print(g.executeGraph())
        #print(Graph.sortGraph(g))
        #print(Graph.isCycleInGraph(g))

    def testGraphCreation(self):
        a = GraphNode('a')
        b = GraphNode('b')
        c = GraphNode('c')
        b1 = GraphNode('b1')

        g = Graph(a)
        g.connect(a, [b, c])
        g.connect(c, [b1])

        edgeList = [a, b, c, b1]
        expectedEdgeSetList = [set([b, c]), set(), set([b1]), set()]
        for edge, expectedEdgeSet in zip(edgeList, expectedEdgeSetList):
            actualEdgeSetList = set(g.edges[edge])
            self.assertTrue(len(expectedEdgeSet - actualEdgeSetList) == 0, "There should not be extra edges")

    def testGraphCycle(self):
        a = GraphNode('a')
        b = GraphNode('b')
        c = GraphNode('c')
        b1 = GraphNode('b1')
        b2 = GraphNode('b2')

        g = Graph(a)
        g.connect(a, [b, c])
        g.connect(c, [b1])
        g.connect(c, [b2])
        g.connect(b1, [b2])
        for _ in range(1):
            assert Graph.isCycleInGraph(g) == False
        self.assertFalse(Graph.isCycleInGraph(g), "Graph does not contain a cycle")

        g.connect(b2, [b1])
        Graph.isCycleInGraph(g)
        for i in range(1):
            assert Graph.isCycleInGraph(g) == True
        self.assertTrue(Graph.isCycleInGraph(g), "Graph contains a cycle")

    def testTopologicalSort(self):
        a = GraphNode('a')
        b = GraphNode('b')
        c = GraphNode('c')
        b1 = GraphNode('b1')
        b2 = GraphNode('b2')

        g = Graph(a)
        g.connect(a, [b, c])
        g.connect(c, [b1])
        g.connect(c, [b2])
        g.connect(b1, [b2])

        sortedList = Graph.sortGraph(g)
        i = 0
        while i < len(sortedList)-1:
            self.assertTrue(sortedList[i][1] <= sortedList[i+1][1], "List is not sorted")
            i += 1

    def testGetSortedTiers(self):
        a = GraphNode('a')
        b = GraphNode('b')
        c = GraphNode('c')
        b1 = GraphNode('b1')
        b2 = GraphNode('b2')

        g = Graph(a)
        g.connect(a, [b, c])
        g.connect(c, [b1])
        g.connect(c, [b2])
        g.connect(b1, [b2])

        tiers = Graph.getSortedTiers(g)
        expectedNodeList = [['a'], ['b', 'c'], ['b1'], ['b2']]
        for level in range(len(tiers)):
            self.assertTrue(len(expectedNodeList[level]) == len(tiers[level]), "Tier nodes have different lenghts")
            for actual in tiers[level]:
                self.assertTrue(actual[0] in expectedNodeList[level], "Unexpected node found in tier")


if __name__ == '__main__':
        a = GraphNode('a')
        b = GraphNode('b')
        c = GraphNode('c')
        b1 = GraphNode('b1')
        b2 = GraphNode('b2')

        g = Graph(a)
        g.connect(a, [b, c])
        g.connect(c, [b1])
        g.connect(c, [b2])
        g.connect(b1, [b2])
        g.connect(b2, [b1])
        print(Graph.getSortedTiers(g))

