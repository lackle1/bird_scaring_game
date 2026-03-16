import pygame
import random
import globals
from models.player import Player
from models.bird import Bird
from models.tilemap import Tilemap

class Game:

    BIRD_SPAWN_FREQ = [20, 120] # Timer will be anywhere between these two values

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

        # Create player object
        self.player = Player()

        # Create crow
        self.birds = []

        self.spawn_timer = Game.get_new_spawn_timer()

    def update(self):
        self.player.update()
        for bird in self.birds:
            bird.update()

        self.player.check_birds(self.birds)

        # Spawn new bird
        self.spawn_timer -= 1
        if self.spawn_timer < 0:
            self.birds.append(Bird())
            self.spawn_timer = Game.get_new_spawn_timer()


    def render(self):
        # Clear the surface
        self.screen.fill((0, 255, 0))

        # Display tilemap
        self.tilemap.render()

        self.screen.blit(self.tilemap.surf, self.tilemap.rect)

        # Draw entities
        self.player.render(self.screen)
        for bird in self.birds:
            bird.render(self.screen)


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