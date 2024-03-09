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
    pygame.display.set_caption('Exibição de Imagem')

    # Define o diretório da imagem
    image_path = "D:/Python/ARPG/image/orc.jpg"

    # Carrega a imagem
    original_image = pygame.image.load(image_path)
    original_width, original_height = original_image.get_size()

    # Redimensiona a imagem para 10px x 10px, mantendo a proporção
    image = pygame.transform.smoothscale(original_image, (50, 50))

    # Posiciona a imagem no centro da tela
    image_rect = image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Loop principal
    running = True
    while running:
        screen.fill((255, 255, 255))  # Preenche a tela com a cor branca

        # Desenha a imagem na tela
        screen.blit(image, image_rect)

        # Atualiza a tela
        pygame.display.flip()

        # Eventos do teclado e mouse
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

    # Finaliza o Pygame
    pygame.quit()

if __name__ == "__main__":
    main()



