from collections import defaultdict, deque
import matplotlib.pyplot as plt
import networkx as nx
import os


def can_visit_neighbour(neighbour, visited, destination, paths, vertex):
    # if the neighbour is not visited and not the destination and the path from the source to the vertex is not empty
    return neighbour not in visited and neighbour != destination and paths[vertex] != [-1]

def get_new_path(vertex, neighbour, paths):
    # return the path from the source to the vertex + the neighbour
    return paths[vertex] + [neighbour]

def is_new_path_shorter_or_lexicographically_smaller(new_path, neighbour, paths):
    # if the path from the source to the neighbour is empty or the new path is shorter or the new path is lexicographically smaller
    return paths[neighbour] == [] or \
        len(new_path) < len(paths[neighbour]) or \
        (len(new_path) == len(paths[neighbour]) and new_path < paths[neighbour])


def bfs(graph, source, destination): 
    '''
    Returns a dictionary where the keys are the vertices and the values are the RREQ paths from the source to that vertex.
    '''
    # Initialize the paths with the source and destination vertices
    paths = defaultdict(list)
    paths[source] = [source]
    paths[destination] = [-1] # If the destination node was not found, the function returns a dictionary where all values are -1.

    # initialize the visited set and the queue
    visited, queue = set(), deque([source])
    visited.add(source)

    # BFS
    while queue:
        # pop the first vertex in the queue
        vertex = queue.popleft()
        # loop over the neighbours of the vertex
        for neighbour in sorted(graph[vertex]):
            # Check if the vertex can be visited
            if can_visit_neighbour(neighbour, visited, destination, paths, vertex):
                # get the new path
                new_path = get_new_path(vertex, neighbour, paths)
                # check if the new path is shorter or lexicographically smaller
                if is_new_path_shorter_or_lexicographically_smaller(new_path, neighbour, paths):
                    # update the path of the neighbour
                    paths[neighbour] = new_path
                    queue.append(neighbour)
                    visited.add(neighbour)
    # return the paths 
    return paths

def visualize_graph(graph, name, source=None, destination=None):
    '''
    Visualizes the graph
    '''
    # create a networkx graph
    G = nx.Graph()
    for node, neighbors in sorted(graph.items()):
        G.add_node(node)
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    
    # create the layout
    pos = nx.spring_layout(G)
    
    # set node colors
    node_colors = ['lightblue'] * len(G.nodes)
    if source is not None:
        node_colors[source-1] = 'green'
    if destination is not None:
        node_colors[destination-1] = 'red'
    
    # draw the graph
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color=node_colors)
    nx.draw_networkx_edges(G, pos, width=2, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
    
    # configure the plot
    plt.axis('off')
    # save the network in ./tests/graphs with the same name as the test case
    plt.savefig(f'./tests/graphs/{name}.png')
    # plt.show()
    # clean the plt
    plt.clf()



if __name__ == '__main__':
    # read test cases from ./tests directory
    test_cases = os.listdir('./tests')
    # remove any directories
    test_cases = [test for test in test_cases if '.' in test]
    # sort the test cases
    test_cases.sort()
    # read the expected results from ./tests/out directory
    expected_results = os.listdir('./tests/out')
    # sort the results
    expected_results.sort()
    # ----------------------------------------------------------------------
    for i, test in enumerate(test_cases):
        graph = defaultdict(list) # this line is used to create a dictionary with default values as empty list
        print(f'TEST CASE {i+1} {test}')
        # read the test case from the file
        with open(f'./tests/{test}', 'r') as f:
            nodes, edges = map(int, f.readline().split())
            for _ in range(edges):
                u, v = map(int, f.readline().split()) # there's an edge between u and v
                graph[u].append(v)
                graph[v].append(u)
            source, destination = map(int, f.readline().split()) # the nodes we want to find the shortest path between them
            print(f'Source: {source}, Destination: {destination}')
            visualize_graph(graph, test.split('.')[0], source, destination)
            paths = bfs(graph, source, destination)

    # ----------------------------------------------------------------------
            # read the expected output from the file
            with open(f'./tests/out/{expected_results[i]}', 'r') as f_expected:
                expected_paths = [list(map(int, line.strip().split())) for line in f_expected.readlines()]

    # ----------------------------------------------------------------------
            # compare the expected paths with the actual paths
            for i in range(nodes):
                if i + 1 in paths:
                    if paths[i+1] == expected_paths[i]:
                        print(' '.join(str(x) for x in paths[i + 1]), '(CORRECT)')
                    else:
                        print(' '.join(str(x) for x in paths[i + 1]), '(INCORRECT)', f'expected: {expected_paths[i]}')
                else:
                    if expected_paths[i] == [-1]:
                        print('-1', '(CORRECT)')
                    else:
                        print('-1', '(INCORRECT)')
        print('-----------------------------------')


  