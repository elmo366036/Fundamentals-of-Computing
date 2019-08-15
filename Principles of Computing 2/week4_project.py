"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors

http://www.codeskulptor.org/#user45_QBCOdeCmwr_69.py

"""

import poc_fifteen_gui
import math
import random

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    def get_zero_position(self):
        """
        Returns the position of the zero tile
        """
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                if self.get_number(row, col) == 0:
                    return row,col

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        #looks at zero position
        if self.get_number(target_row, target_col) != 0:
            return False

        #looks at target_row only.
        for col_idx in range(target_col + 1, self.get_width()):
                if (target_row, col_idx) != self.current_position(target_row, col_idx):
                    return False

        #looks at target_rows + 1 and on)
        for row_idx in range(target_row + 1, self.get_height()):
            for col_idx in range(self.get_width()):
                if (row_idx, col_idx) != self.current_position(row_idx, col_idx):
                    return False

        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        move_string = ""

        # PHASE 0: Initialize
        # target tile has to either be above target row or in target row
        # and in a column to the left
        target_tile = self.current_position(target_row, target_col)
        home_spot = (target_row, target_col)


        move_string = self.__int_move_zero_tile_phase1(move_string, target_tile,
                                                     home_spot)
        move_string = self.__int_move_target_tile_phase2(move_string, target_row,
                                                       target_col)
        move_string = self.__int_move_target_tile_phase3(move_string, target_row,
                                                       target_col)
        move_string = self.__int_move_zero_tile_phase4(move_string)

        return move_string

    def __int_move_zero_tile_phase1(self, move_string, target_tile, home_spot):
        """
        PHASE 1: Move zero to target tile

        """
        dist_home_to_target = (target_tile[0] - home_spot[0],
                               target_tile[1] - home_spot[1])

        # this assumes target tile is to left or up from zero tile
        for dummy_count in range(int(math.fabs(dist_home_to_target[0]))):
            move_string += "u"
        for dummy_count in range(int(math.fabs(dist_home_to_target[1]))):
            if dist_home_to_target[1] > 0:
                move_string += "r"
            elif dist_home_to_target[1] < 0:
                move_string += "l"
        for char in move_string:
            self.update_puzzle(char)
        #print "int move, phase 1", move_string
        #print self
        return move_string

    def __int_move_target_tile_phase2(self, move_string, target_row, target_col):
        """
        PHASE 2: Move target tile to correct column
            initialize variables and constants
        """

        curr_zero_pos = self.get_zero_position()
        curr_target_tile = self.current_position(target_row, target_col)
        home_spot = (target_row, target_col)
        dist_zero_to_target = (curr_target_tile[0] - curr_zero_pos[0],
                               curr_target_tile[1] - curr_zero_pos[1])
        dist_target_to_home = (home_spot[0] - curr_target_tile[0],
                               home_spot[1] - curr_target_tile[1])
        move_left = False
        move_right = False

        # generally, we want to go up & over when swapping tiles unless
        # the zero tile is on the top row. then we have to go down
        if curr_zero_pos[0] == 0:
            swap_left = "dllu"
            swap_right = "drru"
        else:
            swap_left = "ulld"
            swap_right = "urrd"

        # move target tile to correct column
        while target_col != curr_target_tile[1]:
            iteration_move = ""

            # determine if the target cell needs to move right or left
            if dist_target_to_home[1] > 0:
                move_right = True
            elif dist_target_to_home[1] < 1:
                move_left = True

            # move zero tile to correct side of target tile
            if dist_zero_to_target[1] > 0 and move_right:
                #swap zero lrft to right
                iteration_move += swap_right
            elif dist_zero_to_target[1] < 0 and move_left:
                #swap zero right to left
                iteration_move = swap_left

            # move the zero tile
            if move_left:
                iteration_move += "r"
            elif move_right:
                iteration_move += "l"

            move_string += iteration_move
            self.update_puzzle(iteration_move)

            # reset loop variables
            curr_zero_pos = self.get_zero_position()
            curr_target_tile = self.current_position(target_row, target_col)
            dist_zero_to_target = (curr_target_tile[0] - curr_zero_pos[0],
                                   curr_target_tile[1] - curr_zero_pos[1])
            dist_target_to_home = (home_spot[0] - curr_target_tile[0],
                                   home_spot[1] - curr_target_tile[1])
            move_left = False
            move_right = False

        #print "int move, phase 2", move_string
        #print self
        return move_string

    def __int_move_target_tile_phase3(self, move_string, target_row,
                                    target_col):
        """
        PHASE 3: Move target to correct row
            move zero tile to top or bottom of target cell

            determine if the target cell needs to move up or down
        """

        curr_zero_pos = self.get_zero_position()
        curr_target_tile = self.current_position(target_row, target_col)
        home_spot = (target_row, target_col)
        dist_zero_to_target = (curr_target_tile[0] - curr_zero_pos[0],
                               curr_target_tile[1] - curr_zero_pos[1])
        dist_target_to_home = (home_spot[0] - curr_target_tile[0],
                               home_spot[1] - curr_target_tile[1])

        move_up = False
        move_down = False

        if dist_target_to_home[0] > 0:
            move_down = True
        elif dist_target_to_home[0] < 1:
            move_up = True

        # move the zero tile either above or below the target tile
        if dist_zero_to_target[1] > 0 and move_down:
            move_string += "dr"
            self.update_puzzle("dr")
        elif dist_zero_to_target[1] > 0 and move_up:
            move_string += "ur"
            self.update_puzzle("ur")
        elif dist_zero_to_target[1] < 0 and move_down:
            # if the tile is on the top row, go down and left
            if curr_target_tile[0] == 0:
                move_string += "dl"
                self.update_puzzle("dl")
            # else, go above it
            else:
                move_string += "ullddr"
                self.update_puzzle("ullddr")
        elif dist_zero_to_target[1] < 0 and move_up:
            move_string += "ul"
            self.update_puzzle("ul")
        #print self

        move_string = self.__int_move_target_tile_phase3_2(move_string, target_row,
                                                         target_col)

        print self
        return move_string

    def __int_move_target_tile_phase3_2(self, move_string,target_row,
                                      target_col):
        """
        move target tile to correct row
        """
        move_up = False
        move_down = False

        swap_up = "luur"
        swap_down = "lddr"

        # initialize loop variables
        curr_zero_pos = self.get_zero_position()
        curr_target_tile = self.current_position(target_row, target_col)
        home_spot = (target_row, target_col)
        dist_zero_to_target = (curr_target_tile[0] - curr_zero_pos[0],
                                   curr_target_tile[1] - curr_zero_pos[1])
        dist_target_to_home = (home_spot[0] - curr_target_tile[0],
                                   home_spot[1] - curr_target_tile[1])
        while target_row != curr_target_tile[0]:
            iteration_move = ""

            # determine if the target cell needs to move up or down
            if dist_target_to_home[0] > 0:
                move_down = True
            elif dist_target_to_home[0] < 1:
                move_up = True

            # move zero tile to top or bottom of target tile
            if dist_zero_to_target[0] > 0 and move_down:
                #swap zero up to down
                iteration_move += swap_down
            elif dist_zero_to_target[0] < 0 and move_up:
                #swap zero down to up
                iteration_move = swap_up

            # move the zero tile
            if move_up:
                iteration_move += "d"
            elif move_down:
                iteration_move += "u"

            move_string += iteration_move
            self.update_puzzle(iteration_move)
            print self

            # reset loop variables
            curr_zero_pos = self.get_zero_position()
            curr_target_tile = self.current_position(target_row, target_col)
            dist_zero_to_target = (curr_target_tile[0] - curr_zero_pos[0],
                                   curr_target_tile[1] - curr_zero_pos[1])
            dist_target_to_home = (home_spot[0] - curr_target_tile[0],
                                   home_spot[1] - curr_target_tile[1])
            move_up = False
            move_down = False

        #print self
        return move_string

    def __int_move_zero_tile_phase4(self, move_string):
        """
        PHASE 4: Move zero tile to target_row, target_col - 1
        THIS IS A PROBLEM. DOES IT BELONG SOMEWHERE ELSE?
        """
        curr_zero_pos = self.get_zero_position()
        if curr_zero_pos[1] != 0:
            move_string += "ld"
            self.update_puzzle("ld")
        print self
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        move_string = ""

        # PHASE 0: Initialize
        # target tile has to either be above target row or in target row
        # and in a column to the left
        target_tile = self.current_position(target_row, 0)
        home_spot = (target_row, 0)

        # PHASE 1: Move zero tile to (target_row - 1, 1)
        move_string += "ur"
        self.update_puzzle("ur")
        print self

        # PHASE 1_a: Check if target is in home spot. If so, move zero tile
        #            all the way to the right
        curr_zero_pos = self.get_zero_position()
        if home_spot == self.current_position(home_spot[0], home_spot[1]):
            while curr_zero_pos[1] != self.get_width() - 1:
                move_string += "r"
                self.update_puzzle("r")
                curr_zero_pos = self.get_zero_position()
            #print self
            return move_string

        move_string = self.__col0_move_target_tile_phase2(move_string, target_row)
        move_string = self.__col0_move_zero_tile_phase3(move_string, target_row)
        move_string = self.__col0_move_target_tile_phase4(move_string, target_row, home_spot)
        move_string = self.__col0_move_zero_tile_phase5(move_string)
        move_string = self.__col0_apply_3x2_phase6(move_string)
        move_string = self.__col0_move_zero_tile_phase7(move_string)

        return move_string

    def __col0_move_target_tile_phase2(self, move_string, target_row):
        """
        PHASE 2: Move zero tile to target tile

        Move target tile to (target_row - 1, 1) [where zero tile is]
                similiar procedure to solve_interior_tile

                move zero tile to target tile
        """
        # PHASE 2a: Move zero tile to target tile
        target_tile = self.current_position(target_row, 0)
        curr_zero_pos = self.get_zero_position()
        dist_zero_to_target = (target_tile[0] - curr_zero_pos[0],
                               target_tile[1] - curr_zero_pos[1])

        for dummy_count in range(int(math.fabs(dist_zero_to_target[0]))):
            move_string += "u"
            self.update_puzzle("u")
        for dummy_count in range(int(math.fabs(dist_zero_to_target[1]))):
            if dist_zero_to_target[1] > 0:
                move_string += "r"
                self.update_puzzle("r")
            elif dist_zero_to_target[1] < 0:
                move_string += "l"
                self.update_puzzle("l")

        # at this point, the zero tile is where the target tile used to me
        #  the targe tile is either to the left or right of the zero tile
        print self
        return move_string

    def __col0_move_zero_tile_phase3(self, move_string, target_row):
        """
        Phase 3: Move target tile to column 1
        initialize variables and constants
        """
        print "col0_phase3"
        curr_zero_pos = self.get_zero_position()
        curr_target_tile = self.current_position(target_row, 0)
        home_spot = (target_row, 0)
        dist_zero_to_target = (curr_target_tile[0] - curr_zero_pos[0],
                               curr_target_tile[1] - curr_zero_pos[1])
        dist_target_to_home = (home_spot[0] - curr_target_tile[0],
                               home_spot[1] - curr_target_tile[1])

        move_left = False
        move_right = False

        swap_left = "dllu"
        swap_right = "drru"

        while curr_target_tile[1] != 1:
            iteration_move = ""

            # determine if the target cell needs to move right or left
            # in this case, should be left
            if dist_target_to_home[1] > 0:
                move_right = True
            elif dist_target_to_home[1] < 1:
                move_left = True

            # move zero tile to correct side of target tile
            if dist_zero_to_target[1] > 0 and move_right:
                #swap zero lrft to right
                iteration_move += swap_right
            elif dist_zero_to_target[1] < 0 and move_left:
                #swap zero right to left
                iteration_move = swap_left

            # move the zero tile
            if move_left:
                iteration_move += "r"
            elif move_right:
                iteration_move += "l"

            move_string += iteration_move
            self.update_puzzle(iteration_move)

            # reset loop variables
            curr_zero_pos = self.get_zero_position()
            curr_target_tile = self.current_position(target_row, 0)
            dist_zero_to_target = (curr_target_tile[0] - curr_zero_pos[0],
                                   curr_target_tile[1] - curr_zero_pos[1])
            dist_target_to_home = (home_spot[0] - curr_target_tile[0],
                                   home_spot[1] - curr_target_tile[1])
            move_left = False
            move_right = False

        print self
        print "col0_phase3 END"
        return move_string

    def __col0_move_target_tile_phase4(self, move_string, target_row, home_spot):
        """
        PHASE 4: Move target tile to correct row
        """
        print "col0_phase 4 BEGIN"
        print self
        curr_zero_pos = self.get_zero_position()
        curr_target_tile = self.current_position(target_row, 0)
        dist_zero_to_target = (curr_target_tile[0] - curr_zero_pos[0],
                               curr_target_tile[1] - curr_zero_pos[1])
        dist_target_to_home = (home_spot[0] - curr_target_tile[0],
                                   home_spot[1] - curr_target_tile[1])

        # determine if target tile is in the correct row. If so, return
        if curr_target_tile[0] == target_row - 1:
            return move_string

        # move zero tile to top or bottom of target cell

        # determine if the target cell needs to move up or down
        if dist_target_to_home[0] > 0:
            move_down = True
        elif dist_target_to_home[0] < 1:
            move_up = True

        # move the zero tile either above or below the target tile
        if dist_zero_to_target[1] > 0 and move_down:
            move_string += "dr"
            self.update_puzzle("dr")
        elif dist_zero_to_target[1] > 0 and move_up:
            move_string += "ur"
            self.update_puzzle("ur")
        elif dist_zero_to_target[1] < 0 and move_down:
            move_string += "dl"
            self.update_puzzle("dl")
        elif dist_zero_to_target[1] < 0 and move_up:
            move_string += "ul"
            self.update_puzzle("ul")
        print self

        # reset loop variables
        curr_zero_pos = self.get_zero_position()
        curr_target_tile = self.current_position(target_row, 0)
        dist_zero_to_target = (curr_target_tile[0] - curr_zero_pos[0],
                                   curr_target_tile[1] - curr_zero_pos[1])
        dist_target_to_home = (home_spot[0] - curr_target_tile[0],
                                   home_spot[1] - curr_target_tile[1])
        move_up = False
        move_down = False

        move_string = self.col0_move_target_tile_phase4_2(move_string, target_row,
                                                     curr_target_tile,
                                                     dist_target_to_home,
                                                     dist_zero_to_target)
        print self
        print "col0_phase4 END"
        return move_string

    def col0_move_target_tile_phase4_2(self, move_string, target_row,
                                         curr_target_tile, dist_target_to_home,
                                         dist_zero_to_target):
        """
        move target tile to correct row
        this should be a private method but owl test won't allow it
        """
        print "col0_phase_4_2"
        print self
        move_up = False
        move_down = False
        swap_up = "ruul"
        swap_down = "rddl"
        home_spot = (target_row, 0)
        while curr_target_tile[0] != target_row - 1:
            iteration_move = ""

            # determine if the target cell needs to move up or down
            if dist_target_to_home[0] > 0:
                move_down = True
            elif dist_target_to_home[0] < 1:
                move_up = True

            # move zero tile to top or bottom of target tile
            if dist_zero_to_target[0] > 0 and move_down:
                #swap zero up to down
                iteration_move += swap_down
            elif dist_zero_to_target[0] < 0 and move_up:
                #swap zero down to up
                iteration_move = swap_up

            # move the zero tile
            if move_up:
                iteration_move += "d"
            elif move_down:
                iteration_move += "u"

            move_string += iteration_move
            self.update_puzzle(iteration_move)
            print self

            # reset loop variables
            curr_zero_pos = self.get_zero_position()
            curr_target_tile = self.current_position(target_row, 0)
            dist_zero_to_target = (curr_target_tile[0] - curr_zero_pos[0],
                                   curr_target_tile[1] - curr_zero_pos[1])
            dist_target_to_home = (home_spot[0] - curr_target_tile[0],
                                   home_spot[1] - curr_target_tile[1])
            move_up = False
            move_down = False

        return move_string

    def __col0_move_zero_tile_phase5(self, move_string):
        """
        PHASE 5: Move zero tile to (target_row - 1, 0)
        most likely it will be on top
        """
        print "col0_phase5 BEGIN"
        print self
        curr_zero_pos = self.get_zero_position()
        if curr_zero_pos[1] != 0:
            move_string += "ld"
            self.update_puzzle("ld")
        print self
        print "col0_phase5 END"
        return move_string

    def __col0_apply_3x2_phase6(self, move_string):
        """
        PHASE 6: apply move string for 3x2 position
        """
        print "col0_phase6 BEGIN"
        #move_string += "u"
        #self.update_puzzle("u")
        #print self
        print self

        final_move = "ruldrdlurdluurddlur"
        move_string += final_move
        self.update_puzzle(final_move)
        print self

        print "col_0_phase6 END"
        return move_string

    def __col0_move_zero_tile_phase7(self, move_string):
        """
        PHASE 7: Move zero tile to (target_row - 1, width - 1)
        """
        curr_zero_pos = self.get_zero_position()
        while curr_zero_pos[1] != self.get_width() - 1:
            move_string += "r"
            self.update_puzzle("r")
            curr_zero_pos = self.get_zero_position()

        #print self
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # look at zero position
        if self.get_number(0, target_col) != 0:
            return False

        # looks at row 0.
        for col_idx in range(target_col + 1, self.get_width()):
                if (0, col_idx) != self.current_position(0, col_idx):
                    return False

        # look at row 1
        for col_idx in range(target_col, self.get_width()):
                if (1, col_idx) != self.current_position(1, col_idx):
                    return False

        # looks at rows 2 and on)
        for row_idx in range(2, self.get_height()):
            for col_idx in range(self.get_width()):
                if (row_idx, col_idx) != self.current_position(row_idx, col_idx):
                    return False

        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        #look at zero position
        if self.get_number(1, target_col) != 0:
            return False

        #looks at row 1.
        for col_idx in range(target_col + 1, self.get_width()):
                if (1, col_idx) != self.current_position(1, col_idx):
                    return False

        #looks at rows 2 and on)
        for row_idx in range(2, self.get_height()):
            for col_idx in range(self.get_width()):
                if (row_idx, col_idx) != self.current_position(row_idx, col_idx):
                    return False

        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        move_string = ""

        # PHASE 0: Move zero tile one spot left and down
        move_string += "ld"
        self.update_puzzle("ld")
        #print self

        # check if target tile is at (0, target_col). if so, done!
        target_tile = self.current_position(0, target_col)
        if target_col == target_tile[1]:
            return move_string

        # PHASE 1: Reposition target tile to (1, target_col - 1) and zero tile
        # to (1, target_col - 2)
        curr_target_tile = self.current_position(0, target_col)
        curr_zero_pos = self.get_zero_position()
        iteration_string = ""

        # if target tile is in row 1,
        if curr_target_tile[0] == 1:
            #move zero tile to left of target tile
            while curr_zero_pos[1] != curr_target_tile[1] - 1:
                move_string += "l"
                self.update_puzzle("l")
                curr_target_tile = self.current_position(0, target_col)
                curr_zero_pos = self.get_zero_position()
                #print self

        # if not, then move zero under target and swap places
        else:
            while curr_zero_pos[1] != curr_target_tile[1]:
                move_string += "l"
                self.update_puzzle("l")
                curr_target_tile = self.current_position(0, target_col)
                curr_zero_pos = self.get_zero_position()
                print self
            move_string += "u"
            self.update_puzzle("u")
            #print self

            # once under it, move target tile down and zero tile to the left of it
            # if the target tile is not top left corner move zero tile left & down
            if curr_target_tile != (0,0):
                move_string += "ld"
                self.update_puzzle("ld")
            # if it is, do a partial rotation
            else:
                move_string += "rdl"
                self.update_puzzle("rdl")

            #print "solve row0, move zero under target, swap places, move zero to left"
            #print self


        #move target tile to (1, target_col - 1)
        curr_target_tile = self.current_position(0, target_col)
        #curr_zero_pos = self.get_zero_position()
        while curr_target_tile[1] != target_col - 1:
            print curr_target_tile
            move_string += "urrdl"
            self.update_puzzle("urrdl")
            curr_target_tile = self.current_position(0, target_col)
            curr_zero_pos = self.get_zero_position()
            print "solve row0, move target tile to (1, target_col - 1)"

        final_move = "urdlurrdluldrruld"
        move_string += final_move
        self.update_puzzle(final_move)

        #print self
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        move_string = self.solve_interior_tile(1, target_col)
        print move_string
        move_string = move_string[:-2]
        self.update_puzzle("ur")
        #print "solve_row1", target_col
        #print self
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        Is row1_invariant
        """
        move_string = ""

        # PHASE 0: Move zero tile to (0,0)
        curr_zero_pos = self.get_zero_position()
        if curr_zero_pos == (1,1):
            move_string += "ul"
            self.update_puzzle("ul")
        elif curr_zero_pos == (1,0):
            move_string += "u"
            self.update_puzzle("u")
        elif curr_zero_pos == (0,1):
            move_string += "l"
            self.update_puzzle("l")

        #print self

        final_move = ""
        if self.get_number(1,0) == 1:
            if self.get_number(0,1) > self.get_number(1,1):
                final_move = "drul"
        elif self.get_number(1,1) == 1:
            if self.get_number(0,1) > self.get_number(1,0):
                final_move = "rdlu"

        move_string += final_move
        self.update_puzzle(final_move)

        #print self
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """

        result_string = ""
        curr_zero_pos = self.get_zero_position()
        print self

        # PHASE 0: Move zero tile to bottom right position
        print "BEGIN PHASE 0: move zero to bottom right"
        if curr_zero_pos != (self.get_height() - 1, self.get_width() - 1):
            while curr_zero_pos[1] != self.get_width() - 1:
                result_string += "r"
                self.update_puzzle("r")
                curr_zero_pos = self.get_zero_position()
            while curr_zero_pos[0] != self.get_height() - 1:
                result_string += "d"
                self.update_puzzle("d")
                curr_zero_pos = self.get_zero_position()
            print self

        # PHASE 1: Run solve interior tile and col0 for lower rows 2 - height
        print "BEGIN PHASE 1: solve int and col0"
        for row_idx in range(self.get_height() - 1, 1, -1):
            for col_idx in range(self.get_width() - 1, 0, -1):
                # only call solve_interior_tile if lower_row_invariant is true
                if self.lower_row_invariant(row_idx, col_idx):
                    result_string += self.solve_interior_tile(row_idx, col_idx)
                #print self
            # only call solve_col0_tile if lower_row_invariant is true
            if self.lower_row_invariant(row_idx, 0):
                result_string += self.solve_col0_tile(row_idx)
        print self
        print "END PHASE 1: solve int and col0"

        # PHASE 2: Solve rows 1 and 0, stopping at column 1
        print "BEGIN PHASE 2: solve rows 1 and 0"
        for col_idx in range(self.get_width() - 1, 1, -1):
            # only call solve_row1_tile if row1_invariant is true
            if self.row1_invariant(col_idx):
                result_string += self.solve_row1_tile(col_idx)
            # only call solve_row0_tile if row1_invariant is true
            if self.row0_invariant(col_idx):
                result_string += self.solve_row0_tile(col_idx)
        print self
        print "END PHASE 2: solve rows 1 and 0"

        # PHASE 3: Solve 2x2
        print "BEGIN PHASE 3: solve 2x2"
        result_string += self.solve_2x2()
        print self
        print "END PHASE 4: solve 2x2"
        print
        print
        print "Result: "+result_string, len(result_string)
        return result_string

def initialize_puzzle():
    rows = random.randrange(2,7)
    columns = random.randrange(2,7)
    max_tile_num = rows * columns - 1
    numbers = range(max_tile_num + 1)
    random.shuffle(numbers)
    idx = 0

    init_grid = [[col + rows * row
                for col in range(columns)]
                      for row in range(rows)]

    for row in range(rows):
        for col in range(columns):
            init_grid[row][col] = numbers[idx]
            idx += 1
    print init_grid

    poc_fifteen_gui.FifteenGUI(Puzzle(rows, columns, init_grid))


initialize_puzzle()


# TESTS

# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))

#BIG TEST
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4, [[2,15,6,8],[9,13,0,10],[11,7,4,1],[12,3,14,5]]))
#Coop's Test
#my_puzzle = Puzzle(4, 4, [[2,15,6,8],[9,13,0,10],[11,7,4,1],[12,3,14,5]])
#print my_puzzle
#print my_puzzle.solve_puzzle()


#poc_fifteen_gui.FifteenGUI(Puzzle(3, 3,[[8, 7, 6], [5, 4, 3], [2, 1, 0]]))

#TESTS
#my_puzzle = Puzzle(4,4)
#print my_puzzle

#PASSED
#print my_puzzle.lower_row_invariant(2,2)

#PASSED
#my_puzzle = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print my_puzzle
#assert my_puzzle.lower_row_invariant(2,2)
#print my_puzzle.solve_interior_tile(2, 2)
#assert my_puzzle.lower_row_invariant(2, 1)

#PASSED
#my_puzzle = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [0, 7, 8]])
#print my_puzzle
#assert my_puzzle.lower_row_invariant(2,0)
#print my_puzzle.solve_col0_tile(2)
#assert my_puzzle.lower_row_invariant(1,2)

#PASSED
#my_puzzle = Puzzle(4, 5, [[12, 11, 10, 9, 15], [7, 6, 5, 4, 3], [2, 1, 8, 13, 14], [0, 16, 17, 18, 19]])
#print my_puzzle
#assert my_puzzle.lower_row_invariant(3,0)
#print my_puzzle.solve_col0_tile(3)
#assert my_puzzle.lower_row_invariant(2,4)

#PASSED
#my_puzzle = Puzzle(3, 3, [[2, 5, 4], [1, 3, 0], [6, 7, 8]])
#print my_puzzle
#assert my_puzzle.row1_invariant(2)
#print my_puzzle.solve_row1_tile(2)
#assert my_puzzle.row0_invariant(2)
#uldru

#PASSED
#my_puzzle = Puzzle(4, 5, [[7, 6, 5, 3, 2], [4, 1, 9, 8, 0], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#print my_puzzle
#assert my_puzzle.row1_invariant(4)
#print my_puzzle.solve_row1_tile(4)
#assert my_puzzle.row0_invariant(4)

#PASSED
#my_puzzle = Puzzle(3, 3, [[4, 1, 0], [2, 3, 5], [6, 7, 8]])
#print my_puzzle
#assert my_puzzle.row0_invariant(2)
#print my_puzzle.solve_row0_tile(2)
#assert my_puzzle.row1_invariant(1)

#PASSED
#my_puzzle = Puzzle(4, 5, [[7, 6, 5, 3, 0], [4, 8, 2, 1, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#print my_puzzle
#assert my_puzzle.row0_invariant(4)
#print my_puzzle.solve_row0_tile(4)
#assert my_puzzle.row1_invariant(3)

#PASSED
#my_puzzle = Puzzle(4, 5, [[1, 2, 0, 3, 4], [6, 5, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#print my_puzzle
#assert my_puzzle.row0_invariant(2)
#print my_puzzle.solve_row0_tile(2)
#assert my_puzzle.row1_invariant(1)


#PASSED
#my_puzzle = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]])
#print my_puzzle
#print my_puzzle.solve_2x2()

#PASSED
#my_puzzle = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print my_puzzle
#print my_puzzle.solve_puzzle()

#PASSED
#my_puzzle = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
#print my_puzzle
#print my_puzzle.solve_puzzle()

#PASSED
#my_puzzle = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#print my_puzzle
#print my_puzzle.solve_puzzle()

#PASSED
#my_puzzle = Puzzle(3, 6, [[16, 7, 13, 17, 5, 9], [3, 0, 14, 10, 12, 6], [4, 15, 2, 11, 8, 1]])
#print my_puzzle
#print my_puzzle.solve_puzzle()



#see how long result is
#my_puzzle = Puzzle(4, 4, [[15, 11, 8, 12], [14, 10, 9, 13], [2, 6, 1, 4], [3, 7, 5, 0]])
#print my_puzzle
#print my_puzzle.solve_puzzle()
