from unittest import TestCase

from graph import Graph, GraphNode

class GraphTest(TestCase):
    def generateGraph1(self):
        self.a = GraphNode('a')
        self.b = GraphNode('b')
        self.c = GraphNode('c')
        self.b1 = GraphNode('b1')
        self.b2 = GraphNode('b2')

        self.g = Graph(self.a)
        self.g.connect(self.a, [self.b, self.c])
        self.g.connect(self.c, [self.b1])
        self.g.connect(self.c, [self.b2])
        self.g.connect(self.b1, [self.b2])

    def generateGraph2(self):
        five = GraphNode('5')
        seven = GraphNode('7')
        three = GraphNode('3')
        eleven = GraphNode('11')
        eight = GraphNode('8')
        two = GraphNode('2')
        nine = GraphNode('9')
        ten = GraphNode('10')

        self.g2 = Graph(five)
        self.g2.connect(five, [eleven])
        self.g2.connect(seven, [eleven, eight])
        self.g2.connect(three, [eight, ten])
        self.g2.connect(eleven, [two, nine, ten])
        self.g2.connect(eight, [nine])

    def setUp(self):
        self.generateGraph1()

        self.generateGraph2()

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
        g = self.g
        for _ in range(1):
            assert Graph.isCycleInGraph(g) == False
        self.assertFalse(Graph.isCycleInGraph(g), "Graph does not contain a cycle")

        g.connect(self.b2, [self.b1])
        Graph.isCycleInGraph(g)
        for i in range(1):
            assert Graph.isCycleInGraph(g) == True
        self.assertTrue(Graph.isCycleInGraph(g), "Graph contains a cycle")

    def checkGraphOrdering(self, g):
        sortedList = Graph.sortGraph(g)
        i = 0
        while i < len(sortedList)-1:
            self.assertTrue(sortedList[i][1] <= sortedList[i+1][1], "List is not sorted")
            i += 1

    def testTopologicalSort(self):
        g = self.g
        self.checkGraphOrdering(g)

        g = self.g2
        self.checkGraphOrdering(g)

    def testGetSortedTiers(self):
        g = self.g

        tiers = Graph.getSortedTiers(g)
        expectedNodeList = [['a'], ['b', 'c'], ['b1'], ['b2']]
        for level in range(len(tiers)):
            self.assertTrue(len(expectedNodeList[level]) == len(tiers[level]), "Tier nodes have different lenghts")
            for actual in tiers[level]:
                self.assertTrue(actual[0].name in expectedNodeList[level], "Unexpected node found in tier")

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

