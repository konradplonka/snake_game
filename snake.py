import pygame
from point import Point
from typing import List
from colors import Colors
from config import Config
from enum import StrEnum
from moving_direction import MovingDirection


class Status(StrEnum):
    ALIVE = 'alive'
    DEAD = 'dead'

class CanMove:
    points_positions: List[Point]

    def move_up(self) -> None:
        "Moves the snake up one space"
        head_point = self.points_positions[0]
        if head_point.y == 0:
            raise self._make_dead()
        new_head_point = Point(head_point.x, head_point.y - 1)
        self.points_positions.insert(0, new_head_point)
        self.points_positions.pop()

    def move_down(self) -> None:
        "Moves the snake down one space"
        head_point = self.points_positions[0]
        if head_point.y == Config.BOARD_HEIGHT - 1:
            raise self._make_dead()
        new_head_point = Point(head_point.x, head_point.y + 1)
        self.points_positions.insert(0, new_head_point)
        self.points_positions.pop()

    def move_left(self) -> None:
        "Moves the snake left one space"
        head_point = self.points_positions[0]
        if head_point.x == 0:
            raise self._make_dead()
        new_head_point = Point(head_point.x - 1, head_point.y)
        self.points_positions.insert(0, new_head_point)
        self.points_positions.pop()

    def move_right(self) -> None:
        "Moves the snake right one space"
        head_point = self.points_positions[0]
        if head_point.x == Config.BOARD_LENGTH - 1:
            raise self._make_dead()
        new_head_point = Point(head_point.x + 1, head_point.y)
        self.points_positions.insert(0, new_head_point)
        self.points_positions.pop()

class Snake(CanMove):
    COLOR: Colors = Colors.GREEN
    points_positions: List[Point]

    class IsDeadException(Exception):
        pass

    def __init__(self, x:int=10, y:int=10) -> None:
        self.points_positions = [Point(x, y), Point(x + 1, y), Point(x + 2, y)]
        self._status = Status.ALIVE

    def draw(self, surface: pygame.Surface) -> pygame.Surface:
        "Draws snake on the screen"
        for point in self.points_positions:
            rect = (Config.X_OFFSET + Config.GRID_SIZE * point.x,
                    Config.Y_OFFSET + Config.GRID_SIZE * point.y,
                    Config.GRID_SIZE,
                    Config.GRID_SIZE)
            pygame.draw.rect(surface, self.COLOR, rect)

    def _get_last_two_points_moving_direction(self) -> MovingDirection:
        "Returns moving direction of last two points in the body"
        if self.points_positions[-2].x - self.points_positions[-1].x == -1:
            return MovingDirection.LEFT
        elif self.points_positions[-2].x - self.points_positions[-1].x == 1:
            return MovingDirection.RIGHT
        elif self.points_positions[-2].y - self.points_positions[-1].y == -1:
            return MovingDirection.UP
        elif self.points_positions[-2].y - self.points_positions[-1].y == 1:
            return MovingDirection.DOWN
        else:
            raise NotImplementedError('Cannot obtain moving direction of last two points!')


    def add_element(self, point: Point, moving_direction: MovingDirection) -> None:
        "Adds collected element to the snake body"
        moving_direction = self._get_last_two_points_moving_direction()
        last_body_point = self.get_body_positions()[-1]
        if moving_direction == MovingDirection.UP:
            new_last_body_point = Point(last_body_point.x, last_body_point.y +1)
        elif moving_direction == MovingDirection.DOWN:
            new_last_body_point = Point(last_body_point.x, last_body_point.y - 1)
        elif moving_direction == MovingDirection.RIGHT:
            new_last_body_point = Point(last_body_point.x + 1, last_body_point.y)
        elif moving_direction == MovingDirection.LEFT:
            new_last_body_point = Point(last_body_point.x - 1, last_body_point.y)
        else:
            raise NotImplementedError

        self.points_positions.insert(0, point)

    def get_head_position(self) -> Point:
        "Gets snake head position"
        return self.points_positions[0]

    def get_body_positions(self) -> List[Point]:
        "Gets snake body positions"
        return self.points_positions[1:]

    def _make_dead(self):
        self._status = Status.DEAD
        self._on_dead()

    def _on_dead(self):
        raise self.IsDeadException

    def update_status(self):
        "Makes snake dead when head hits body of the snake"
        for index, point in enumerate(list(set(self.get_body_positions()))):
            if index == 1:
                continue
            if point == self.get_head_position():
                self._make_dead()







