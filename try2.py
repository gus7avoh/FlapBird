import pygame
import os
import random

TELA_LARGURA = 500
TELA_ALTURA = 800

FONTE_2D = os.path.join('fonts', 'PressStart2P-Regular.ttf')

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','pipes', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bases', 'base.png')))

IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','birds', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','birds','bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','birds','bird3.png'))),
]

IMAGEM_BACKGROUND = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','background', 'bg.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','background', 'white.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','background', 'spring.png')))
]

pygame.font.init()
FONTE_PONTOS = pygame.font.Font(FONTE_2D, 25)
FONTE_TITULO = pygame.font.Font(FONTE_2D, 35)
FONTE_FLAP = pygame.font.Font(FONTE_2D, 40)
FONTE_LM = pygame.font.Font(FONTE_2D, 15)

class BackGround:
    IMGS = IMAGEM_BACKGROUND

    def __init__(self):
        self.x = 0
        self.y = 0

    def desenhar(self, tela, vetor):
        tela.blit(self.IMGS[vetor], (self.x, self.y))



class Passaro:
    IMGS = IMAGENS_PASSARO
    # animações da rotação
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # o angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # definir qual imagem do passaro vai usar
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # se o passaro tiver caindo eu não vou bater asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        # desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA
     
    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False

class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

def reiniciar(canos,remover_canos,adicionar_cano):
    adicionar_cano = False
    canos.clear()
    canos.append(Cano(700))
    remover_canos.clear()

def desenhar_tela(tela, passaro, canos, chao, pontos):
    BackGround().desenhar(tela, 1)

    passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()


def tela_inicial(tela, passaro, chao, last=0, maximo=0):
    BackGround().desenhar(tela, 0) 
    chao.desenhar(tela)
    passaro.desenhar(tela)

    titulo1 = FONTE_FLAP.render(f"flappy bird", 1, (255, 255, 0))
    tela.blit(titulo1, (50, 200))

    texto2 = FONTE_TITULO.render(f"Press space", 1, (35,35,142))
    tela.blit(texto2, (65, 440))

    texto3 = FONTE_TITULO.render(f"to play", 1, (35,35,142))
    tela.blit(texto3, (130, 490))

    if last > 0:
        lastPoints = FONTE_LM.render(f"Last points: {last}", 1, (255, 255, 255))
        tela.blit(lastPoints, (10, 10))

    if maximo > 0:
        maxPoints = FONTE_LM.render(f"Max points: {maximo}", 1, (255, 255, 255))
        tela.blit(maxPoints, (10, 50))

    pygame.display.update()

def menu(chao, passaro, tela, relogio, tabelaPontos):
    last = 0
    maximo = 0
    if tabelaPontos:
        last = tabelaPontos[-1]
        maximo = max(tabelaPontos)

    menu = True
    while menu:
        relogio.tick(30)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    menu = False
        
        chao.mover()
        tela_inicial(tela, passaro, chao, last, maximo)

def runGame(passaro,chao,canos,tela,pontos,relogio,tabelaPontos):

    rodando =  True                 
    while rodando:
        relogio.tick(30)

        # interação com o usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    passaro.pular()

        # mover as coisas
        
        passaro.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:   
            if cano.colidir(passaro):
                tabelaPontos.append(pontos)
                reiniciar(canos,remover_canos,adicionar_cano)
                rodando = False

            if not cano.passou and passaro.x > cano.x:
                cano.passou = True
                adicionar_cano = True
            cano.mover()

            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
        for cano in remover_canos:
            canos.remove(cano)

        
        if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
            tabelaPontos.append(pontos)
            reiniciar(canos,remover_canos,adicionar_cano)
            passaro.y = 350
            passaro.x = 230
            passaro.angulo = 0
            rodando = False

        desenhar_tela(tela, passaro, canos, chao, pontos)

def main():
    passaro = Passaro(230, 350)
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()
    tabelaPontos = []

    while(True):
        menu(chao, passaro, tela, relogio, tabelaPontos)
        runGame(passaro, chao, canos, tela, pontos, relogio, tabelaPontos)

if __name__ == '__main__':
    main()