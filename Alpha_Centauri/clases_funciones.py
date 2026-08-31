import pygame
import cv2,time
from pyvidplayer2 import Video
import os
from random import randrange
#COLORES
NEGRO=(0,0,0)
BLANCO=(240,240,255)
TURQUESA=(0, 200, 220)
AZUL_MARINO=(20, 20, 35)

#OTROS

#FUNCIONES
def aplicar_filtro_oscuro(superficie, opacidad_personaje):
    if superficie is None:
        return None
    img_oscura = superficie.copy()
    filtro = pygame.Surface(img_oscura.get_size(), pygame.SRCALPHA)
    filtro.fill((0, 0, 0, 120)) 
    img_oscura.blit(filtro, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    img_oscura.set_alpha(opacidad_personaje)
    return img_oscura

def puede_moverse(x, y, ancho, alto, superficie_colision, escala):
    if superficie_colision is None:
        return True  # Si no hay imagen cargada, se mueve libremente por seguridad
    
    # Puntos estratégicos del hitbox del astronauta (pies y centro)
    puntos_chequeo = [
        (x + 8, y + alto - 8),                  # Pie izquierdo
        (x + ancho - 8, y + alto - 8),          # Pie derecho
        (x + ancho // 2, y + alto - 8)          # Centro inferior
    ]
    
    for px, py in puntos_chequeo:
        # Convertir coordenadas del mundo a coordenadas de la imagen de colisión original
        img_x = int(px / escala)
        img_y = int(py / escala)
        
        if 0 <= img_x < superficie_colision.get_width() and 0 <= img_y < superficie_colision.get_height():
            color = superficie_colision.get_at((img_x, img_y))
            # Si el píxel NO es completamente transparente (es decir, pintaste una pared), choca
            if color[3] > 10:
                return False
    return True


    
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



#DISPLAY DE TEXTO EN CAJA (O CAJA DE DIALOGO)
def display_texto(pan,texto,textura):
    fuente=pygame.font.SysFont("Consolas",36,bold=True)

    #textura del personaje que habla
    textura=pygame.image.load(textura).convert_alpha()
    textura=pygame.transform.scale(textura,(750,700))
    textura_rect=textura.get_rect()
    pan.blit(textura,textura_rect)

    #primero la cajita del txto
    ancho_caja=600*2
    alto_caja=int(600*0.30)
    caja_rect=pygame.Rect(0,0,ancho_caja,alto_caja)
    caja_rect.center=(600+160,600)
    pygame.draw.rect(pan, AZUL_MARINO, caja_rect, border_radius=8)
    pygame.draw.rect(pan, TURQUESA, caja_rect, width=3, border_radius=8)
    #dibujamos el txto 
    txto=fuente.render(texto,True,BLANCO)
    pan.blit(txto,(caja_rect.x+100,caja_rect.y+45))
    
#DISPLAY DE INFO AL SALIR DE LA NAVE
def planeta_info(pan,texto1,texto2,color,septitulox,septituloy,septxtx,septxty):
    #caja de texto principal
    fuente=pygame.font.SysFont("Consolas",25,bold=True)
    fuente_titulo=pygame.font.SysFont("twcen",60,bold=True)
    #primero la cajita del txto
    ancho_caja=600
    alto_caja=700
    caja_rect=pygame.Rect(0,0,ancho_caja,alto_caja)
    caja_rect.center=(1100,400)
    pygame.draw.rect(pan, AZUL_MARINO, caja_rect, border_radius=8)
    pygame.draw.rect(pan, TURQUESA, caja_rect, width=3, border_radius=8)
    #caja de texto del TITULO
    # titulo_caja=pygame.Rect(0,0,(ancho_caja-50),int(alto_caja*0.15))
    # titulo_caja.center=(1100,112)
    # pygame.draw.rect(pan,color,titulo_caja,width=3,border_radius=20)
    #txto principal
    txto=fuente.render(f"\n\n{texto1}",True,BLANCO)
    pan.blit(txto,(caja_rect.x+septxtx,caja_rect.y+septxty))
    #texto titulo
    txto2=fuente_titulo.render(texto2,True,color)
    pan.blit(txto2,(septitulox,septituloy))
    #boton de chau (en otra cajita + chiquita)

#BOTON UNIVERSAL DE CHAU
def boton_chau(pan,x,y,color,texto,separacionx,separaciony):
    fuente=pygame.font.SysFont("twcen",30,bold=True)
    boton=pygame.Rect(0,0,300,100) 
    boton.center=(x,y)
    pygame.draw.rect(pan,color,boton,width=8,border_radius=8)
    txto=fuente.render(texto,True,BLANCO)
    pan.blit(txto,(boton.x+separacionx,boton.y+separaciony))
    return boton


#DISPLAY DE 2 OPCIONES (sin terminar)
def trivia_alien(pos_mouse,pan,pregunta,t1,t2,t3,correcta):
    fuente=pygame.font.Font(None,36)
    titulo_caja=pygame.Rect(0,0,600,500)
    titulo_caja.center=(700,200)
    pygame.draw.rect(pan,NEGRO,titulo_caja,border_radius=8)
    texto_pregunta=fuente.render(pregunta,True,BLANCO)
    pregunta_rect=texto_pregunta.get_rect()
    pan.blit(texto_pregunta,pregunta_rect)

    rect1=pygame.Rect(220, 120, 100, 50)
    rect1.center=(700,300)
    rect2=pygame.Rect(200, 120, 200, 50)
    rect2.center=(700,400)
    rect3=pygame.Rect(280, 120, 300, 50)
    rect3.center=(700,500)
    
    rects=[]
    rects.append(rect1)
    rects.append(rect2)
    rects.append(rect3)

    opciones=[t1,t2,t3]
    opcion_correcta=correcta
    seleccionada=None
    for i,rect in enumerate(rects):
         color=(100,200,100) if rect.collidepoint(pos_mouse) else (70,70,70)
         pygame.draw.rect(pan,color,rect,border_radius=8)
         txto=fuente.render(opciones[i],True,BLANCO)
         txto_rect=txto.get_rect(center=rect.center)
         pan.blit(txto,txto_rect)
         if rect.collidepoint(pos_mouse):
              seleccionada=opciones[i]
              if seleccionada==opcion_correcta:
                   print("bien")

         

#FILTRO OSCURO PARA CONVOS CON PERSONAJES
def filtro(x,y,pan):
     filtro=pygame.Surface((x,y),pygame.SRCALPHA)
     filtro.fill((0,0,0,128))
     pan.blit(filtro,(0,0))


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

class TriviaNPC:
     def __init__(self,textura,x,y,escalax,escalay):
          self.textura=pygame.image.load(textura).convert_alpha()
          self.textura=pygame.transform.scale(self.textura,(escalax,escalay))
          self.rect=self.textura.get_rect()
          self.rect.center=(x,y)
     def texto(self,pan,texto,textura_convo):
          display_texto(pan,texto,textura_convo)



class NPC(pygame.sprite.Sprite):
     def __init__(self,x1,x2,y1,y2,textura,escalax,escalay):
          super().__init__()
          x=randrange(x1,x2,3)
          y=randrange(y1,y2,1)
          self.image=pygame.image.load(textura).convert_alpha()
          self.image=pygame.transform.scale(self.image,(escalax,escalay))#no esta en ingles el codigo,pygame group no me toma textura sino image 
          self.rect=self.image.get_rect()
          self.rect.center=(x,y)
     def update(self):
          self.rect.x+=2

          
