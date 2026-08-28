# Importing pygame module
import pygame
from random import randint
from clases_funciones import *
pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
ancho,alto=window.get_size()
fuente=pygame.font.SysFont("Consolas",15)
reloj=pygame.time.Clock()

#TEXTURAS
textura_jugador=pygame.image.load("Alpha_Centauri/assets/imagenes/objetos/mercurio/rover.png").convert_alpha()



fondo=pygame.image.load("Alpha_Centauri/assets/imagenes/fondos/mercurio.png")
fondo_rect=fondo.get_rect()

#SONIDOS
#musica principal
pygame.mixer.music.load("Alpha_Centauri//assets/sonidos/musica_menu.wav")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
#voces
voz_piedritas=pygame.mixer.Sound("Alpha_Centauri/assets/sonidos/dialogopiedras.wav")
#OBJETOS

jugador=Jugador(textura_jugador,600,800,400,300)

#npcs que estan ahi nomas
lista_npcs=pygame.sprite.Group()
for i in range(4):
     lista_npcs.add(NPC(700,1500,500,700,"Alpha_Centauri/assets/imagenes/objetos/mercurio/alien_1.png",100,100))
for i in range(2):
     lista_npcs.add(NPC(200,800,500,700,"Alpha_Centauri/assets/imagenes/objetos/mercurio/alien_1.png",100,100))
     
#el npc de trivia
trivia=TriviaNPC("Alpha_Centauri/assets/imagenes/objetos/mercurio/alien_1.png",500,500,100,100)
#FUNCIONES



      

def main():
    hablando=False
    responder=False
    chau_display=False
    loop=True
    video("Alpha_Centauri/assets/videos/intro.mp4","Intro")
    while loop:
        window.fill((255,255,255))
        window.blit(fondo,fondo_rect)                
        window.blit(jugador.textura,jugador.hitbox)
        jugador.movimiento(jugador)
        lista_npcs.draw(window)

        planeta_info(window,"Mercurio es el planeta más pequeño de nuestro \n sistema solar y el más cercano al Sol \nA pesar de su proximidad al Sol, Mercurio no es el planeta más caliente de nuestro sistema solar; ese título le corresponde a la cercana Venus, gracias a su densa atmósfera. \nSin embargo, Mercurio es el planeta más rápido, \norbitando alrededor del Sol cada 88 días terrestres","MERCURIO",(pygame.Color("azure3")))
        boton=boton_chau(window,1150,655,(pygame.Color("seashell3")),"CERRAR")

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                loop=False
            elif event.type==pygame.KEYDOWN:
                  if event.key==pygame.K_ESCAPE:
                        loop=False
            elif event.type==pygame.MOUSEBUTTONDOWN:
                  if event.button==1:
                       if boton.collidepoint(event.pos):
                            chau_display=True
                       elif trivia.rect.collidepoint(event.pos):
                            hablando=True
                       elif resp.collidepoint(event.pos):
                                 responder=True

        if chau_display:
            cambio_texto(window,fondo,fondo_rect,jugador.textura,jugador.hitbox)
            lista_npcs.draw(window)
            jugador.movimiento(jugador)
            window.blit(trivia.textura,trivia.rect)
            if hablando:
                    filtro(ancho,alto,window)
                    trivia.texto(window,"Bienvenido a Mercurio","Alpha_Centauri/assets/imagenes/objetos/mercurio/alien_convo.png")
                    resp=boton_chau(window,1000,600,pygame.Color("lightblue1"),"Responder")
                    # if responder:
                    #      display2opciones()
                 
        

        pygame.display.update()

main()
import Jupiter
Jupiter.main()
pygame.quit()