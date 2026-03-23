import globals

class Grid:
    """
    Spatial partitioning grid
    """
    CELL_WIDTH = 96
    CELL_HEIGHT = 72

    def __init__(self):
        self.rows = int(globals.SCREEN_HEIGHT/self.CELL_HEIGHT)
        self.cols = int(globals.SCREEN_WIDTH/self.CELL_WIDTH)
        self.grid = [[[] for _ in range(self.cols)] for _ in range(self.rows)]


    def update_position(self, cell_coords, pos, unit):
        tmp_x, tmp_y = (int(pos[0]/self.CELL_WIDTH), int(pos[1]/self.CELL_HEIGHT))

        if cell_coords[0] != tmp_x or cell_coords[1] != tmp_y:
            if 0 <= tmp_x < self.cols and 0 <= tmp_y < self.rows:
                self.grid[tmp_y][tmp_x].append(unit)
                if cell_coords != (-1, -1): # Check that the unit has entered the grid
                    if unit in self.grid[cell_coords[1]][cell_coords[0]]:
                        self.grid[cell_coords[1]][cell_coords[0]].remove(unit)
            else:
                tmp_x = tmp_y = -1

        return tmp_x, tmp_y

    def get_unit_from_adjacent_cells(self, cell_x, cell_y):
        dx = [0, 1, 0, -1, 0]
        dy = [0, 0, 1, 0, -1]

        units = []

        for i in range(5):
            tmp_x, tmp_y = cell_x + dx[i], cell_y + dy[i]
            if 0 <= tmp_x < self.cols and 0 <= tmp_y < self.rows:
                for unit in self.get_units_from_cell(tmp_x, tmp_y):
                    units.append(unit)

        return units


    def get_units_from_cell(self, cell_x, cell_y):
        return self.grid[cell_y][cell_x]