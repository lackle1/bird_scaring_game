import pygame
from models.player import Player
from models.crow import Crow

class Game:
    SCREEN_WIDTH = 800.0
    SCREEN_HEIGHT = 600.0

    def __init__(self):
        # Initialize pygame components
        pygame.init()
        self.screen = pygame.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
        pygame.display.set_caption("Bird Scare")
        self.clock = pygame.time.Clock()
        self.dt = 0  # Delta time
        self.running = True

        # Create player object
        self.player = Player(Game.SCREEN_WIDTH/2, Game.SCREEN_HEIGHT/2)

        # Create crow
        self.crow = Crow(0, 0)



    def update(self):
        self.player.update()

    def render(self):
        # Clear the surface
        self.screen.fill((0, 255, 0))

        # Draw entities
        self.player.render(self.screen)
        self.crow.render(self.screen)


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