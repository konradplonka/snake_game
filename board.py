import pygame
from config import Config
from colors import Colors
from typing import List
from point import Point
from random import randint
from colors import Colors


class Board:
    _fields: List[Colors]
    _element: Point

    def __init__(self) -> None:
        self._fields = self._generate_empty_fields()
        self._element: Point = None

    def _generate_empty_fields(self) -> None:
        "Generates empty fields filled with white color"
        fields = []
        row_fields = []

        for row in range(Config.BOARD_HEIGHT):
            for col in range(Config.BOARD_LENGTH):
                row_fields.append(Colors.WHITE)
            fields.append(row_fields)
            row_fields = []

        return fields

    def draw_board(self, surface: pygame.Surface) -> None:
        "Draws board together with element to collect"
        self._draw_area(surface)
        self._draw_element(surface)

    def _draw_area(self, surface: pygame.Surface) -> None:
        "Draws empty area filled with white color"
        surface.fill(Colors.WHITE)
        rect = (Config.X_OFFSET,
                Config.Y_OFFSET,
                Config.GRID_SIZE * Config.BOARD_LENGTH,
                Config.GRID_SIZE * Config.BOARD_HEIGHT)
        pygame.draw.rect(surface, Colors.GRAY, rect, 1)

    def _draw_element(self, surface: pygame.Surface) -> None:
        "Draws element to collect by the snake"
        for row_num in range(Config.BOARD_HEIGHT):
            for col_num in range(Config.BOARD_LENGTH):
                field_color = self._fields[row_num][col_num]
                if field_color == Colors.WHITE:
                    continue
                rect = (Config.X_OFFSET + Config.GRID_SIZE * col_num,
                        Config.Y_OFFSET + Config.GRID_SIZE * row_num,
                        Config.GRID_SIZE,
                        Config.GRID_SIZE)
                pygame.draw.rect(surface, field_color, rect)

    def new_element(self, exluded_positions: List[Point]) -> None:
        "Generates new element to collect"
        point = exluded_positions[0]

        while point in exluded_positions:
            x_pos_random = randint(0, Config.BOARD_LENGTH - 1)
            y_pos_random = randint(0, Config.BOARD_HEIGHT - 1)
            point = Point(x_pos_random, y_pos_random)

        self._fields[point.y][point.x] = Colors.BLUE
        self._element = point


    def clear_element(self, surface: pygame.Surface) -> None:
        "Clears current element to collect on the board"
        self._fields[self._element.y][self._element.x] = Colors.WHITE
        self._element = None
