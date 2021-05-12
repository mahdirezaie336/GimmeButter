# Searching Robot

This game is a practice of three AI search algorithms:

 - A* Algorithm
 - Bidirectional BFS
 - Iterative Deepening Search

The game is about a robot which tries to serve customer ASAP. At first, There is a bunch of foods on a table and all foods are given to the customers previously except for butter. This robot's duty is to give butter to the customer by putting it on a specific position on the table.

The robot's sensors gets a first perception of items on table at first.  The sensor driver puts that perception as a text file with the following format into a specific directory:

![First Perception](README_files/input.png)

First line is width and height of table. Other lines describes the table items. Items are these:
 - Numbers are cost of moving over that part of table.
 - 'r' is the position of the robot itself.
 - 'b' is the first position of a butter.
 - 'p' is a point to put a butter on it.
 
After finding shortest path, the output will be something like this:

![Output Animation](README_files/result.gif)


