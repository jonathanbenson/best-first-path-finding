
import matplotlib.pyplot as plt
import networkx as nx
import time

ADJ_FILE_PATH = 'adjacencies.txt'
COORD_FILE_PATH = 'coordinates.txt'

def get_adj(adj_file_path) :
    '''
    Returns a dictionary that models the adjacencies.

    Each key:value pair =
    <name>: <list of adjacency names>

    Example:
    {
        'Anthony': ['Bluff_City', 'Kiowa', 'Attica', 'Harper'],
        'Attica': ['Medicine_Lodge'],
        'Augusta': ['Winfield', 'Andover', 'Leon', 'Wichita']
    }

    '''

    adj_dict = dict()

    with open(adj_file_path, 'r') as adj_reader :

        for line in adj_reader.readlines() :

            if len(line) > 1 :

                split_line = line.split()

                adj_dict[split_line[0]] = [adj.strip() for adj in split_line[1:]]

    return adj_dict

def get_coord(coord_file_path) :

    '''
    Returns a dictionary that models the coordinates of a node.

    Each key:value pair =
    <name>: (longitude, latitude)

    Example:
    {
        'Abilene': (38.9220277, -97.2666667),
        'Andover': (37.6868403, -97.1657752),
        'Anthony': (37.1575168, -98.0728946)
    }

    '''

    coord_dict = dict()

    with open(coord_file_path, 'r') as coord_reader :

        for line in coord_reader.readlines() :

            if len(line) > 1 :

                split_line = line.split()

                coord_dict[split_line[0]] = (float(split_line[1]), float(split_line[2]))

    return coord_dict

def get_node_name_input(node_names, prompt) :

    while True :

        try :

            index = int(input(prompt))

            node_name = node_names[index]

            print(f'You chose \'{node_name}\'')

            time.sleep(1.5)

            return node_name

        except (ValueError, IndexError) :

            print(f'Error. Select a number from 0 to {len(node_names) - 1}')

            continue

def greedy_path(adj_dict, coord_dict, start_node, end_node):
    # Calculate Euclidean distance between two coordinates
    def euclidean_distance(coord1, coord2):
        return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5

    # Create a networkx graph from the adjacency dictionary
    G = nx.Graph()
    G.add_nodes_from(adj_dict.keys())
    for node, neighbors in adj_dict.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor, weight=euclidean_distance(coord_dict[node], coord_dict[neighbor]))

    # Create a dictionary to keep track of the distance from start_node to each node
    distance_dict = {node: float('inf') for node in G.nodes()}
    distance_dict[start_node] = 0

    # Create a dictionary to keep track of the parent of each node in the path
    parent_dict = {node: None for node in G.nodes()}

    # Initialize the current node and the list of visited nodes
    current_node = start_node
    visited_nodes = set()

    # Loop until the current node is the end node or there are no more nodes to visit
    while current_node != end_node and len(visited_nodes) < len(G.nodes()):
        visited_nodes.add(current_node)
        # Find the neighbor closest to the end node
        neighbor_dists = [(n, euclidean_distance(coord_dict[n], coord_dict[end_node])) for n in G.neighbors(current_node) if n not in visited_nodes]
        if not neighbor_dists:
            # If no neighbors can be reached, backtrack to the previous node
            current_node = parent_dict[current_node]
            continue
        neighbor_dists.sort(key=lambda x: x[1])
        neighbor = neighbor_dists[0][0]
        # Update the distance and parent dictionaries with the new node
        distance_dict[neighbor] = distance_dict[current_node] + G[current_node][neighbor]['weight']
        parent_dict[neighbor] = current_node
        current_node = neighbor

    # If the end node was not found, return an empty path
    if current_node != end_node:
        return []

    # Create the path from the parent dictionary
    path = [end_node]
    current_node = end_node
    while current_node != start_node:
        current_node = parent_dict[current_node]
        path.append(current_node)
    path.reverse()

    return path



def display_graph(adj_dict, coord_dict, path=None):
    G = nx.Graph()
    G.add_nodes_from(adj_dict.keys())
    for node, neighbors in adj_dict.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    nx.set_node_attributes(G, coord_dict, 'pos')
    pos = nx.get_node_attributes(G, 'pos')

    # Create a dictionary to store edge and node colors
    edge_colors = {}
    node_colors = {}
    for node in G.nodes():
        node_colors[node] = 'blue'
    for edge in G.edges():
        edge_colors[edge] = 'blue'

    # Color the edges and nodes in the path with a different color
    if path:
        path_edges = list(zip(path, path[1:]))
        for edge in G.edges():
            if edge in path_edges or edge[::-1] in path_edges:
                edge_colors[edge] = 'red'
                node_colors[edge[0]] = 'red'
                node_colors[edge[1]] = 'red'
        # Color the start and destination nodes green
        node_colors[path[0]] = 'green'
        node_colors[path[-1]] = 'green'

    # Draw the graph with edge and node colors
    nx.draw(G, pos, with_labels=True, edge_color=[edge_colors[edge] for edge in G.edges()], node_color=[node_colors[node] for node in G.nodes()])
    plt.show()



def main() :

    adj_dict = get_adj(ADJ_FILE_PATH)
    coord_dict = get_coord(COORD_FILE_PATH)

    node_names = [k for k in coord_dict.keys()]
    options = '\n'.join([str(i) + ' - ' + city_name for i, city_name in enumerate(coord_dict.keys())])

    start_node_name = get_node_name_input(node_names, f'{options}\nEnter the starting city index from the options above. ')
    dest_node_name = get_node_name_input(node_names, f'{options}\nEnter the destination city index from the options above. ')

    path = greedy_path(adj_dict, coord_dict, start_node_name, dest_node_name)

    display_graph(adj_dict, coord_dict, path)

if __name__ == '__main__' :
    main()