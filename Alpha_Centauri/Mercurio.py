# Importing pygame module
import pygame
from random import randint
from clases_funciones import *
from textos import mercurio, venus_preguntas
pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
ancho,alto=window.get_size()
fuente=pygame.font.SysFont("Consolas",15)
reloj=pygame.time.Clock()
mouse_pos=pygame.mouse.get_pos()

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

#npcs que estan ahi nomas (reemplazar con obketos)
# lista_npcs=pygame.sprite.Group()
# for i in range(4):
#      lista_npcs.add(NPC(700,1500,500,700,"Alpha_Centauri/assets/imagenes/objetos/mercurio/alien_1.png",100,100))
# for i in range(2):
#      lista_npcs.add(NPC(200,800,500,700,"Alpha_Centauri/assets/imagenes/objetos/mercurio/alien_1.png",100,100))
     
#el npc de trivia
trivia=TriviaNPC("Alpha_Centauri/assets/imagenes/objetos/mercurio/alien_1.png",500,500,100,100)
test="pregunta"
#FUNCIONES



      

def main():
    hablando=False
    responder=False
    chau_display=False
    loop=True
    #video("Alpha_Centauri/assets/videos/intro.mp4","Intro")

    while loop:
        window.fill((255,255,255))
        window.blit(fondo,fondo_rect)                
        window.blit(jugador.textura,jugador.hitbox)
        jugador.movimiento(jugador)
        #lista_npcs.draw(window)

        planeta_info(window,mercurio,"MERCURIO",(pygame.Color("azure3")),960,80,55,60)
        boton=boton_chau(window,1100,655,(pygame.Color("lightslateblue")),"CERRAR",90,35)

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
            #lista_npcs.draw(window)
            jugador.movimiento(jugador)
            window.blit(trivia.textura,trivia.rect)
            if hablando:
                    filtro(ancho,alto,window)
                    trivia.texto(window,"Bienvenido a Mercurio","Alpha_Centauri/assets/imagenes/objetos/mercurio/alien_convo.png")
                    resp=boton_chau(window,1100,600,pygame.Color("lightslateblue"),"Responder",70,30)
                    if responder:
                          cambio_texto(window,fondo,fondo_rect,jugador.textura,jugador.hitbox)
                          jugador.movimiento(jugador)
                          window.blit(trivia.textura,trivia.rect)
                          trivia_alien(mouse_pos,window,"test","uno","dos","tres",2)


        pygame.display.update()

main()
import Jupiter
Jupiter.main()
pygame.quit()