# MazeDefense
* Similar to 2D tower Defense Game.
* Map is a maze.
* Zombie from right entry will find a path and walk to left one.
* Chilies can be placed to kill zombie.
* Brick can be placed to set up the wall.
* Shovel can be used to break wall.
* Treasure Chest is hidden behind wall. Find it to win the game
# modules
	numpy, opencv, pygame
# Run
	python Game.py
# Controls
	w,a,s,d		movement keys
	q		open bag
	space		swich to zombie's view
# Technique
	A* searching algorithm
	Multithreading
	Image analyzing(recognize the wall and road in a maze picture)
