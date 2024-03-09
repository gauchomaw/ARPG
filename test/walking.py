import os
import pygame
from pygame.locals import *

def main():
    # Inicializa o Pygame
    pygame.init()

    # Configurações da janela
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Simulação de Caminhada')

    # Cores
    WHITE = (255, 255, 255)

    # Tamanho dos blocos isométricos
    BLOCK_WIDTH = 64
    BLOCK_HEIGHT = 32

    # Carrega a imagem do personagem
    character_path = "D:/Python/ARPG/image/orc.jpg"
    character = pygame.image.load(character_path)
    character = pygame.transform.scale(character, (50, 50))  # Redimensiona a imagem do personagem
    character_width, character_height = character.get_size()

    # Posição inicial do personagem
    character_x = SCREEN_WIDTH // 2 - character_width // 2
    character_y = SCREEN_HEIGHT // 2 - character_height // 2

    # Velocidade de movimento do personagem
    character_speed = 0.1

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

    # Inicializa as variáveis de direção do movimento do personagem
    step_x, step_y, distance = 0, 0, 0

    # Loop principal
    running = True
    while running:
        screen.fill(WHITE)

        # Desenha a imagem do personagem
        screen.blit(character, (character_x, character_y))

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
