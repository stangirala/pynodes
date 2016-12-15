from abc import ABCMeta, abstractmethod
import concurrent.futures
import time
from collections import defaultdict

class GraphNode:
    def __init__(self, name, node=None):
        self.node = node
        self.future = None
        self.parent = []
        self.name = name

    def getName(self):
        return self.node.name

class Graph:
    # does graph stuff
    def __init__(self, root):
        # lets have a root for now and sort later.
        self.edges = defaultdict(set)
        self.nodes = set()
        self.root = GraphNode(root)
        self.edgeCounts = defaultdict(int)

    def connect(self, parentNode, childrenNodes):
        # does not check for cycles
        parentGraphNode = parentNode
        childrenGraphNodes = childrenNodes

        map(lambda x: x.parent.append(parentGraphNode), childrenGraphNodes)
        for childGraphNode in childrenGraphNodes:
            self.edgeCounts[childGraphNode] += self.edgeCounts[parentGraphNode] + 1
            self.edges[parentGraphNode].add(childGraphNode)

        self.nodes.add(parentGraphNode)
        for childGraphNode in childrenGraphNodes:
            self.nodes.add(childGraphNode)

    @staticmethod
    def executeGraph(graph):
        tiers = Graph.getSortedTiers(graph)
        tierLevels = len(tiers)

        with concurrent.futures.ProcessPoolExecutor() as executors:
            for level in xrange(tierLevels):
                for tierNode in tiers[level]:
                    if len(node.parent) == 0:
                        outFuture = executors.submit(node.execute, None)
                    else:
                        outFuture = executors.submit(node.execute, node.parent[0].future.get())
                    node.future = outFuture

                while len([tierNode for tierNode in tiers[level] if tierNode.future.done()]) != len(tiers[level]):
                    time.sleep(1)

    @staticmethod
    def sortGraph(graph):
        if Graph.isCycleInGraph(graph):
            return None

        edgeCounts = list(graph.edgeCounts.items())
        edgeCounts.sort(key=lambda x: x[1])
        return [(tup[0].name, tup[1]) for tup in edgeCounts]

    @staticmethod
    def getSortedTiers(graph):
        sortedNodes = Graph.sortGraph(graph)

        if len(sortedNodes) == 0:
            return

        sortedNodes.append((GraphNode("sentinel"), sortedNodes[-1][1]+1))
        tiers = defaultdict(list)
        tierLevel = 0
        i = 0
        while i < len(sortedNodes)-1:
            tiers[tierLevel].append(sortedNodes[i])
            if not sortedNodes[i][1] == sortedNodes[i+1][1]:
                tierLevel += 1
            i += 1

        return tiers

    @staticmethod
    def isCycleInGraph(graph, prev=None, visitedNodes=[]):
        if prev is None:
            for node in graph.nodes:
                visitedNodes.append(node)
                if Graph.isCycleInGraph(graph, node, visitedNodes):
                    return True
                del visitedNodes[-1]
            return False
        else:
            children = graph.edges[prev]
            for child in children:
                if child in visitedNodes:
                    return True
                visitedNodes.append(child)
                if Graph.isCycleInGraph(graph, child, visitedNodes):
                    return True
                del visitedNodes[-1]
            return False
