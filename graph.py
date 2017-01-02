from abc import ABCMeta, abstractmethod
import concurrent.futures
import time
from collections import defaultdict

class Node(metaclass=ABCMeta):
    def setName(self, name):
        self.name = name

    @abstractmethod
    def execute(self, args):
        pass

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

        for childGraphNode in childrenGraphNodes:
            childGraphNode.parent.append(parentGraphNode)
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
            for level in range(tierLevels):
                for tierNode in tiers[level]:
                    if len(tierNode[0].parent) == 0:
                        outFuture = executors.submit(tierNode[0].node.execute, None)
                    else:
                        # currently ignores other parents
                        outFuture = executors.submit(tierNode[0].node.execute, tierNode[0].parent[0].future.result())
                    tierNode[0].future = outFuture

                # Wait while tier finishes
                while len([tierNode for tierNode in tiers[level] if tierNode[0].future.done()]) != len(tiers[level]):
                    time.sleep(0.1)

    @staticmethod
    def sortGraph(graph):
        if Graph.isCycleInGraph(graph):
            return []

        edgeCounts = list(graph.edgeCounts.items())
        edgeCounts.sort(key=lambda x: x[1])
        return edgeCounts

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
