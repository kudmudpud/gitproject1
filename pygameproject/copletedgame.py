import pygame, sys
import random
from button import Button
from random import randrange as rnd
from random import randint

pygame.init()

# задаются параметры(размеры) приложения
SCREEN = pygame.display.set_mode((1200, 720))

# рандомайзер фонов для экрана меню
test_list = ["12.png", "13.png", "14.jpg", "15.png", "17.jpg"]
random_index = random.randint(0, len(test_list) - 1)
BG = pygame.image.load(test_list[random_index])


# функция отвечающая за шрифт и размер текста
def get_font(size):
    return pygame.font.Font("font.ttf", size)


# функция отвечающая за цвет мячика в игре арканоид
def random_color():
    levels = range(32,256,5)
    return tuple(random.choice(levels) for _ in range(3))

# функция игры арканоид
def arcanoid():
    # задаем иконку игре
    pygame.display.set_icon(pygame.image.load("arcanoid.png"))

    # размеры экрана
    WIDTH, HEIGHT = 1200, 720
    # кадры в секунду
    fps = 60
    # настройки платформы
    paddle_w = 330
    paddle_h = 35
    paddle_speed = 15
    paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)
    # настройки мяча
    ball_radius = 20
    ball_speed = 6
    ball_rect = int(ball_radius * 2 ** 0.5)
    ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
    dx, dy = 1, -1
    # настройки блоков
    block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(5)]
    color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(5)]

    pygame.init()
    sc = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    # настройки фона игры с тем же рандомайзером
    test_list1 = ["23.png", "25.png", "1.jpg", "26.jpg", "22.jpg", "27.jpg", "28.jpg"]
    random_index1 = random.randint(0, len(test_list1) - 1)

    img = pygame.image.load(test_list1[random_index1])
    # название и напутствие
    pygame.display.set_caption("Arcanoid!       Destroy all blocks to WIN!!!")

    # функция отвечающая за столкновения
    def detect_collision(dx, dy, ball, rect):
        if dx > 0:
            delta_x = ball.right - rect.left
        else:
            delta_x = rect.right - ball.left
        if dy > 0:
            delta_y = ball.bottom - rect.top
        else:
            delta_y = rect.bottom - ball.top

        if abs(delta_x - delta_y) < 10:
            dx, dy = -dx, -dy
        elif delta_x > delta_y:
            dy = -dy
        elif delta_y > delta_x:
            dx = -dx
        return dx, dy


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        # заливка фона изображением
        sc.blit(img, (0, 0))
        # отрисовка объектов
        [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
        pygame.draw.rect(sc, pygame.Color("white"), paddle)
        pygame.draw.circle(sc, pygame.Color(random_color()), ball.center, ball_radius)
        # движение мяча
        ball.x += ball_speed * dx
        ball.y += ball_speed * dy
        # столкновения с горизонтальными границами
        if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
            dx = -dx
        # столкновения с верхней границей
        if ball.centery < ball_radius:
            dy = -dy
        # столкновение с платформой
        if ball.colliderect(paddle) and dy > 0:
            dx, dy = detect_collision(dx, dy, ball, paddle)
        # столкновения с блоками
        hit_index = ball.collidelist(block_list)
        if hit_index != -1:
            hit_rect = block_list.pop(hit_index)
            hit_color = color_list.pop(hit_index)
            dx, dy = detect_collision(dx, dy, ball, hit_rect)
            hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
            pygame.draw.rect(sc, hit_color, hit_rect)
            fps += 2
        # поражение
        if ball.bottom > HEIGHT:
            play1()
        # победа
        elif not len(block_list):
            play()
        # управление
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddle_speed
        if key[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.right += paddle_speed
        # обновления экрана
        pygame.display.flip()
        clock.tick(fps)


# функция игры пинг понг
def ping_pong():
    # иконка пинг понга
    pygame.display.set_icon(pygame.image.load("ping.png"))

    pygame.init()

    # размеры приложения
    WIDTH, HEIGHT = 1200, 720

    # рандомайзер фонов для понг понга
    test_list1 = ["23.png", "25.png", "1.jpg", "26.jpg", "22.jpg", "27.jpg", "28.jpg"]
    random_index1 = random.randint(0, len(test_list1) - 1)

    img = pygame.image.load(test_list1[random_index1])

    # функция отвечающая за шрифт и размер текста
    def get_font(size):
        return pygame.font.Font("font.ttf", size)

    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    # название и напутсвие
    pygame.display.set_caption("Pong!       Score 10 points to WIN!!!")

    CLOCK = pygame.time.Clock()

    # настройки платформы

    player = pygame.Rect(0, 0, 10, 100)
    player.center = (WIDTH - 100, HEIGHT / 2)

    opponent = pygame.Rect(0, 0, 10, 100)
    opponent.center = (100, HEIGHT / 2)

    player_score, opponent_score = 0, 0

    # настройки мяча

    ball = pygame.Rect(0, 0, 20, 20)
    ball.center = (WIDTH / 2, HEIGHT / 2)

    x_speed, y_speed = 1, 1

    while True:
        keys_pressed = pygame.key.get_pressed()
        # заливка фона изображением
        SCREEN.blit(img, (0, 0))

        # правая стрелка
        if keys_pressed[pygame.K_RIGHT]:
            if player.top > 0:
                player.top -= 2
        # левая стрелка
        if keys_pressed[pygame.K_LEFT]:
            if player.bottom < HEIGHT:
                player.bottom += 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # настройки и движения мяча
        if ball.y >= HEIGHT:
            y_speed = -1
        if ball.y <= 0:
            y_speed = 1
        if ball.x <= 0:
            player_score += 1
            ball.center = (WIDTH / 2, HEIGHT / 2)
            x_speed, y_speed = random.choice([1, -1]), random.choice([1, -1])
        if ball.x >= WIDTH:
            opponent_score += 1
            ball.center = (WIDTH / 2, HEIGHT / 2)
            x_speed, y_speed = random.choice([1, -1]), random.choice([1, -1])
        if player.x - ball.width <= ball.x <= player.right and ball.y in range(player.top - ball.width,
                                                                               player.bottom + ball.width):
            x_speed = -1
        if opponent.x - ball.width <= ball.x <= opponent.right and ball.y in range(opponent.top - ball.width,
                                                                                   opponent.bottom + ball.width):
            x_speed = 1
        # победа
        if player_score >= 10:
            play2()
        # поражение
        if opponent_score >= 10:
            play3()

        # вывод счета на экран
        point = ":"
        player_score_text = get_font(75).render(str(player_score), True, "white")
        opponent_score_text = get_font(75).render(str(opponent_score), True, "white")
        point_text = get_font(75).render(str(point), True, "white")

        if opponent.y < ball.y:
            opponent.top += 1
        if opponent.bottom > ball.y:
            opponent.bottom -= 1

        ball.x += x_speed * 2
        ball.y += y_speed * 2


        pygame.draw.rect(SCREEN, "white", player)
        pygame.draw.rect(SCREEN, "white", opponent)
        pygame.draw.circle(SCREEN, "white", ball.center, 10)

        SCREEN.blit(player_score_text, (WIDTH / 2 + 120, 50))
        SCREEN.blit(opponent_score_text, (WIDTH / 2 - 170, 50))
        SCREEN.blit(point_text, (WIDTH / 2 - 20, 50))

        pygame.display.update()
        CLOCK.tick(300)

# функции меню после выигрыша или поражения
# они все аналогичные, я опишу только одну
def play():
    while True:
        # отслеживание мыши
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        # цвет фона
        SCREEN.fill("black")
        # сам текст
        PLAY_TEXT = get_font(45).render("WIN!!!", True, "White")
        # координирование размещения на экране
        PLAY_RECT = PLAY_TEXT.get_rect(center=(600, 200))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)
        # кнопка возвращения в главное меню
        PLAY_BACK = Button(image=None, pos=(600, 360),
                           text_input="BACK to MENU", font=get_font(75), base_color="White", hovering_color="Green")
        # кнопка повторить предидущее действие
        PLAY_RETRY = Button(image=None, pos=(600, 490),
                           text_input="RETRY", font=get_font(75), base_color="White", hovering_color="Green")

        # смена цвета кнопок при наведении на них мышкой
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        PLAY_RETRY.changeColor(PLAY_MOUSE_POS)
        PLAY_RETRY.update(SCREEN)

        # присвоение действий каждой кнопке
        for event in pygame.event.get():
            # выход
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # вернуться в главное меню
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
            # повторить
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_RETRY.checkForInput(PLAY_MOUSE_POS):
                    arcanoid()

        pygame.display.update()


def play1():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("LOSE(", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(600, 200))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(600, 360),
                           text_input="BACK to MENU", font=get_font(75), base_color="White", hovering_color="Green")
        PLAY_RETRY = Button(image=None, pos=(600, 490),
                           text_input="RETRY", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        PLAY_RETRY.changeColor(PLAY_MOUSE_POS)
        PLAY_RETRY.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_RETRY.checkForInput(PLAY_MOUSE_POS):
                    arcanoid()

        pygame.display.update()


def play2():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("WIN!!!", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(600, 200))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(600, 360),
                           text_input="BACK to MENU", font=get_font(75), base_color="White", hovering_color="Green")
        PLAY_RETRY = Button(image=None, pos=(600, 490),
                           text_input="RETRY", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        PLAY_RETRY.changeColor(PLAY_MOUSE_POS)
        PLAY_RETRY.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_RETRY.checkForInput(PLAY_MOUSE_POS):
                    ping_pong()

        pygame.display.update()


def play3():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("LOSE(", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(600, 200))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(600, 360),
                           text_input="BACK to MENU", font=get_font(75), base_color="White", hovering_color="Green")
        PLAY_RETRY = Button(image=None, pos=(600, 490),
                           text_input="RETRY", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        PLAY_RETRY.changeColor(PLAY_MOUSE_POS)
        PLAY_RETRY.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_RETRY.checkForInput(PLAY_MOUSE_POS):
                    ping_pong()

        pygame.display.update()

# мануал игр и меню
def options():
    while True:
        # иконка
        pygame.display.set_icon(pygame.image.load("options.png"))
        # отслеживание мышки
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        # название
        pygame.display.set_caption("Optoins")
        # заливка фона
        SCREEN.fill("black")

        # здесь текстом расписано управление в приложении
        OPTIONS_TEXT = get_font(45).render("CONTROLS:", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(600, 75))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        OPTIONS_TEXT = get_font(45).render("In THE GAME:", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(600, 150))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        OPTIONS_TEXT = get_font(45).render("right arrow ->", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(600, 210))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        OPTIONS_TEXT = get_font(45).render("left arrow <-", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(600, 270))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        OPTIONS_TEXT = get_font(45).render("In THE MENU:", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(600, 330))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        OPTIONS_TEXT = get_font(45).render("mouse 🖱", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(600, 410))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        # выйти из мануала
        OPTIONS_BACK = Button(image=None, pos=(600, 580),
                              text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        # присвоение действия кнопке
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # вернуться в меню
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

# главное меню
def main_menu():
    while True:
        # заливка картинокой фона
        SCREEN.blit(BG, (0, 0))
        # название
        pygame.display.set_caption("Menu")
        # иконка
        pygame.display.set_icon(pygame.image.load("logo.png"))
        # отслеживание мыши
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        # текст меню
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#e3d1d1")
        # координаты расположения текста
        MENU_RECT = MENU_TEXT.get_rect(center=(600, 100))

        # запустить пинг понг
        PLAY1_BUTTON = Button(image=pygame.image.load("Play Ping Pong Rect.png"), pos=(600, 350),
                             text_input="PING PONG", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        # запустить арканоид
        PLAY2_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(600, 220),
                              text_input="ARCANOID", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        # запуск мануала
        OPTIONS_BUTTON = Button(image=pygame.image.load("Options Rect.png"), pos=(600, 480),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        # выход из игры
        QUIT_BUTTON = Button(image=pygame.image.load("Quit Rect.png"), pos=(600, 610),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # смена цвета кнопки при наведении на нее мышкой
        for button in [PLAY1_BUTTON, PLAY2_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # присвоение действий каждой кнопке
        for event in pygame.event.get():
            # вход
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # запуск пинг понга
                if PLAY1_BUTTON.checkForInput(MENU_MOUSE_POS):
                    ping_pong()
                # запуск арканоида
                if PLAY2_BUTTON.checkForInput(MENU_MOUSE_POS):
                    arcanoid()
                # запуск мануала
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                # выход
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()