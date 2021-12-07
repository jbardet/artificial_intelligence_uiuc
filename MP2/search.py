# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,astar)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze

from collections import deque
from heapq import heappop, heappush

def search(maze, searchMethod):
    return {
        "bfs": bfs,
    }.get(searchMethod, [])(maze)

def bfs(maze):
    # Write your code here
    """
    This function returns optimal path in a list, which contains start and objective.
    If no path found, return None.
    """
    Path = []
    Explored = []
    Frontier = []
    Parent = {}

    Objectives = maze.getObjectives()
    start = maze.getStart()
    Frontier.append(start)

    while len(Frontier) > 0 :
        parent_node = Frontier.pop(0)

        if parent_node in Explored :
            continue
        Explored.append(parent_node)

        if parent_node in Objectives :
            while parent_node != start :
                Path.insert(0, parent_node)
                parent_node = Parent[parent_node]
            Path.insert(0, start)
            return Path

        Neig = maze.getNeighbors(parent_node[0], parent_node[1])
        for j in Neig :
            if j not in Explored :
                if maze.isValidMove(j[0], j[1]) :
                    Frontier.append(j)
                    Parent[j] = parent_node

    return None
