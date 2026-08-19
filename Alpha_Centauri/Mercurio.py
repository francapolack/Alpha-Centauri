# Importing pygame module
import pygame
from random import randint
from Alpha_Centauri.clases_funciones import *
pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
fuente=pygame.font.SysFont("Consolas",15)
reloj=pygame.time.Clock()

#TEXTURAS
textura_jugador=pygame.image.load("Alpha_Centauri/imagenes/objetos/mercurio/rover.png").convert_alpha()
textura_jugador_arriba=pygame.image.load("Alpha_Centauri/imagenes/objetos/mercurio/roverarr.png").convert_alpha()
textura_jugador_abajo=pygame.image.load("Alpha_Centauri/imagenes/objetos/mercurio/roveraba.png").convert_alpha()

piedritas_textura=pygame.image.load("Alpha_Centauri/imagenes/objetos/mercurio/alien_1.png")
piedritas_izq_textura=pygame.transform.flip(piedritas_textura, True, False)

fondo=pygame.image.load("Alpha_Centauri/imagenes/fondos/mercurio.png")
fondo_rect=fondo.get_rect()

#SONIDOS
#musica principal
pygame.mixer.music.load("Alpha_Centauri/musica_menu.wav")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
#voces
voz_piedritas=pygame.mixer.Sound("Alpha_Centauri/sonidos/dialogopiedras.wav")
#OBJETOS

jugador=Jugador(textura_jugador,500,800,400,400)

alien_1=NPC(piedritas_textura,700,500,200,120)
alien_2=NPC(piedritas_izq_textura,900,500,200,120)

#FUNCIONES
def exploracion():
      window.blit(alien_1.textura,alien_1.hitbox)
      window.blit(alien_2.textura,alien_2.hitbox)
      if jugador.hitbox.colliderect(alien_1.hitbox):
              voz_piedritas.play()
              display_texto(window,"Alien de piedra:\n *Sonidos de piedra*")
      elif jugador.hitbox.colliderect(alien_2.hitbox):
              voz_piedritas.play()
              display_texto(window,"Alien de piedra:\n *Sonidos de piedra(pero con un acento diferente)*")
      

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
        exploracion()

        pygame.display.update()
main()
import Jupiter
Jupiter.main()
pygame.quit()