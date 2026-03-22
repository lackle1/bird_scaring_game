class Entity:
    cell_x, cell_y = -1, -1
    """
    Abstract class for entities
    """
    def update(self):
        pass

    def render(self, screen):
        pass

    def get_cell_coords(self):
        return self.cell_x, self.cell_y

    def set_cell_coords(self, x, y):
        self.cell_x, self.cell_y = x, y