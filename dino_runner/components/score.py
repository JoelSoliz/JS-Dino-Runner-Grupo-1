from dino_runner.components.message import draw_message_component


class Score:
    def __init__(self):
        self.score = 0

    def update(self, game):
        self.score += 1
        if self.score % 100 == 0:
            game.game_speed += 2

    def draw(self, screen):
        draw_message_component(
            f"Points: {self.score}",
            screen,
            font_size=22,
            pos_x_center=1000,
            pos_y_center=50
        )

    def restart_score(self):
        self.score = 0
