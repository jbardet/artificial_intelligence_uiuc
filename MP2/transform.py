
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.

        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """
    alpha_min = arm.getArmLimit()[0][0]
    alpha_max = arm.getArmLimit()[0][1]
    beta_min = arm.getArmLimit()[1][0]
    beta_max = arm.getArmLimit()[1][1]
    offset = [alpha_min, beta_min]
    n_row = round((alpha_max-alpha_min)/granularity) + 1
    n_col = round((beta_max-beta_min)/granularity) + 1

    input_map = []
    for row in range(0, n_row) :
        column = []
        for col in range(0, n_col) :
            column.append(SPACE_CHAR)
        input_map.append(column)

    input_map[int((arm.getArmAngle()[0]-alpha_min)/granularity)][int((arm.getArmAngle()[1]-beta_min)/granularity)] = START_CHAR

    for row in range(0, n_row) :
        for col in range(0, n_col) :
            arm.setArmAngle(idxToAngle((row, col), offset, granularity))
            if doesArmTouchObjects(arm.getArmPosDist(), obstacles) :
                #input_map[row][col] = 'O'
                input_map[row][col] = WALL_CHAR
            elif isArmWithinWindow(arm.getArmPos(), window) == False :
                #input_map[row][col] = 'W'
                input_map[row][col] = WALL_CHAR
            elif doesArmTipTouchGoals(arm.getEnd(), goals) :
                input_map[row][col] = OBJECTIVE_CHAR
            elif doesArmTouchObjects(arm.getArmPosDist(), goals, isGoal=True) and not doesArmTipTouchGoals(arm.getEnd(), goals) :
                #input_map[row][col] = 'G'
                input_map[row][col] = WALL_CHAR

    return Maze(input_map, offset, granularity)
