from abc import ABCMeta, abstractmethod
import concurrent.futures
import time
from collections import defaultdict
import queue

from graph import Graph, GraphNode, Node

class A(Node):
    def __init__(self, val, name):
        self.val = val
        self.setName(name)

    def execute(self, args):
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

def one():
    a = GraphNode('a', A(1, 'a'))
    b = GraphNode('b', B('b'))
    c = GraphNode('c', A(2, 'c'))
    b1 = GraphNode('b1', B('b1'))
    b2 = GraphNode('b2', B('b2'))

    g = Graph(a)
    g.connect(a, [b, c])
    g.connect(c, [b1])
    g.connect(c, [b2])
    g.connect(b1, [b2])

    Graph.executeGraph(g)

    assert b2.future.result() == 'words'

def two():
    a = GraphNode('a', A(1, 'a'))
    b = GraphNode('b', B('b'))
    c = GraphNode('c', A(1, 'c'))
    b1 = GraphNode('b1', B('b1'))
    b2 = GraphNode('b2', B('b2'))

    g = Graph(a)
    g.connect(a, [b, c])
    g.connect(c, [b1])
    g.connect(c, [b2])
    g.connect(b1, [b2])

    Graph.executeGraph(g)

    assert b2.future.result() == 'world'

if __name__ == '__main__':
  one()
  two()
