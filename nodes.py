# Class for storing address nodes and the distances between them.
# Ref: Joe James - Python: 2 Ways to Represent GRAPHS https://www.youtube.com/watch?v=HDUzBEG1GlA
# Above reference modified for Node and Graph class.
import csv


class Node:
    def __init__(self, address):
        self.address = address


"""
Class for creation of the self-adjusting adjacency matrix
At worst this will be time and space complexity of O(n).
As the list grows, the size of the matrix matches the total amount of elements.
"""
class Matrix:
    nodes = {}  # node dictionary {key:value}
    edge_weights = []  # edge dictionary {key:value}
    edge_index = {}   # edge indices for lookup

    # Add node to node dictionary and build out adjacency matrix template
    def add_node(self, new_node):
        self.nodes[new_node.address] = new_node
        # Appends 0 to rows and columns to grow the matrix appropriately
        for row in self.edge_weights:
            row.append(0)
        self.edge_weights.append([0] * (len(self.edge_weights) + 1))
        self.edge_index[new_node.address] = len(self.edge_index)

    # Distance between nodes is symmetrical, this adds the directed edge weight in both directions
    def add_undirected_edge(self, node_a, node_b, weight=1.0):
        self.edge_weights[self.edge_index[node_a.address]][self.edge_index[node_b.address]] = weight
        self.edge_weights[self.edge_index[node_b.address]][self.edge_index[node_a.address]] = weight


# Definition to read the distance table CSV and create the adjacency matrix.
# Time and space complexity is O(n) depending on the number of elements read in from the CSV file.
def load_nodes(csv_file, my_graph):
    # Initialize destination node to -1 in order to start at 0 in the for loop.
    to_node = -1
    key_list = []
    with open(csv_file) as nodeCSV:
        reader = csv.reader(nodeCSV, delimiter=",")
        for i in reader:
            n = Node("")
            n.address = i[0]
            my_graph.add_node(n)
            key_list.append(n)
            # Destination node moves to next entry.
            to_node += 1
            # Initializes origin node to -1 so that it can start at 0 everytime the CSV is iterated through.
            from_node = -1
            """
            Distance CSV is only filled in on one side of the matrix.
            Breaks out if the "to" and "from" nodes are at the same address (Distance is zero).
            Time isn't wasted checking all the blank entries.
            """
            for j in i[1:]:
                if j == "0.0" or "":
                    break

                from_node += 1
                my_graph.add_undirected_edge(key_list[from_node], key_list[to_node], float(j))

