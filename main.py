
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

def display_graph(adj_dict, coord_dict):
    G = nx.Graph()
    G.add_nodes_from(adj_dict.keys())
    for node, neighbors in adj_dict.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    nx.set_node_attributes(G, coord_dict, 'pos')
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True)
    plt.show()


def main() :

    adj_dict = get_adj(ADJ_FILE_PATH)
    coord_dict = get_coord(COORD_FILE_PATH)

    node_names = [k for k in coord_dict.keys()]
    options = '\n'.join([str(i) + ' - ' + city_name for i, city_name in enumerate(coord_dict.keys())])

    start_node_name = get_node_name_input(node_names, f'{options}\nEnter the starting city index from the options above. ')
    dest_node_name = get_node_name_input(node_names, f'{options}\nEnter the destination city index from the options above. ')

    display_graph(adj_dict, coord_dict)

if __name__ == '__main__' :
    main()