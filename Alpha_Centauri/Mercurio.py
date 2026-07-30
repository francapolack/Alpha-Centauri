import pygame
import pymunk
import sys
import random
from class_definitions import Jugador

pygame.init()
pygame.font.init()
pygame.mixer.init()

#definicion de PANTALLA
pantalla=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.set_caption("Mercurio")

#CONSTANTES ACA
FPS=60
FUENTE_DIALOGOS=pygame.font.SysFont("Consolas",300)
ANCHO_PC,ALTO_PC=pygame.display.get_surface().get_size()
    #COLORES
NEGRO=(0,0,0)
BLANCO=(255,255,255)
    #TEXTURAS
textura_jugador=pygame.image.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/imagenes/camina_adelante.png").convert_alpha()
rueda_textura=pygame.image.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/imagenes/objetos/mercurio/ROVER_RUEDA.png").convert_alpha()
base_textura=pygame.image.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/imagenes/objetos/mercurio/ROVER_BASE.png").convert_alpha()
camara_textura=pygame.image.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/imagenes/objetos/mercurio/ROVER_CAMARAS.png").convert_alpha()

#VARIABLES
RUNNING=True
GRAVEDAD=1000
PARTES_AGARRADAS=[]

#BASES PARA EK JUEGO
fps=pygame.time.Clock()

fisica=pymunk.Space()
fisica.gravity=(0,GRAVEDAD)

fondo=pygame.image.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/imagenes/fondos/laboratorio.png")
fondo_rect=fondo.get_rect()

#musica y SONIDOS
musica_mercurio="Alpha-Centauri-6to-A-o/Alpha_Centauri/musica_menu.wav"
click_sonido=pygame.mixer.Sound("Alpha-Centauri-6to-A-o/Alpha_Centauri/click.wav")
pygame.mixer.music.load(musica_mercurio)
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

#sobre las partes del ROVER
class PartesRover:
    AGARRADO=False
    def __init__(self,textura):
        self.textura=textura
        self.hitbox=self.textura.get_rect()
        self.x=random.randint(30,40)
        self.y=random.randint(50,60)
        self.velocidad=1
        self.tamanio=30

#DEFINICION DE OBJETOS
jugador=Jugador(textura_jugador,(ANCHO_PC//2),(ALTO_PC-45))
camara=PartesRover(camara_textura)
class Main:
    fps.tick(100)
    while RUNNING: 
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                RUNNING=False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()  
                 
        fisica.step(1/60.0)
        while len(PARTES_AGARRADAS)<4:
            while camara.AGARRADO!=True:
                camara.hitbox.y+=camara.velocidad
                if camara.hitbox.colliderect(jugador.hitbox):
                    camara.AGARRADO==True
                    PARTES_AGARRADAS.append("CÁMARA")
                    print("fin")
            
        #MOSTRA TODO EN LA PANTALIA
        pantalla.fill(BLANCO)
        pantalla.blit(fondo,fondo_rect)
        pantalla.blit(jugador.textura,jugador.hitbox)
        pantalla.blit(camara.textura,camara.hitbox)
        #reiniciooooo
        pygame.display.flip()
        fps.tick(FPS)

Main()
pygame.quit()
        