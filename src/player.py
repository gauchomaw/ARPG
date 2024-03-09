import pygame
import math
from skill import Skill
from constants import *

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
        self.mana = 50
        self.score = 0

        # Lista de habilidades
        self.skills = [
            Skill("Skill 1", pygame.K_q, 10),
            Skill("Skill 2", pygame.K_w, 20),
            Skill("Skill 3", pygame.K_e, 30),
            Skill("Skill 4", pygame.K_r, 40, 100),
            Skill("Skill 5", pygame.MOUSEBUTTONDOWN, 10)  # Última habilidade acionada pelo clique do mouse
        ]

        # Habilidade selecionada inicialmente
        self.selected_skill:Skill = None


        self.area_effect_radius = 100  # Raio da área de efeito da habilidade em pixels
        self.area_effect_color = (255, 0, 0, 128)  # Cor semi-transparente vermelha


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

        # Desenha as skills
        self.draw_skills(screen)
        
        # Desenha a pontuação 
        self.draw_score(screen)
        # Desenha barra de XP
        self.draw_xp_bar(screen)
        # desenha barra de HP
        self.draw_hp_bar(screen)
        # desenha barra de mana
        self.draw_mana_bar(screen)

        # Desenha a área de efeito da habilidade (se houver)
        if self.selected_skill and self.selected_skill.area_damage > 0:
            pygame.draw.circle(screen, self.area_effect_color, self.rect.center, self.area_effect_radius, 2)



    def draw_hp_bar(self, screen):
        # Configurações da barra de HP
        bar_width = 200
        bar_height = 20
        bar_border_width = 1

        # Calcula a largura do preenchimento da barra de HP
        fill_width = int((self.hp / 100) * bar_width)

        pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - bar_width // 2, SCREEN_HEIGHT - 30, fill_width, bar_height))
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - bar_width // 2, SCREEN_HEIGHT - 30, bar_width, bar_height), bar_border_width)
        
        # Desenha o texto indicando o HP atual
        font = pygame.font.SysFont(None, 18)
        hp_text = font.render(f'HP: {self.hp}', True, BLACK)
        text_rect = hp_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        screen.blit(hp_text, text_rect)

    def draw_mana_bar(self, screen):
        # Configurações da barra de HP
        bar_width = 200
        bar_height = 20
        bar_border_width = 1

        # Calcula a largura do preenchimento da barra de mana
        fill_width = int((self.mana / 100) * bar_width)

        pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH - bar_width - 10, SCREEN_HEIGHT - 30, fill_width, bar_height))
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - bar_width - 10, SCREEN_HEIGHT - 30, bar_width, bar_height), bar_border_width)
        
        # Desenha o texto indicando o HP atual
        font = pygame.font.SysFont(None, 18)
        mana_text = font.render(f'Mana: {self.mana}', True, BLACK)
        text_rect = mana_text.get_rect(center=(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 20))
        screen.blit(mana_text, text_rect)

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

    def draw_skills(self, screen):
        font = pygame.font.Font(None, 24)
        #skill_text = font.render("Skills:", True, BLACK)
        #screen.blit(skill_text, (10, 60))  # Posição inicial da lista de habilidades

        # Posição inicial do primeiro retângulo
        rect_x = 330
        rect_y = 540

        # Desenha um retângulo para cada habilidade
        for skill in self.skills:

            # Desenha o retângulo
            pygame.draw.rect(screen, skill.backgound_color, (rect_x, rect_y, 20, 20))

            # Renderiza a tecla da habilidade dentro do retângulo
            skill_key = pygame.key.name(skill.key)
            skill_surface = font.render(skill_key, True, BLACK)
            text_rect = skill_surface.get_rect(center=(rect_x + 10, rect_y + 10))
            screen.blit(skill_surface, text_rect)

            # Atualiza a posição para o próximo retângulo
            rect_x += 30  # Adiciona um espaço de 10 pixels entre cada retângulo    

    