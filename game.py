"""
Модуль игры «Змейка» на Pygame.

Делает логику змейки, поедание яблок и отрисовку на графическом экране.
"""

import random
import sys
import pygame

# Константы игрового поля
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Цвета (RGB)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        """Инициализация базового объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self, occupied_positions=None):
        """Инициализирует яблоко и задаёт его случайные координаты."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_positions or [])

    def randomize_position(self, occupied_positions):
        """Делает новую случайную позицию для яблока."""
        while True:
            new_x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            new_y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_position = (new_x, new_y)

            if new_position not in occupied_positions:
                self.position = new_position
                break

    def draw(self, surface):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(
            self.position[0], self.position[1], GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self):
        """Инициализирует змейку и сбрасывает её состояние."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def reset(self):
        """Сбрасывает параметры змейки в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            opposite = (-self.next_direction[0], -self.next_direction[1])
            if opposite != self.direction:
                self.direction = self.next_direction

    def move(self):
        """Обновляет позицию змейки и обрабатывает границы и столкновения."""
        self.update_direction()

        cur_x, cur_y = self.get_head_position()
        dir_x, dir_y = self.direction

        new_x = (cur_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (cur_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_position = (new_x, new_y)

        if new_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self, surface):
        """Отрисовывает все сегменты змейки."""
        for position in self.positions:
            rect = pygame.Rect(
                position[0], position[1], GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(surface, self.body_color, rect)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш на клавиатуре."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT


def main():
    """Основной игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Змейка")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        clock.tick(10)

        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()