import pygame
import os
from menu import draw_menu
from obstacle import Obstacle
from gameover import game_over_screen
from player import Player

pygame.init()

screen_width = 1300
screen_height = 1300
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rain Game")

font = pygame.font.SysFont("bold", 55)

pygame.mixer.init()

pygame.mixer.music.load('image/rain-01.mp3')

background_image_path = "image/Background.jpg"
if os.path.exists(background_image_path):
    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
else:
    background_image = pygame.Surface((screen_width, screen_height))
    background_image.fill(black)

clock = pygame.time.Clock()

def game():
    player = Player()
    obstacles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    game_over = False
    score = 0
    lives = 5

    ADD_OBSTACLE = pygame.USEREVENT + 1
    obstacle_add_time = 1000 
    pygame.time.set_timer(ADD_OBSTACLE, obstacle_add_time)

    pygame.mixer.music.play(loops=-1)

    while not game_over and lives > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == ADD_OBSTACLE:
                new_obstacle = Obstacle()
                obstacles.add(new_obstacle)
                all_sprites.add(new_obstacle)
                if obstacle_add_time > 200:
                    obstacle_add_time -= 10
                pygame.time.set_timer(ADD_OBSTACLE, obstacle_add_time)

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        obstacles.update()
        if pygame.sprite.spritecollideany(player, obstacles):
            lives -= 1
            if lives > 0:
                for obstacle in obstacles:
                    if pygame.sprite.collide_rect(player, obstacle):
                        obstacle.kill()
            else:
                game_over = True
        screen.blit(background_image, (0, 0))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        score_text = font.render("Score: {}".format(score), True, white)
        screen.blit(score_text, (10, 10))
        lives_text = font.render("Lives: {}".format(lives), True, white)
        screen.blit(lives_text, (screen_width - 200, 10))

        pygame.display.update()

        clock.tick(30)
        score += 1

    pygame.mixer.music.stop()

    return score

running = True
while running:
    play_button, exit_button = draw_menu(screen, font, background_image)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if play_button.collidepoint(mouse_pos):
                score = game()
                game_over_screen(score, screen, font, screen_height, screen_width)
                pygame.time.wait(2000)

            if exit_button.collidepoint(mouse_pos):
                running = False

pygame.quit()

