# CS440-Intro-AI-Project-1-Maze-Runner

Summary:

A maze will be a square grid of cells / locations, where each cell is either empty or occupied. An agent wishes to travel from the upper left corner to the lower right corner, along the shortest path possible. The agent can only move from empty cells to neighboring empty cells in the up/down direction, or left/right - each cell has potentially four neighbors.

Mazes may be generated in the following way: for a given dimension dim construct a dim x dim array; given a probability p of a cell being occupied (0 < p < 1), read through each cell in the array and determine at random if it should be filled or empty. When filling cells, exclude the upper left and lower right corners (the start and goal, respectively). It is convenient to define a function to generate these maps for a given dim and p.

Bonus: A Moving Target

In this section, the target is no longer stationary, and can move between neighboring cells (up/down/left/right). Each time you perform a search, if you fail to find the target, the target will move to a neighboring cell (with uniform probability for each). However, all is not lost - every time you search a cell, you are now given two pieces of information instead of one: first, you are told whether or not the search was successful (same false negative rates as before); and if the search was unsuccessful, you are told whether or not the target is within Manhattan distance 5 of your current location.

MORE INFO: CS440 - FireMaze.pdf

FINAL REPORT: AI_1 (1).pdf
