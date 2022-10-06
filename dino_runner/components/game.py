import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.message import draw_message_component
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.score import Score

from dino_runner.utils.constants import BG, ICON, RUNNING, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.executing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()

        self.death_count = 0
        self.score = Score()

    def execute(self):
        self.executing = True
        while self.executing:
            if not self.playing:
                self.show_menu()

        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.reset_game()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def reset_game(self):
        self.game_speed = 20
        self.obstacle_manager.reset_obstacles()
        self.score.restart_score()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self.game_speed, self.player, self.on_death)
        self.score.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.score.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def show_menu(self):
        self.screen.fill((255, 255, 255)) # pintar mi ventana *
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        if self.death_count == 0: # mostrar mensaje de bienvenida *
            draw_message_component("Press any key to start", self.screen)
        else:
            draw_message_component("Press any key to restart", self.screen)
            draw_message_component(
                f"Your Score: {self.score.score}",
                self.screen,
                pos_y_center=half_screen_height + 50
            )
            draw_message_component(
                f"Death count: {self.death_count}",
                self.screen,
                pos_y_center=half_screen_height + 100
            )

        self.screen.blit(RUNNING[0], (half_screen_width - 30, half_screen_height - 140)) # mostrar un icono *
        pygame.display.update() # actualizar ventana *
        self.handle_key_events_on_menu() # escuchar eventos

    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.executing = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def on_death(self):
        self.playing = False
        self.death_count += 1
