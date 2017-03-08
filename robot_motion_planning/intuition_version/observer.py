'''
Micromouse Maze Solver
Author: Lei Mao
Website: https://github.com/leimao/
Date: 2017/2/15
Content: Observe mouse's action from people's view.
'''
import numpy as np


def orientation_observed(reference_observed, orientation_mouse, reference_mouse = 'up'):
    '''
    Transform the orientation that the mouse thinks in mouse's memory to the orientation that people obeserved.
    '''
    if reference_mouse == 'up':
        if reference_observed == 'up':
            orientation_observed = orientation_mouse
        elif reference_observed == 'down':
            translation_dict = {'up':'down','down':'up','left':'right','right':'left'}
            orientation_observed = translation_dict[orientation_mouse]
        elif reference_observed == 'left':
            translation_dict = {'up':'left','down':'right','left':'down','right':'up'}
            orientation_observed = translation_dict[orientation_mouse]
        elif reference_observed == 'right':
            translation_dict = {'up':'right','down':'left','left':'up','right':'down'}
            orientation_observed = translation_dict[orientation_mouse]
    else:
        raise Exception('Orientation reference other than up is not defined.')

    return orientation_observed


def coordinate_observed(reference_mouse, reference_observed, coordinate_mouse):
    '''
    Transform the coordinate that the mouse thinks in mouse's memory to the coordinate that people obeserved.
    '''
    reference_difference = np.array(reference_observed) - np.array(reference_mouse)
    coordinate_observed = (np.array(coordinate_mouse) + reference_difference).astype(int).tolist()

    return coordinate_observed


def destination_expectation(maze, starting, direction_list, movement_list):
    if len(direction_list) != len(movement_list):
        raise Exception('Lengths of direction_list and movement_list were not equal.')
    location = starting[:]
    crash = False
    for i in xrange(len(direction_list)):
        if direction_list[i] == 'up':
            # Examine crash
            for j in xrange(movement_list[i]):
                if maze.walls[location[0]][location[1]+j] & 1 == 0:
                    crash = True
            # Update location
            location = [location[0],location[1]+movement_list[i]]

        elif direction_list[i] == 'down':
            # Examine crash
            for j in xrange(movement_list[i]):
                if maze.walls[location[0]][location[1]-j] & 4 == 0:
                    crash = True
            # Update location
            location = [location[0],location[1]-movement_list[i]]

        elif direction_list[i] == 'left':
            # Examine crash
            for j in xrange(movement_list[i]):
                if maze.walls[location[0]-j][location[1]] & 8 == 0:
                    crash = True
            # Update location
            location = [location[0]-movement_list[i],location[1]]

        elif direction_list[i] == 'right':
            # Examine crash
            for j in xrange(movement_list[i]):
                if maze.walls[location[0]+j][location[1]] & 2 == 0:
                    crash = True
            # Update location
            location = [location[0]+movement_list[i],location[1]]

    if crash == True:
        print('Warning: mouse crashed into wall.')

    return location
