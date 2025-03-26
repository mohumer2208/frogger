import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("frogger")

frogpic = pygame.transform.scale(pygame.image.load("frog.png"), (50, 50))
carpic = pygame.transform.scale(pygame.image.load("car.png"), (100, 100))
logpic = pygame.transform.scale(pygame.image.load("log.png"), (200, 50))

frogrect = pygame.Rect(400, 550, 20, 20)

cars = []
for i in range(5):
    cars.append(pygame.Rect(WIDTH + i * 200, 350 + (i % 3) * 40, 40, 20))

carspeed = 3

river_rect = pygame.Rect(0, 100, WIDTH, 150)
logs = []
logspeeds = []
for i in range(3):
    logs.append(pygame.Rect(i * 250, 150 + (i % 2) * 40, 60, 20))
    logspeeds.append(2 if i % 2 == 0 else -2)

lives = 3
game_active = True
running = True

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_active:
                if event.key == pygame.K_LEFT and frogrect.left > 0:
                    frogrect.x -= 20
                elif event.key == pygame.K_RIGHT and frogrect.right < WIDTH:
                    frogrect.x += 20
                elif event.key == pygame.K_UP and frogrect.top > 0:
                    frogrect.y -= 20
                elif event.key == pygame.K_DOWN and frogrect.bottom < HEIGHT:
                    frogrect.y += 20
            else:
                game_active = True
                lives = 3
                frogrect.topleft = (400, 550)

    if game_active:
        for car in cars:
            car.x -= carspeed
            if car.right < 0:
                car.left = WIDTH

        for i in range(len(logs)):
            logs[i].x += logspeeds[i]
            if logs[i].left > WIDTH:
                logs[i].right = 0
            elif logs[i].right < 0:
                logs[i].left = WIDTH

        if any(frogrect.colliderect(car) for car in cars):
            lives -= 1
            frogrect.topleft = (400, 550)
            pygame.mixer.Sound("crash.ogg").play()
            if lives <= 0:
                game_active = False

        if frogrect.colliderect(river_rect):
            on_log = False
            for i in range(len(logs)):
                if frogrect.colliderect(logs[i]):
                    on_log = True
                    frogrect.x += log_speeds[i]
            if not on_log:
                lives -= 1
                frogrect.topleft = (400, 550)
                if lives <= 0:
                    game_active = False

        for car in cars:
            screen.blit(carpic, car)
        for log in logs:
            screen.blit(logpic, log)
        screen.blit(frogpic, frogrect)

        for i in range(lives):
            screen.blit(frogpic, (10 + i * 20, 570))
    else:
        font = pygame.font.Font(None, 50)
        text = font.render("game over", True, (255, 0, 0))
        screen.blit(text, (200, 250))

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()


