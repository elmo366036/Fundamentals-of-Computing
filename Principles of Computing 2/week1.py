"""
Student portion of Zombie Apocalypse mini-project
http://www.codeskulptor.org/#user45_AMJSBtllOr_19.py
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui
import math

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None,
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            #self._zombie_list = [(10,14)]
            self._zombie_list = [(10,10), (10,14), (8, 12)]
        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = [(10,12)]

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        #need to iterate through the grid and set all cells to empty
        for dummy_row in range(self._grid_height):
            for dummy_col in range(self._grid_width):
                self.set_empty(dummy_row, dummy_col)

        self._zombie_list = []
        self._human_list = []

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        # is this right?
        for pos in self._zombie_list:
            yield pos
        return

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col))

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # is this right?
        for pos in self._human_list:
            yield pos
        return

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """

        visited = poc_grid.Grid(self._grid_height, self._grid_width)

        distance_field = [[self._grid_height * self._grid_width for dummy_col in range(self._grid_width)]
                           for dummy_row in range(self._grid_height)]

        boundary = poc_queue.Queue()

        if entity_type == HUMAN:				#determine obj_list
            obj_list = self._human_list
        elif entity_type == ZOMBIE:
            obj_list = self._zombie_list

        for obj in obj_list:
            boundary.enqueue(obj)				#add objects to the Queue
            visited.set_full(obj[0], obj[1])	#set visited to 1
            distance_field[obj[0]][obj[1]] = 0	#set distance field(obj) to 0

        #add obstacle
        while len(boundary) != 0:				#bfs
            current_cell = boundary.dequeue()
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor_cell in neighbors:
                if visited.is_empty(neighbor_cell[0], neighbor_cell[1]) and self.is_empty(neighbor_cell[0], neighbor_cell[1]):
                    boundary.enqueue((neighbor_cell[0], neighbor_cell[1]))
                    visited.set_full(neighbor_cell[0], neighbor_cell[1])
                    distance_field[neighbor_cell[0]][neighbor_cell[1]] = distance_field[current_cell[0]][current_cell[1]] + 1

        return distance_field

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """

        distance_field = zombie_distance_field
        print distance_field

        index = 0
        for human in self._human_list:

            #determine neighboring distances frmo distance_field for human
            row = human[0]
            col = human[1]
            ans = []
            ans_index = []
            if row > 0:
                ans.append(distance_field[row - 1][col])
                ans_index.append(0)
            if row < self._grid_height - 1:
                ans.append(distance_field[row + 1][col])
                ans_index.append(1)
            if col > 0:
                ans.append(distance_field[row][col - 1])
                ans_index.append(2)
            if col < self._grid_width - 1:
                ans.append(distance_field[row][col + 1])
                ans_index.append(3)
            if (row > 0) and (col > 0):
                ans.append(distance_field[row - 1][col - 1])
                ans_index.append(4)
            if (row > 0) and (col < self._grid_width - 1):
                ans.append(distance_field[row - 1][col + 1])
                ans_index.append(5)
            if (row < self._grid_height - 1) and (col > 0):
                ans.append(distance_field[row + 1][col - 1])
                ans_index.append(6)
            if (row < self._grid_height - 1) and (col < self._grid_width - 1):
                ans.append(distance_field[row + 1][col + 1])
                ans_index.append(7)

            #determine the neighboring cell with the max distance that is not an obstacle
            #create vector to it
            max_dist = float("-Inf")
            for distance in ans:
                if distance != self._grid_height * self._grid_width and distance > max_dist:
                    max_dist = distance
            max_dist_index = ans.index(max_dist)
            max_ans_index = ans_index[max_dist_index]
            movements = {0:(-1,0), 1:(1,0), 2:(0,-1), 3:(0,1), 4:(-1,-1), 5:(-1,1), 6:(1,-1), 7:(1,1)}
            movement_vector = movements[max_ans_index]

            #if the max distance is 0, do nothing
            if max_dist != 0:
                human = (human[0] + movement_vector[0], human[1] + movement_vector[1])
                self._human_list[index] = human
            index += 1

    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        distance_field = human_distance_field
        print distance_field

        index = 0
        for zombie in self._zombie_list:

            #if the zombie is already next to a human, do nothing
            if distance_field[zombie[0]][zombie[1]] == 0:
                return

            #determine neighboring distances frmo distance_field for human
            row = zombie[0]
            col = zombie[1]
            ans = []
            ans_index = []
            if row > 0:
                ans.append(distance_field[row - 1][col])
                ans_index.append(0)
            if row < self._grid_height - 1:
                ans.append(distance_field[row + 1][col])
                ans_index.append(1)
            if col > 0:
                ans.append(distance_field[row][col - 1])
                ans_index.append(2)
            if col < self._grid_width - 1:
                ans.append(distance_field[row][col + 1])
                ans_index.append(3)

            #determine the neighboring cell with the max distance that is not an obstacle
            #create vector to it
            min_dist = float("Inf")
            for distance in ans:
                if distance != self._grid_height * self._grid_width and distance < min_dist:
                    min_dist = distance
            #if there is no min_dist, return
            if min_dist == float("Inf"):
                return
            min_dist_index = ans.index(min_dist)
            min_ans_index = ans_index[min_dist_index]
            movements = {0:(-1,0), 1:(1,0), 2:(0,-1), 3:(0,1)}
            movement_vector = movements[min_ans_index]

            #if the movement_vector points to a space with greater distance than the current
            #position, move to it, if not, stay in same spot
            if min_dist != 0:
                zombie = (zombie[0] + movement_vector[0], zombie[1] + movement_vector[1])
                self._zombie_list[index] = zombie
            index += 1

# Start up gui for simulation - You will need to write some code above
# before this will work without errors


#poc_zombie_gui.run_gui(Apocalypse(30, 40))
