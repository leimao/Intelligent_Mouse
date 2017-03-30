'''
Micromouse Maze Solver
Author: Lei Mao
Website: https://github.com/leimao/
Date: 2017/2/15
Content: Definition of maze class.
Notes: This maze class is modified from the maze class in the Udacity Machine Learning Nanodegree Capstone Project. This maze class is more advanced because it is able to tolerate rectangle mazes.
'''


import numpy as np

class Maze(object):
    def __init__(self, filename):
        '''
        Maze objects have two main attributes:
        - dim: mazes should be rectangle, with sides of even length. (integer)
        - walls: passages are coded as a 4-bit number, with a bit value taking
            0 if there is a wall and 1 if there is no wall. The 1s register
            corresponds with a square's top edge, 2s register the right edge,
            4s register the bottom edge, and 8s register the left edge. (numpy
            array)

        The initialization function also performs some consistency checks for
        wall positioning.
        '''
        with open(filename, 'rb') as f_in:

            # The first line should be integers of the maze dimensions
            dims = (f_in.next()).split(',')
            self.dim_x = int(dims[0])
            self.dim_y = int(dims[1])

            # The second line should be the x coordinates of the maze destinations
            destinations_x = np.array((f_in.next()).split(',')).astype(int)

            # The third line should be the y coordinates of the maze destinations
            destinations_y = np.array((f_in.next()).split(',')).astype(int)

            # Examine the destinations of the maze
            if len(destinations_x) != len(destinations_y):
                raise Exception('Maze destinations coordinates not paired!')
            for x in destinations_x:
                if x > self.dim_x - 1:
                    raise Exception('Maze destinations x coordinates exception!')
            for y in destinations_y:
                if y > self.dim_y - 1:
                    raise Exception('Maze destinations y coordinates exception!')

            # Save the coordinates of the maze
            self.destinations = list()
            for x, y in zip(destinations_x, destinations_y):
                self.destinations.append([x,y])

            # Subsequent lines describe the permissability of walls
            walls = []
            for line in f_in:
                walls.append(map(int,line.split(',')))
            self.walls = np.array(walls)

        # Perform validation on maze
        # Maze dimensions
        # That the maze dimensions have to be even in length is simply due to the convenience during maze visualization.
        if (self.dim_x % 2) or (self.dim_y % 2):
            raise Exception('Maze dimensions must be even in length!')
        if self.walls.shape != (self.dim_x, self.dim_y):
            raise Exception('Maze shape does not match dimension attribute!')

        # Wall permeability
        wall_errors = []
        # vertical walls
        for x in range(self.dim_x-1):
            for y in range(self.dim_y):
                if (self.walls[x,y] & 2 != 0) != (self.walls[x+1,y] & 8 != 0):
                    wall_errors.append([(x,y), 'v'])
        # horizontal walls
        for y in range(self.dim_y-1):
            for x in range(self.dim_x):
                if (self.walls[x,y] & 1 != 0) != (self.walls[x,y+1] & 4 != 0):
                    wall_errors.append([(x,y), 'h'])

        if wall_errors:
            for cell, wall_type in wall_errors:
                if wall_type == 'v':
                    cell2 = (cell[0]+1, cell[1])
                    print 'Inconsistent vertical wall betweeen {} and {}'.format(cell, cell2)
                else:
                    cell2 = (cell[0], cell[1]+1)
                    print 'Inconsistent horizontal wall betweeen {} and {}'.format(cell, cell2)
            raise Exception('Consistency errors found in wall specifications!')


    def is_permissible(self, cell, direction):
        """
        Returns a boolean designating whether or not a cell is passable in the
        given direction. Cell is input as a list. Directions may be
        input as single letter 'u', 'r', 'd', 'l', or complete words 'up', 
        'right', 'down', 'left'.
        """
        dir_int = {'u': 1, 'r': 2, 'd': 4, 'l': 8,
                   'up': 1, 'right': 2, 'down': 4, 'left': 8}
        try:
            """if permissible: return 1 else return 0"""
            return (self.walls[tuple(cell)] & dir_int[direction] != 0)
        except:
            print 'Invalid direction provided!'


    def dist_to_wall(self, cell, direction):
        """
        Returns a number designating the number of open cells to the nearest
        wall in the indicated direction. Cell is input as a list. Directions
        may be input as a single letter 'u', 'r', 'd', 'l', or complete words
        'up', 'right', 'down', 'left'.
        """
        dir_move = {'u': [0, 1], 'r': [1, 0], 'd': [0, -1], 'l': [-1, 0],
                    'up': [0, 1], 'right': [1, 0], 'down': [0, -1], 'left': [-1, 0]}

        sensing = True
        distance = 0
        curr_cell = list(cell) # make copy to preserve original
        while sensing:
            if self.is_permissible(curr_cell, direction):
                distance += 1
                curr_cell[0] += dir_move[direction][0]
                curr_cell[1] += dir_move[direction][1]
            else:
                sensing = False
        return distance



class Maze_Learned(object):
    def __init__(self, size_max = 100):
        '''
        Initialized the Maze_Learned objects to a numpy matrix with a size of size_max x size_max, representing all grid has wall at four directions.
        '''
        # Put walls everywhere in the maze
        self.walls = np.zeros((size_max, size_max), dtype=np.int32)

    def is_permissible(self, cell, direction):
        """
        Returns a boolean designating whether or not a cell is passable in the
        given direction. Cell is input as a list. Directions may be
        input as single letter 'u', 'r', 'd', 'l', or complete words 'up', 
        'right', 'down', 'left'.
        """
        dir_int = {'u': 1, 'r': 2, 'd': 4, 'l': 8,
                   'up': 1, 'right': 2, 'down': 4, 'left': 8}
        try:
            """if permissible: return 1 else return 0"""
            return (self.walls[tuple(cell)] & dir_int[direction] != 0)
        except:
            print 'Invalid direction provided!'


    def dist_to_wall(self, cell, direction):
        """
        Returns a number designating the number of open cells to the nearest
        wall in the indicated direction. Cell is input as a list. Directions
        may be input as a single letter 'u', 'r', 'd', 'l', or complete words
        'up', 'right', 'down', 'left'.
        """
        dir_move = {'u': [0, 1], 'r': [1, 0], 'd': [0, -1], 'l': [-1, 0],
                    'up': [0, 1], 'right': [1, 0], 'down': [0, -1], 'left': [-1, 0]}

        sensing = True
        distance = 0
        curr_cell = list(cell) # make copy to preserve original
        while sensing:
            if self.is_permissible(curr_cell, direction):
                distance += 1
                curr_cell[0] += dir_move[direction][0]
                curr_cell[1] += dir_move[direction][1]
            else:
                sensing = False
        return distance
