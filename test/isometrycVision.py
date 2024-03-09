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
    pygame.display.set_caption('Visão Isométrica com Imagem')

    # Cores
    WHITE = (255, 255, 255)

    # Tamanho dos blocos isométricos
    BLOCK_WIDTH = 64
    BLOCK_HEIGHT = 32

    # Carrega a imagem
    image_path = "D:/Python/ARPG/image/orc.jpg"
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (32, 32))  # Redimensiona a imagem para 50x50 pixels
    image_width, image_height = image.get_size()

    # Função para converter coordenadas isométricas para coordenadas de tela
    def iso_to_screen(x, y):
        screen_x = (x - y) * (BLOCK_WIDTH / 2)
        screen_y = (x + y) * (BLOCK_HEIGHT / 2)
        return screen_x, screen_y

    # Loop principal
    running = True
    while running:
        screen.fill(WHITE)

        # Desenha a imagem isométrica
        for y in range(5):
            for x in range(5):
                screen_x, screen_y = iso_to_screen(x, y)
                screen.blit(image, (screen_x - image_width / 2, screen_y - image_height))

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
