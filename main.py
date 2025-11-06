import pygame
import random

# --- 1. Инициализация Pygame ---
pygame.init()

# --- 2. Константы и настройки игры ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20  # Размер одного сегмента змейки и еды в пикселях
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_GREEN = (120, 215, 120)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
BLUE = (51,51,255)
LIGHT_BLUE = (65, 105, 255)

SNAKE_SPEED = 10  # Скорость змейки (количество движений в секунду)

# --- 3. Настройка окна игры ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 30)

# --- 4. Функции для игры ---

def generate_food(snake_body):
    """Генерирует новую позицию для еды, убеждаясь, что она не на змейке."""
    while True:
        food_x = random.randint(0, GRID_WIDTH - 1)
        food_y = random.randint(0, GRID_HEIGHT - 1)
        # Проверяем, не появилась ли еда на теле змейки
        if (food_x, food_y) not in snake_body:
            return (food_x, food_y)

def draw_grid():
    """Рисует сетку на экране для наглядности (опционально)."""
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

def reset_game():
    """Сбрасывает все игровые параметры для новой игры."""
    global snake, direction, food, score, game_over
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # Начальная позиция змейки (голова)
    # Добавляем еще несколько сегментов, чтобы змейка была видна
    snake.append((snake[0][0] - 1, snake[0][1]))
    snake.append((snake[0][0] - 2, snake[0][1]))

    direction = (1, 0)  # Начальное направление: вправо (dx, dy)
    food = generate_food(snake)
    score = 0
    game_over = False

# --- 5. Переменные игры ---
snake = [] # Инициализируется в reset_game()
direction = (0, 0) # Инициализируется в reset_game()
food = (0, 0) # Инициализируется в reset_game()
score = 0 # Инициализируется в reset_game()
game_over = False # Инициализируется в reset_game()

# Первый запуск игры
reset_game()


#-----------------------------------------------------------------
# ----------------- 6. Основной игровой цикл ---------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1) # Вверх
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)  # Вниз
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0) # Влево
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)  # Вправо
            elif event.key == pygame.K_r and game_over: # Перезапуск игры
                reset_game()

    if not game_over:
        # Обновление позиции змейки
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        # Проверка на столкновение со стенами
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            game_over = True

        # Проверка на столкновение с собой
        if new_head in snake:
            game_over = True
        
        if not game_over: # Если игра еще не окончена после проверок
            snake.insert(0, new_head) # Добавляем новую голову

            # Проверка, съела ли змейка еду
            if new_head == food:
                score += 1
                food = generate_food(snake) # Генерируем новую еду
            else:
                snake.pop() # Удаляем хвост, если еда не была съедена (змейка движется)

    # --- 7. Отрисовка на экране ---
    screen.fill(LIGHT_GREEN) # Заливаем фон
    draw_grid() # Рисуем сетку

    # Отрисовка еды
    pygame.draw.rect(screen, RED,
                     (food[0] * GRID_SIZE, food[1] * GRID_SIZE,
                      GRID_SIZE, GRID_SIZE))

    # Отрисовка змейки: голова синяя, тело светло-синее
    for idx, segment in enumerate(snake):
        color = BLUE if idx == 0 else LIGHT_BLUE
        pygame.draw.rect(screen, color,
                         (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE,
                          GRID_SIZE, GRID_SIZE))

    # Отрисовка счета
    score_text = font.render(f"Счет: {score}", True, BLACK)
    screen.blit(score_text, (5, 5))

    # Отрисовка сообщения "Game Over"
    if game_over:
        game_over_text = font.render("ИГРА ОКОНЧЕНА! Нажмите R для перезапуска.", True, BLACK)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(game_over_text, text_rect)

    # Обновление всего экрана
    pygame.display.flip()

    # Управление скоростью игры
    clock.tick(SNAKE_SPEED)

# --- 8. Завершение Pygame ---
pygame.quit()
