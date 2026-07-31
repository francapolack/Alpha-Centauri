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
textura_jugador=pygame.image.load("Alpha_Centauri/imagenes/objetos/mercurio/rover.png").convert_alpha()


piedritas_textura=pygame.image.load("Alpha_Centauri/imagenes/objetos/mercurio/alien_1.png")
piedritas_izq_textura=pygame.transform.flip(piedritas_textura, True, False)

fondo=pygame.image.load("Alpha_Centauri/imagenes/fondos/mercurio.png")
fondo_rect=fondo.get_rect()

#SONIDOS
#musica principal
pygame.mixer.music.load("Alpha_Centauri/musica_menu.wav")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)
#voces
voz_piedritas=pygame.mixer.Sound("Alpha_Centauri/sonidos/dialogopiedras.wav")
#OBJETOS

jugador=Jugador(textura_jugador,500,800)


alien_1=Piedritas(piedritas_textura,500,500,200,120)
alien_2=Piedritas(piedritas_izq_textura,1450,200,200,120)

#FUNCIONES
def exploracion():
      if jugador.hitbox.colliderect(alien_1.hitbox):
              voz_piedritas.play()
              display_texto(window,600,600,"Hola!!Hola!!")
      elif jugador.hitbox.colliderect(alien_2.hitbox):
              voz_piedritas.play()
              display_texto(window,600,600,"¿De donde venis?")
      window.blit(alien_1.textura,alien_1.hitbox)
      window.blit(alien_2.textura,alien_2.hitbox)

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