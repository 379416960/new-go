import pygame
import random
# 初始化
pygame.init()
# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
# 设置屏幕大小
size = (500, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("贪吃蛇")
# 初始化贪吃蛇
snake = [(250, 250)]
direction = 'right'
# 初始化食物
food = (random.randint(0, 49)*10, random.randint(0, 49)*10)
# 设置帧率
clock = pygame.time.Clock()
# 游戏循环
while True:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # 处理按键事件
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != 'right':
                direction = 'left'
            elif event.key == pygame.K_RIGHT and direction != 'left':
                direction = 'right'
            elif event.key == pygame.K_UP and direction != 'down':
                direction = 'up'
            elif event.key == pygame.K_DOWN and direction != 'up':
                direction = 'down'
    # 移动贪吃蛇
    if direction == 'left':
        x = snake[0][0] - 10
        y = snake[0][1]
    elif direction == 'right':
        x = snake[0][0] + 10
        y = snake[0][1]
    elif direction == 'up':
        x = snake[0][0]
        y = snake[0][1] - 10
    elif direction == 'down':
        x = snake[0][0]
        y = snake[0][1] + 10
    snake.insert(0, (x, y))
    snake.pop()
    # 判断是否吃到食物
    if snake[0] == food:
        food = (random.randint(0, 49)*10, random.randint(0, 49)*10)
        snake.append(snake[-1])
    # 判断是否撞到墙或自己
    if snake[0][0] < 0 or snake[0][0] > 490 or snake[0][1] < 0 or snake[0][1] > 490:
        pygame.quit()
        quit()
    for i in range(1, len(snake)):
        if snake[0] == snake[i]:
            pygame.quit()
            quit()
    # 绘制屏幕
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, [food[0], food[1], 10, 10])
    for i in snake:
        pygame.draw.rect(screen, BLACK, [i[0], i[1], 10, 10])
    pygame.display.flip()
    # 设置帧率
    clock.tick(10)
# 退出
pygame.quit()
quit()