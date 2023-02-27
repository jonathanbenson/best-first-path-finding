
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
    '''
    Prompts the user to enter an index number corresponding to
    the name of a node they want to select as either the start or destination.
    '''

    while True :

        try :

            # if the user does not enter an int, it will raise a ValueError
            index = int(input(prompt))

            # if the int the user entered is not a valid index, it will raise an IndexError
            node_name = node_names[index]

            # tell the user the node name corresponding to the index number they chose
            print(f'You chose \'{node_name}\'')
            time.sleep(1.5)

            return node_name

        except (ValueError, IndexError) :

            print(f'Error. Select a number from 0 to {len(node_names) - 1}')

            continue

def get_best_first_path(adj_dict, coord_dict, start_node, dest_node):
    '''
    Finds a path between the start and end nodes using a greedy algorithm that picks the node that is closest to the
    dest node first. If no path exists, returns an empty list.

    params :
        - adj_dict (dict): A dictionary representing the adjacency of the graph. The keys of the dictionary are the nodes
            of the graph, and the values are lists of the adjacent nodes.
        - coord_dict (dict): A dictionary representing the coordinates of the nodes in the graph. The keys of the
            dictionary are the nodes of the graph, and the values are tuples of the x and y coordinates of the node.
        - start_node (str): The starting node for the path.
        - end_node (str): The ending node for the path.

    return :
        list: A list of nodes representing the path from the start node to the end node, or an empty list if no path
        exists.

    errors :
        ValueError: If the start or end node is not in the graph.
    '''

    # calculate Euclidean distance between two coordinates
    def euclidean_distance(coord1, coord2):
        return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5

    # a networkx graph from the adjacency dictionary
    G = nx.Graph()
    G.add_nodes_from(adj_dict.keys())
    for node, neighbors in adj_dict.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor, weight=euclidean_distance(coord_dict[node], coord_dict[neighbor]))

    # a dict to keep track of the distance from start_node to each node
    distance_dict = {node: float('inf') for node in G.nodes()}
    distance_dict[start_node] = 0

    # a dict to keep track of the parent of each node in the path
    parent_dict = {node: None for node in G.nodes()}

    # init the current node and the list of visited nodes
    current_node = start_node
    visited_nodes = set()

    # loop until the current node is the dest node or there are no more nodes to visit
    while current_node != dest_node and len(visited_nodes) < len(G.nodes()):

        visited_nodes.add(current_node)

        # get the neighbor closest to the dest node
        neighbor_dists = [(n, euclidean_distance(coord_dict[n], coord_dict[dest_node])) for n in G.neighbors(current_node) if n not in visited_nodes]
        
        if not neighbor_dists:

            # if no neighbors can be reached, backtrack to the previous node
            current_node = parent_dict[current_node]
            continue

        neighbor_dists.sort(key=lambda x: x[1])
        neighbor = neighbor_dists[0][0]

        # update the distance and parent dictionaries with the new node
        distance_dict[neighbor] = distance_dict[current_node] + G[current_node][neighbor]['weight']
        parent_dict[neighbor] = current_node
        current_node = neighbor

    # if the dest node was not found, return an empty path
    if current_node != dest_node:
        return []

    # Create the path from the parent dictionary
    path = [dest_node]
    current_node = dest_node

    while current_node != start_node:
        current_node = parent_dict[current_node]
        path.append(current_node)

    # reverse the path so that it ends with the dest node    
    path.reverse()

    return path



def display_graph(adj_dict, coord_dict, path):
    '''
    Displays the graph given the adjacency and coordinate dictionaries, and a path.
    '''

    # adapt the parsed adj dict and coord dict into an nx graph
    G = nx.Graph()
    G.add_nodes_from(adj_dict.keys())

    for node, neighbors in adj_dict.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    nx.set_node_attributes(G, coord_dict, 'pos')
    pos = nx.get_node_attributes(G, 'pos')

    # dictionaries to store edge and node colors
    edge_colors = {}
    node_colors = {}
    for node in G.nodes():
        node_colors[node] = 'grey'
    for edge in G.edges():
        edge_colors[edge] = 'grey'

    # color the edges and nodes in the path with a different color
    if len(path) > 0 :
        path_edges = list(zip(path, path[1:]))

        for edge in G.edges():

            if edge in path_edges or edge[::-1] in path_edges:
                edge_colors[edge] = 'orange'
                node_colors[edge[0]] = 'orange'
                node_colors[edge[1]] = 'orange'

        # the start node is red, and the dest node is green
        node_colors[path[0]] = 'red'
        node_colors[path[-1]] = 'green'

    # display the graph
    nx.draw(G, pos, with_labels=True, edge_color=[edge_colors[edge] for edge in G.edges()], node_color=[node_colors[node] for node in G.nodes()])
    plt.show()



def main() :

    # retrieve the adjacency and coordinate dictionaries
    adj_dict = get_adj(ADJ_FILE_PATH)
    coord_dict = get_coord(COORD_FILE_PATH)

    # names of the nodes
    node_names = [k for k in coord_dict.keys()]

    # <index> - <node name>
    # a string used to show which indices go with which node names
    options = '\n'.join([str(i) + ' - ' + city_name for i, city_name in enumerate(coord_dict.keys())])

    # get start and dest node from user input
    start_node_name = get_node_name_input(node_names, f'{options}\nEnter the starting node index from the options above. ')
    dest_node_name = get_node_name_input(node_names, f'{options}\nEnter the destination node index from the options above. ')

    # compute the best-first path
    path = get_best_first_path(adj_dict, coord_dict, start_node_name, dest_node_name)

    # display the graph
    display_graph(adj_dict, coord_dict, path)

if __name__ == '__main__' :
    main()