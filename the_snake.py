from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый объект игры."""

    def __init__(self, position=(0, 0), body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовывает объект на поверхности."""


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self):
        position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )
        super().__init__(position, APPLE_COLOR)

    def randomize_position(self):
        """Перемещает яблоко в новую случайную позицию."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    # Метод draw класса Apple
    def draw(self, surface):
        """Рисует объект на экране."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змею в игре."""

    def __init__(self):
        super().__init__((GRID_SIZE * 5, GRID_SIZE * 5), SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def move(self):
        """Передвигает змею в текущем направлении."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
        self.last = self.positions[-1]
        x, y = self.direction
        self.positions.insert(
            0,
            (
                (self.positions[0][0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
                (self.positions[0][1] + (y * GRID_SIZE)) % SCREEN_HEIGHT,
            ),
        )
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сбрасывает змею в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None

    # Метод draw класса Snake
    def draw(self, surface):
        """Рисует змею на экране."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(
                (position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змеи."""
        return self.positions[0]

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Обновляет направление змеи после нажатия клавиши."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Обрабатывает нажатия клавиш и обновляет направление движения."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            keydown = [
                (pygame.K_UP, DOWN, UP),
                (pygame.K_DOWN, UP, DOWN),
                (pygame.K_LEFT, RIGHT, LEFT),
                (pygame.K_RIGHT, LEFT, RIGHT),
            ]
            for key, direction, next_direction in keydown:
                if event.key == key and game_object.direction != direction:
                    game_object.next_direction = next_direction
                    break


def main():
    """Основная функция игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
