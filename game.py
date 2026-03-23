import pygame
import random
import globals
from grid import Grid
from models.player import Player
from models.bird import Bird
from models.tilemap import Tilemap

class Game:

    BIRD_SPAWN_FREQ = [10, 50] # Timer will be anywhere between these two values

    @staticmethod
    def get_new_spawn_timer():
        return random.randint(Game.BIRD_SPAWN_FREQ[0], Game.BIRD_SPAWN_FREQ[1])

    def __init__(self):
        # Initialize pygame components
        pygame.init()
        self.screen = pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
        pygame.display.set_caption("Bird Scare")
        self.clock = pygame.time.Clock()
        self.dt = 0  # Delta time
        self.running = True

        # Create a tilemap
        self.tilemap = Tilemap("content/grass.png")

        self.entities = []

        # Create player object
        self.player = Player()
        self.entities.append(self.player)

        self.spawn_timer = Game.get_new_spawn_timer()

        # Create a grid object
        self.grid = Grid()
        cell_x, cell_y = self.grid.update_position(self.player.get_cell_coords(), self.player.pos, self.player)
        self.player.set_cell_coords(cell_x, cell_y)

        # Define game state
        self.curr_state = "playing"

        # Create UI elements
        self.score_font = pygame.font.Font("content/Arcade-Normal/ARCADE_N.TTF", 24)

    def update_game(self):
        for entity in self.entities:
            entity.update()
            cell_x, cell_y = self.grid.update_position(entity.get_cell_coords(), entity.pos, entity)
            entity.set_cell_coords(cell_x, cell_y)
            if isinstance(entity, Bird):
                if entity.scared:
                    if entity.pos[0] < -entity.rect.width or entity.pos[0] > globals.SCREEN_WIDTH or entity.pos[
                        1] < -entity.rect.height or entity.pos[1] > globals.SCREEN_HEIGHT:
                        self.entities.remove(entity)

        self.player.check_birds(self.grid)

        # Spawn new bird
        self.spawn_timer -= 1
        if self.spawn_timer < 0:
            new_bird = Bird()
            self.entities.append(new_bird)
            self.spawn_timer = Game.get_new_spawn_timer()
            cell_x, cell_y = self.grid.update_position(new_bird.get_cell_coords(), new_bird.pos, new_bird)
            new_bird.set_cell_coords(cell_x, cell_y)

    def update_pause(self):
        pass

    def update(self):
        if self.curr_state == "playing":
            self.update_game()
        elif self.curr_state == "pause":
            self.update_pause()


    def render(self):
        # Clear the surface
        self.screen.fill((0, 255, 0))

        # Display tilemap
        self.tilemap.render()

        self.screen.blit(self.tilemap.surf, self.tilemap.rect)

        # Draw entities
        for entity in self.entities:
            entity.render(self.screen)

        score = self.score_font.render(str(self.player.score), True, (255, 255, 255))
        self.screen.blit(score, (30, 30))

        if self.curr_state == "pause":
            # Blur and draw the UI if the game is paused
            pass


    def handle_events(self) -> None:
        # Check for pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:  # If the screen is closed, quit the program
                self.running = False


    def game_loop(self):
        """
        Classic game loop
        """
        while self.running:
            # Restart immediately for smoother movement
            self.dt = self.clock.tick(60) / 1000.0

            self.handle_events()

            self.update()

            self.render()

            # updates the entire canvas
            pygame.display.flip()

        # Exit the loop
        pygame.quit()