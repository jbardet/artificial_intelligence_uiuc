# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,extra)

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "extra": extra,
    }.get(searchMethod)(maze)

class Node :
    def __init__(self, I, P) :
        self.I = I
        self.P = P

class Node2 :
    def __init__(self, I, P, O) :
        self.I = I
        self.P = P
        self.O = O
    f = 0
    g = 0

def mst_astar(targets, edgesSo):
    targ = list(targets)
    G = {}
    edges = []
    edgesSorted = []
    for (c, n1, n2) in edgesSo:
        if n1 in targ and n2 in targ:
            edgesSorted.append((c-1, n1, n2))
    nodesMst = []

    i = 0
    cost = 0
    vis = 0

    while vis != len(targets):
        minEdge = edgesSorted[i]
        i+=1

        try:
            if minEdge[1] in G[minEdge[2]] or minEdge[2] in G[minEdge[1]]:
                continue
            else:
                cost += minEdge[0]

                if minEdge[1] in nodesMst and minEdge[2] not in nodesMst:
                    G[minEdge[2]] = set()
                    G[minEdge[2]].add(minEdge[2])
                    nodesMst.append(minEdge[2])
                if minEdge[2] in nodesMst and minEdge[1] not in nodesMst:
                    G[minEdge[1]] = set()
                    G[minEdge[1]].add(minEdge[1])
                    nodesMst.append(minEdge[1])
                if minEdge[1] not in nodesMst and minEdge[2] not in nodesMst:
                    G[minEdge[1]] = set()
                    G[minEdge[2]] = set()
                    G[minEdge[1]].add(minEdge[1])
                    G[minEdge[2]].add(minEdge[2])
                    nodesMst.append(minEdge[1])
                    nodesMst.append(minEdge[2])

                G[minEdge[1]] = G[minEdge[1]].union(G[minEdge[2]])
                G[minEdge[2]] = G[minEdge[1]]

                for link in G[minEdge[1]]:
                    G[link] = G[link].union(G[minEdge[1]])
                for link in G[minEdge[2]]:
                    G[link] = G[link].union(G[minEdge[2]])
        except KeyError:
            cost += minEdge[0]
            if minEdge[1] in nodesMst and minEdge[2] not in nodesMst:
                G[minEdge[2]] = set()
                G[minEdge[2]].add(minEdge[2])
                nodesMst.append(minEdge[2])
            if minEdge[2] in nodesMst and minEdge[1] not in nodesMst:
                G[minEdge[1]] = set()
                G[minEdge[1]].add(minEdge[1])
                nodesMst.append(minEdge[1])
            if minEdge[1] not in nodesMst and minEdge[2] not in nodesMst:
                G[minEdge[1]] = set()
                G[minEdge[2]] = set()
                G[minEdge[1]].add(minEdge[1])
                G[minEdge[2]].add(minEdge[2])
                nodesMst.append(minEdge[1])
                nodesMst.append(minEdge[2])

            G[minEdge[1]] = G[minEdge[1]].union(G[minEdge[2]])
            G[minEdge[2]] = G[minEdge[1]]

            for link in G[minEdge[1]]:
                G[link] = G[link].union(G[minEdge[1]])
            for link in G[minEdge[2]]:
                G[link] = G[link].union(G[minEdge[2]])
        if (len(nodesMst) == len(targets)):
            vis = len(G[nodesMst[0]])

    return cost

def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    Path = []
    Explored = []
    Frontier = []
    score = 1

    start = maze.getStart()
    Frontier.append(start)
    Explored.append(start)
    node = [Node(start, None)]
    node.append(Node(start, None))

    while len(Frontier) > 0 :
        node.remove(node[0])
        parent_node = node[0]
        Neig = maze.getNeighbors(Frontier[0][0], Frontier[0][1])
        for j in Neig :
            if j not in Explored :
                Frontier.append(j)
                Explored.append(j)
                node.append(Node(j, parent_node))
        if Frontier[0] == maze.getObjectives()[0] :
            Frontier.remove(Frontier[0])
            break
        else :
            Frontier.remove(Frontier[0])

    while parent_node.I != maze.getStart() :
        Path.append(parent_node.I)
        parent_node = parent_node.P
        score = score+1

    Path.append(maze.getStart())
    Path.reverse()

    return Path

def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    Path = []
    Explored = []
    Frontier = []
    g = 0

    start = maze.getStart()
    Frontier.append(start)
    Explored.append(start)
    node = [Node(start, None)]
    node.append(Node(start, None))
    node[-1].g = 0

    node[-1].f = (abs(maze.getStart()[0]-maze.getObjectives()[0][0])
     + abs(maze.getStart()[1]-maze.getObjectives()[0][1]))

    while len(Frontier) > 0 :
        node.remove(node[0])
        move_f = Frontier[0]
        move_n = node[0]
        initialize = node[0].f
        for i in node :
            if i.f < initialize :
                Frontier[Frontier.index(i.I)] = move_f
                Frontier[0] = i.I
                node[node.index(i)] = move_n
                node[0] = i
                initialize = i.f
        parent_node = node[0]
        g = parent_node.g + 1
        Neig = maze.getNeighbors(Frontier[0][0], Frontier[0][1])
        for j in Neig :
            if j not in Explored :
                m = abs(j[0]-maze.getObjectives()[0][0]) + abs(j[1]-maze.getObjectives()[0][1])
                f = g + m
                Frontier.append(j)
                Explored.append(j)
                node.append(Node(j, parent_node))
                node[-1].f = f
                node[-1].g = g
        if Frontier[0] == maze.getObjectives()[0] :
            Frontier.remove(Frontier[0])
            break
        else :
            Frontier.remove(Frontier[0])

    while parent_node.I != maze.getStart() :
        Path.append(parent_node.I)
        parent_node = parent_node.P
    Path.append(maze.getStart())
    Path.reverse()

    return Path

def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here
    Path = []
    Explored = []
    g = 0

    start = maze.getStart()
    node = [Node2(start, None, maze.getObjectives()), Node2(start, None, maze.getObjectives())]

    while len(node[-1].O) > 0 :
        node.remove(node[0])
        move = node[0]
        initialize = node[0].f

        for i in node :
            if i.f < initialize :
                node[node.index(i)] = move
                node[0] = i
                initialize = i.f
                move = node[0]
                initialize = node[0].f

        for i in node :
            if i.f == initialize :
                if i.g > node[0].g :
                    node[node.index(i)] = move
                    node[0] = i
                    initialize = i.f
                    move = node[0]
                    initialize = node[0].f
        Neig = maze.getNeighbors(node[0].I[0], node[0].I[1])
        parent_node = node[0]
        g = node[0].g + 1

        for i in Explored :
            for j in Neig :
                if j == i.I :
                    if parent_node.O == i.O :
                        Neig.remove(j)

        for j in Neig :
            distance = float("inf")
            node.append(Node2(j, parent_node, parent_node.O))
            Explored.append(node[-1])
            for i in node[-1].O :
                heuristic = (abs(j[0] - i[0]) + abs(j[1] - i[1]))
                if heuristic < distance :
                    distance = heuristic
            node[-1].g = g
            node[-1].f = g + distance + (len(node[-1].O)-1)*(maze.getDimensions()[0]-3)

        for k in node :
            for l in k.O :
                if k.I == l :
                    obj = k.O.copy()
                    obj.remove(l)
                    node.append(Node2(k.I, k.P , obj))
                    distance = float("inf")
                    if len(node[-1].O) > 0 :
                        for j in node[-1].O :
                            heuristic = (abs(node[-1].I[0] - j[0]) + abs(node[-1].I[1] - j[1]))
                            if heuristic < distance :
                                distance = heuristic
                        node[-1].f = g + distance + (len(node[-1].O)-1)*(maze.getDimensions()[0]-3)

    Path.append(node[-1].I)
    while ((parent_node.I != maze.getStart()) or (len(parent_node.O) != 4)):
        Path.append(parent_node.I)
        parent_node = parent_node.P
    Path.append(maze.getStart())
    Path.reverse()

    return Path

def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here

    Path = []
    Explored = []
    g = 0
    MST = []
    Objectives = maze.getObjectives()
    Heuristic = {}

    for i in Objectives :
        for j in Objectives :
             if j != i :
                heuristic = abs(i[0] - j[0]) + abs(i[1] - j[1])
                MST.append([heuristic, i, j])
    for i in MST :
        for j in MST :
            if (i[1] == j[2]) and (i[2] == j[1]) :
                MST.remove(j)

    MST.sort()
    start = maze.getStart()
    node = [Node2(start, None, maze.getObjectives()), Node2(start, None, maze.getObjectives())]

    Heuristic[tuple(maze.getObjectives())] = mst_astar(node[0].O, MST)

    while len(node[-1].O) > 0 :
        node.remove(node[0])
        move = node[0]
        initialize = node[0].f

        for i in node :
            if i.f < initialize :
                node[node.index(i)] = move
                node[0] = i
                initialize = i.f
                move = node[0]
                initialize = node[0].f

        for i in node :
            if i.f == initialize :
                if i.g > node[0].g :
                    node[node.index(i)] = move
                    node[0] = i
                    initialize = i.f
                    move = node[0]
                    initialize = node[0].f

        Neig = maze.getNeighbors(node[0].I[0], node[0].I[1])
        parent_node = node[0]
        g = node[0].g + 1

        for l in node[0].O :
            if node[0].I == l :
                node[0].O.remove(l)

        for i in Explored :
            for j in Neig :
                if j == i.I and parent_node.O == i.O :
                    Neig.remove(j)

        for j in Neig :

            distance = float("inf")
            curr = Node2(j, parent_node, (parent_node.O).copy())

            for i in curr.O :
                heuristic = (abs(j[0] - i[0]) + abs(j[1] - i[1]))
                if heuristic < distance :
                    distance = heuristic
            curr.g = g

            try:
                hmst = Heuristic[tuple(curr.O)]
            except KeyError:
                if len(curr.O) < 2:
                    hmst = 0
                else:
                    #In order to compute the mediumSearch in time (<6min) I had to give
                    #more value to the heuristic with the MST, so that's why the factor 3
                    #stands here. For tinySearch and smallSearch we can remove this factor.
                    hmst = (mst_astar((curr.O).copy(), MST))*3
                    Heuristic[tuple(curr.O)] = hmst
            curr.f = g + distance + hmst

            node.append(curr)
        Explored.append(node[0])

    Path.append(node[-1].I)
    while ((parent_node != None and parent_node.I != maze.getStart()) or (parent_node != None and len(parent_node.O) != len(maze.getObjectives()))) :
        Path.append(parent_node.I)
        parent_node = parent_node.P
    Path.append(maze.getStart())
    Path.reverse()

    return Path


def extra(maze):
    """
    Runs extra credit suggestion.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []
