import pygame
import random
import math
import os

# Configurações da janela
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TILE_SIZE = 50
TILE_SIZE_PLAYER = 40  # Tamanho do jogador
MAP_WIDTH = WINDOW_WIDTH // TILE_SIZE
MAP_HEIGHT = WINDOW_HEIGHT // TILE_SIZE
FPS = 60

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Diretório da aplicação
APP_PATH = os.path.dirname(os.path.abspath(__file__))

# Diretório de imagens
PARENT_PATH = os.path.dirname(APP_PATH)
IMAGE_PATH = os.path.join(PARENT_PATH, "image")

class Mapa:
    def __init__(self):
        self.mapa, self.obstaculos = self.gerar_mapa()

    def gerar_mapa(self):
        # Criar um mapa inicialmente preenchido com blocos pretos
        mapa = [[0 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        obstaculos = []

        # Começar a partir da borda esquerda
        x, y = 0, random.randint(0, MAP_HEIGHT-1)

        # Fazer um caminho para a borda direita
        x = 0
        while x < MAP_WIDTH - 1:
            mapa[y][x] = 1
            direcao = random.choice([-1, 1])
            y += random.choice([-1, 0, 1])
            y = max(0, min(y, MAP_HEIGHT - 1))
            x += direcao
            x = max(0, min(x, MAP_WIDTH - 1))  # Garantir que x esteja dentro dos limites do mapa

        # Criar retângulos para os obstáculos
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if mapa[y][x] == 0:
                    obstaculos.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        return mapa, obstaculos

    def desenhar_mapa(self, tela):
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                #cor = WHITE if self.mapa[y][x] == 1 else BLACK
                #pygame.draw.rect(tela, cor, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                if self.mapa[y][x] == 1:
                    grass_image = pygame.image.load(os.path.join(IMAGE_PATH, "grass.jpg"))
                    grass_image = pygame.transform.scale(grass_image, (TILE_SIZE, TILE_SIZE))
                    tela.blit(grass_image, (x * TILE_SIZE, y * TILE_SIZE))
                    #pygame.draw.rect(tela, WHITE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                else:
                    pygame.draw.rect(tela, BLACK, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def colide_com_obstaculo(self, jogador):
        for obstaculo in self.obstaculos:
            if jogador.colliderect(obstaculo):
                return True
        return False


class Jogador:
    def __init__(self, mapa):
        # Iniciar o jogador em um bloco branco aleatório
        while True:
            x = random.randint(0, MAP_WIDTH - 1)
            y = random.randint(0, MAP_HEIGHT - 1)
            if mapa.mapa[y][x] == 1:
                self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE_PLAYER, TILE_SIZE_PLAYER)
                break
        self.velocidade = 5
        self.destino_x = self.rect.x
        self.destino_y = self.rect.y
        self.pos_anterior = self.rect.topleft

    def mover_para(self, x, y, mapa):
        self.destino_x = x
        self.destino_y = y

    def atualizar(self, mapa):
        self.pos_anterior = self.rect.topleft  # Armazenar a posição anterior
        dx = self.destino_x - self.rect.x
        dy = self.destino_y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            step_x = dx / dist * self.velocidade
            step_y = dy / dist * self.velocidade
            if dist <= self.velocidade:  # Se a distância restante for menor ou igual à velocidade
                self.rect.x = self.destino_x
                self.rect.y = self.destino_y
            else:
                next_x = self.rect.x + step_x
                next_y = self.rect.y + step_y
                temp_rect = pygame.Rect(next_x, next_y, TILE_SIZE_PLAYER, TILE_SIZE_PLAYER)
                if not mapa.colide_com_obstaculo(temp_rect):
                    self.rect.x = next_x
                    self.rect.y = next_y
                else:
                    # Encontrou um obstáculo
                    self.rect.topleft = self.pos_anterior  # Restaurar a posição anterior

    def desenhar(self, tela):
        pygame.draw.rect(tela, GREEN, self.rect)


def main():
    pygame.init()
    tela = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Gerador de Mapas Aleatórios')
    relogio = pygame.time.Clock()

    mapa = Mapa()
    jogador = Jogador(mapa)

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Botão esquerdo do mouse
                    jogador.mover_para(evento.pos[0], evento.pos[1], mapa)

        # Atualizar o jogador
        jogador.atualizar(mapa)

        # Limpar a tela
        tela.fill(BLACK)

        # Desenhar o mapa
        mapa.desenhar_mapa(tela)

        # Desenhar o jogador
        jogador.desenhar(tela)

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
