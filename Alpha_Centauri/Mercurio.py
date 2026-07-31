# Importing pygame module
import pygame
from random import randint
from class_definitions import Jugador, NPC as Piedritas,display_texto
pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
fuente=pygame.font.SysFont("Consolas",36,bold=True)
reloj=pygame.time.Clock()

#TEXTURAS
textura_jugador=textura_jugador=pygame.image.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/imagenes/camina_adelante.png").convert_alpha()


piedritas_textura=pygame.image.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/imagenes/objetos/mercurio/alien_1.png")

fondo=pygame.image.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/imagenes/fondos/mercurio.png")
fondo_rect=fondo.get_rect()

#SONIDOS
#musica principal
pygame.mixer.music.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/sonidos/mercurio.wav")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

#OBJETOS
jugador=Jugador(textura_jugador,500,500)
alien_1=Piedritas(piedritas_textura,500,500)

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
              

        
        display_texto(window,600,600,"Holi")
        window.blit(alien_1.textura,alien_1.hitbox)
        window.blit(jugador.textura,jugador.hitbox)
        pygame.display.update()
main()
pygame.quit()