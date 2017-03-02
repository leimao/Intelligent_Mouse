'''
Micromouse Maze Solver
Author: Lei Mao
Website: https://github.com/leimao/
Date: 2017/2/15
Content: Visualize maze using Python turtle library.
Notes: This script is modified from the original showmaze.py in Udacity Machine Learning Nanodegree Capstone Project and is able to plot rectangle mazes.
'''

from maze import Maze
import turtle
import sys
import os

if __name__ == '__main__':
    '''
    This function uses Python's turtle library to draw a picture of the maze
    given as an argument when running the script.
    '''

    # Create a maze based on input argument on command line.
    testmaze = Maze(str(sys.argv[1]))
    starting = [0,0]

    # Intialize the window and drawing turtle.
    window = turtle.Screen()
    wally = turtle.Turtle()
    # Control the speed of turtle: [0:10]
    # 'fastest': 0; 'fast': 10, 'normal': 6, 'slow': 3, 'slowest': 1 
    wally.speed(0)
    # Control the shape of turtle
    # wally.shape('arrow')
    wally.hideturtle()
    wally.penup()
    # Control the screen refresher rate
    wally.tracer(0, 0)

    # maze centered on (0, 0), squares are 30 units in length.
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

            # only check bottom wall if on lowest row
            if y == 0 and not testmaze.is_permissible([x,y], 'down'):
                wally.goto(origin_x + sq_size * x, origin_y)
                wally.setheading(0)
                wally.pendown()
                wally.forward(sq_size)
                wally.penup()

            # only check left wall if on leftmost column
            if x == 0 and not testmaze.is_permissible([x,y], 'left'):
                wally.goto(origin_x, origin_y + sq_size * y)
                wally.setheading(90)
                wally.pendown()
                wally.forward(sq_size)
                wally.penup()

    # show the destinations with red color
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

    # show the start with green color
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

    # save screen
    result_directory = 'result/'
    if not os.path.exists('result/'):
        os.makedirs('result/')

    file_name = str(sys.argv[1]).split('.')[0] + '.eps'
    ps = window.getcanvas().postscript(file = result_directory + file_name)

    window.exitonclick()
