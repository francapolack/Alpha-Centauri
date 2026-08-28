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
# def exploracion():
      
#       if jugador.hitbox.colliderect(alien_1.hitbox):
#               voz_piedritas.play()
#               display_texto(window,"Alien de piedra:\n *Sonidos de piedra*")
#       elif jugador.hitbox.colliderect(alien_2.hitbox):
#               voz_piedritas.play()
#               display_texto(window,"")
      

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
        window.blit(jugador.textura,jugador.hitbox)

        jugador.movimiento(jugador)
        lista_npcs.draw(window)
        planeta_info(window,"info de mercurio \nblah blah blah","Mercurio",(pygame.Color("azure3")))

        pygame.display.update()
main()
# import Jupiter
# Jupiter.main()
pygame.quit()