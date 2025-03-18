import pygame

pygame.init()
pygame.mixer.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frogger Game")


CARIMAGE = pygame.image.load("car.png")
LOGIMAGE = pygame.image.load("log.png")
FROGIMAGE = pygame.image.load("frog.png")


frog_rect = pygame.Rect(400, 550, 40, 40)
car_speed = 3
log_speed = 2
lives = 3
game_active = True


cars = []
for i in range(5):
    cars.append({
        "rect": pygame.Rect(WIDTH + i * 250, 350 + (i % 3) * 50, 50, 30),
        "speed": car_speed
    })

# Log setup
logs = []
for i in range(3):
    logs.append({
        "rect": pygame.Rect(i * 300, 150 + (i % 2) * 50, 100, 30),
        "speed": log_speed * (1 if i % 2 == 0 else -1)
    })


river_rect = pygame.Rect(0, 100, WIDTH, 200)


running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_active:
                if event.key == pygame.K_LEFT and frog_rect.left > 0:
                    frog_rect.x -= 40
                elif event.key == pygame.K_RIGHT and frog_rect.right < WIDTH:
                    frog_rect.x += 40
                elif event.key == pygame.K_UP and frog_rect.top > 0:
                    frog_rect.y -= 40
                elif event.key == pygame.K_DOWN and frog_rect.bottom < HEIGHT:
                    frog_rect.y += 40
            else:
                game_active = True
                lives = 3
                frog_rect.topleft = (400, 550)

    if game_active:
        for car in cars:
            car["rect"].x -= car["speed"]
            if car["rect"].right < 0:
                car["rect"].left = WIDTH

        for log in logs:
            log["rect"].x += log["speed"]
            if log["rect"].left > WIDTH:
                log["rect"].right = 0
            elif log["rect"].right < 0:
                log["rect"].left = WIDTH

        if any(frog_rect.colliderect(car["rect"]) for car in cars):
            lives -= 1
            frog_rect.topleft = (400, 550)
            pygame.mixer.Sound("crash.ogg").play()
            if lives <= 0:
                game_active = False

        if frog_rect.colliderect(river_rect):
            on_log = False
            for log in logs:
                if frog_rect.colliderect(log["rect"]):
                    on_log = True
                    frog_rect.x += log["speed"]
            if not on_log:
                lives -= 1
                frog_rect.topleft = (400, 550)
                if lives <= 0:
                    game_active = False


        for car in cars:
            screen.blit(CARIMAGE, car["rect"])
        for log in logs:
            screen.blit(LOGIMAGE, log["rect"])
        screen.blit(FROGIMAGE, frog_rect)

        for i in range(lives):
            screen.blit(FROGIMAGE, (10 + i * 40, 580))
    else:
        font = pygame.font.Font(None, 50)
        text = font.render("Game Over! Press any key to restart", True, (255, 0, 0))
        screen.blit(text, (200, 250))

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()

