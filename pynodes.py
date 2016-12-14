from abc import ABCMeta, abstractmethod

class Node(metaclass=ABCMeta):
    @abstractmethod
    def execute():
        # Inputs => Output
        pass

class Graph:
    # does graph stuff
    def __init__(self, root):
        # lets have a root for now and sort later.
        self.edges = {}
        self.nodes = set()
        self.root = root

    def connect(self, a, b):
        # does not check for cycles
        self.edges[a] = b
        self.edges[b] = None
        self.nodes.add(a)
        self.nodes.add(b)

    def executeGraph(self):
        node = self.root

        # does not accept args yet
        out = node.execute()
        while node in self.edges and self.edges[node] is not None:
            # assumes linked list currently
            node = self.edges[node]
            out = node.execute()
        return out

class A(Node):
    def execute(args):
        print('hello')
        return 1

class B(Node):
    def execute(args):
        if args == 1:
            print('world')
        else:
            print('words')
        return None

if __name__ == '__main__':
    a = A()
    b = B()

    g = Graph(a)
    g.connect(a, b)
    print(g.executeGraph())
