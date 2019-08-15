
"""
Clone of 2048 game.
http://www.codeskulptor.org/#user45_qEXd3cmnX1_9.py
"""

import poc_2048_gui
import random
import math

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    '''
    Function that merges a single row or column in 2048.
    '''
    output = line[:]
    pos = 0
    zereos_added = 0
    while (pos + zereos_added) < len(line) - 1:
        frame = output[pos:pos + 2]
        if 0 in frame:
            output = shift_left(output, output.index(0))[:]
            zereos_added += 1
            continue
        elif frame[0] == frame[1]:
            output[pos] *= 2
            output = shift_left(output, pos + 1)[:]
            zereos_added += 1
            pos += 1
        else:
            pos += 1
    return output

def shift_left(list_to_shift, pos):
    '''
    This is called by mmerge and shifts the list to the right
    and adds a zero at the end
    '''
    list_to_shift.pop(pos)
    list_to_shift.append(0)
    return list_to_shift

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        self._grid = []

        #all of the below code creates the starting indices.
        #probably not pythonic
        self._top_row = []
        self._bottom_row = []
        self._left_col = []
        self._right_col = []
        self._starting_rows_columns = {}

        for col in range(self._width):
            self._top_row.append((0,col))
            self._bottom_row.append((self._height - 1, col))
        for row in range(self._height):
            self._left_col.append((row,0))
            self._right_col.append((row, self._width - 1))

        self._starting_rows_columns[UP] = self._top_row
        self._starting_rows_columns[DOWN] = self._bottom_row
        self._starting_rows_columns[LEFT] = self._left_col
        self._starting_rows_columns[RIGHT] = self._right_col

        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_col in range(self._width)]
                           for dummy_row in range(self._height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        for row in range(self._height):
            print self._grid[row]
        return ""

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        merge_indices = self._starting_rows_columns[direction]
        replaced_tiles = False

        for starting_index in merge_indices:
            list_to_merge = []
            step = 0
            pos = [0,0] #this is the position of the cell during traversal
                        #pos[0] is the row and pos[1] is the column

            while (pos[0] < self._height and pos[0] >= 0) and (pos[1] < self._width and pos[1] >= 0):
                #this while statement checks to make sure that the position is within
                #self.grid.
                index_row = starting_index[0] + step * OFFSETS[direction][0]
                index_col = starting_index[1] + step * OFFSETS[direction][1]
                step += 1
                pos[0] = int(math.fabs(step*OFFSETS[direction][0]))	#determine row
                pos[1] = int(math.fabs(step*OFFSETS[direction][1]))	#determine col
                list_to_merge.append(self._grid[index_row][index_col])

            merged_list = merge(list_to_merge)
            print list_to_merge, merged_list

            step = 0
            for list_index in range(len(merged_list)):
                index_row = starting_index[0] + step * OFFSETS[direction][0]
                index_col = starting_index[1] + step * OFFSETS[direction][1]
                if merged_list[list_index] != list_to_merge[list_index]:
                    self._grid[index_row][index_col] = merged_list[list_index]
                    replaced_tiles = True
                step += 1

        if replaced_tiles == True:
            self.new_tile()


    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        #Select a random square in the grid that has a value of 0
        while True:
            rand_square = [random.randrange(0,self._height),
                           random.randrange(0,self._width)]
            if self._grid[rand_square[0]][rand_square[1]] == 0:
                break
        #set that square to either 2 or 4
        seed = random.randint(1,10)
        if seed == 1:
            tile_value = 4
        else: tile_value = 2
        self._grid[rand_square[0]][rand_square[1]] = tile_value

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

#game = TwentyFortyEight(4,5)
#poc_2048_gui.run_gui(game)
#print game
