import os
import pygame
from pygame.locals import *
import random
import time
import math

# Configurações da janela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Diretório da aplicação
APP_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Diretório de imagens
PARENT_DIRECTORY = os.path.dirname(APP_DIRECTORY)
IMAGE_DIRECTORY = os.path.join(PARENT_DIRECTORY, "image")

def move_character_to_click(mouse_x, mouse_y, character_x, character_y):
    """
    Calcula a direção e a distância do movimento do personagem até o clique do mouse.

    Args:
        mouse_x (int): A coordenada x do clique do mouse.
        mouse_y (int): A coordenada y do clique do mouse.
        character_x (int): A coordenada x atual do personagem.
        character_y (int): A coordenada y atual do personagem.

    Returns:
        tuple: Uma tupla contendo os componentes x e y do passo e a distância total até o clique do mouse.
    """
    dx = mouse_x - character_x
    dy = mouse_y - character_y
    distance = max(abs(dx), abs(dy))
    if distance != 0:
        step_x = dx / distance
        step_y = dy / distance
        return step_x, step_y, distance
    else:
        return 0, 0, 0  # Retorna valores padrão se a distância for zero


def create_enemies(num_enemies, enemy_width, enemy_height):
    """
    Cria uma lista de posições aleatórias para os inimigos.

    Args:
        num_enemies (int): O número de inimigos a serem criados.
        enemy_width (int): A largura do inimigo.
        enemy_height (int): A altura do inimigo.

    Returns:
        list: Uma lista de tuplas representando as posições dos inimigos.
    """
    enemies = []
    for _ in range(num_enemies):
        enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
        enemy_y = random.randint(0, SCREEN_HEIGHT - enemy_height)
        enemies.append((enemy_x, enemy_y))
    return enemies

def draw_enemies(screen, enemy_img, enemies):
    """
    Desenha os inimigos na tela.

    Args:
        screen (Surface): A superfície da tela onde os inimigos serão desenhados.
        enemy_img (Surface): A imagem do inimigo.
        enemies (list): Uma lista de tuplas representando as posições dos inimigos.
    """
    for enemy_pos in enemies:
        screen.blit(enemy_img, enemy_pos)


def remove_colliding_enemies(character_score, character_xp, enemies, character_x, character_y, character_width, character_height, enemy_width, enemy_height):
    """
    Remove os inimigos que colidem com o personagem e atualiza o score e o XP.

    Args:
        character_score (int): O score atual do personagem.
        character_xp (int): O XP atual do personagem.
        enemies (list): Uma lista de tuplas representando as posições dos inimigos.
        character_x (int): A coordenada x atual do personagem.
        character_y (int): A coordenada y atual do personagem.
        character_width (int): A largura do personagem.
        character_height (int): A altura do personagem.
        enemy_width (int): A largura do inimigo.
        enemy_height (int): A altura do inimigo.

    Returns:
        tuple: Uma tupla contendo a lista de inimigos restantes, o novo score e o novo XP.
    """    
    non_colliding_enemies = []
    character_rect = pygame.Rect(character_x, character_y, character_width, character_height)
    for enemy_pos in enemies:
        enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], enemy_width, enemy_height)
        if not character_rect.colliderect(enemy_rect):
            non_colliding_enemies.append(enemy_pos)
        else:
            character_score = increment_score(character_score)
            character_xp = increment_xp(character_xp)

    return non_colliding_enemies, character_score, character_xp


def increment_score(score):
    """
    Função para incrementar o score em 1 a cada inimigo removido.

    Args:
    score (int): O score atual do jogador.

    Returns:
    int: O novo score após o incremento.
    """
    return score + 1

def increment_xp(xp, min_increment=2, max_increment=10):
    """
    Função para incrementar o XP com cada inimigo morto com um número randômico entre min_increment e max_increment.

    Args:
    xp (int): O XP atual do jogador.
    min_increment (int, opcional): O valor mínimo de incremento de XP. Padrão é 2.
    max_increment (int, opcional): O valor máximo de incremento de XP. Padrão é 10.

    Returns:
    int: O novo XP após o incremento.
    """
    return xp + random.randint(min_increment, max_increment)

def add_new_enemies(enemies, num_new_enemies, enemy_width, enemy_height):
    """
    Adiciona novos inimigos à lista de inimigos existente.

    Args:
        enemies (list): Uma lista de tuplas representando as posições dos inimigos.
        num_new_enemies (int): O número de novos inimigos a serem adicionados.
        enemy_width (int): A largura do inimigo.
        enemy_height (int): A altura do inimigo.

    Returns:
        list: Uma lista atualizada de tuplas representando as posições dos inimigos.
    """
    for _ in range(num_new_enemies):
        enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
        enemy_y = random.randint(0, SCREEN_HEIGHT - enemy_height)
        enemies.append((enemy_x, enemy_y))
    return enemies

def draw_score(screen, score):
    """
    Desenha o score na tela.

    Args:
        screen (Surface): A superfície da tela onde o score será desenhado.
        score (int): O score atual do jogador.
    """
    # Fonte para o placar
    font = pygame.font.SysFont(None, 24)
    score_text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(score_text, (10, 10))

def draw_xp_bar(screen, xp):
    """
    Desenha a barra de experiência na tela e exibe o nível do personagem.

    Args:
        screen (Surface): A superfície da tela onde a barra de experiência será desenhada.
        xp (int): O XP atual do personagem.
    """
    bar_width = 200
    bar_height = 20
    
    # Ajusta a xp_bar para um valor máximo de 100
    xp_bar = xp
    xp_bar = xp_bar % 100
    
    fill_width = int(bar_width * (xp_bar / 100))  # Ajusta o preenchimento da barra de acordo com a experiência atual
    pygame.draw.rect(screen, GREEN, (10, SCREEN_HEIGHT - 30, fill_width, bar_height))
    pygame.draw.rect(screen, BLACK, (10, SCREEN_HEIGHT - 30, bar_width, bar_height), 1)

    # Atualiza o nível do personagem a cada 100 pontos de experiência
    level = (xp // 100) + 1

    # Exibe o nível do personagem na tela
    font = pygame.font.SysFont(None, 18)
    level_text = font.render(f'Level: {level}', True, BLACK)
    text_rect = level_text.get_rect(center=(bar_width / 2 + 10, SCREEN_HEIGHT - 40))
    screen.blit(level_text, text_rect)

def draw_health_bar(screen, health):
    """
    Desenha a barra de vida na tela.

    Args:
        screen (Surface): A superfície da tela onde a barra de vida será desenhada.
        health (int): A vida atual do personagem.
    """
    bar_width = 200
    bar_height = 20
    
    fill_width = int(bar_width * (health / 100))  # Ajusta o preenchimento da barra de acordo com a vida atual
    pygame.draw.rect(screen, RED, (310, SCREEN_HEIGHT - 30, fill_width, bar_height))
    pygame.draw.rect(screen, BLACK, (310, SCREEN_HEIGHT - 30, bar_width, bar_height), 1)


def main():
    # Inicializa o Pygame
    pygame.init()

    # Seta tela com dimensões definidas
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Simulação ARPG')

    # Arquivos de char e enimies
    character_path = os.path.join(IMAGE_DIRECTORY, "warrior.png")
    enemy_path = os.path.join(IMAGE_DIRECTORY, "skeleton.png")

    # Carrega a imagem do personagem
    character_img = pygame.image.load(character_path).convert_alpha()
    character_img = pygame.transform.scale(character_img, (50, 50))  # Redimensiona a imagem do personagem
    character_width, character_height = character_img.get_size()

    # Carrega a imagem do inimigo
    enemy_img = pygame.image.load(enemy_path).convert_alpha()
    enemy_img = pygame.transform.scale(enemy_img, (50, 50))  # Redimensiona a imagem do inimigo
    enemy_width, enemy_height = enemy_img.get_size()

    # Posição inicial do personagem
    character_x = SCREEN_WIDTH // 2 - character_width // 2
    character_y = SCREEN_HEIGHT // 2 - character_height // 2

    # Velocidade de movimento do personagem
    character_speed = 0.5

    # Variável para armazenar a vida do personagem
    character_health = 100

    # Variável para armazenar o score
    character_score = 0

    # Variável para armazenar o xp
    character_xp = 0

    # Inicializa as variáveis de direção do movimento do personagem
    step_x, step_y, distance = 0, 0, 0

    # Cria inimigos iniciais
    enemies = create_enemies(5, enemy_width, enemy_height)

    # Contador para controlar o tempo para adicionar novos inimigos
    last_enemy_add_time = time.time()

    # Loop principal
    running = True
    while running:

        # Preenche com fundo branco
        screen.fill(WHITE)

        # Desenha a imagem do personagem
        screen.blit(character_img, (character_x, character_y))

        # Desenha inimigos
        draw_enemies(screen, enemy_img, enemies)

        # Verifica colisões e remove inimigos
        enemies, character_score, character_xp = remove_colliding_enemies(character_score, character_xp, enemies, character_x, character_y, character_width, character_height, enemy_width, enemy_height)

        # Verifica se é hora de adicionar novos inimigos
        if time.time() - last_enemy_add_time > 5:  # Adiciona novos inimigos a cada 5 segundos
            enemies = add_new_enemies(enemies, random.randint(10, 20), enemy_width, enemy_height)  # Adiciona novos inimigos aleatórios entre 10 e 20
            last_enemy_add_time = time.time()  # Atualiza o tempo do último inimigo adicionado

        # Exibe o placar na tela
        draw_score(screen, character_score)
        
        # Exibe a barra de experiência na tela
        draw_xp_bar(screen, character_xp)

        # Exibe a barra de vida na tela
        draw_health_bar(screen, character_health)

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
                step_x, step_y, distance = move_character_to_click(mouse_x, mouse_y, character_x, character_y)
                print(f"step_x = {step_x}, step_y = {step_y}, distance = {distance}")

        # Atualiza a posição do personagem para simular caminhada até o clique do mouse
        if distance > 0:
            print("distance = ", str(distance))
            character_x += step_x * character_speed
            character_y += step_y * character_speed
            distance -= character_speed

    # Finaliza o Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
