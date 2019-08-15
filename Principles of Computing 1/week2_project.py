"""
Clone of 2048 game.
http://www.codeskulptor.org/#user45_qEXd3cmnX1_3.py
"""

import poc_2048_gui
import random

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
    #print list, index
    return list_to_shift

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.height = grid_height
        self.width = grid_width
        self.grid = []

        #all of the below code creates the starting indices.
        #probably not pythonic
        self.top_row = []
        self.bottom_row = []
        self.left_col = []
        self.right_col = []
        self.starting_rows_columns = {}

        for col in range(self.width):
            self.top_row.append((0,col))
            self.bottom_row.append((self.height - 1, col))
        for row in range(self.height):
            self.left_col.append((row,0))
            self.right_col.append((row, self.width - 1))

        self.starting_rows_columns["UP"] = self.top_row
        self.starting_rows_columns["DOWN"] = self.bottom_row
        self.starting_rows_columns["LEFT"] = self.left_col
        self.starting_rows_columns["RIGHT"] = self.right_col

        print self.starting_rows_columns
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self.grid = [[0 for col in range(self.width)]
                           for row in range(self.height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        for row in range(self.height):
            print self.grid[row]
        return ""

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        ind = OFFSETS.get(direction)

        print ind
        pass

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        #Select a random square in the grid that has a value of 0
        while True:
            rand_square = [random.randrange(0,self.height),
                           random.randrange(0,self.width)]
            if self.grid[rand_square[0]][rand_square[1]] == 0:
                break
        #set that square to either 2 or 4
        seed = random.randint(1,10)
        if seed == 1:
            tile_value = 4
        else: tile_value = 2
        self.grid[rand_square[0]][rand_square[1]] = tile_value

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.grid[row][col]

game = TwentyFortyEight(4,5)
poc_2048_gui.run_gui(game)
print game
