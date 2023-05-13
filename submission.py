# Name: Mostafa Wael Kamal
# Section: 2
# B.N.: 28


from collections import defaultdict, deque

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




if __name__ == '__main__':
    graph = defaultdict(list) # this line is used to create a dictionary with default values as empty list
    # read the test case from the file
    nodes, edges = map(int, input().split())
    for _ in range(edges):
        u, v = map(int, input().split()) # there's an edge between u and v
        graph[u].append(v)
        graph[v].append(u)
    source, destination = map(int, input().split()) # the nodes we want to find the shortest path between them
    paths = bfs(graph, source, destination)
    for i in range(nodes):
        if i + 1 in paths:
            print(' '.join(str(x) for x in paths[i + 1]))
        else:
            print('-1')




  