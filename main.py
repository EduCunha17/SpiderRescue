import pygame
import random
import sys

# ==========================
# Inicialização
# ==========================

pygame.init()

LARGURA = 800
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Spider Rescue - Homem-Aranha")

clock = pygame.time.Clock()

fonte = pygame.font.SysFont("Arial", 30)
# ==========================
# Imagens
# ==========================
import os


def caminho_recurso(caminho_relativo):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, caminho_relativo)

pygame.mixer.music.load(caminho_recurso("assets/sounds/musica.mp3"))
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

img_homem = pygame.image.load(caminho_recurso("assets/images/homem_aranha.png"))
img_homem = pygame.transform.scale(img_homem, (120, 120))

img_donzela = pygame.image.load(caminho_recurso("assets/images/donzela.png"))
img_donzela = pygame.transform.scale(img_donzela, (90, 90))

img_vilao = pygame.image.load(caminho_recurso("assets/images/vilao.png"))
img_vilao = pygame.transform.scale(img_vilao, (70, 70))
img_fundo = pygame.image.load(caminho_recurso("assets/images/fundo.png"))
img_fundo = pygame.transform.scale(img_fundo, (800, 600))

# ==========================
# Sons
# ==========================

som_coletar = pygame.mixer.Sound(caminho_recurso("assets/sounds/som_coletar.mp3"))
som_dano = pygame.mixer.Sound(caminho_recurso("assets/sounds/som_dano.mp3"))

# ==========================
# Jogador
# ==========================

jogador = pygame.Rect(330, 420, 140, 180)

velocidade = 7

# ==========================
# Pontuação
# ==========================

pontos = 0
vidas = 30

# ==========================
# Donzelas
# ==========================

donzelas = []

for i in range(5):

    donzela = {

        "x": random.randint(20, 760),

        "y": random.randint(-600, -50),

        "raio": 30,

        "velocidade": random.randint(4, 8)

    }

    donzelas.append(donzela)

    # ==========================
    # Vilões
    # ==========================

    viloes = []

    for i in range(4):
        vilao = {
            "x": random.randint(20, 760),
            "y": random.randint(-800, -50),
            "raio": 35,
            "velocidade": random.randint(5, 9)
        }

        viloes.append(vilao)

# ==========================
# Loop Principal
# ==========================

rodando = True
menu = True

while rodando:
    while menu:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_RETURN:
                    menu = False

                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        tela.blit(img_fundo, (0, 0))

        titulo = fonte.render("SPIDER RESCUE", True, (255, 255, 0))
        linha1 = fonte.render("Pegue as donzelas", True, (255, 255, 255))
        linha2 = fonte.render("Evite os viloes", True, (255, 255, 255))
        linha3 = fonte.render("A / D = Mover", True, (255, 255, 255))
        linha4 = fonte.render("PRESSIONE ENTER PARA JOGAR", True, (0, 255, 0))
        linha5 = fonte.render("ESC = SAIR", True, (255, 0, 0))

        tela.blit(titulo, (250, 120))
        tela.blit(linha1, (250, 200))
        tela.blit(linha2, (250, 240))
        tela.blit(linha3, (250, 280))
        tela.blit(linha4, (250, 340))
        tela.blit(linha5, (250, 380))

        pygame.display.flip()
        clock.tick(60)

    # ----------------------
    # Eventos
    # ----------------------

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

    # ----------------------
    # Movimento jogador
    # ----------------------

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        jogador.x -= velocidade

    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        jogador.x += velocidade

    if jogador.x < 0:
        jogador.x = 0

    if jogador.x > LARGURA - jogador.width:
        jogador.x = LARGURA - jogador.width

    # ----------------------
    # Movimento donzelas
    # ----------------------

    for donzela in donzelas:

        donzela["y"] += donzela["velocidade"]

        if donzela["y"] > ALTURA + 30:

            donzela["y"] = random.randint(-300, -50)

            donzela["x"] = random.randint(20, 760)

        # Colisão

        jogador_colisao = pygame.Rect(
            jogador.x,
            jogador.y,
            jogador.width,
            jogador.height
        )

        donzela_colisao = pygame.Rect(
            donzela["x"] - donzela["raio"],
            donzela["y"] - donzela["raio"],
            donzela["raio"] * 2,
            donzela["raio"] * 2
        )

        if jogador_colisao.colliderect(donzela_colisao):

            pontos += 1
            som_coletar.play()

            donzela["y"] = random.randint(-300, -50)

            donzela["x"] = random.randint(20, 760)
    # ----------------------
    # Movimento dos vilões
    # ----------------------

    for vilao in viloes:

        vilao["y"] += vilao["velocidade"]

        if vilao["y"] > ALTURA + 30:

            vilao["y"] = random.randint(-300, -50)
            vilao["x"] = random.randint(20, 760)

        vilao_colisao = pygame.Rect(

            vilao["x"] - vilao["raio"],
            vilao["y"] - vilao["raio"],
            vilao["raio"] * 2,
            vilao["raio"] * 2

        )

        if jogador.colliderect(vilao_colisao):

            vidas -= 1
            som_dano.play()

            vilao["y"] = random.randint(-300, -50)
            vilao["x"] = random.randint(20, 760)
    # ----------------------
    # Desenhos
    #

    tela.blit(img_fundo, (0, 0))

    texto = fonte.render(f"Pontos: {pontos}/20", True, (255,255,255))
    texto_vidas = fonte.render(f"Vidas: {vidas}", True, (255,255,255))

    tela.blit(texto, (20, 20))
    tela.blit(texto_vidas, (620, 20))

    tela.blit(img_homem, (jogador.x, jogador.y))

    for donzela in donzelas:
        tela.blit(
            img_donzela,
            (donzela["x"] - 20, donzela["y"] - 20)
        )
    for vilao in viloes:
        tela.blit(
            img_vilao,
            (vilao["x"] - 20, vilao["y"] - 20)
        )
    pygame.display.flip()
    if pontos >= 20:
        pygame.mixer.music.stop()
        tela.fill((0, 0, 0))

        texto = fonte.render("VOCE VENCEU!", True, (0, 255, 0))

        tela.blit(texto, (250, 280))

        pygame.display.flip()

        pygame.time.delay(3000)

        rodando = False

    if vidas <= 0:
        pygame.mixer.music.stop()
        tela.fill((0, 0, 0))

        texto = fonte.render("GAME OVER", True, (255, 0, 0))

        tela.blit(texto, (280, 280))

        pygame.display.flip()

        pygame.time.delay(3000)

        rodando = False
    clock.tick(60)

pygame.quit()

sys.exit()