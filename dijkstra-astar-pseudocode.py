


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








































    