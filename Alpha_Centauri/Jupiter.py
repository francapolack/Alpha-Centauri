# Importing pygame module
import pygame
from random import randint
from class_definitions import Jugador, NPC as Piedritas,display_texto
pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
fuente=pygame.font.SysFont("Consolas",25,bold=True)
reloj=pygame.time.Clock()

#TEXTURAS
textura_jugador=pygame.image.load("Alpha_Centauri/imagenes/camina_adelante.png").convert_alpha()


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
voz_gigantes=pygame.mixer.Sound("Alpha_Centauri/sonidos/dialogopiedras.wav")
#OBJETOS

jugador=Jugador(textura_jugador,500,800,80,80)

alien_1=Piedritas(piedritas_textura,500,400,500,500)

#FUNCIONES
def exploracion():          
      if alien_1.hitbox.x<1000:
        alien_1.hitbox.x+=1
      elif alien_1.hitbox.x>=1000:
          
        alien_1.hitbox.x-=2
      if jugador.hitbox.colliderect(alien_1.hitbox):
              voz_gigantes.play()
              display_texto(window,600,600,"...")
      window.blit(alien_1.textura,alien_1.hitbox)


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

        tecla=pygame.key.get_pressed()
        if tecla[pygame.K_LEFT] or tecla[pygame.K_a]:
                jugador.hitbox.move_ip(-jugador.VELOCIDAD,0)
        elif tecla[pygame.K_RIGHT] or tecla[pygame.K_d]:
                jugador.hitbox.move_ip(jugador.VELOCIDAD,0)
        elif tecla[pygame.K_UP] or tecla[pygame.K_w]:
                jugador.hitbox.move_ip(0,-jugador.VELOCIDAD)
        elif tecla[pygame.K_DOWN] or tecla[pygame.K_s]:
                jugador.hitbox.move_ip(0,jugador.VELOCIDAD)

        exploracion()

        
        window.blit(jugador.textura,jugador.hitbox)

        pygame.display.update()
main()
pygame.quit()