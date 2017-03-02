'''
Micromouse Maze Solver
Author: Lei Mao
Website: https://github.com/leimao/
Date: 2017/2/16
Content: Visualize micromouse solving maze using Python turtle library.
Notes: This script is modified from the original showmaze.py in Udacity Machine Learning Nanodegree Capstone Project and is able to show the actions of micromouse.
'''

import numpy as np
import turtle
import random
import sys
import os
from maze import Maze
from maze import Maze_Learned
from planner import best_path
from planner import length_count
from mouse import Mouse
from observer import orientation_observed
from observer import coordinate_observed
from observer import destination_expectation

if __name__ == '__main__':
    '''
    This function uses Python's turtle library to present the animation of micromouse solving the maze given as an argument when running the script.
    '''
    testmaze = Maze(str(sys.argv[1]))
    testmouse = Mouse(memory_size = 40, movements = [0,1,2,3], heuristic = True, intuition = True)

    # Check arguments
    if (str(sys.argv[2]) != 'complete') and (str(sys.argv[2]) != 'incomplete'):
        raise Exception('Argument Error!')

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

    # Intialize the window and drawing turtle.
    window = turtle.Screen()

    # Press enter to start
    # This is for recording purpose
    raw_input("Press Enter to continue...")

    wally = turtle.Turtle()

    # Control the speed of turtle: [0:10]
    # 'fastest': 0; 'fast': 10, 'normal': 6, 'slow': 3, 'slowest': 1 
    wally.speed(0)
    # Control the shape of turtle
    wally.shape('arrow')
    wally.hideturtle()
    wally.penup()
    # Control the screen refresher rate
    wally.tracer(0, 0)

    # Maze centered on (0, 0), squares are 30 units in length.
    sq_size = 30
    label_size = 20
    origin_x = testmaze.dim_x * sq_size / -2
    origin_y = testmaze.dim_y * sq_size / -2

    # iterate through squares one by one to decide where to draw walls
    for x in range(testmaze.dim_x):
        for y in range(testmaze.dim_y):
            if not testmaze.is_permissible([x,y], 'up'):
                wally.goto(origin_x + sq_size * x, origin_y + sq_size * (y+1))
                # Set turtle heading orientation
                # 0 - east, 90 - north, 180 - west, 270 - south
                wally.setheading(0)
                wally.pendown()
                wally.forward(sq_size)
                wally.penup()

            if not testmaze.is_permissible([x,y], 'right'):
                wally.goto(origin_x + sq_size * (x+1), origin_y + sq_size * y)
                wally.setheading(90)
                wally.pendown()
                wally.forward(sq_size)
                wally.penup()

            # Only check bottom wall if on lowest row
            if y == 0 and not testmaze.is_permissible([x,y], 'down'):
                wally.goto(origin_x + sq_size * x, origin_y)
                wally.setheading(0)
                wally.pendown()
                wally.forward(sq_size)
                wally.penup()

            # Only check left wall if on leftmost column
            if x == 0 and not testmaze.is_permissible([x,y], 'left'):
                wally.goto(origin_x, origin_y + sq_size * y)
                wally.setheading(90)
                wally.pendown()
                wally.forward(sq_size)
                wally.penup()

    # Show the destinations with red color
    for destination in testmaze.destinations:
        wally.goto(origin_x + sq_size * destination[0] + (sq_size - label_size) / 2, origin_y + sq_size * destination[1] + (sq_size - label_size) / 2)
        wally.color('','red')
        wally.begin_fill()
        wally.setheading(0)
        wally.forward(label_size)
        wally.setheading(90)
        wally.forward(label_size)
        wally.setheading(180)
        wally.forward(label_size)
        wally.setheading(270)
        wally.forward(label_size)
        wally.end_fill()

    # Show the start with green color
    wally.goto(origin_x + sq_size * starting[0] + (sq_size - label_size) / 2, origin_y + sq_size * starting[1] + (sq_size - label_size) / 2)
    wally.color('','green')
    wally.begin_fill()
    wally.setheading(0)
    wally.forward(label_size)
    wally.setheading(90)
    wally.forward(label_size)
    wally.setheading(180)
    wally.forward(label_size)
    wally.setheading(270)
    wally.forward(label_size)
    wally.end_fill()

    # Plot micromouse path
    # Initialize micromouse
    wally.goto(origin_x + sq_size * starting[0] + sq_size / 2, origin_y + sq_size * starting[1] + sq_size / 2)
    wally.color('orange')
    wally.setheading(90)
    wally.tracer(1, 200)
    wally.showturtle()
    wally.pendown()

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
    #while (testmouse.percentage_visited < 0.99): # Return when mouse visited all the grids reachable
    #while (testmouse.found_destination == False): # Return when mouse found destination

    # If argument 1 is 'incomplete', return when mouse found destination
    # If argument 2 is 'complete', return when mouse visited all the grids reachable

    while ((testmouse.percentage_visited < 1.0) if (str(sys.argv[2]) == 'complete') else (testmouse.found_destination == False)):
        print(testmouse.percentage_visited)

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

        print('location_real',location_real)

        print('total num_actions',num_actions_1)

        print('length_movement',length_movement_1)

        print('coverage',percentage_maze_visited_observed)
        
        # Plot path
        direction_dict = {'up': 90, 'down': 270, 'left': 180, 'right': 0}
        for direction, movement in zip(direction_list_observed, movement_list_observed):
            wally.setheading(direction_dict[direction])
            wally.forward(movement * sq_size)


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
    
    # Plot path
    wally.color('purple')
    direction_dict = {'up': 90, 'down': 270, 'left': 180, 'right': 0}
    for direction, movement in zip(direction_list_observed, movement_list_observed):
        wally.setheading(direction_dict[direction])
        wally.forward(movement * sq_size)
    

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

    print('total num_actions',num_actions_2)

    print('length_movement',length_movement_2)
        
    # Plot path
    wally.color('blue')
    direction_dict = {'up': 90, 'down': 270, 'left': 180, 'right': 0}
    for direction, movement in zip(direction_list_observed, movement_list_observed):
        wally.setheading(direction_dict[direction])
        wally.forward(movement * sq_size)

    print('Final score', num_actions_2 + 1./30 * (num_actions_1 + num_actions_2))

    # Save screen
    result_directory = 'result/'
    if not os.path.exists('result/'):
        os.makedirs('result/')

    file_name = str(sys.argv[1]).split('.')[0] + '_contest_route_' + str(sys.argv[2]) + '.eps'
    ps = window.getcanvas().postscript(file = result_directory + file_name)

    window.exitonclick()
