import pygame as pg
import pygame_gui as pggui
import random

from pygame_gui.elements import UITextBox

import globals
from grid import Grid
from models.player import Player
from models.bird import Bird
from models.tilemap import Tilemap
from models.upgrades.scare_upgrade import ScareUpgrade
from models.upgrades.spawn_upgrade import SpawnUpgrade
from models.upgrades.speed_upgrade import SpeedUpgrade


class Game:
    def __init__(self):
        # Initialize pg components
        pg.init()
        self.screen = pg.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
        pg.display.set_caption("Bird Scare")
        self.clock = pg.time.Clock()
        self.dt = 0  # Delta time
        self.running = True

        # Create a tilemap
        self.tilemap = Tilemap("content/sprites/grass.png")

        self.entities = []

        # Create player object
        self.player = Player()
        self.entities.append(self.player)

        self.bird_spawn_freq = [30, 100]  # Timer will be anywhere between these two values

        self.spawn_timer = self.get_new_spawn_timer()

        # Create a grid object
        self.grid = Grid()
        cell_x, cell_y = self.grid.update_position(self.player.get_cell_coords(), self.player.pos, self.player)
        self.player.set_cell_coords(cell_x, cell_y)

        # Create upgrades
        self.upgrades = []

        self.upgrades.append(SpeedUpgrade(self.player))
        self.upgrades.append(SpawnUpgrade(self.bird_spawn_freq))
        self.upgrades.append(ScareUpgrade(self.player))

        # Define game state
        self.curr_state = "start"

        # Threshold to next upgrade
        self.upgrade_threshold = 5

        # Create UI elements
        self.pause_manager = pggui.UIManager((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
        self.pause_manager.add_font_paths(
            "pixel",
            "content/fonts/ARCADE_N.TTF"
        )
        # Reload theme so it picks up the font
        self.pause_manager.get_theme().load_theme("content/themes/pause_theme.json")

        center_x = globals.SCREEN_WIDTH // 2
        center_y = globals.SCREEN_HEIGHT // 2

        play_layout_rect = pg.Rect(
            center_x - globals.BUTTON_WIDTH // 2,
            center_y - globals.BUTTON_HEIGHT - globals.BUTTONS_SPACING // 2,
            globals.BUTTON_WIDTH,
            globals.BUTTON_HEIGHT
        )
        self.play_button = pggui.elements.UIButton(relative_rect=play_layout_rect,
                                                   text='Play',
                                                   manager=self.pause_manager)

        quit_layout_rect = pg.Rect(
            center_x - globals.BUTTON_WIDTH // 2,
            center_y + globals.BUTTONS_SPACING // 2,
            globals.BUTTON_WIDTH,
            globals.BUTTON_HEIGHT
        )
        self.quit_button = pggui.elements.UIButton(relative_rect=quit_layout_rect,
                                                   text='Quit',
                                                   manager=self.pause_manager)

        pause_text_rect = pg.Rect(
            center_x - globals.TEXT_WIDTH // 2,
            play_layout_rect.top - globals.TEXT_HEIGHT - globals.TEXT_SPACING,
            globals.TEXT_WIDTH,
            globals.TEXT_HEIGHT
        )

        shadow_rect = pause_text_rect.move(4, 4)

        self.pause_shadow = pggui.elements.UILabel(
            relative_rect=shadow_rect,
            text="Pause",
            manager=self.pause_manager,
            object_id="#shadow_label"
        )

        self.pause_label = pggui.elements.UILabel(
            relative_rect=pause_text_rect,
            text="Pause",
            manager=self.pause_manager
        )

        self.score_font = pg.font.Font("content/fonts/ARCADE_N.TTF", 24)

        self.upgrade_manager = pggui.UIManager((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))

        # Upgrade menu GUI
        self.upgrade_manager.add_font_paths(
            "pixel",
            "content/fonts/ARCADE_N.TTF"
        )

        # Reload theme so it picks up the font
        self.upgrade_manager.get_theme().load_theme("content/themes/upgrade_theme.json")

        self.upgrade_buttons = []

        margin = 60
        spacing = 20

        usable_height = globals.SCREEN_HEIGHT - 2 * margin - 2 * spacing
        button_height = usable_height // 3
        button_width = globals.SCREEN_WIDTH - 2 * margin

        for i in range(3):
            rect = pg.Rect(
                margin,
                margin + i * (button_height + spacing),
                button_width,
                button_height
            )

            button = pggui.elements.UIButton(
                relative_rect=rect,
                text=str(self.upgrades[i]),
                manager=self.upgrade_manager
            )

            self.upgrade_buttons.append(button)

        self.start_manager = pggui.UIManager((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
        self.start_manager.add_font_paths(
            "pixel",
            "content/fonts/ARCADE_N.TTF"
        )
        # Reload theme so it picks up the font
        self.start_manager.get_theme().load_theme("content/themes/pause_theme.json")

        top_offset = globals.SCREEN_HEIGHT // 5  # pushes everything slightly down
        spacing = globals.BUTTONS_SPACING + 10

        title_rect = pg.Rect(
            center_x - globals.TEXT_WIDTH,
            top_offset - globals.TEXT_HEIGHT,
            globals.TEXT_WIDTH * 2,
            globals.TEXT_HEIGHT * 2
        )

        shadow_rect = title_rect.move(4, 4)

        self.start_shadow = pggui.elements.UILabel(
            relative_rect=shadow_rect,
            text="Bird Scare",
            manager=self.start_manager,
            object_id="#shadow_label"
        )

        self.title_label = pggui.elements.UILabel(
            relative_rect=title_rect,
            text="Bird Scare",
            manager=self.start_manager
        )

        play_rect = pg.Rect(
            center_x - globals.BUTTON_WIDTH // 2,
            top_offset + spacing + globals.TEXT_SPACING,
            globals.BUTTON_WIDTH,
            globals.BUTTON_HEIGHT
        )

        self.start_button = pggui.elements.UIButton(
            relative_rect=play_rect,
            text="Start",
            manager=self.start_manager
        )

        options_rect = pg.Rect(
            center_x - globals.BUTTON_WIDTH // 2,
            play_rect.bottom + spacing,
            globals.BUTTON_WIDTH,
            globals.BUTTON_HEIGHT
        )

        self.options_button = pggui.elements.UIButton(
            relative_rect=options_rect,
            text="Options",
            manager=self.start_manager
        )

        quit_rect = pg.Rect(
            center_x - globals.BUTTON_WIDTH // 2,
            options_rect.bottom + spacing,
            globals.BUTTON_WIDTH,
            globals.BUTTON_HEIGHT
        )

        self.quit_start_button = pggui.elements.UIButton(
            relative_rect=quit_rect,
            text="Quit",
            manager=self.start_manager
        )


    def get_new_spawn_timer(self):
        return random.randint(self.bird_spawn_freq[0], self.bird_spawn_freq[1])


    def update_game(self):
        for entity in self.entities:
            entity.update()
            cell_x, cell_y = self.grid.update_position(entity.get_cell_coords(), entity.pos, entity)
            entity.set_cell_coords(cell_x, cell_y)
            if isinstance(entity, Bird):
                if entity.scared:
                    if entity.pos[0] < -entity.sprite_dims.x or entity.pos[0] > globals.SCREEN_WIDTH or entity.pos[1] < -entity.sprite_dims.y or entity.pos[1] > globals.SCREEN_HEIGHT:
                        self.entities.remove(entity)
                        self.player.score += 1

        self.player.check_birds(self.grid)

        # Spawn new bird
        self.spawn_timer -= 1
        if self.spawn_timer < 0:
            new_bird = Bird()
            self.entities.append(new_bird)
            self.spawn_timer = self.get_new_spawn_timer()
            cell_x, cell_y = self.grid.update_position(new_bird.get_cell_coords(), new_bird.pos, new_bird)
            new_bird.set_cell_coords(cell_x, cell_y)

        # Check if the upgrades threshold has been reached
        if self.player.score >= self.upgrade_threshold:
            self.upgrade_threshold += self.upgrade_threshold * 1.5
            self.curr_state = "upgrade"

    def update_upgrades(self):
        self.upgrade_manager.update(self.dt)

    def update_pause(self):
        self.pause_manager.update(self.dt)

    def update_start(self):
        self.start_manager.update(self.dt)

    def update(self):
        if self.curr_state == "playing":
            self.update_game()
        elif self.curr_state == "pause":
            self.update_pause()
        elif self.curr_state == "upgrade":
            self.update_upgrades()
        elif self.curr_state == "start":
            self.update_start()

    def add_blur(self):
        # Blur and draw the UI if the game is paused
        small = pg.transform.smoothscale(self.screen, (200, 150))
        blur = pg.transform.smoothscale(small, (globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))
        self.screen.blit(blur, (0, 0))


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
            self.add_blur()
            self.pause_manager.draw_ui(self.screen)
        elif self.curr_state == "upgrade":
            self.add_blur()
            self.upgrade_manager.draw_ui(self.screen)
        elif self.curr_state == "start":
            self.add_blur()
            self.start_manager.draw_ui(self.screen)

    def handle_pause_events(self, event):
        if event.type == pggui.UI_BUTTON_PRESSED:
            if event.ui_element == self.play_button:
                self.curr_state = "playing"
            elif event.ui_element == self.quit_button:
                self.running = False

        self.pause_manager.process_events(event)

    def handle_start_events(self, event):
        if event.type == pggui.UI_BUTTON_PRESSED:
            if event.ui_element == self.start_button:
                self.curr_state = "playing"
            elif event.ui_element == self.quit_start_button:
                self.running = False

        self.start_manager.process_events(event)

    def handle_upgrade_events(self, event):
        if event.type == pggui.UI_BUTTON_PRESSED:
            for i in range(len(self.upgrade_buttons)):
                if event.ui_element == self.upgrade_buttons[i]:
                    self.upgrades[i].activate()

            self.curr_state = "playing"

        self.upgrade_manager.process_events(event)

    def handle_events(self) -> None:
        # Check for pg events
        for event in pg.event.get():
            if event.type == pg.QUIT:  # If the screen is closed, quit the program
                self.running = False
            if pg.key.get_pressed()[pg.K_ESCAPE] and self.curr_state == "playing":
                self.curr_state = "pause"

            if self.curr_state == "pause":
                self.handle_pause_events(event)
            elif self.curr_state == "upgrade":
                self.handle_upgrade_events(event)
            elif self.curr_state == "start":
                self.handle_start_events(event)


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
            pg.display.flip()

        # Exit the loop
        pg.quit()