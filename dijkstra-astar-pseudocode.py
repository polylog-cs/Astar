


A*

open_nodes = {start}
closed_nodes = {}

while open_nodes not empty:
    cur_node = remove from open_nodes the one with min dist(start, node) + heuristic(node)

    # open all neighbors
    for neighbor in neighbors of cur_node:
        if neighbor not in closed_nodes:
            put neighbor in open_nodes

    closed_nodes.add(cur_node)



Dijsktra with potentials

open_nodes = {start}
closed_nodes = {}

while open_nodes not empty:
    cur_node = remove from open_nodes the node minimizing dist(start, node) + potential(node) - potential(start)

    # open all neighbors
    for neighbor in neighbors of cur_node:
        if neighbor not in closed_nodes:
            put neighbor in open_nodes, 
            update its distance as:
                dist[neighbor] = min(dist[neighbor], dist[cur_node] + length(cur_node, neighbor) + potential(neighbor) - potential(cur_node))

    closed_nodes.add(cur_node)

    

def Dijsktra(start, end)

    def potential(node):
        return sqrt( (node.x - end.x)^2 + (node.y - end.y)^2 ))

    for (u,v) in edges:
        length(u, v) = length(u, v) + potential(v) - potential(u) 

    open_nodes = {start}
    closed_nodes = {}

    while open_nodes not empty:
        cur_node = remove from open_nodes the node minimizing dist[node]
        if cur_node == end:
            return
        closed_nodes.add(cur_node)

        # open all neighbors
        for neighbor in neighbors of cur_node:
            if neighbor not in closed_nodes:
                put neighbor in open_nodes if it is not there already, 
                dist[neighbor] = min(dist[neighbor], dist[cur_node] + length(cur_node, neighbor) )







def Astar(start, end):
    
    def potential(node):
        return sqrt( (node.x - end.x)^2 + (node.y - end.y)^2)

    # potential reweighting
    # for (u,v) in edges:
    #     length(u,v) += potential(v) - potential(u)

    open_nodes = {start}
    closed_nodes = {}

    while open_nodes not empty:
        cur_node = remove from open_nodes the node minimizing dist[node] + potential(node) 
        if cur_node = end:
            return
        closed_nodes.add(cur_node)

        # open all neighbors
        for neighbor in neighbors of cur_node:
            if neighbor not in closed_nodes:
                put neighbor in open_nodes if it is not already there
                dist[neighbor] = min(dist[neighbor], dist[cur_node] + length(cur_node, neighbor))




def sqrt():
    pass
def argmin():
    pass

# A* pseudocode
def Astar(G, start, end):
    #PART 1: Compute clever potentials
    def potential(node):
        return sqrt( (node.x - end.x)^2 + (node.y - end.y)^2)

    #PART 2: Potential reweighting
    for edge in G.edges:
        edge.length += potential(edge[1]) - potential(edge[0])

    #PART 3: Run Dijkstra
    open_nodes = [start]
    closed_nodes = []
    distances = {}
    while open_nodes != []:
        # always remove the currently closest node
        cur_node = argmin(open_nodes, lambda node: distances[node] )

        open_nodes.remove(cur_node)
        closed_nodes.append(cur_node)
        if cur_node == end:
            return distances[end]
        # relax all neighbors
        for neighbor, edge_length in cur_node.neighbors:
            distances[neighbor] = min(distances[neighbor], distances[cur_node] + edge_length)
            if neighbor not in closed_nodes and neighbor not in open_nodes:
                open_nodes.append(neighbor)
                
    return -1



# A* pseudocode
def Astar(G, start, end):
    #PART 1: Compute clever potentials
    def potential(node):
        return sqrt( (node.x - end.x)^2 + (node.y - end.y)^2)

    #PART 2: Potential reweighting
    # for edge in G.edges:
    #     edge.length += potential(edge[1]) - potential(edge[0])

    #PART 3: Run Dijkstra
    open_nodes = [start]
    closed_nodes = []
    distances = {}
    while open_nodes != []:
        # always remove the currently closest node
        cur_node = argmin(open_nodes, lambda node: distances[node] + potential(node) - potential(start) )

        open_nodes.remove(cur_node)
        closed_nodes.append(cur_node)
        if cur_node == end:
            return distances[end]
        # relax all neighbors
        for neighbor, edge_length in cur_node.neighbors:
            distances[neighbor] = min(distances[neighbor], distances[cur_node] + edge_length)
            if neighbor not in closed_nodes and neighbor not in open_nodes:
                open_nodes.append(neighbor)
                
    return -1




# A* pseudocode
def Astar(G, start, end):
    #PART 1: Compute clever potentials
    def potential(node):
        return sqrt( (node.x - end.x)^2 + (node.y - end.y)^2)

    #PART 2: Potential reweighting
    # for edge in G.edges:
    #     edge.length += potential(edge[1]) - potential(edge[0])

    #PART 3: Run Dijkstra
    open_nodes = [start]
    closed_nodes = []
    distances = {}
    while open_nodes != []:
        # always remove the currently closest node
        cur_node = argmin(open_nodes, lambda node: distances[node] + potential(node) )

        open_nodes.remove(cur_node)
        closed_nodes.append(cur_node)
        if cur_node == end:
            return distances[end]
        # relax all neighbors
        for neighbor, edge_length in cur_node.neighbors:
            distances[neighbor] = min(distances[neighbor], distances[cur_node] + edge_length)
            if neighbor not in closed_nodes and neighbor not in open_nodes:
                open_nodes.append(neighbor)
                
    return -1






























    