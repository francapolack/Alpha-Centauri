# Importing pygame module
import pygame
from random import randint
from class_definitions import Jugador, Agarrables as PartesRover
pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((600, 600))
fuente=pygame.font.Font(None,36)
reloj=pygame.time.Clock()

#TEXTURAS
textura_jugador=textura_jugador=pygame.image.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/imagenes/camina_adelante.png").convert_alpha()
jugador=Jugador(textura_jugador,500,500)
#SONIDOS


#ROVER
camara=PartesRover(800,0)

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
                text=fuente.render("Usa WASD",True,(0,0,255))
                window.blit(text,(10,10))

        camara.y+=camara.velocidad

        if camara.y>jugador.hitbox.y and jugador.hitbox.x<camara.x+camara.tamanio:
            camara.y=0
            camara.x=randint(0,550)
            if jugador.hitbox.x>=camara.x and jugador.hitbox.y>=camara.y:
                score+=1
                
        
        pygame.draw.rect(window, (0, 0, 255),(camara.x,camara.y,camara.tamanio,camara.tamanio))
        #window.blit(fondo,fondo_rect)
        score_text=fuente.render(f"Score:{score}",True,(0,255,255))
        window.blit(score_text,(10,10))
        window.blit(jugador.textura,jugador.hitbox)
        pygame.display.update()
main()
pygame.quit()