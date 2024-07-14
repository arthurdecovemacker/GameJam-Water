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

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rain Game")
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super(Obstacle, self).__init__()
        obstacle_image_path = "image/raindrop.webp"
        if os.path.exists(obstacle_image_path):
            self.surf = pygame.image.load(obstacle_image_path).convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (obstacle_size, obstacle_size))
        else:
            self.surf = pygame.Surface((obstacle_size, obstacle_size))
            self.surf.fill(blue)
        self.rect = self.surf.get_rect(center=(random.randint(0, screen_width - obstacle_size), 0))
    
    def update(self):
        self.rect.move_ip(0, speed)
        if self.rect.top > screen_height:
            self.kill()