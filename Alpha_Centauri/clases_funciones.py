import pygame
import cv2,time
from pyvidplayer2 import Video
import os
from random import randint
#COLORES
NEGRO=(0,0,0)
BLANCO=(240,240,255)
TURQUESA=(0, 200, 220)
AZUL_MARINO=(20, 20, 35)
#OTROS

#FUNCIONES


    
#VIDEOS

FFMPEG_RUTA=r"C:/ffmpeg/bin"
#os environ= como un diccionario de las variables de entorno (donde estan como las librerias y cosas asi) y os.pathsep=(buscador de carpetas)
os.environ["PATH"]=FFMPEG_RUTA+os.pathsep+os.environ["PATH"]

#funcion de video
def video(ruta,nombre):
    vid=Video(ruta,use_pygame_audio=True)
    display=pygame.display.set_mode((vid.current_size))
    pygame.display.set_caption(nombre)
    while vid.active:
         for event in pygame.event.get():
              if event.type==pygame.QUIT:
                   vid.stop()
         if vid.draw(display,(0,0),force_draw=False):
              pygame.display.update()
         pygame.time.wait(16)
    vid.close()
    pygame.quit()


#DISPLAY DE TEXTO EN CAJA
def display_texto(pan,texto):
    fuente=pygame.font.SysFont("Consolas",36,bold=True)
    #primero la cajita del txto
    ancho_caja=int(600*2)
    alto_caja=int(600*0.30)
    caja_rect=pygame.Rect(0,0,ancho_caja,alto_caja)
    caja_rect.center=(600+160,600)
    pygame.draw.rect(pan, AZUL_MARINO, caja_rect, border_radius=8)
    pygame.draw.rect(pan, TURQUESA, caja_rect, width=3, border_radius=8)
    #dibujamos el txto 
    txto=fuente.render(texto,True,BLANCO)
    pan.blit(txto,(caja_rect.x+100,caja_rect.y+45))

#DISPLAY DE 2 OPCIONES (sin terminar)
def opciones(pan,f,frect,txt1,txt2):
    pass
    """
     pygame.mouse.get_pos()
     pan.blit(f,frect)
     fuente=pygame.font.Font(None,36)

     globotxta=pygame.image.load("Alpha_Centauri/imagenes/objetos/general/globo.png")
     globotxt_flip=pygame.transform.flip(globotxta, True, False)

    #opcion 1
     globo1=globotxta
     globo1_rect=globo1.get_rect()
     if pygame.mouse.get_pressed()[0] and globo1_rect.collidepoint(mouse_pos):
          
     #txto1=fuente.render(txt1,True,NEGRO)
     #pan.blit(globo1,txto1)



    #opcion 2
     #globo2=globotxt_flip
     #globo2_rect=globo2.get_rect()
    """

#LIMPIAR PANTALLA PARA TEXTO
def cambio_texto(pan,f,frect,j,jrect):
    pan.blit(f,frect)
    pan.blit(j,jrect)






#CLASES
class Jugador:
    VELOCIDAD=9
    def __init__(self,textura,x,y,escalax,escalay):
        self.textura_inicial=textura
        self.textura=pygame.transform.scale(self.textura_inicial,(escalax,escalay))
        self.hitbox=self.textura.get_rect()
        self.hitbox.center=(x,y)
        self.pos_x=self.hitbox.x
        self.pos_y=self.hitbox.y
    def movimiento(self,jugador):
        tecla=pygame.key.get_pressed()
        if tecla[pygame.K_LEFT] or tecla[pygame.K_a]:
                jugador.hitbox.move_ip(-jugador.VELOCIDAD,0)
        elif tecla[pygame.K_RIGHT] or tecla[pygame.K_d]:
                jugador.hitbox.move_ip(jugador.VELOCIDAD,0)
        elif tecla[pygame.K_UP] or tecla[pygame.K_w]:
                jugador.hitbox.move_ip(0,-jugador.VELOCIDAD)
        elif tecla[pygame.K_DOWN] or tecla[pygame.K_s]:
                jugador.hitbox.move_ip(0,jugador.VELOCIDAD)


#medio deprecado....
# class NPC:
#     def __init__(self,textura,x,y,escalax,escalay):
#         self.estado="DERECHA"
#         self.textura_inicial=textura
#         self.textura=pygame.transform.scale(textura,(escalax,escalay))
#         self.hitbox=self.textura.get_rect()
#         self.hitbox.center=(x,y)
       
class NPC(pygame.sprite.Sprite):
     def __init__(self,x1,x2,y1,y2,textura):
          super().__init__()
          x=randint(x1,x2)
          y=randint(y1,y2)
          self.image=pygame.image.load("Alpha_Centauri/assets/imagenes/objetos/jupiter/alien_1.png").convert_alpha()
          self.image=pygame.transform.scale(self.image,(80,80))#no esta en ingles el codigo,pygame group no me toma textura sino image 
          self.rect=self.image.get_rect()
          self.rect.topleft=(x,y)
     def update(self):
          self.rect.x+=2

#crea 3 esparcidos por coordenadas random
def lista_sprites(x1,x2,y1,y2,textura):
     x=randint(x1,x2)
     y=randint(y1,y2)   

     alien_1=NPC(x,y,textura)
     alien_2=NPC(x,y,textura)
     alien_3=NPC(x,y,textura)

     return alien_1,alien_2,alien_3


     


class Objeto:
     def __init__(self,textura,x,y,escalax,escalay,texto,sonido):
          self.textura=textura
          self.x=x
          self.y=y
          self.escalax=escalax
          self.escalay=escalay
          self.texto=texto
          self.sonido=sonido
          
