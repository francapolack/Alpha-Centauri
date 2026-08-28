# Importing pygame module
import pygame
from random import randint
from clases_funciones import *
pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
fuente=pygame.font.SysFont("Consolas",15)
reloj=pygame.time.Clock()

#TEXTURAS
textura_jugador=pygame.image.load("Alpha_Centauri/assets/imagenes/objetos/mercurio/rover.png").convert_alpha()


piedritas_textura=pygame.image.load("Alpha_Centauri/assets/imagenes/objetos/mercurio/alien_1.png")
piedritas_izq_textura=pygame.transform.flip(piedritas_textura, True, False)

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

lista_npcs=pygame.sprite.Group()
for i in range(4):
     lista_npcs.add(NPC(700,1500,500,700,"Alpha_Centauri/assets/imagenes/objetos/mercurio/alien_1.png",100,100))
for i in range(2):
     lista_npcs.add(NPC(200,800,500,700,"Alpha_Centauri/assets/imagenes/objetos/mercurio/alien_1.png",100,100))
     

#FUNCIONES



      

def main():
    
    chau_display=False
    loop=True
    while loop:
        window.fill((255,255,255))
        window.blit(fondo,fondo_rect)                
        window.blit(jugador.textura,jugador.hitbox)
        jugador.movimiento(jugador)
        lista_npcs.draw(window)

        planeta_info(window,"info de mercurio \nblah blah blah","MERCURIO",(pygame.Color("azure3")))
        boton=boton_chau(window,1150,655,(pygame.Color("seashell3")))

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
                       elif trivia.collidepoint(event.pos):
                            responder=True

        if chau_display:
            cambio_texto(window,fondo,fondo_rect,jugador.textura,jugador.hitbox)
            lista_npcs.draw(window)
            jugador.movimiento(jugador)

        

        pygame.display.update()

main()
# import Jupiter
# Jupiter.main()
pygame.quit()