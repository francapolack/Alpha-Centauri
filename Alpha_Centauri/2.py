import pygame
import pymunk
import sys


#toda la wea deel setup aquii
def dialogo(texto):
    ancho_caja=int(ANCHO_PC*0.90)
    alto_caja=int(ALTO_PC*0.22)
    caja_rect=pygame.Rect(0,0,ancho_caja,alto_caja)
    caja_rect.center=(ANCHO_PC//2,)
#comienzo del loop
def Main():
    pygame.init()
    pygame.mixer.init()


    estado="cinematica"

    fase_narrativa=1#1 es la PC, 2 es explicando lo que hace un rover, 3 es explicando como jugar
    caracteres_vistos=0
    conteo_frames=0

    while True:
        mouse=pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if estado=="cinematica":
                    if fase_narrativa==1:
                        if event.key in [pygame.K_RETURN,pygame.K_SPACE]:
                            sonido_click.play()
                            fase_narrativa=2

                    elif fase_narrativa==2:
                        if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                            sonido_click.play()
                            fase_narrativa=3
                            caracteres_vistos=0
                            conteo_frames=0

                    elif fase_narrativa==3:
                        if event.key in [pygame.K_RETURN,pygame.K_SPACE]:
                            sonido_click.play()
                    

                        
