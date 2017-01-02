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
        if args[0] == 1:
            return 'world'
        elif len(args) > 1 and args[1] == 1:
            return 'words'
        else:
            return 'heckles'

def one():
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

def two():
    a = GraphNode('a', A(1, 'a'))
    b = GraphNode('b', B('b'))
    c = GraphNode('c', A(1, 'c'))
    b1 = GraphNode('b1', A(1, 'b1'))
    b2 = GraphNode('b2', B('b2'))

    g = Graph(a)
    g.connect(a, [b, c])
    g.connect(c, [b1])
    g.connect(c, [b2])
    g.connect(b1, [b2])

    Graph.executeGraph(g)

    assert b2.future.result() == 'world'

def three():
    a = GraphNode('a', A(1, 'a'))
    b = GraphNode('b', B('b'))
    c = GraphNode('c', A(9, 'c'))
    b1 = GraphNode('b1', A(2, 'b1'))
    b2 = GraphNode('b2', B('b2'))

    g = Graph(a)
    g.connect(a, [b, c])
    g.connect(c, [b1])
    g.connect(c, [b2])
    g.connect(b1, [b2])

    Graph.executeGraph(g)

    assert b2.future.result() == 'heckles'

if __name__ == '__main__':
  one()
  two()
  three()
