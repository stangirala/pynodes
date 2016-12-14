from abc import ABCMeta, abstractmethod
import concurrent.futures
import time
from collections import defaultdict
import queue

from graph import Graph, GraphNode

class Node(metaclass=ABCMeta):
    def setName(self, name):
        self.name = name

    @abstractmethod
    def execute(args):
        # Inputs => Output
        pass

class A(Node):
    def __init__(self, val, name):
        self.val = val
        self.setName(name)
    def execute(self):
        if self.val == 1:
            return 1
        else:
            return 0

class B(Node):
    def __init__(self, name):
        self.setName(name)

    def execute(self, args):
        if args == 1:
            return 'world'
        else:
            return 'words'

class C(Node):
    def __init__(self, name):
        self.setName(name)

    def execute(self, args):
        if args == 1:
            print('world')
        else:
            print('words')
        return None

if __name__ == '__main__':
    a = GraphNode(A(1, 'a'))
    b = GraphNode(B('b'))
    c = GraphNode(A(2, 'c'))
    b1 = GraphNode(B('b1'))
    b2 = GraphNode(B('b2'))

    g = Graph(a)
    g.connect(a, [b, c])
    g.connect(c, [b1])
    g.connect(c, [b2])
    g.connect(b1, [b2])
    g.connect(b2, [b1])

    #print(g.executeGraph())
    print(Graph.sortGraph(g))
    print(Graph.isCycleInGraph(g))
