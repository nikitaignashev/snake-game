"""
Модуль игры «Змейка» на Pygame.

Делаем механику движения змейки, поедания яблок,
увеличения длины и прохода сквозь границы игрового поля.
"""

import random
import sys
import pygame

# --- Константы игрового поля и графики ---
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Цвета (RGB)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)

# Направления движения (сдвиг по X и Y в шагах сетки)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        """Инициализирует базовые свойства игрового объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Абстрактный метод для отрисовки объекта на поверхности."""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко и его появление на поле."""

    def __init__(self, occupied_positions=None):
        """Создаёт яблоко и задаёт ему случайную позицию."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_positions or [])

    def randomize_position(self, occupied_positions):
        """
        Делаем новую случайную позицию яблока на сетке,
        учитывая занятые змейкой клетки.
        """
        while True:
            new_x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            new_y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_position = (new_x, new_y)
            
            if new_position not in occupied_positions:
                self.position = new_position
                break

    def draw(self, surface):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс, описывающий змейку, её движение и логику столкновений."""

    def __init__(self):
        """Инициализирует змейку и сбрасывает её в начальное состояние."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def reset(self):
        """Сбрасывает змейку в исходное состояние при старте/проигрыше."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT

    def get_head_position(self):
        """Возвращает координаты головы змейки (первый элемент списка)."""
        return self.positions[0]

    def update_direction(self):
        """
        Обновляет текущее направление движения, запрещая
        разворот на 180 градусов.
        """
        if self.next_direction:
            opposite = (-self.next_direction[0], -self.next_direction[1])
            if opposite != self.direction:
                self.direction = self.next_direction

    def move(self):
        """
        Обновляет координаты сегментов змейки.
        Делаем проход через границы и сброс при столкновении с собой.
        """
        self.update_direction()
        
        cur_x, cur_y = self.get_head_position()
        dir_x, dir_y = self.direction

        # Рассчитываем новую позицию с учётом сквозных границ поля
        new_x = (cur_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (cur_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_position = (new_x, new_y)

        # Проверка на столкновение с самим собой (начиная со 2-го сегмента)
        if new_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self, surface):
        """Отрисовывает все сегменты змейки."""
        for position in self.positions:
            rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)


def handle_keys(snake):
    """
    Собирает нажатия клавиш клавиатуры и события выхода.
    Изменяет следующее направление змейки.
    """
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
    """Главный игровой цикл и инициализация компонентов."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Змейка")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        # Регулировка скорости игры (10 кадров в секунду)
        clock.tick(10)

        # 1. Обработка пользовательского ввода
        handle_keys(snake)

        # 2. Обновление состояния объектов и логика
        snake.move()

        # Проверка съедания яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # 3. Отрисовка объектов и обновление экрана (без следов)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()