import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("monkey's growing tail!")

GAME_FONT = pygame.font.SysFont('couriernew', 20, True)

BLACK = (0, 0, 0)
BLUE = (35, 150, 255)
YELLOW = (220, 220, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
WHITE = (220, 220, 220)

SNAKE_SIZE = 10
FOOD_SIZE_L = 15
FOOD_SIZE_H = 40
INIT_VELOCITY = 3
TIME_LENGTH = 300

FPS = 60

EAT_FOOD = pygame.USEREVENT + 1

OUCH_SFX = pygame.mixer.Sound('/Users/mankimanford/Documents/Code/PygameSnake/assets/ouch.mp3')
CHOMP = pygame.mixer.Sound('/Users/mankimanford/Documents/Code/PygameSnake/assets/chomp.mp3')
MUSIC = pygame.mixer.Sound('/Users/mankimanford/Documents/Code/PygameSnake/assets/music.mp3')
GAMEOVER = pygame.mixer.Sound('/Users/mankimanford/Documents/Code/PygameSnake/assets/gameover.mp3')

GRASS_BACKGROUND = pygame.image.load(os.path.join(
    '/Users/mankimanford/Documents/Code/PygameSnake/assets/grass.png'))

BURGER_IMG = pygame.image.load(os.path.join(
    '/Users/mankimanford/Documents/Code/PygameSnake/assets/burger.png'))
ASIAN_FOOD = pygame.image.load(os.path.join(
    '/Users/mankimanford/Documents/Code/PygameSnake/assets/asian.png'))
SALMON = pygame.image.load(os.path.join(
    '/Users/mankimanford/Documents/Code/PygameSnake/assets/salmon.png'))
PIZZA = pygame.image.load(os.path.join(
    '/Users/mankimanford/Documents/Code/PygameSnake/assets/pizza.png'))

SNAKE_HEAD_IMG_U = pygame.transform.scale(pygame.image.load(os.path.join(
    '/Users/mankimanford/Documents/Code/PygameSnake/assets/snakehead.png')), (SNAKE_SIZE*2, SNAKE_SIZE*3))
SNAKE_HEAD_IMG_L = pygame.transform.rotate(SNAKE_HEAD_IMG_U, 90)
SNAKE_HEAD_IMG_D = pygame.transform.rotate(SNAKE_HEAD_IMG_U, 180)
SNAKE_HEAD_IMG_R = pygame.transform.rotate(SNAKE_HEAD_IMG_U, 270)


SNAKE_BODY_IMG_U = pygame.transform.scale(pygame.image.load(
    os.path.join('/Users/mankimanford/Documents/Code/PygameSnake/assets/snakebody.png')), (SNAKE_SIZE*2, SNAKE_SIZE*2.5))
SNAKE_BODY_IMG_L = pygame.transform.rotate(SNAKE_BODY_IMG_U, 90)

SNAKE_TAIL_IMG_U = pygame.transform.scale(pygame.image.load(
    os.path.join('/Users/mankimanford/Documents/Code/PygameSnake/assets/snaketail.png')), (SNAKE_SIZE*2, SNAKE_SIZE*2.5))
SNAKE_TAIL_IMG_L = pygame.transform.rotate(SNAKE_TAIL_IMG_U, 90)
SNAKE_TAIL_IMG_D = pygame.transform.rotate(SNAKE_TAIL_IMG_U, 180)
SNAKE_TAIL_IMG_R = pygame.transform.rotate(SNAKE_TAIL_IMG_U, 270)

global food_counter

def handle_food(snake, food):
    if snake.colliderect(food):
        pygame.event.post(pygame.event.Event(EAT_FOOD))
        food.x = random.randint(40, 760)
        food.y = random.randint(70, 570)
        size = random.randint(FOOD_SIZE_L, FOOD_SIZE_H)
        food.width = size
        food.height = size
    return food


def tail_movement(tails, snake):
    if len(tails) > 0:
        for i in range(len(tails) - 1, 0, -1):
            tails[i].x = tails[i - 1].x
            tails[i].y = tails[i - 1].y
        tails[0].x = snake.x
        tails[0].y = snake.y
    return tails


def snake_handle(keys_pressed, snake, direction, snake_speed):

    if direction == 'u':
        snake.y -= snake_speed
    if direction == 'd':
        snake.y += snake_speed
    if direction == 'l':
        snake.x -= snake_speed
    if direction == 'r':
        snake.x += snake_speed

    if keys_pressed[pygame.K_UP] and direction != 'd':
        direction = 'u'
    if keys_pressed[pygame.K_DOWN] and direction != 'u':
        direction = 'd'
    if keys_pressed[pygame.K_LEFT] and direction != 'r':
        direction = 'l'
    if keys_pressed[pygame.K_RIGHT] and direction != 'l':
        direction = 'r'

    return direction

def draw_window(snake, food, tails, points, health, time, direction, snake_speed, food_counter):
    divisor = 4
    if snake_speed < 4:
        divisor = 4
    elif snake_speed > 4:
        divisor = 3
    elif snake_speed > 5:
        divisor = 2

    WINDOW.blit(GRASS_BACKGROUND, (0, 0))

    health_bar = ""
    health = health // 100
    for i in range(0, health):
        health_bar += "O"

    for i in range(len(tails) - 2, 0, -1):
        #pygame.draw.rect(WINDOW, YELLOW, tails[i])
        if i == len(tails) - 2:
            if tails[i - 1].x == tails[i].x and tails [i - 1].y - tails[i].y < 0:
                WINDOW.blit(SNAKE_TAIL_IMG_U, (tails[i].x - 5, tails[i].y - 10))
            elif tails[i - 1].x == tails[i].x and tails [i - 1].y - tails[i].y > 0:
                WINDOW.blit(SNAKE_TAIL_IMG_D, (tails[i].x - 5, tails[i].y - 10))
            elif tails[i - 1].y == tails[i].y and tails [i - 1].x - tails[i].x > 0:
                WINDOW.blit(SNAKE_TAIL_IMG_R, (tails[i].x - 10, tails[i].y - 5))
            elif tails[i - 1].y == tails[i].y and tails [i - 1].x - tails[i].x < 0:
                WINDOW.blit(SNAKE_TAIL_IMG_L, (tails[i].x - 10, tails[i].y - 5))
        elif tails[i + 1].x == tails[i].x and i % divisor == 0:
            WINDOW.blit(SNAKE_BODY_IMG_U, (tails[i].x - 5, tails[i].y - 10))
        elif tails[i + 1].x != tails[i].x and i % divisor == 0:
            WINDOW.blit(SNAKE_BODY_IMG_L, (tails[i].x - 10, tails[i].y - 5))

    #pygame.draw.rect(WINDOW, YELLOW, snake)
    if direction == 'u':
        WINDOW.blit(SNAKE_HEAD_IMG_U, (snake.x - 5, snake.y - 5))
    elif direction == 'l':
        WINDOW.blit(SNAKE_HEAD_IMG_L, (snake.x - 5, snake.y - 5))
    elif direction == 'd':
        WINDOW.blit(SNAKE_HEAD_IMG_D, (snake.x - 5, snake.y - 15))
    else:
        WINDOW.blit(SNAKE_HEAD_IMG_R, (snake.x - 10, snake.y - 5))

    if food_counter == 1:
        food_item = pygame.transform.scale(PIZZA, (food.width+10, food.width+5))
    elif food_counter == 2:
        food_item = pygame.transform.scale(BURGER_IMG, (food.width+10, food.width+5))
    elif food_counter == 3:
        food_item = pygame.transform.scale(ASIAN_FOOD, (food.width+10, food.width+5))
    else:
        food_item = pygame.transform.scale(SALMON, (food.width+10, food.width+5))
        food_counter = 1
    #pygame.draw.rect(WINDOW, RED, food)
    WINDOW.blit(food_item, (food.x - 5, food.y - 2))
    show_points = GAME_FONT.render("POINTS: " + str(points), 1, RED)
    show_health = GAME_FONT.render("HEALTH: " + health_bar, 1, YELLOW)
    show_time = GAME_FONT.render("TIME: " + str(time//50), 1, WHITE)
    WINDOW.blit(show_points, (100, 40))
    WINDOW.blit(show_time, (350, 520))
    WINDOW.blit(show_health, (500, 40))
    pygame.display.update()

def main():
    snake = pygame.Rect(400, 500, SNAKE_SIZE, SNAKE_SIZE)
    size = random.randint(FOOD_SIZE_L, FOOD_SIZE_H)
    food = pygame.Rect(200,100, size, size)
    tails = []
    direction = 'u'
    snake_speed = INIT_VELOCITY
    run = True
    clock = pygame.time.Clock()
    add_tail = False
    tail_counter = 0
    tick = 0
    dead = False
    calories = 0
    points = 0
    point_counter = 0
    time_bonus = 0
    health = 1000
    damage_buffer = False
    damage_counter = 100
    time = 1050
    food_counter = 1
    MUSIC.play()




    while(run):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == EAT_FOOD:
                CHOMP.play()
                pygame.time.delay(food.width)
                snake_speed += 0.10
                add_tail = True
                calories = food.width
                health += 10
                if food.width >= 37:
                    calories *= 3
                    health += 40
                    snake_speed *= 0.95
                if health > 1000:
                    health = 1000
                points = points + calories + point_counter + (time_bonus//10)
                time_bonus = 1000
                time += 120
                if food.width < 20:
                    time += 240
                point_counter += 5
                food_counter += 1
                if food_counter > 4:
                    food_counter = 1
                temp_snake = pygame.Rect(snake.x, snake.y, SNAKE_SIZE, SNAKE_SIZE)

        if add_tail:
            tail_counter += 1
            tail = pygame.Rect(temp_snake.x, temp_snake.y, SNAKE_SIZE, SNAKE_SIZE)
            tails.append(tail)
        if tail_counter >= calories:
            add_tail = False
            tail_counter = 0
                
        tails = tail_movement(tails, snake)
        keys_pressed = pygame.key.get_pressed()
        direction = snake_handle(keys_pressed, snake, direction, snake_speed)
        food = handle_food(snake, food)


        time -= 1
        if time % 105 == 0:
            health += 25

        draw_window(snake, food, tails, points, health, time, direction, snake_speed, food_counter)


        damage_counter -= 1
        for i in range(10, len(tails)):
            if snake.colliderect(tails[i]):
                if damage_buffer:
                    health -= 1
                    time += 1
                    pygame.time.delay(2)
                else:
                    health -= 100
                    time +=10
                    OUCH_SFX.play()
                    damage_buffer = True
                    damage_counter = 100
                    pygame.time.delay(100)

            if damage_counter < 0:
                damage_buffer = False
                damage_counter = 100

        if health < 0 or time == 0:
            MUSIC.stop()
            GAMEOVER.play()
            break

        if time_bonus > 0:
            time_bonus -= 1

    pygame.time.delay(3000)
    main()

if __name__ == "__main__":
            main()