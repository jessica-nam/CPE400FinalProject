# The team will simulate a mesh network where nodes and links may fail (Figure 5). Nodes and links may fail intermittently, as an input to the simulation, each node and link will have a certain probability to fail. When such failure occurs, the network must adapt and re-route to avoid the faulty link/node.

from collections import defaultdict
import random

# Node names (represents vertices in the graph)
nodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]

# Graph (keys = node, value = connected nodes)
graph = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "D"],
    "D": ["B", "C", "E", "F"],
    "E": ["D", "G"],
    "F": ["D", "G", "H"],
    "G": ["E", "F"],
    "H": ["F", "I"],
    "I": ["H", "J", "K"],
    "J": ["I", "K", "L"],
    "K": ["I", "J", "L", "M", "N"],
    "L": ["J", "K", "N"],
    "M": ["K", "N"],
    "N": ["K", "L", "M"]
}

def simulate_failures(graph, probability):
    """ Simulate link failures in the graph based on the given probability. """

    # New graph with empty connections (will fill this later)
    updated_graph = defaultdict(list) # Using defaultdict here to automatically create lists for missing keys

    # Go through the nodes and its neighbors in old graph
    for node, neighbors in graph.items():
        # This list will store the neighbors that remain connected after failure
        connected_neighbors = []
        # Iterate through each neighbor of the node we are looking at right now
        for neighbor in neighbors:
            # Generate random number from 0 to 1 and if it is greater than probability of failure...
            if random.random() > probability:
                connected_neighbors.append(neighbor) # The node and its neighbor are still connected so we add the neighbor to the list

        # If there are no connections after failure...
        if not connected_neighbors:
            connected_neighbors.append(random.choice(neighbors)) # Randomly choose a neighbor to stay connected

        # Update new graph with the connected neighbors
        updated_graph[node] = connected_neighbors
        # Update reverse connections because graph should be bidirectional
        for connected_neighbor in connected_neighbors:
            updated_graph[connected_neighbor].append(node)
    
    # output which link is broken 

    # Return graph with simulated link failures
    return updated_graph


def dijkstras_unweighted(graph, start_node):
    unvisited = []
    for node in graph:
        unvisited.append(node)
    unvisited.remove(start_node)

    #Just initializing all the paths
    table = {}
    for node in graph:
        table[node] = [None, None, None, None, None, None, None, None, None, None]
    table[start_node] = []
    current_node = start_node

    #Running through dijkstras now
    while len(unvisited) > 0:
        #This makes a list of adjacent nodes that are also unvisited
        adjacent_nodes = [node for node in graph[current_node] if node in unvisited]

        #This adds the node into the table
        for node in adjacent_nodes:
            if None in table[node] or len(table[current_node])+1 < len(table[node]):
              table[node] = table[current_node].copy()
              table[node].append(node)
        
        #This makes current_node the minimum unvisited node
        current_node = unvisited[0]
        for node in unvisited:
            if len(table[current_node]) > len(table[node]):
              current_node = node

        #This removes the current_node from the unvisited list
        unvisited.remove(current_node)
    
    return table

def main():
    # User inputs values for path search
    start_node = input("\nInput the start node: ")
    end_node = input("Input the end node: ")
    probability = float(input("Input the probability of a node/link breaking: "))

    # User user's given probability to simulate failures
    updated_graph = simulate_failures(graph, probability)
    # Calculate the shortest path distance on updated failure graph
    distance_table = dijkstras_unweighted(updated_graph, start_node)

    # Find distance between start and end nodes in distance table from dijkstras
    distance = distance_table[end_node]
    # If a path is found and the distance is not 999999 (represents infinity), then a path exists
    if distance != 999999:
        print(f"\nShortest path distance: {distance}")
    else:
        print("\nNo path found.")

if __name__ == "__main__":
    main()
