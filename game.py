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

# Création de la fenêtre du jeu
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rain Game")

# Fontes
font = pygame.font.SysFont("monospace", 35)

# Charger l'image de fond
background_image = pygame.image.load("Background.jpg")  # Assurez-vous que le fichier background.jpg existe dans le même répertoire que votre script
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Taille et position des obstacles
obstacle_size = 50

# Vitesse des obstacles
speed = 10

# Définition des horloges pour le framerate
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill(red)
        self.rect = self.surf.get_rect(center=(screen_width / 2, screen_height - 100))
        self.speed = 10
    
    def update(self, pressed_keys):
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super(Obstacle, self).__init__()
        self.surf = pygame.Surface((obstacle_size, obstacle_size))
        self.surf.fill(green)
        self.rect = self.surf.get_rect(center=(random.randint(0, screen_width - obstacle_size), 0))
    
    def update(self):
        self.rect.move_ip(0, speed)
        if self.rect.top > screen_height:
            self.kill()

def game():
    player = Player()
    obstacles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    game_over = False
    score = 0
    lives = 3  # Nombre de vies du joueur

    ADD_OBSTACLE = pygame.USEREVENT + 1
    pygame.time.set_timer(ADD_OBSTACLE, 250)

    while not game_over and lives > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == ADD_OBSTACLE:
                new_obstacle = Obstacle()
                obstacles.add(new_obstacle)
                all_sprites.add(new_obstacle)

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        obstacles.update()

        if pygame.sprite.spritecollideany(player, obstacles):
            lives -= 1
            if lives == 0:
                game_over = True

        # Affichage de l'image de fond
        screen.blit(background_image, (0, 0))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Affichage du score et des vies
        score_text = font.render("Score: {}".format(score), True, white)
        screen.blit(score_text, (10, 10))
        lives_text = font.render("Lives: {}".format(lives), True, white)
        screen.blit(lives_text, (screen_width - 200, 10))

        pygame.display.update()

        clock.tick(30)
        score += 1

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
