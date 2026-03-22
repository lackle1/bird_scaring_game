import globals

class Grid:
    """
    Spatial partitioning grid
    """
    CELL_WIDTH = 96
    CELL_HEIGHT = 72

    def __init__(self):
        rows = int(globals.SCREEN_HEIGHT/self.CELL_HEIGHT)
        cols = int(globals.SCREEN_WIDTH/self.CELL_WIDTH)
        self.grid = [[[] for _ in range(cols)] for _ in range(rows)]
        print(self.grid)


    def update_position(self, cell_coords, pos, unit):
        tmp_x, tmp_y = (int(pos[0]/self.CELL_WIDTH), int(pos[1]/self.CELL_HEIGHT))
        rows = len(self.grid)
        cols = len(self.grid[0])

        if cell_coords[0] != tmp_x or cell_coords[1] != tmp_y:
            if 0 < tmp_x < cols and 0 < tmp_y < rows:
                self.grid[tmp_y][tmp_x].append(unit)
                if cell_coords != (-1, -1): # Check that the unit has entered the grid
                    if unit in self.grid[cell_coords[1]][cell_coords[0]]:
                        self.grid[cell_coords[1]][cell_coords[0]].remove(unit)
            else:
                tmp_x = tmp_y = -1

        return tmp_x, tmp_y




    def get_units_from_cell(self, cell_x, cell_y):
        return self.grid[cell_y][cell_x]