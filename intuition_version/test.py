'''
Micromouse Maze Solver
Author: Lei Mao
Website: https://github.com/leimao/
Date: 2017/2/16
Content: Simulate micromouse in the maze.
'''

import numpy as np
import pandas as pd
import random
import sys
import time
from maze import Maze
from maze import Maze_Learned
from planner import best_path
from planner import length_count
from mouse import Mouse
from observer import orientation_observed
from observer import coordinate_observed
from observer import destination_expectation


def mouse_test(maze, mouse, mode):
    
    # Check arguments
    if (mode != 'complete') and (mode != 'incomplete'):
        raise Exception('Argument Error!')

    testmaze = maze
    testmouse = mouse

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

    # Stage 1: Mouse exploration

    # Statistics
    num_actions_1 = 0
    length_movement_1 = 0
    num_actions_2 = 0
    length_movement_2 = 0
    maze_visited_observed = np.zeros((testmaze.dim_x, testmaze.dim_y), dtype = np.int32)
    maze_visited_observed[tuple(starting)] = 1
    percentage_maze_visited_observed = float(np.sum(maze_visited_observed))/(maze_visited_observed.shape[0] * maze_visited_observed.shape[1])

    # Explore the maze

    # If argument 1 is 'incomplete', return when mouse found destination
    # If argument 2 is 'complete', return when mouse visited all the grids reachable

    while ((testmouse.percentage_visited < 1.0) if (mode == 'complete') else (testmouse.found_destination == False)):

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
            testmouse.destinations.append(testmouse.location_defined)

        # Count number of actions
        num_actions_1 += (len(path_list) - 1)

        # Count the length of movements
        length_movement_1 += length_count(path_list = path_list)

        # Update location_last
        location_last = location_real

        #print('location_real',location_real)
        #print('total num_actions',num_actions_1)
        #print('length_movement',length_movement_1)
        #print('coverage',percentage_maze_visited_observed)


    # Stage 2: Mouse goes back to starting point
    # The actions of mouse in this stage were not accounted in the total actions

    direction_list, movement_list, path_list = testmouse.return_origin()

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
    
    # Update location_last
    location_last = location_real

    # Count number of actions
    num_actions_1 += (len(path_list) - 1)

    # Count the length of movements
    length_movement_1 += length_count(path_list = path_list)
    
    # Stage 3: Mouse goes to the destination again

    direction_list, movement_list, path_list = testmouse.go_destinations()

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
    
    # Update location_last
    location_last = location_real  
    
    # Count number of actions
    num_actions_2 += (len(path_list) - 1)

    # Count the length of movements
    length_movement_2 += length_count(path_list = path_list)

    #print('total num_actions',num_actions_2)
    #print('length_movement',length_movement_2)
    #print('Final score', num_actions_2 + 1./30 * num_actions_1)

    score = num_actions_2 + 1./30 * (num_actions_1 + num_actions_2)

    return (num_actions_1, length_movement_1, num_actions_2, length_movement_2, percentage_maze_visited_observed, score)



if __name__ == '__main__':
    '''
    Simulate the mouse in the maze multiple times and record the simulation results.
    '''

    # Create Pandas DataFrame to record simulation results
    column_names = ['maze', 'mode', 'intuition', 'num_actions_1', 'length_movement_1', 'num_actions_2', 'length_movement_2', 'true_coverage', 'score', 'computation_time']
    df = pd.DataFrame(columns = column_names)

    num_tests = 20
    modes = ['complete', 'incomplete']
    intuitions = [False, True]

    for mode in modes:
        for intuition in intuitions:
            for i in xrange(num_tests):
                print('Simulation: %d. Mode: %s. Intuition: %s' %(i, mode, intuition))
                time_start = time.time()
                testmaze = Maze(str(sys.argv[1]))
                testmouse = Mouse(memory_size = 40, movements = [0,1,2,3], heuristic = True, intuition = intuition)
                result = mouse_test(maze = testmaze, mouse = testmouse, mode = mode)
                time_end = time.time()
                computation_time = time_end - time_start
                df = df.append({column_names[0]: (str(sys.argv[1]).split('.')[0]).split('_')[-1], column_names[1]:mode, column_names[2]:intuition, column_names[3]:result[0], column_names[4]:result[1], column_names[5]:result[2], column_names[6]:result[3], column_names[7]:result[4], column_names[8]:result[5], column_names[9]:computation_time}, ignore_index=True)
                # Print result
                print('The final score is %f.' %result[5])
                # Print computation time
                print('The computation time is %f.' %computation_time)
                # Save Pandas DataFrame to csv after each simulation
                df.to_csv('test_result_maze_' + (str(sys.argv[1]).split('.')[0]).split('_')[-1] + '.csv', sep=',',  index=False)