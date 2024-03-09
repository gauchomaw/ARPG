import os

# Configurações da janela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (192, 192, 192)

# Quantidade de Frames por segundo
FPS = 60

# Mobs
# Habilitar ataque dos mobs
MOB_ENABLE_ATTACK = False
# Tempo de spawn dos mobs
MOB_TIME_SPAW_SEC = 5

# Diretório da aplicação
APP_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Diretório de imagens
PARENT_DIRECTORY = os.path.dirname(APP_DIRECTORY)
IMAGE_DIRECTORY = os.path.join(PARENT_DIRECTORY, "image")

