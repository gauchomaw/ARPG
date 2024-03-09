import pygame
import random
import math

from constants import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Carrega a imagem do inimigo
        self.image = pygame.image.load(os.path.join(IMAGE_DIRECTORY, "skeleton.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center = (x, y))
        self.speed = 1
        self.target_pos = None
        self.xp = 0
        self.hp = random.randint(1, 20)
        self.score = 0
        self.width, self.height = self.image.get_size()
        self.target = None  # Alvo atual do inimigo (o jogador)
        self.hit_by_player = False  # Flag para indicar se o inimigo foi atingido pelo jogador

    def update(self, player_rect):
        # Atualiza a posição do inimigo em direção ao jogador
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance != 0:
            # Normaliza o vetor de direção
            dx /= distance
            dy /= distance

            # Move o inimigo
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

    def take_damage(self, hp):
        # Reduz o HP do inimigo
        print("self.hp before = ", str(self.hp))
        self.hp -= hp
        print("self.hp after = ", str(self.hp))