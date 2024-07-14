import pygame
import random
import os
from menu import draw_menu

# Initialize Pygame
pygame.init()

# Window dimensions
screen_width = 1300
screen_height = 1300

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rain Game")

# Fonts
font = pygame.font.SysFont("monospace", 35)

# Check if the background image exists before loading
background_image_path = "Background.jpg"
if os.path.exists(background_image_path):
    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
else:
    background_image = pygame.Surface((screen_width, screen_height))
    background_image.fill(black)

# Obstacle size and speed
obstacle_size = 50
speed = 10

# Clock for framerate
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        player_image_path = "player.png"
        if os.path.exists(player_image_path):
            self.surf = pygame.image.load(player_image_path).convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (150, 150))  # Resize the image to 50x50 pixels
        else:
            self.surf = pygame.Surface((50, 50))
            self.surf.fill(red)
        self.rect = self.surf.get_rect(center=(screen_width / 2, screen_height - 70))
        self.speed = 5
    
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
        self.surf.fill(blue)
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
    lives = 3  # Number of player lives

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

        # Check for collisions
        if pygame.sprite.spritecollideany(player, obstacles):
            lives -= 1
            if lives > 0:
                # Remove the colliding obstacle to avoid multiple collisions
                for obstacle in obstacles:
                    if pygame.sprite.collide_rect(player, obstacle):
                        obstacle.kill()
            else:
                game_over = True

        # Display background image
        screen.blit(background_image, (0, 0))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Display score and lives
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
    
    # "Game Over!" text
    game_over_text = font.render("Game Over!", True, red)
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(game_over_text, game_over_rect)

    # Score text
    score_text = font.render("Score: {}".format(score), True, red)
    score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(score_text, score_rect)

    pygame.display.update()

# Main loop with menu
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
                # Display game over screen
                game_over_screen(score)
                pygame.time.wait(2000)  # 2-second pause

            if exit_button.collidepoint(mouse_pos):
                running = False

pygame.quit()
