# Class for storing nodes and the distances between them.
# Ref: Joe James - Python: 2 Ways to Represent GRAPHS https://www.youtube.com/watch?v=HDUzBEG1GlA
# Above reference modified for Node and Graph class.
import csv


class Node:
    # Constructor for a new Node object.
    def __init__(self, address):
        #self.label = label
        self.address = address
        # start with a distance of positive infinity.
        #self.distance = float('inf')


class Matrix:

    nodes = {}  # node dictionary {key:value}
    edge_weights = []  # edge dictionary {key:value}
    edge_index = {}   # edge indices for lookup

    # add node to node dictionary and build out adjacency matrix template
    def add_node(self, new_node):
        self.nodes[new_node.address] = new_node
        # build out adjacency matrix template
        for row in self.edge_weights:
            row.append(0)
        self.edge_weights.append([0] * (len(self.edge_weights) + 1))
        self.edge_index[new_node.address] = len(self.edge_index)

    # distance between nodes is symmetrical, this adds the directed edge weight in both directions
    def add_undirected_edge(self, node_a, node_b, weight=1.0):
        self.edge_weights[self.edge_index[node_a.address]][self.edge_index[node_b.address]] = weight
        self.edge_weights[self.edge_index[node_b.address]][self.edge_index[node_a.address]] = weight

    def print_graph(self):
        for v, i in self.edge_index.items():
            print(str(v) + ' ', end='')
            for j in range(len(self.edge_weights)):
                print(str(self.edge_weights[i][j]) + ' ', end='')
            print(' ')


def load_nodes(csv_file, my_graph):
    counter = 0
    to_node = -1
    key_list = []
    with open(csv_file) as nodeCSV:
        reader = csv.reader(nodeCSV, delimiter=",")
        for i in reader:
            #n = Node(0, "")
            n = Node("")
            #address = i[0]
            #n.label = counter
            n.address = i[0]  #address
            my_graph.add_node(n)
            key_list.append(n)
            to_node += 1
            from_node = -1

            for j in i[1:]:
                if j == "0.0" or "":
                    break

                from_node += 1
                my_graph.add_undirected_edge(key_list[from_node], key_list[to_node], float(j))
            counter += 1


"""
def loadNodes(csv_file, myGraph):
    counter = 0
    with open(csv_file) as nodeCSV:
        reader = csv.reader(nodeCSV, delimiter=",")
        for i in reader:
            address = i[0]
            myGraph.add_node(Node(counter, address))
            counter += 1


def loadDistances(csv_file, myGraph):
    from_node = 0
    to_node = 1
    with open(csv_file) as distanceCSV:
        reader = csv.reader(distanceCSV, delimiter=",")
        for i in reader:

            for j in i[1:]:

                if j == "0.0" or "":
                    break
                myGraph.add_undirected_edge(myGraph.adjacency_list[from_node], myGraph.adjacency_list[to_node], float(j))
                to_node += 1
"""


