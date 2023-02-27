
### Summary
Given information pertaining to a graph which contains the location of each node on an x-y plane and adjacencies between each node,
the program contained in `main.py` computes the shortest path between two nodes with a greedy search algorithm.

The greedy search heuristic simply picks the node closest to the destination until it either reaches the destination or a dead-end. If it reaches a 
dead-end, the search backtracks to the previous parent node and continuous the search.

### Required Python Dependencies
1. Python ^3.7
2. pytest
3. matplotlib
4. networkx

### Execution
In the project directory...
1. Run `pytest test.py` to test the project.
2. Run `python main.py` to run the program.

### Program input
1. `adjacencies.txt`
    - A file detailing the adjacencies between nodes in the graph
    - Each line contains first the node, and then the nodes it is adjacent to separated by whitespace
2. `coordinates.txt`
    - A file containing the x-y coordinate locations of the nodes in the graph
    - Each line first contains the node name, and then the x-value and y-value separated by whitespace