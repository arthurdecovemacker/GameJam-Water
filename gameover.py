import pygame

pygame.init()

white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)


def game_over_screen(score, screen ,font ,screen_height,screen_width):
    screen.fill(black)

    game_over_text = font.render("Game Over!", True, red)
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(game_over_text, game_over_rect)

    score_text = font.render("Score: {}".format(score), True, red)
    score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(score_text, score_rect)

    pygame.display.update()