#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import traceback

RIGHT = 0
BOTTOM = 1
LEFT = 2
TOP = 3


def printGreeting():
    program_desc = """This program will solve mazes using a recursive search."""
    print program_desc
    print "Running maze search... "


def processCommandLineArgs():
    if len(sys.argv) != 6:
        sys.stderr.write("Invalid args count; Requires 5 arguments\n")
        sys.stderr.write(
            "Usage: %s filename start_row start_col finish_row finish_col\n" % (sys.argv[0],))
        return None, None, None
    else:
        for char in sys.argv[2:]:
            if not char.isdigit():
                print "Start and Fisnish row and column must be non negative interger"
                return None, None, None
    filename, start_row, start_col, end_row, end_col = sys.argv[1:]
    return filename, (int(start_row), int(start_col)), (int(end_row), int(end_col))


def readMazeFile(filename):
    try:
        maze_file = open(filename, "r")
        data = maze_file.readlines()
        data_num = []
        for line in data:
            data_num.append([int(char)
                            for char in line.split() if char.isdigit()])
        maze_size = data_num[0]
        maze = []
        for i in range(maze_size[0]):
            row = []
            for j in range(maze_size[1]):
                row.append(data_num[i * maze_size[1] + j + 1])
            maze.append(row)
        return maze
    except:
        print traceback.print_exc()
        return None


def outsideMaze(maze, path_so_far, finish_pos):
    recent_pos = path_so_far[-1]
    if finish_pos[0] >= len(maze) or finish_pos[1] >= len(maze[0]):
        print "Finish position can't be outside maze."
        return True
    if recent_pos[0] >= len(maze) or recent_pos[1] >= len(maze[0]):
        return True


def searchMaze(maze, start_pos, finish_pos):
    path_so_far = []
    path_so_far.append(start_pos)
    if searchMazeRecurse(maze, path_so_far, finish_pos):
        return path_so_far
    else:
        return None


def searchMazeRecurse(maze, path_so_far, finish_pos):
    if outsideMaze(maze, path_so_far, finish_pos):
        return False
    if finish_pos in path_so_far:
        return True
    current_pos = path_so_far[-1]
    square = maze[current_pos[0]][current_pos[1]]
    if square[RIGHT] == 0:
        pos = (current_pos[0], current_pos[1] + 1)
        if pos not in path_so_far:
            path_so_far.append(pos)
            if searchMazeRecurse(maze, path_so_far, finish_pos):
                return True
    if square[BOTTOM] == 0:
        pos = (current_pos[0] + 1, current_pos[1])
        if pos not in path_so_far:
            path_so_far.append(pos)
            if searchMazeRecurse(maze, path_so_far, finish_pos):
                return True
    if square[LEFT] == 0:
        pos = (current_pos[0], current_pos[1] - 1)
        if pos not in path_so_far:
            path_so_far.append(pos)
            if searchMazeRecurse(maze, path_so_far, finish_pos):
                return True
    if square[TOP] == 0:
        pos = (current_pos[0] - 1, current_pos[1])
        if pos not in path_so_far:
            path_so_far.append(pos)
            if searchMazeRecurse(maze, path_so_far, finish_pos):
                return True
    miss_path = path_so_far.pop()
    return False


def printPath(paths):
    if paths is not None:
        print "Results: Found the following solution path: "
        for path in paths:
            print path
    else:
        print "Results: No solution found!"


def main():
    """
    Usage: %maze.py filename start_row start_col finish_row finish_col
    """
    printGreeting()
    # process arguments
    filename, start_pos, finish_pos = processCommandLineArgs()
    if filename == None:
        return 0
    maze = readMazeFile(filename)
    path_solution = searchMaze(maze, start_pos, finish_pos)
    printPath(path_solution)

if __name__ == "__main__":
    sys.exit(main())
