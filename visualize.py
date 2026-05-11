import pygame
import time

from environment import MazeEnv
from agent import QLearningAgent

pygame.init()

# =========================
# GRID SETTINGS
# =========================

ROWS = 10
COLS = 10
CELL_SIZE = 60

GRID_W = COLS * CELL_SIZE
GRID_H = ROWS * CELL_SIZE

SIDE_PANEL = 260

WIDTH = GRID_W + SIDE_PANEL
HEIGHT = GRID_H

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Maze - Q Learning")

clock = pygame.time.Clock()

# =========================
# COLORS
# =========================

BG = (18, 20, 28)
PANEL = (28, 32, 44)

WALL = (90, 100, 130)
PATH = (35, 40, 55)
GOAL = (80, 220, 120)
TRAP = (230, 120, 80)

AGENT = (80, 170, 255)
TEXT = (240, 240, 240)

# =========================
# FONTS
# =========================

title_font = pygame.font.SysFont("Segoe UI", 28, bold=True)
font = pygame.font.SysFont("Segoe UI", 18)

# =========================
# ENV + AGENT
# =========================

env = MazeEnv() #окруж
agent = QLearningAgent() #ии

try:
    agent.load() #загрузка обученной модели
    print("Model loaded")
except:
    print("No model found")

state = env.reset()
done = False

episodes = 0
steps = 0
speed = 0.1

episode_reward = 0

# =========================
# DRAW CELL
# =========================

def draw_cell(r, c, color):

    x = c * CELL_SIZE
    y = r * CELL_SIZE

    pygame.draw.rect(
        screen,
        color,
        (x+3, y+3, CELL_SIZE-6, CELL_SIZE-6),
        border_radius=8
    )

# =========================
# LOOP основной цикл
# =========================

running = True

while running:

    screen.fill(BG)

    # =====================
    # EVENTS обработка событий
    # =====================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                state = env.reset()
                done = False
                steps = 0

            if event.key == pygame.K_s:
                agent.save()
                print("Saved")

            if event.key == pygame.K_UP:
                speed = max(0.02, speed - 0.02)

            if event.key == pygame.K_DOWN:
                speed += 0.02

    # =====================
    # GRID
    # =====================

    for r in range(ROWS):
        #2х цикл проходит и рисует клетки
        for c in range(COLS):

            color = PATH

            if (r, c) in env.walls:
                color = WALL

            if (r, c) in env.traps:
                color = TRAP

            if (r, c) == env.goal:
                color = GOAL

            draw_cell(r, c, color) #округление углов

    # =====================
    # AI STEP
    # =====================

    if not done:

        action = agent.choose_action(state)

        next_state, reward, done = env.step(action) #окружение (env) сообщ где агент

        agent.update(state, action, reward, next_state) #анализирует результат

        state = next_state

        episode_reward += reward
        steps += 1

        time.sleep(speed)

    else:

        episodes += 1
        agent.log_episode(episode_reward) #сохранение данных в лог, камбек на старт

        episode_reward = 0
        steps = 0

        state = env.reset()
        done = False

    # =====================
    # DRAW AGENT
    # =====================

    ax, ay = env.agent_pos

    cx = ay * CELL_SIZE + CELL_SIZE // 2
    cy = ax * CELL_SIZE + CELL_SIZE // 2

    pygame.draw.circle(screen, AGENT, (cx, cy), 18)

    # =====================
    # SIDE PANEL
    # =====================

    pygame.draw.rect(screen, PANEL, (GRID_W, 0, SIDE_PANEL, HEIGHT))

    # TITLE
    title = title_font.render("AI MAZE", True, TEXT)
    screen.blit(title, (GRID_W + 60, 20))

    # INFO
    info = [
        f"Episodes: {episodes}",
        f"Steps: {steps}",
        f"Reward: {int(episode_reward)}",
        f"Epsilon: {round(agent.epsilon, 2)}"
    ]

    for i, line in enumerate(info):
        txt = font.render(line, True, TEXT)
        screen.blit(txt, (GRID_W + 30, 80 + i * 30))

    # CONTROLS
    controls_title = font.render("Controls:", True, TEXT)
    screen.blit(controls_title, (GRID_W + 30, 220))

    controls = [
        "R - Reset",
        "S - Save model",
        "UP - Faster",
        "DOWN - Slower"
    ]

    for i, line in enumerate(controls):
        txt = font.render(line, True, TEXT)
        screen.blit(txt, (GRID_W + 30, 250 + i * 25))

    pygame.display.update() #отрисовка общей картины
    clock.tick(60) #FPS

pygame.quit()