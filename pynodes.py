from abc import ABCMeta, abstractmethod
import concurrent.futures
import time

class Node(metaclass=ABCMeta):
    @abstractmethod
    def execute(args):
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
        with concurrent.futures.ProcessPoolExecutor() as executors:
            while node in self.edges and self.edges[node] is not None:
                # assumes linked list currently
                outFuture = executors.submit(node.execute, None)
                node = self.edges[node]
            return outFuture.result()

class A(Node):
    def execute(self, args):
        time.sleep(5)
        print('hello')
        return 1

class B(Node):
    def execute(self, args):
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
