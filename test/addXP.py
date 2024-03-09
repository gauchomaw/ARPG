import os
import pygame
from pygame.locals import *
import random
import time

def main():
    # Inicializa o Pygame
    pygame.init()

    # Configurações da janela
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Simulação de Caminhada Isométrica')

    # Cores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)

    # Tamanho dos blocos isométricos
    BLOCK_WIDTH = 64
    BLOCK_HEIGHT = 32

    # Caminhos das imagens
    character_path = "D:/Python/ARPG/image/char.jpg"
    enemy_path = "D:/Python/ARPG/image/orc.jpg"

    # Carrega a imagem do personagem
    character = pygame.image.load(character_path)
    character = pygame.transform.scale(character, (50, 50))  # Redimensiona a imagem do personagem
    character_width, character_height = character.get_size()

    # Carrega a imagem do inimigo
    enemy = pygame.image.load(enemy_path)
    enemy = pygame.transform.scale(enemy, (50, 50))  # Redimensiona a imagem do inimigo
    enemy_width, enemy_height = enemy.get_size()

    # Posição inicial do personagem
    character_x = SCREEN_WIDTH // 2 - character_width // 2
    character_y = SCREEN_HEIGHT // 2 - character_height // 2

    # Velocidade de movimento do personagem
    character_speed = 0.1

    # Variável para armazenar o placar
    score = 0    

    # Variáveis para armazenar a experiência
    xp = 0
    max_xp = 100

    # Função para converter coordenadas isométricas para coordenadas de tela
    def iso_to_screen(x, y):
        screen_x = (x - y) * (BLOCK_WIDTH / 2)
        screen_y = (x + y) * (BLOCK_HEIGHT / 2)
        return screen_x, screen_y

    # Função para calcular a direção e a distância do movimento do personagem até o clique do mouse
    def move_character_to_click(mouse_x, mouse_y):
        dx = mouse_x - character_x
        dy = mouse_y - character_y
        distance = max(abs(dx), abs(dy))
        if distance != 0:
            step_x = dx / distance
            step_y = dy / distance
            return step_x, step_y, distance
        else:
            return 0, 0, 0  # Retorna valores padrão se a distância for zero

    # Função para criar inimigos
    def create_enemies(num_enemies):
        enemies = []
        for _ in range(num_enemies):
            enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
            enemy_y = random.randint(0, SCREEN_HEIGHT - enemy_height)
            enemies.append((enemy_x, enemy_y))
        return enemies

    # Função para desenhar inimigos na tela
    def draw_enemies(enemies):
        for enemy_pos in enemies:
            screen.blit(enemy, enemy_pos)

    # Função para remover inimigos que colidem com o personagem
    def remove_colliding_enemies(enemies, xp):
        non_colliding_enemies = []
        character_rect = pygame.Rect(character_x, character_y, character_width, character_height)
        for enemy_pos in enemies:
            enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], enemy_width, enemy_height)
            if not character_rect.colliderect(enemy_rect):
                non_colliding_enemies.append(enemy_pos)
            else:
                 # Incrementa o placar quando há colisão com o inimigo
                increment_score()

                # Incrementa a experiência quando há colisão com o inimigo
                xp += 1

        return non_colliding_enemies, xp

    # Função para adicionar novos inimigos
    def add_new_enemies(enemies, num_new_enemies):
        for _ in range(num_new_enemies):
            enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
            enemy_y = random.randint(0, SCREEN_HEIGHT - enemy_height)
            enemies.append((enemy_x, enemy_y))
        return enemies

    # Função para desenhar a barra de experiência na tela
    def draw_xp_bar(xp, max_xp):
        bar_width = 200
        bar_height = 20
        fill_width = int(bar_width * (xp / max_xp))
        pygame.draw.rect(screen, GREEN, (10, SCREEN_HEIGHT - 30, fill_width, bar_height))
        pygame.draw.rect(screen, BLACK, (10, SCREEN_HEIGHT - 30, bar_width, bar_height), 2)

    # Função para incrementar o placar
    def increment_score():
        nonlocal score
        score += 1

    # Inicializa as variáveis de direção do movimento do personagem
    step_x, step_y, distance = 0, 0, 0

    # Cria inimigos iniciais
    num_enemies = 5
    enemies = create_enemies(num_enemies)

    # Contador para controlar o tempo para adicionar novos inimigos
    last_enemy_add_time = time.time()

    # Fonte para o placar
    font = pygame.font.SysFont(None, 36)

    # Loop principal
    running = True
    while running:
        screen.fill(WHITE)

        # Desenha a imagem do personagem
        screen.blit(character, (character_x, character_y))

        # Desenha inimigos
        draw_enemies(enemies)

        # Verifica colisões e remove inimigos
        enemies, xp = remove_colliding_enemies(enemies, xp)

        # Verifica se é hora de adicionar novos inimigos
        if time.time() - last_enemy_add_time > 5:  # Adiciona novos inimigos a cada 5 segundos
            enemies = add_new_enemies(enemies, random.randint(2, 5))  # Adiciona novos inimigos aleatórios entre 2 e 5
            last_enemy_add_time = time.time()  # Atualiza o tempo do último inimigo adicionado

        # Exibe o placar na tela
        score_text = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_text, (10, 10))

        # Exibe a barra de experiência na tela
        draw_xp_bar(xp, max_xp)

        # Atualiza a tela
        pygame.display.flip()

        # Eventos do teclado e mouse
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                # Obtém a posição do clique do mouse
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Calcula a direção e a distância do movimento do personagem até o clique do mouse
                step_x, step_y, distance = move_character_to_click(mouse_x, mouse_y)

        # Atualiza a posição do personagem para simular caminhada até o clique do mouse
        if distance > 0:
            character_x += step_x * character_speed
            character_y += step_y * character_speed
            distance -= character_speed

    # Finaliza o Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
