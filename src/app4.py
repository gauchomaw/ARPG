import pygame
import math
import os
import random
import time

from typing import List


# Configurações da janela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Quantidade de Frames por segundo
FPS = 60

# Habilitar ataque dos mobs
ENABLE_MOB_ATTACK = False

# Diretório da aplicação
APP_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Diretório de imagens
PARENT_DIRECTORY = os.path.dirname(APP_DIRECTORY)
IMAGE_DIRECTORY = os.path.join(PARENT_DIRECTORY, "image")

# Tempo de spawn dos mobs
TIME_SPAWN_SEC = 30

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Carrega a imagem do jogador
        self.image = pygame.image.load(os.path.join(IMAGE_DIRECTORY, "warrior.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center = (x, y))
        self.speed = 5
        self.target_pos = None
        self.xp = 0
        self.hp = 100
        self.score = 0
        self.skill = Skill(damage=1, area_damage=0)

    def move_to_click(self, mouse_x, mouse_y):
        # Define o ponto de destino do jogador como o ponto clicado pelo mouse
        self.target_pos = (mouse_x, mouse_y)

    def update(self):
        # Se houver um ponto de destino definido, mova o jogador em direção a esse ponto
        if self.target_pos:
            # Calcula a diferença entre a posição atual do jogador e o ponto de destino
            dx = self.target_pos[0] - self.rect.centerx
            dy = self.target_pos[1] - self.rect.centery

            # Calcula a distância total até o ponto de destino
            distance = math.sqrt(dx ** 2 + dy ** 2)

            # Se a distância for maior que a velocidade do jogador, mova o jogador
            if distance > self.speed:
                # Calcula a proporção de quanto o jogador deve se mover nesta atualização
                ratio = self.speed / distance
                dx *= ratio
                dy *= ratio

                # Move o jogador
                self.rect.x += dx
                self.rect.y += dy
            else:
                # Se a distância for menor que a velocidade, mova o jogador diretamente para o ponto de destino
                self.rect.center = self.target_pos
                # Limpa o ponto de destino para parar o movimento suave
                self.target_pos = None
                
    def draw(self, screen):
        # Desenha a imagem do jogador na tela
        screen.blit(self.image, self.rect)
        
        # Desenha a pontuação 
        self.draw_score(screen)
        # Desenha barra de XP
        self.draw_xp_bar(screen)
        # desenha barra de HP
        self.draw_hp_bar(screen)


    def draw_hp_bar(self, screen):
        # Configurações da barra de HP
        bar_width = 200
        bar_height = 20
        bar_border_width = 1

        # Calcula a largura do preenchimento da barra de HP
        fill_width = int((self.hp / 100) * bar_width)

        # Desenha o contorno da barra de HP
        #pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - bar_width // 2, SCREEN_HEIGHT - 30, bar_width, bar_height), bar_border_width)
        
        # Desenha o preenchimento da barra de HP
        #pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - bar_width // 2 + bar_border_width, SCREEN_HEIGHT - 30 + bar_border_width, fill_width - 2, bar_height))

        pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - bar_width // 2, SCREEN_HEIGHT - 30, fill_width, bar_height))
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - bar_width // 2, SCREEN_HEIGHT - 30, bar_width, bar_height), 1)
        
        # Desenha o texto indicando o HP atual
        font = pygame.font.SysFont(None, 18)
        hp_text = font.render(f'HP: {self.hp}', True, BLACK)
        text_rect = hp_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        screen.blit(hp_text, text_rect)

    def draw_score(self, screen):
        font = pygame.font.Font(None, 18)
        text = font.render("Score: " + str(self.score), True, BLACK)
        screen.blit(text, (10, 10))

    def draw_xp_bar(self, screen):
        bar_width = 200
        bar_height = 20
        
        # Ajusta a xp_bar para um valor máximo de 100
        xp_bar = self.xp
        xp_bar = xp_bar % 100
        
        fill_width = int(bar_width * (xp_bar / 100))  # Ajusta o preenchimento da barra de acordo com a experiência atual
        pygame.draw.rect(screen, GREEN, (10, SCREEN_HEIGHT - 30, fill_width, bar_height))
        pygame.draw.rect(screen, BLACK, (10, SCREEN_HEIGHT - 30, bar_width, bar_height), 1)

        # Atualiza o nível do personagem a cada 100 pontos de experiência
        level = (self.xp // 100) + 1

        # Exibe o nível do personagem na tela
        font = pygame.font.SysFont(None, 18)
        level_text = font.render(f'Level: {level}', True, BLACK)
        text_rect = level_text.get_rect(center=(bar_width // 2, SCREEN_HEIGHT - 20))
        screen.blit(level_text, text_rect)

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
        self.hp = random.randint(1, 100)
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
        self.hp -= hp


class Skill:
    def __init__(self, damage = 1, area_damage = 0):
        self.damage = damage
        self.area_damage = area_damage

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


            if ENABLE_MOB_ATTACK:
                # Atualiza o movimento dos inimigos em direção ao jogador
                for enemy in self.enemies:
                    enemy.update(self.player.rect)
               
            # Verifica colisões e remove inimigos
            #self.remove_colliding_enemies()

            # Verifica se é hora de adicionar novos inimigos
            if time.time() - self.last_enemy_add_time > TIME_SPAWN_SEC:  # Adiciona novos inimigos a cada 5 segundos
                self.create_enemies(random.randint(10, 20))  # Adiciona novos inimigos aleatórios entre 10 e 20
                self.last_enemy_add_time = time.time()  # Atualiza o tempo do último inimigo adicionado

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.player.move_to_click(mouse_x, mouse_y)
                    self.handle_player_attack(mouse_x, mouse_y)
                    moving = True  # Define a flag como True para indicar que o jogador está se movendo
                elif event.type == pygame.MOUSEBUTTONUP:
                    moving = False  # Define a flag como False para indicar que o jogador parou de se mover
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

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

    # def remove_colliding_enemies(self):
    #     character_rect = self.player.rect.copy()  # Cria uma cópia do retângulo do jogador

    #     # Lista temporária para armazenar os inimigos que não colidem
    #     non_colliding_enemies = []

    #     for enemy in self.enemies:
    #         enemy_rect = enemy.rect

    #         if not character_rect.colliderect(enemy_rect):
    #             # Se não houver colisão, adiciona o inimigo à lista de não colidência
    #             non_colliding_enemies.append(enemy)
    #             # Reseta a flag de hit do inimigo quando não há colisão
    #             enemy.hit_by_player = False
    #         elif not enemy.hit_by_player:
    #             # Se houver colisão e o inimigo não foi atingido pelo jogador, adiciona o inimigo à lista de não colidindo
    #             non_colliding_enemies.append(enemy)

    #         # else:
    #         #     # Se houver colisão, atualiza a pontuação e a experiência do jogador
    #         #     self.player.score += 1
    #         #     self.player.xp += random.randint(2, 10)
    #         #     #enemy.take_damage(random.randint(1, 2))
    #         #     enemy.take_damage(self.player.skill.damage)

    #         #     # Verifica se o HP do inimigo é menor ou igual a zero
    #         #     #print(enemy.hp)
    #         #     if enemy.hp <= 0:
    #         #         # Se o HP for menor ou igual a zero, não adiciona o inimigo à lista de não colidindo
    #         #         # Isso efetivamente remove o inimigo da tela
    #         #         pass
    #         #     else:
    #         #         # Caso contrário, adiciona o inimigo à lista de não colidindo
    #         #         non_colliding_enemies.append(enemy)

    #     # Atualiza a lista de inimigos para incluir apenas aqueles que não colidem
    #     self.enemies = non_colliding_enemies

    def handle_player_attack(self, mouse_x, mouse_y):
        enemies_to_remove = []  # Lista temporária para armazenar os inimigos a serem removidos

        # Percorre todos os inimigos e verifica se o clique do mouse atingiu algum deles
        for enemy in self.enemies:
            if enemy.rect.collidepoint(mouse_x, mouse_y):
                self.player.score += 1
                self.player.xp += random.randint(2, 10)

                # Se o inimigo foi atingido, reduz seu HP pela quantidade de dano do jogador
                enemy.take_damage(self.player.skill.damage)

                # Marca o inimigo como atingido pelo jogador
                enemy.hit_by_player = True

                # Causa dano em área se houver
                if self.player.skill.area_damage > 0:
                    for other_enemy in self.enemies:
                        # Calcula a distância entre o inimigo clicado e os outros inimigos
                        distance = math.sqrt((enemy.rect.centerx - other_enemy.rect.centerx) ** 2 +
                                            (enemy.rect.centery - other_enemy.rect.centery) ** 2)
                        # Se o inimigo estiver dentro da área de dano, aplica o dano
                        if distance <= self.player.skill.area_damage:
                            other_enemy.take_damage(self.player.skill.damage)

                # Verifica se o HP do inimigo é menor ou igual a zero
                if enemy.hp <= 0:
                    # Adiciona o inimigo à lista de inimigos a serem removidos
                    enemies_to_remove.append(enemy)

        # Remove os inimigos que estão na lista de inimigos a serem removidos
        for enemy in enemies_to_remove:
            if enemy in self.enemies:
                self.enemies.remove(enemy)




if __name__ == "__main__":
    game = Game()
    game.run()
