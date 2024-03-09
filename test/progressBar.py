import pygame
import sys

# Inicializar o Pygame
pygame.init()

# Definir cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Definir tamanho da janela
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Criar a janela
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Barra de Progresso")

# Função para desenhar a barra de progresso
def draw_progress_bar(window, color_back, color_fill, x, y, width, height, progress, border_radius=0):
    pygame.draw.rect(window, color_back, (x, y, width, height), border_radius=border_radius)
    progress_width = (progress / 100) * (width - 2 * border_radius)
    pygame.draw.rect(window, color_fill, (x, y, progress_width + border_radius * 2, height), border_radius=border_radius)

# Função principal
def main():
    running = True
    progressForward = 0
    progressReward = 100

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        # Atualizar a barra de progresso incremental
        progressForward += 1
        if progressForward >= 100:
            progressForward = 0
        
        # Atualizar a barra de progresso decremental
        progressReward -= 1
        if progressReward <= 0:
            progressReward = 100

        # Limpar a tela
        window.fill(WHITE)

        # Desenhar a barra de progresso com fundo preto e preenchimento verde e bordas arredondadas
        draw_progress_bar(window, BLACK, GREEN, 10, 50, 100, 20, progressForward, border_radius=3)

        # Desenhar a barra de progresso com fundo preto e preenchimento verde e bordas arredondadas
        draw_progress_bar(window, BLACK, RED, 10, 80, 100, 20, progressReward, border_radius=5)

        # Atualizar a tela
        pygame.display.update()

        # Controlar a taxa de atualização
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()
