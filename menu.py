import pygame

# Initialisation de Pygame
pygame.init()

pygame.display.set_caption("rain game")

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
blue = (0, 0, 255)
grey = (169, 169, 169)

def draw_menu(screen, font, background_image):
    screen.blit(background_image, (0, 0))  # Affichage de l'image de fond

    title_text = font.render("Rain Game", True, black)
    screen.blit(title_text, (screen.get_width() / 2 - title_text.get_width() / 2, screen.get_height() / 2 - title_text.get_height() / 2 - 100))

    play_button = pygame.Rect(screen.get_width() / 2 - 100, screen.get_height() / 2 - 50, 200, 50)
    exit_button = pygame.Rect(screen.get_width() / 2 - 100, screen.get_height() / 2 + 50, 200, 50)

    pygame.draw.rect(screen, grey, play_button)
    pygame.draw.rect(screen, grey, exit_button)

    play_text = font.render("Play", True, black)
    exit_text = font.render("Exit", True, black)

    screen.blit(play_text, (play_button.x + play_button.width / 2 - play_text.get_width() / 2, play_button.y + play_button.height / 2 - play_text.get_height() / 2))
    screen.blit(exit_text, (exit_button.x + exit_button.width / 2 - exit_text.get_width() / 2, exit_button.y + exit_button.height / 2 - exit_text.get_height() / 2))

    pygame.display.update()

    return play_button, exit_button
