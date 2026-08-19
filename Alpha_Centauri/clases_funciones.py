import pygame
import os
#COLORES
NEGRO=(0,0,0)
BLANCO=(240,240,255)
TURQUESA=(0, 200, 220)
AZUL_MARINO=(20, 20, 35)

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
    def movimiento(self,jugador,textura,aba,arr):
        tecla=pygame.key.get_pressed()
        if tecla[pygame.K_LEFT] or tecla[pygame.K_a]:
                self.textura_inicial=pygame.transform.flip(textura,True,False)
                jugador.hitbox.move_ip(-jugador.VELOCIDAD,0)
        elif tecla[pygame.K_RIGHT] or tecla[pygame.K_d]:
                jugador.hitbox.move_ip(jugador.VELOCIDAD,0)
        elif tecla[pygame.K_UP] or tecla[pygame.K_w]:
                self.textura_inicial=arr
                jugador.hitbox.move_ip(0,-jugador.VELOCIDAD)
        elif tecla[pygame.K_DOWN] or tecla[pygame.K_s]:
                self.textura_inicial=aba
                jugador.hitbox.move_ip(0,jugador.VELOCIDAD)



class NPC:
    def __init__(self,textura,x,y,escalax,escalay):
        self.estado="DERECHA"
        self.textura_inicial=textura
        self.textura=pygame.transform.scale(textura,(escalax,escalay))
        self.hitbox=self.textura.get_rect()
        self.hitbox.center=(x,y)
        if self.estado=="IZQUIERDA":
            self.textura_inicial=pygame.transform.flip(textura, True, False)
            

#FUNCIONES
#no es una clase pero no conviene hacer otro docx separado 
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

def cambio_texto(pan,f,frect,j,jrect):
    pan.blit(f,frect)
    pan.blit(j,jrect)



def aplicar_filtro_oscuro(superficie, opacidad_personaje):
    """Genera una copia oscurecida del personaje para darle énfasis al que habla."""
    if superficie is None:
        return None
    img_oscura = superficie.copy()
    filtro = pygame.Surface(img_oscura.get_size(), pygame.SRCALPHA)
    filtro.fill((0, 0, 0, 120)) 
    img_oscura.blit(filtro, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    img_oscura.set_alpha(opacidad_personaje)
    return img_oscura

def cargar_img_mapa(carpeta,nombre_archivo, ALTO_MAPA,ancho_fijo=None):
    ruta = os.path.join(carpeta, "imagenes", nombre_archivo)
    if os.path.exists(ruta):
        img = pygame.image.load(ruta).convert_alpha()
        if ancho_fijo:
            ancho_final = ancho_fijo
        else:
            ancho_final = int(img.get_width() * (ALTO_MAPA / img.get_height()))
        return pygame.transform.scale(img, (ancho_final, ALTO_MAPA))
        
    ancho_aux = ancho_fijo if ancho_fijo else 35
    surf = pygame.Surface((ancho_aux, ALTO_MAPA))
    surf.fill((255, 0, 0))
    return surf

def os_join(carpeta,nombre):
     objeto=os.path.join(carpeta,nombre)
     if os.path.exists:
          return True