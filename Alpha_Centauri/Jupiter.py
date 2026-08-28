# Importing pygame module
import pygame
from random import randint
from clases_funciones import *
pygame.init()
pygame.mixer.init()

#setup pantalla
window = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
fuente=pygame.font.SysFont("Consolas",25,bold=True)
reloj=pygame.time.Clock()
mouse_pos=pygame.mouse.get_pos()
#TEXTURAS
textura_jugador=pygame.image.load("Alpha_Centauri/assets/imagenes/spritesviejos/camina_atras.PNG").convert_alpha()

alien=pygame.image.load("Alpha_Centauri/assets/imagenes/objetos/jupiter/alien_1.png").convert_alpha()



fondo=pygame.image.load("Alpha_Centauri/assets/imagenes/fondos/jupiter.png")
fondo_rect=fondo.get_rect()

#SONIDOS
#musica principal
pygame.mixer.music.load("Alpha_Centauri/assets/sonidos/musica_menu.wav")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
#voces
voz_gigantes=pygame.mixer.Sound("Alpha_Centauri/assets/sonidos/dialogojupiter.mp3")
#OBJETOS

jugador=Jugador(textura_jugador,500,800,80,80)
lista_npcs=pygame.sprite.Group()
for i in range(4):
     lista_npcs.add(NPC(100,900,100,900,"Alpha_Centauri/assets/imagenes/objetos/jupiter/alien_1.png",600,600))
#FUNCIONES
# def cinematica():
#       pass
# def exploracion(): 
#       window.blit(alien_1.textura,alien_1.hitbox)
#       #display_texto(window,600,600,"RENEE:¡¿Qué es eso?!")         
#       if alien_1.hitbox.x<1000:
#         alien_1.hitbox.x+=7
#       else:
#         alien_1.hitbox.x-=2
#         alien_1.estado="IZQUIERDA" 

#       if alien_1.estado=="IZQUIERDA":
#         cambio_texto(window,fondo,fondo_rect,jugador.textura,jugador.hitbox)
#         window.blit(alien_1.textura,alien_1.hitbox)

#         display_texto(window,600,600,"MARK:Ve a ayudarlo!")

#         cambio_texto(window,fondo,fondo_rect,jugador.textura,jugador.hitbox)
#         window.blit(alien_1.textura,alien_1.hitbox)


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
        
        jugador.movimiento(jugador)
        lista_npcs.draw(window)
        #exploracion()

        pygame.display.update()
main()
pygame.quit()