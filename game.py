import pygame
import random
from menu import draw_menu

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre du jeu
screen_width = 1300
screen_height = 1300

# Couleurs
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
blue = (0, 0, 255)
grey = (169, 169, 169)

# Création de la fenêtre du jeu
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rain Game")

# Fontes
font = pygame.font.SysFont("monospace", 35)

# Charger l'image de fond
background_image = pygame.image.load("Background.jpg")  # Assurez-vous que le fichier background.jpg existe dans le même répertoire que votre script
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Position initiale du joueur
player_size = 50
player_pos = [screen_width / 2, screen_height - 2 * player_size]

# Taille et position des obstacles
obstacle_size = 50

# Vitesse des obstacles
speed = 10

# Définition des horloges pour le framerate
clock = pygame.time.Clock()

# Fonction pour détecter les collisions
def detect_collision(player_pos, obstacle_pos):
    p_x, p_y = player_pos
    o_x, o_y = obstacle_pos

    if (o_x >= p_x and o_x < (p_x + player_size)) or (p_x >= o_x and p_x < (o_x + obstacle_size)):
        if (o_y >= p_y and o_y < (p_y + player_size)) or (p_y >= o_y and p_y < (o_y + obstacle_size)):
            return True
    return False

# Fonction principale du jeu
def game():
    player_pos = [screen_width / 2, screen_height - 2 * player_size]
    obstacle_pos = [random.randint(0, screen_width - obstacle_size), 0]
    game_over = False
    score = 0
    lives = 1  # Nombre de vies du joueur

    while not game_over and lives > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()
        
        # Vitesse du joueur en fonction des vies restantes
        player_speed = 11 - (3 - lives) * 2  # Vitesse réduite de 2 pour chaque vie perdue
        
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size:
            player_pos[0] += player_speed

        # Affichage de l'image de fond
        screen.blit(background_image, (0, 0))

        if obstacle_pos[1] >= 0 and obstacle_pos[1] < screen_height:
            obstacle_pos[1] += speed
        else:
            obstacle_pos = [random.randint(0, screen_width - obstacle_size), 0]
            score += 1

        if detect_collision(player_pos, obstacle_pos):
            lives -= 1
            obstacle_pos = [random.randint(0, screen_width - obstacle_size), 0]
            if lives == 0:
                game_over = True

        pygame.draw.rect(screen, red, (player_pos[0], player_pos[1], player_size, player_size))
        pygame.draw.rect(screen, green, (obstacle_pos[0], obstacle_pos[1], obstacle_size, obstacle_size))

        # Affichage du score et des vies
        score_text = font.render("Score: {}".format(score), True, white)
        screen.blit(score_text, (10, 10))
        lives_text = font.render("Lives: {}".format(lives), True, white)
        screen.blit(lives_text, (screen_width - 200, 10))

        pygame.display.update()

        clock.tick(30)

    return score

def game_over_screen(score):
    screen.fill(black)
    
    # Texte "Game Over!"
    game_over_text = font.render("Game Over!", True, red)
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(game_over_text, game_over_rect)

    # Texte du score
    score_text = font.render("Score: {}".format(score), True, red)
    score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(score_text, score_rect)

    pygame.display.update()


# Boucle principale avec le menu
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
                # Affichage de l'écran de fin
                game_over_screen(score)
                pygame.time.wait(2000)  # Pause de 2 secondes

            if exit_button.collidepoint(mouse_pos):
                running = False

pygame.quit()
