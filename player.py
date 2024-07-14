import pygame
import random
import os
from menu import draw_menu

pygame.init()

screen_width = 1300
screen_height = 1300

white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

obstacle_size = 50
speed = 10


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        player_image_path = "image/player.png"
        if os.path.exists(player_image_path):
            self.surf = pygame.image.load(player_image_path).convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (150, 150))
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
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width