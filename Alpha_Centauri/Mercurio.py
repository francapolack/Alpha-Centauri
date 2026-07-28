import pygame
import pymunk
import sys
import random
#me duele la espaldaaaaaaaaaaaaaaaaaaa :(
pygame.init()
pygame.font.init()
pygame.mixer.init()
from class_definitions import Objetos_clickeables as Partes_Rover, Jugador
#definicion de PANTALLA
pantalla=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.set_caption("Mercurio")

#CONSTANTES ACA
FPS=60
JUGADOR_VELOCIDAD=2
TILE_TAM=32
FUENTE_DIALOGOS=pygame.font.SysFont("Consolas",300)
    #COLORES
NEGRO=(0,0,0)
BLANCO=(255,255,255)
#TEXTURAS
textura_jugador=pygame.image.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/imagenes/camina_adelante.png").convert_alpha()
rueda_textura=pygame.image.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/imagenes/objetos/mercurio/ROVER_RUEDA.png").convert_alpha()
base_textura=pygame.image.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/imagenes/objetos/mercurio/ROVER_BASE.png").convert_alpha()
camara_textura=pygame.image.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/imagenes/objetos/mercurio/ROVER_CAMARA.png").convert_alpha()

#VARIABLES ()
CONDICION_COMPLETA=False
RUNNING=True
GRAVEDAD=1000
SELECCIONADOS=[]
ESTADO_ACTUAL=""

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
cayendo_evento=pygame.USEREVENT
pygame.time.set_timer(cayendo_evento,200)

parte=pygame.Surface((20,20),pygame.SRCALPHA)
rueda=Partes_Rover(rueda_textura,10,10)
base=Partes_Rover(base_textura,10,13)
camara=Partes_Rover(camara_textura,10,16)
partes=[]



            

#DEFINICION DE CLASES,FUNCIONES Y OBJETOS 
ANCHO_PC,ALTO_PC=pygame.display.get_surface().get_size()



jugador=Jugador(textura_jugador)

def Main():
    fps.tick(100)
    while RUNNING: 
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                RUNNING=False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type==cayendo_evento:
                x=random.randrange(10,pantalla.get_width()-10)
                partes.append(pygame.Rect(x,-20,20,20))

        for partesrect in partes[:]:
            partesrect.y+=1
            if partesrect.top>pantalla.get_height():
                partes.remove(partesrect)
                    
        fisica.step(1/60.0)


        #MOVIMIENTO DEL JUGRADOR
        tecla=pygame.key.get_pressed()
        if tecla[pygame.K_LEFT] or tecla[pygame.K_a]:
            jugador.textura=pygame.image.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/imagenes/izquierdapataadelante.png")
            jugador.hitbox.move_ip(-JUGADOR_VELOCIDAD,0)

        elif tecla[pygame.K_RIGHT] or tecla[pygame.K_d]:
            jugador.hitbox.move_ip(JUGADOR_VELOCIDAD,0)

        elif tecla[pygame.K_UP] or tecla[pygame.K_w]:
            jugador.hitbox.move_ip(0,-JUGADOR_VELOCIDAD)

        elif tecla[pygame.K_DOWN] or tecla[pygame.K_s]:
            jugador.hitbox.move_ip(0,JUGADOR_VELOCIDAD)

        #MOSTRA TODO EN LA PANTALIA
        pantalla.fill(BLANCO)
        pantalla.blit(fondo,fondo_rect)
        pantalla.blit(jugador.textura,jugador.hitbox)
        for partesrect in partes:
            pantalla.blit(parte,partesrect)

        #reiniciooooo
        pygame.display.flip()
        fps.tick(FPS)

Main()
pygame.quit()
        