import pygame
from point import Point
from board import Board
from config import Config
from snake import Snake
from enum import StrEnum
from colors import Colors
from moving_direction import MovingDirection


class GameStatus(StrEnum):
    RUNNING = 'Running'
    GAME_OVER = 'Game Over'


class SnakeGame():
    _board: Board
    _snake: Snake
    _score: int
    _surface: pygame.Surface
    _game_status: GameStatus

    def __init__(self) -> None:
        self._board = Board()
        self._snake = Snake()
        self._score = 0
        self._surface = self._prepare_game_screen()
        self._game_status = GameStatus.RUNNING

        pygame.init()

    def _increase_score(self) -> None:
        "Increases user score in gameplay"
        self._score += 1

    def _prepare_game_screen(self) -> pygame.Surface:
        "Prepares game screen based on dimensions stored in Config class"
        screen_width = 2 * Config.X_OFFSET + Config.BOARD_HEIGHT * Config.GRID_SIZE
        screen_height = 2 * Config.Y_OFFSET + Config.BOARD_LENGTH * Config.GRID_SIZE
        screen_dim = (screen_width, screen_height)

        surface = pygame.display.set_mode(screen_dim)
        return surface

    def _draw_score(self) -> None:
        "Shows score on the screen"
        font = pygame.font.SysFont('Calibri', 25, True, False)
        score_text = font.render(f'Score: {str(self._score)}', True, Colors.BLACK)
        self._surface.blit(score_text, [25, 10])

    def _move_snake(self, moving_direction: MovingDirection) -> None:
        "Moves snake in direction specified in moving direction"
        if moving_direction == MovingDirection.LEFT:
            self._snake.move_left()
        elif moving_direction == MovingDirection.RIGHT:
            self._snake.move_right()
        elif moving_direction == MovingDirection.UP:
            self._snake.move_up()
        elif moving_direction == MovingDirection.DOWN:
            self._snake.move_down()

    def _show_game_over_screen(self) -> None:
        "Shows game over screen"
        font = pygame.font.SysFont('Calibri', 25, True, False)
        game_over_text = font.render('Game Over', True, Colors.RED)
        replay_text = font.render("Press Esc to replay", True, Colors.RED)
        self._surface.blit(game_over_text, [240, 200])
        self._surface.blit(replay_text, [205, 235])

    def _on_game_over(self) -> None:
        self._game_status = GameStatus.GAME_OVER
        self._show_game_over_screen()

    def _restart_game(self) -> None:
        self._score = 0
        self._game_status = GameStatus.RUNNING
        self._snake = Snake()
        self._board.clear_element(self._surface)
        self._board.new_element(self._snake.points_positions)


    def _is_running(self) -> None:
        "Checks if game status is running"
        if self._game_status == GameStatus.RUNNING:
            return True
        else:
            return False

    def run_game(self) -> None:
        done = False
        pressing_down = False
        clock = pygame.time.Clock()
        counter = 0
        element = None

        moving_direction = MovingDirection.LEFT
        prev_move = MovingDirection.LEFT
        while not done:
            counter += 1
            if counter > 5:
                counter = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and prev_move != MovingDirection.LEFT:
                        moving_direction = MovingDirection.RIGHT
                    if event.key == pygame.K_LEFT and prev_move != MovingDirection.RIGHT:
                        moving_direction = MovingDirection.LEFT
                    if event.key == pygame.K_UP and prev_move != MovingDirection.DOWN:
                        moving_direction = MovingDirection.UP
                    if event.key == pygame.K_DOWN and prev_move != MovingDirection.UP:
                        moving_direction = MovingDirection.DOWN
                    if event.key == pygame.K_ESCAPE:
                        self._restart_game()

            self._board.draw_board(self._surface)
            if self._is_running():
                if not self._board._element:
                    self._board.new_element(self._snake.points_positions)

                if self._board._element:
                    if self._snake.get_head_position() == self._board._element:
                        self._snake.add_element(self._board._element, moving_direction)
                        self._board.clear_element(self._surface)
                        self._increase_score()
                try:
                    if counter % Config.FPS_RATE == 0:
                        self._move_snake(moving_direction)
                        prev_move = moving_direction
                        self._snake.update_status()

                    self._snake.draw(self._surface)

                except Snake.IsDeadException:
                    self._game_status = GameStatus.GAME_OVER

            else:
                self._snake.draw(self._surface)
                self._show_game_over_screen()

            self._draw_score()

            pygame.display.flip()
            clock.tick(Config.FPS_RATE)


if __name__ == '__main__':
    snake_game = SnakeGame()
    snake_game.run_game()
