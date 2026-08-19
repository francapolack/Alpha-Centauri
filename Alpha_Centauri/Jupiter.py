# Importing pygame module
import pygame
from random import randint
from Alpha_Centauri.clases_funciones import *
pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
fuente=pygame.font.SysFont("Consolas",25,bold=True)
reloj=pygame.time.Clock()
mouse_pos=pygame.mouse.get_pos()
#TEXTURAS
textura_jugador=pygame.image.load("Alpha_Centauri/imagenes/camina_adelante.png").convert_alpha()
izq_jugador=pygame.image.load("Alpha_Centauri/imagenes/izquierdapataadelante.png")

piedritas_textura=pygame.image.load("Alpha_Centauri/imagenes/objetos/jupiter/alien_1.png")
piedritas_izq_textura=pygame.transform.flip(piedritas_textura, True, False)

fondo=pygame.image.load("Alpha_Centauri/imagenes/fondos/jupiter.png")
fondo_rect=fondo.get_rect()

#SONIDOS
#musica principal
pygame.mixer.music.load("Alpha_Centauri/musica_menu.wav")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
#voces
voz_gigantes=pygame.mixer.Sound("Alpha_Centauri/sonidos/dialogojupiter.mp3")
#OBJETOS

jugador=Jugador(textura_jugador,500,800,80,80)

alien_1=NPC(piedritas_textura,500,200,500,500)

#FUNCIONES
def cinematica():
      pass
def exploracion(): 
      window.blit(alien_1.textura,alien_1.hitbox)
      display_texto(window,600,600,"RENEE:¡¿Qué es eso?!")         
      if alien_1.hitbox.x<1000:
        alien_1.hitbox.x+=7
      else:
        alien_1.hitbox.x-=2
        alien_1.estado="IZQUIERDA" 

      if alien_1.estado=="IZQUIERDA":
        cambio_texto(window,fondo,fondo_rect,jugador.textura,jugador.hitbox)
        window.blit(alien_1.textura,alien_1.hitbox)

        display_texto(window,600,600,"MARK:Ve a ayudarlo!")

        cambio_texto(window,fondo,fondo_rect,jugador.textura,jugador.hitbox)
        ayudar=display_opciones(window,600,300,"AYUDAR AL ALIEN",50)
        escapar=display_opciones(window,600,300,"ESCAPAR",50)
        window.blit(alien_1.textura,alien_1.hitbox)

        if pygame.mouse.get_pressed()[0] and ayudar.hitbox.collidepoint(mouse_pos):
            print("meow")     
        elif pygame.mouse.get_pressed()[0] and escapar.rect.colllidepoint(mouse_pos):
            print("woof") 


def main():
    loop=True
    while loop:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                loop=False
            elif event.type==pygame.KEYDOWN:
                  if event.key==pygame.K_ESCAPE:
                        loop=False

        window.fill((255, 255, 255))
        window.blit(fondo,fondo_rect)
        window.blit(jugador.textura,jugador.hitbox)
        
        movimiento(jugador)

        exploracion()

        pygame.display.update()
main()
pygame.quit()