import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000,800

WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("Space Wars")

BG = pygame.image.load("Rain/bg.jpeg")

Player_width = 40
Player_height = 60
Player_Vel = 5
Star_Vel = 5
Star_width = 10
Star_height = 10

Font = pygame.font.SysFont("comicsans", 24)

def draw(player, elapsed_time, stars, score):
    WIN.blit(BG, (0,0))
    time_text = Font.render(f"Time: {round(elapsed_time)}s", 1, "White")
    score_text = Font.render(f"Score: {score}",1,"White")
    WIN.blit(time_text, (10,10))
    WIN.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
    pygame.draw.rect(WIN, "blue", player)

    for star in stars:
        pygame.draw.rect(WIN, "red", star)

    pygame.display.update()

def main():
    run = True
    score = 0
    Player = pygame.Rect(200, HEIGHT - Player_height, Player_width, Player_height)
    Clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000   #milliseconds
    star_count = 0              #when the next star should be added

    stars = []
    Hit = False

    while run:
        # Clock.tick(144)
        star_count += Clock.tick(144)   #return no of milliseconds since last tick
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(5):
                star_x = random.randint(0,WIDTH - Star_width)
                star = pygame.Rect(star_x, -Star_height, Star_width, Star_height)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and Player.x - Player_Vel >= 0:
            Player.x -= Player_Vel
        elif keys[pygame.K_RIGHT] and Player.x + Player_Vel <= (WIDTH - Player_width):
            Player.x += Player_Vel

        for star in stars[:]:
            star.y += Star_Vel
            if star.y > HEIGHT:
                stars.remove(star)
                score += 1
            elif star.y + star.height >= Player.y and star.colliderect(Player):
                stars.remove(star)
                Hit = True
                break

        if Hit:
            lost_text = Font.render("You lost!", 1, "White")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(5000)
            break

        draw(Player,elapsed_time,stars,score)

    pygame.quit()

if __name__ == "__main__":
    main()