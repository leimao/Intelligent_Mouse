# Intelligent Mouse
Author: Lei Mao
Date: 3/2/2017

## Introduction

[Micromouse](https://en.wikipedia.org/wiki/Micromouse) is a contest where small robot mice (micromouse) solve a maze. It is very popular in US, UK and Japan among the young juniors who are interested in designing robots and programming artificial intelligence. In Micromouse contest, the players are going to test their micromouse to solve the maze. 
The project goal is to design a micromouse that could explore and find destination efficiently in the virtual maze.
A maze solver algorithm and a maze explorer algorithm were developed for micromouse using real-time dynamic programming. 
Equipped with such algorithms, the micromouse shows extremely potent ability in maze exploration optimal route planning��

## Maze Specifications

- The maze exists on an m x n grid of squares, m and n are even. 
- The maximum value of m and n is 20 due to my settings of micromouse memory limit. Theoretically, m and n can be any large even number, as long as I set the micromouse memory limit larger.
- The micromouse could start anywhere and reach anywhere designated in the maze. By default, the start location is at the bottom-left corner of the maze. To change the start location, I will need to change the variable in the python script.
- Mazes are provided to the system via text file. It contains the dimensions of the maze, the destination coordinates of the maze, and the wall information.
- On the first line of the text file is a number describing the number of squares on each dimension of the maze m x n. 
- On the second line of the text file is the x-coordinates of destination squares.
- On the second line of the text file is the y-coordinates of destination squares.
- On the following m line of the text file is wall information of maze along the y-axis (totally n dimensions).
- Maze files are named in a format like "test_maze_01.txt".

---
### An example maze
---

  12,12
  5,5,6,6
  5,6,5,6
  1,5,7,5,5,5,7,5,7,5,5,6
  3,5,14,3,7,5,15,4,9,5,7,12
  11,6,10,10,9,7,13,6,3,5,13,4
  10,9,13,12,3,13,5,12,9,5,7,6
  9,5,6,3,15,5,5,7,7,4,10,10
  3,5,15,14,10,3,6,10,11,6,10,10
  9,7,12,11,12,9,14,9,14,11,13,14
  3,13,5,12,2,3,13,6,9,14,3,14
  11,4,1,7,15,13,7,13,6,9,14,10
  11,5,6,10,9,7,13,5,15,7,14,8
  11,5,12,10,2,9,5,6,10,8,9,6
  9,5,5,13,13,5,5,12,9,5,5,12

---

- Each number represents a four-bit number that has a bit value of 0 if an edge is closed (walled) and 1 if an edge is open (no wall)
  - the 1s register corresponds with the upwards-facing side
  - the 2s register the right side
  - the 4s register the bottom side, and 
  - the 8s register the left side. 

For example, the number 10 means that a square is open on the left and right, with walls on top and bottom (0*1 + 1*2 + 0*4 + 1*8 = 10). 
Note that, due to array indexing, the first data row in the text file corresponds with the leftmost column in the maze, its first element being the starting square (bottom-left) corner of the maze.

## Micromouse Specifications

- The micromouse has four obstacle sensors, mounted on the front of the micromouse, its left side, its right side and its back. 
- Obstacle sensors detect the number of open squares in the direction of the sensor once in one time step.
- In each time step, the micromouse choose a direction from ��up��, ��down��, ��left�� and ��right�� and a movement step length from 0, 1, 2, or 3. 
- It is assumed that the micromouse��s turning and movement is perfect. 
- If the micromouse tries to move into a wall, the robot stays where it is. 
- The micromouse are going to do two runs in the maze. In the first run, the micromouse explore the maze and return to the start square. It does not matter if the micromouse did not reach the destination. In the second run, the micromouse shall reach the destination and the simulation ends. In both runs, the time steps were counted.
- The micromouse specifications are coded in file "mouse.py".


## Micromouse Strategy

- The micromouse has two strategies when it reached the destination in the first run. 
- Strategy I: Return to the start square and proceed to the second run. This is called "incomplete" mode in the micromouse specifications.
- Strategy II: Keep exploring until it has learned all the information in the maze followed by returning to the start square. This is called "complete" mode in the micromouse specifications.
- The micromouse can also use "intuition" and "heuristics" to accelarte computing.

## Scoring

- The scoring function is analogous to the one used in real Micromouse contest. 
- The final score is equal to the number of time steps required to execute the second run plus one thirtieth the number of time steps required to execute the both runs. 
- For examples, if it takes 100 time steps to explore the maze and return, and 20 time steps to reach the destination, the score is 20 + (100 + 20) / 30 = 24. 


## Source codes

Codes for the project includes the following files:
- maze.py   
  This script contains functions for constructing the maze objects.
- mouse.py  
  This script establishes the micromouse class controlling the actions of miromouse.
- observer.py
  This script contains some functions for micromouse movement visualization.
- planner.py
  This script contains the functions that decide micromouse's actions.
- showmaze.py
  This script can be used to create a visual demonstration of what a maze looks like.
  To run showmaze.py, run the following command in the shell:
  python showmaze.py test_maze_01.txt
- showmouse.py
  This script can be used to create a visual demonstration of how micromouse is exploring and solving the maze.
  To run showmouse.py, run the following command in the shell:
  python showmouse.py test_maze_01.txt complete
  or
  python showmouse.py test_maze_01.txt incomplete
  where "complete" and "incomplete" designate the strategy of micromouse.
  Please also remember to hit "Enter" once in the shell to start the micromouse
- showplanner.py
  This script can be used to create a visual demonstration of the optimal actions of micromouse in the maze.
  To run showplanner.py, run the following command in the shell:
  python showplanner.py test_maze_01.txt
- test.py
  This script allows you to test your micromouse in different modes on different mazes.
  To run test.py, run the following command in the shell:
  python test.py test_maze_01.txt
  
The script uses the turtle module to visualize the maze; you can click on the window with the visualization after drawing is complete to close the window. 
To allow more changes to the micromouse, the scripts can be modified accordingly.

## Results

Watch the micromouse exploring and solving the maze on [YouTube](https://www.youtube.com/playlist?list=PLVLJFoX8B37F6t81x2bK_Pe86TU2txIFn) and read the paper of the project attached.
