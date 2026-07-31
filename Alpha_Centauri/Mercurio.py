# Importing pygame module
import pygame
from random import randint
from class_definitions import Jugador, Agarrables as PartesRover,display_texto
pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((600, 600))
fuente=pygame.font.SysFont("Consolas",36,bold=True)
reloj=pygame.time.Clock()

#TEXTURAS
textura_jugador=textura_jugador=pygame.image.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/imagenes/camina_adelante.png").convert_alpha()
jugador=Jugador(textura_jugador,500,500)
#SONIDOS


#ROVER
camara=PartesRover(800,0)
rueda=PartesRover(700,0)
base=PartesRover(600,0)
def main():
    loop=True
    score=0
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        window.fill((255, 255, 255))

        tecla=pygame.key.get_pressed()
        if tecla[pygame.K_LEFT] or tecla[pygame.K_a]:
                jugador.hitbox.move_ip(-jugador.VELOCIDAD,0)
        elif tecla[pygame.K_RIGHT] or tecla[pygame.K_d]:
                jugador.hitbox.move_ip(jugador.VELOCIDAD,0)

        camara.y+=camara.velocidad
        if jugador.hitbox.x>=camara.x and jugador.hitbox.y>=camara.y:
                    score+=1
                    camara.AGARRADO==True
                    logrado=fuente.render("Has construido el ROVER!!",True,(0,244,244))
                    window.blit(logrado,(80,10))
                    
        
        pygame.draw.rect(window, (0, 0, 255),(camara.x,camara.y,camara.tamanio,camara.tamanio))
        pygame.draw.rect(window, (0, 255, 0),(base.x,base.y,base.tamanio,base.tamanio))
        pygame.draw.rect(window, (255, 0, 0),(rueda.x,rueda.y,rueda.tamanio,rueda.tamanio))
        #window.blit(fondo,fondo_rect)
        display_texto(window,600,600,"Holi")
        window.blit(jugador.textura,jugador.hitbox)
        pygame.display.update()
main()
pygame.quit()