import pygame
import time
import random
import math
from typing import List

from constants import *
from player import Player
from enemy import Enemy

class Game():
    def __init__(self):
        # Inicialização do Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.player = Player(200, 200)
        self.all_sprites = pygame.sprite.Group(self.player)

        self.enemies:List[Enemy] = []
        self.last_enemy_add_time = time.time()

    def run(self):

        self.create_enemies(5)

        # Flag para controlar se o jogador está se movendo
        moving = False  

        # Loop principal
        running = True
        while running:
            self.clock.tick(FPS)
            self.screen.fill(WHITE)

            # Desenha inimigos
            self.draw_enemies(self.screen)

            if MOB_ENABLE_ATTACK:
                # Atualiza o movimento dos inimigos em direção ao jogador
                for enemy in self.enemies:
                    enemy.update(self.player.rect)

            # Verifica se é hora de adicionar novos inimigos
            if time.time() - self.last_enemy_add_time > MOB_TIME_SPAW_SEC:  # Adiciona novos inimigos a cada TIME_SPAWN_SEC segundos
                self.create_enemies(random.randint(10, 20))  # Adiciona novos inimigos aleatórios entre 10 e 20
                self.last_enemy_add_time = time.time()  # Atualiza o tempo do último inimigo adicionado

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Define a habilidade selecionada
                    self.player.skills[4].backgound_color = GRAY
                    self.player.selected_skill = self.player.skills[4]
                    print(f"Nova habilidade selecionada - Tecla: {self.player.selected_skill.key}, Dano: {self.player.selected_skill.damage}, Dano em Área: {self.player.selected_skill.area_damage}")

                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.player.move_to_click(mouse_x, mouse_y)
                    self.handle_player_attack(mouse_x, mouse_y)
                    moving = True  # Define a flag como True para indicar que o jogador está se movendo
                elif event.type == pygame.MOUSEBUTTONUP:
                    moving = False  # Define a flag como False para indicar que o jogador parou de se mover
                    self.player.skills[4].backgound_color = BLUE
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    for skill in self.player.skills:
                        if event.key == skill.key:

                            skill.backgound_color = GRAY
                            # Define a habilidade selecionada
                            self.player.selected_skill = skill
                            print(f"Nova habilidade selecionada - Tecla: {pygame.key.name(skill.key)}, Dano: {skill.damage}, Dano em Área: {skill.area_damage}")
                            # Realiza o ataque com a habilidade selecionada
                            self.handle_player_attack(self.player.rect.centerx, self.player.rect.centery)
                elif event.type == pygame.KEYUP:
                    for skill in self.player.skills:
                        if event.key == skill.key:
                            skill.backgound_color = BLUE


            if moving:
                # Obtém a posição atual do mouse
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.player.move_to_click(mouse_x, mouse_y)

            self.player.update()
            self.player.draw(self.screen)
           
            pygame.display.flip()

        pygame.quit()

    def create_enemies(self, num_enemies):
        enemy = Enemy(50, 50)
        for _ in range(num_enemies):
            enemy_x = random.randint(0, SCREEN_WIDTH - enemy.width)
            enemy_y = random.randint(0, SCREEN_HEIGHT - enemy.height)
            self.enemies.append(Enemy(enemy_x, enemy_y))

    def draw_enemies(self, screen):
        for enemy in self.enemies:
            screen.blit(enemy.image, enemy.rect)


    def handle_player_attack(self, mouse_x, mouse_y):
        # Verifica se há uma habilidade selecionada
        if self.player.selected_skill:
            selected_skill = self.player.selected_skill

            print("selected_skill.damage = ", selected_skill.damage)
            print("selected_skill.area_damage = ", selected_skill.area_damage)
            # Se a habilidade selecionada não causar dano em área, trata o ataque como um clique do mouse
            if selected_skill.area_damage == 0:
                self.handle_player_attack_single(mouse_x, mouse_y, selected_skill.damage)
            else:
                self.handle_player_attack_area(selected_skill.damage, selected_skill.area_damage)

    def handle_player_attack_single(self, mouse_x, mouse_y, damage):
        # Percorre todos os inimigos e verifica se o clique do mouse atingiu algum deles
        for enemy in self.enemies:
            if enemy.rect.collidepoint(mouse_x, mouse_y):
                # Verifica se o jogador colidiu diretamente com o inimigo
                if self.player.rect.colliderect(enemy.rect):
                    # Calcula o dano com base na habilidade do jogador
                    enemy.take_damage(damage)

                    # Marca o inimigo como atingido pelo jogador
                    enemy.hit_by_player = True

                    # Incrementa o score
                    self.player.score += 1

                    # Incrementa a experiência
                    self.player.xp += random.randint(2, 10)

                    # Verifica se o HP do inimigo é menor ou igual a zero
                    if enemy.hp <= 0:
                        # Se o HP for menor ou igual a zero, remove o inimigo da lista
                        self.enemies.remove(enemy)

    def handle_player_attack_area(self, damage, area_damage):
        print("Handling area attack...")
        print("Player position:", self.player.rect.center)
        print("Area damage:", area_damage)
        
        defeated_enemies = []  # Lista para armazenar os inimigos derrotados nesta rodada

        # Aplica o dano em área para os inimigos dentro do alcance da habilidade
        for enemy in self.enemies:
            distance = math.sqrt((self.player.rect.centerx - enemy.rect.centerx) ** 2 +
                                (self.player.rect.centery - enemy.rect.centery) ** 2)
            print("Distance to enemy:", distance)
            if distance <= area_damage:
                print("Enemy within area of effect - Enemy HP:", enemy.hp)
                print("damage:", damage)
                enemy.take_damage(damage)

                # Verifica se o HP do inimigo é menor ou igual a zero após o dano
                if enemy.hp <= 0:
                    defeated_enemies.append(enemy)  # Adiciona o inimigo à lista de derrotados

        # Remove os inimigos derrotados da lista principal de inimigos
        for enemy in defeated_enemies:
            self.enemies.remove(enemy)
            
            # Incrementa o score
            self.player.score += 1

            # Incrementa a experiência
            self.player.xp += random.randint(2, 10)


if __name__ == "__main__":
    game = Game()
    game.run()