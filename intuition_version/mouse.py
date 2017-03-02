'''
Micromouse Maze Solver
Author: Lei Mao
Website: https://github.com/leimao/
Date: 2017/2/15
Content: Maze exploration micromouse controller. The intention of this controller is to explore the maze as much as possible in minimum number of steps.
'''
import numpy as np
import random
import sys
from maze import Maze
from maze import Maze_Learned
from planner import best_path
from planner import length_count
from observer import orientation_observed
from observer import coordinate_observed
from observer import destination_expectation


class Mouse(object):
    def __init__(self, memory_size = 100, movements = [0,1,2,3], heuristic = True, intuition = False):
        # Initialize Mouse object
        self.maze_learned = Maze_Learned(size_max = memory_size)
        self.maze_visited = np.zeros((memory_size, memory_size), dtype = np.int32)
        # Dimension of the memories
        self.dim_x = memory_size
        self.dim_y = memory_size
        # The location of mouse in mouse's memory
        self.location_defined = [memory_size/2, memory_size/2]
        self.maze_visited[tuple(self.location_defined)] = 1
        # The orientation of mouse in mouse's memory
        self.orientation = 'up'
        # Set the orientation of mouse when it was put into the maze as 'up' in mouse's memory
        self.location_reference = self.location_defined[:]
        self.orientation_reference = 'up'
        # The movement of mouse allowed in each action
        self.movements = movements
        # Found the final destination
        self.found_destination = False
        # Starting point memorized
        self.starting = [memory_size/2, memory_size/2]
        # Final destination memorized
        self.destinations = list()
        # Heuristic destination candidates selection
        self.heuristic = heuristic
        # Percentage of visited maze
        self.percentage_visited = 0
        # Use intuition
        self.intuition = intuition

    def obstacle_sensor(self, maze, location_real, orientation_real):
        '''
        Measure the distance to the obstacles from the four sensors on the micromouse. Here I am using four sensors because I want to generalize my micromouse to any maze, any starting point and destination. Theoretically, having four sensors is equivalent to having three sensors.
        maze: Maze class. Real whole maze information.
        location: coordinates of current real location. The micromouse does not know its real location.
        return: a list of distance information from the up, down, left and right in mouse memory.
        '''
        # Prepare directions dictionary in order
        directions_dict = {'up':['up','down','left','right'], 'down':['down','up','right','left'],'left':['left','right','down','up'],'right':['right','left','up','down']}
        directions = directions_dict[orientation_real]
        # The distance information in real maze
        distances_real = list()
        for direction in directions:
            distances_real.append(maze.dist_to_wall(cell = tuple(location_real), direction = direction))
        # The distance adusted for mouse's memory given the orientation_reference is 'up'
        distance_defined = list()
        if self.orientation_reference == 'up':
            if self.orientation == 'up':
                distance_defined = [distances_real[0], distances_real[1], distances_real[2], distances_real[3]]
            elif self.orientation == 'down':
                distance_defined = [distances_real[1], distances_real[0], distances_real[3], distances_real[2]]
            elif self.orientation == 'left':
                distance_defined = [distances_real[3], distances_real[2], distances_real[0], distances_real[1]]
            elif self.orientation == 'right':
                distance_defined = [distances_real[2], distances_real[3], distances_real[1], distances_real[0]]
        else:
            raise Exception('Orientation reference other than up is not defined.')
            
        return distance_defined
        
    def learn_maze(self, distances_defined):
        '''
        Learn to depict maze using the sensor and location information.
        distances_defined: a list of distance to the mouse_defined up, down, left, right obstacles.
        location_defined: coordinates of current location that the micromouse defined.
        maze_learned: the wall information of maze that the mouse has learned. For this maze, there is something special here. The maze_learned for the micromouse was initialized with a maze of certain size large enough where there is four walls in each grid. The micromouse would erase the wall with the information from the sensor. Passages are coded as a 4-bit number, with a bit value taking 0 if there is a wall and 1 if there is no wall. The 1s register corresponds with a square's top edge, 2s register the right edge, 4s register the bottom edge, and 8s register the left edge (The same to maze.walls).
        return: an updated maze_learned.
        '''
        # Learn the maze
        # orientation_defined: up
        for y in xrange(self.location_defined[1], self.location_defined[1] + distances_defined[0]):
            self.maze_learned.walls[self.location_defined[0]][y] = (self.maze_learned.walls[self.location_defined[0]][y]|1)
        for y in xrange(self.location_defined[1] + 1, self.location_defined[1] + distances_defined[0] + 1):
            self.maze_learned.walls[self.location_defined[0]][y] = (self.maze_learned.walls[self.location_defined[0]][y]|4)
        # orientation_defined: down
        for y in xrange(self.location_defined[1] - distances_defined[1] + 1, self.location_defined[1] + 1):
            self.maze_learned.walls[self.location_defined[0]][y] = (self.maze_learned.walls[self.location_defined[0]][y]|4)
        for y in xrange(self.location_defined[1] - distances_defined[1], self.location_defined[1]):
            self.maze_learned.walls[self.location_defined[0]][y] = (self.maze_learned.walls[self.location_defined[0]][y]|1)
        # orientation_defined: left
        for x in xrange(self.location_defined[0] - distances_defined[2] + 1, self.location_defined[0] + 1):
            self.maze_learned.walls[x][self.location_defined[1]] = (self.maze_learned.walls[x][self.location_defined[1]]|8)
        for x in xrange(self.location_defined[0] - distances_defined[2], self.location_defined[0]):
            self.maze_learned.walls[x][self.location_defined[1]] = (self.maze_learned.walls[x][self.location_defined[1]]|2)
        # orientation_defined: right
        for x in xrange(self.location_defined[0], self.location_defined[0] + distances_defined[3]):
            self.maze_learned.walls[x][self.location_defined[1]] = (self.maze_learned.walls[x][self.location_defined[1]]|2)
        for x in xrange(self.location_defined[0] + 1, self.location_defined[0] + distances_defined[3] + 1):
            self.maze_learned.walls[x][self.location_defined[1]] = (self.maze_learned.walls[x][self.location_defined[1]]|8)

    def destination_next(self):
        '''
        Choose a destination for the action based on the maze learned.
        The next destination candidates are among the unvisited grids in mouse's memory which has at most three walls.
        Calculate the number of actions, length of movement for the mouse moving to each of the destination candidates.
        Choose the destination that takes the least number of actions. If the number of actions are the same, choose the destination that takes the smallest length of movement. If the length of movement is the same, just randomly pick one.
        '''
        # Find out destination candidates
        destination_candidates = list()
        for x in xrange(self.dim_x):
            for y in xrange(self.dim_y):
                # Check whether the grid does not have four walls
                if self.maze_learned.walls[x][y] != 0:
                    # Check whether the grid has been visited
                    if self.maze_visited[x][y] == 0:
                        destination_candidates.append([x,y])

        # If the mouse has been any corner of the maze and there is no destination candidate left, the mouse choose starting point as its next destination.
        if len(destination_candidates) == 0:
            destination_candidates.append(self.starting)

        # If among the destination candidates, there is any destination candidates that are the neighbors of the micromouse's current location, randomly pick one of such destination candidates and remove other destination candidates.
        if self.intuition == True:
            destination_candidates_intuition = list()
            for destination_candidate in destination_candidates:
                manhattan_distance = np.sum(np.absolute(np.array(destination_candidate) - np.array(self.location_defined)))
                if manhattan_distance == 1:
                    # up
                    if ((destination_candidate[1] - self.location_defined[1]) == 1) and (self.maze_learned.is_permissible(cell = self.location_defined, direction = 'up')):
                        destination_candidates_intuition.append(destination_candidate)
                    # down
                    elif ((destination_candidate[1] - self.location_defined[1]) == -1) and (self.maze_learned.is_permissible(cell = self.location_defined, direction = 'down')):
                        destination_candidates_intuition.append(destination_candidate)
                    # left
                    elif ((destination_candidate[0] - self.location_defined[0]) == -1) and (self.maze_learned.is_permissible(cell = self.location_defined, direction = 'left')):
                        destination_candidates_intuition.append(destination_candidate)
                    # right
                    elif ((destination_candidate[0] - self.location_defined[0]) == 1) and (self.maze_learned.is_permissible(cell = self.location_defined, direction = 'right')):
                        destination_candidates_intuition.append(destination_candidate)

            if len(destination_candidates_intuition) > 0:
                destination_candidates = random.sample(destination_candidates_intuition,1)
            #print(destination_candidates)

        '''
        Heuristic destnation selection
        Because the number of destination candidates might be large, it would be slow to calculate the best path to all destination candidates. We could select the destination candidates heuristically by only selecting the destination candidates that are very close to the current location of mouse regarding the Manhattan Distance.
        '''
        # Calculate the Manhattan Distance of each destination candidate to the current location of mouse
        
        if self.heuristic == True:
            manhattan_distances = list()
            for destination_candidate in destination_candidates:
                manhattan_distances.append(np.sum(np.absolute(np.array(destination_candidate) - np.array(self.location_defined))))
            manhattan_distances_sorted_index = np.argsort(manhattan_distances)

            
            if len(destination_candidates) > 4:
                destination_candidates_heuristic = list()
                for i in xrange(4):
                    destination_candidates_heuristic.append(destination_candidates[manhattan_distances_sorted_index[i]])
            else:
                destination_candidates_heuristic = destination_candidates[:]
                          
            destination_candidates = destination_candidates_heuristic[:]
        
  
        #print('destination_candidates')
        #print(destination_candidates)

        # Calculate the number of actions and the length of movements it will take to the destination
        num_actions_candidates = list()
        length_candidates = list()

        for destination in destination_candidates:
            direction_list, movement_list, path_list = best_path(maze = self.maze_learned, starting = self.location_defined, destinations = [destination], movements = self.movements)
            num_actions = len(path_list) - 1
            num_actions_candidates.append(num_actions)
            length = length_count(path_list = path_list)
            length_candidates.append(length)

        num_actions_candidates = np.array(num_actions_candidates)
        length_candidates = np.array(length_candidates)
        
        # The index of destinations which takes the least number of actions
        candidates_1_index = np.argwhere(num_actions_candidates == np.amin(num_actions_candidates)).astype(int).flatten().tolist()

        # The index of destinations which takes the shortest length of movements
        candidates_2_index = np.argwhere(length_candidates == np.amin(length_candidates[candidates_1_index])).astype(int).flatten().tolist()

        if len(candidates_1_index) > 1:
            if len(candidates_2_index) > 1:
                destination_index = random.sample(candidates_2_index,1)[0]
            else:
                destination_index = candidates_2_index[0]
        else:
            destination_index = candidates_1_index[0]

        destination_best = destination_candidates[destination_index]
        direction_list, movement_list, path_list = best_path(maze = self.maze_learned, starting = self.location_defined, destinations = [destination_best], movements = self.movements)

        return destination_best, direction_list, movement_list, path_list

    def mouse_action(self, maze, location_real, orientation_real):
        '''
        Control the mouse action in order in one time step.
        '''
        # Detect obstacles
        distance_defined = self.obstacle_sensor(maze = maze, location_real = location_real, orientation_real = orientation_real)

        # Update maze_learned in mouse's memory
        self.learn_maze(distance_defined)

        # Calculate the percentage of visited maze
        num_reachable = 0
        num_visited = 0
        for x in xrange(self.dim_x):
            for y in xrange(self.dim_y):
                if self.maze_visited[x][y] != 0:
                    num_visited += 1
                if (self.maze_learned.walls[x][y] != 0) or ([x,y] == self.starting):
                    num_reachable += 1
        self.percentage_visited = float(num_visited)/num_reachable

        # Choose the destination candidate and take actions
        destination_best, direction_list, movement_list, path_list = self.destination_next()

        # Update the mouse's location
        self.location_defined = destination_best

        # Update the mouse's orientation
        self.orientation = direction_list[-1]

        # Update maze_visted
        self.maze_visited[tuple(self.location_defined)] = 1

        return destination_best, direction_list, movement_list, path_list

    def return_origin(self):
        '''
        Return to the starting point memorized from the current location based on the knowledge of maze_learned.
        '''
        # Find the best path using least number actions
        direction_list, movement_list, path_list = best_path(maze = self.maze_learned, starting = self.location_defined, destinations = [self.starting], movements = self.movements)

        # Update the mouse's location
        self.location_defined = path_list[-1]

        # Update the mouse's orientation
        self.orientation = direction_list[-1]

        return direction_list, movement_list, path_list

    def go_destinations(self):
        '''
        Go to the destination point memorized from the current location based on the knowledge of maze_learned.
        '''
        # Find the best path using least number actions
        direction_list, movement_list, path_list = best_path(maze = self.maze_learned, starting = self.location_defined, destinations = self.destinations, movements = self.movements)

        # Update the mouse's location
        self.location_defined = path_list[-1]

        # Update the mouse's orientation
        self.orientation = direction_list[-1]

        return direction_list, movement_list, path_list

if __name__ == '__main__':

    testmaze = Maze(str(sys.argv[1]))
    testmouse = Mouse(memory_size = 40, movements = [0,1,2,3], heuristic = True, intuition = True)
    # Initialize the micromouse
    starting = [0,0]
    destination_final = testmaze.destinations
    location_real = starting[:]
    orientation_real = 'up'
    # Set references
    location_reference = starting[:]
    orientation_reference = orientation_real
    # Set last location
    location_last = starting[:]

    # Statistics
    num_actions = 0
    length_movement = 0
    maze_visited_observed = np.zeros((testmaze.dim_x, testmaze.dim_y), dtype = np.int32)
    percentage_maze_visited_observed = float(np.sum(maze_visited_observed))/(maze_visited_observed.shape[0] * maze_visited_observed.shape[1])

    # Explore the maze
    while (testmouse.percentage_visited < 1.0): # Return when mouse visited all the grids reachable
    #while (testmouse.found_destination == False): # Return when mouse found destination

        # Action parameters of mouse
        destination_best, direction_list, movement_list, path_list = testmouse.mouse_action(maze = testmaze, location_real = location_real, orientation_real = orientation_real)

        # Action parameters observed
        # Directions
        direction_list_observed = list()
        for direction in direction_list:
            direction_list_observed.append(orientation_observed(reference_mouse = testmouse.orientation_reference, reference_observed = orientation_reference, orientation_mouse = direction))
        # Movements
        movement_list_observed = movement_list[:]
        
        # Current mouse location observed
        location_real = coordinate_observed(reference_mouse = testmouse.location_reference, reference_observed = location_reference, coordinate_mouse = testmouse.location_defined)

        # Current mouse orientation observed
        orientation_real = orientation_observed(reference_mouse = testmouse.orientation_reference, reference_observed = orientation_reference, orientation_mouse = testmouse.orientation)

        # Expected mouse location based on the directions and movements
        location_expected = destination_expectation(maze = testmaze, starting = location_last, direction_list = direction_list_observed, movement_list = movement_list_observed)

        # Check whether location_real and location_expected match
        if location_real != location_expected:
            print('Warning: location_expected did not match location_real.')

        # Update observed maze_visited
        maze_visited_observed[tuple(location_real)] = 1
        percentage_maze_visited_observed = float(np.sum(maze_visited_observed))/(maze_visited_observed.shape[0] * maze_visited_observed.shape[1])

        # Check if the mouse reached final destination
        if location_real in destination_final:
            testmouse.found_destination = True

        # Count number of actions
        num_actions += (len(path_list) - 1)

        # Count the length of movements
        length_movement += length_count(path_list = path_list)

        # Update location_last
        location_last = location_real

        print('location_real',location_real)

        print('total num_actions',num_actions)

        print('length_movement',length_movement)

        print('coverage',percentage_maze_visited_observed)


        



