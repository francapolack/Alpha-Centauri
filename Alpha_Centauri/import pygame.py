import pygame
import random

pygame.init()

ancho=800
alto=600
pantalla=pygame.display.set_mode((ancho,alto))

pygame.display.set_caption("ya weon no quiero programar mas")

clock=pygame.time.Clock()
FPS=60

jugador_x=350
jugador_y=500
jugador_velocidad=7

obj_x=random.randint(0,ancho-50)
obj_y=0
obj_velocidad=2
obj_tamanio=40

score=0
font=pygame.font.Font(None,36)

running=True

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    keys=pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        jugador_x-=jugador_velocidad
    elif keys[pygame.K_RIGHT]:
        jugador_x+=jugador_velocidad

    jugador_x=max(0,min(jugador_x,ancho-50))

    obj_y+=obj_velocidad
#   
    if obj_y>jugador_y and jugador_x<obj_x+ obj_tamanio:
        score+=1
        obj_y=0
        obj_x=random.randint(0,ancho-50)
        obj_velocidad+=0.1

    pantalla.fill((0,0,0))
    pygame.draw.rect(pantalla,(255,255,255),(jugador_x,jugador_y,50,20))
    pygame.draw.rect(pantalla,(255,0,0),(obj_x,obj_y,obj_tamanio,obj_tamanio))

    score_text=font.render(f"Score:{score}",True,(255,255,255))
    pantalla.blit(score_text,(10,10))
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()