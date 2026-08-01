import pygame

#colores
BLANCO=(240,240,255)
TURQUESA=(0, 200, 220)
AZUL_MARINO=(20, 20, 35)

class Jugador:
    VELOCIDAD=9
    def __init__(self,textura,x,y,escalax,escalay):
        self.textura_inicial=textura
        self.textura=pygame.transform.scale(self.textura_inicial,(escalax,escalay))
        self.hitbox=self.textura.get_rect()
        self.hitbox.center=(x,y)
        self.pos_x=self.hitbox.x
        self.pos_y=self.hitbox.y
        
def movimiento(jugador):
    tecla=pygame.key.get_pressed()
    if tecla[pygame.K_LEFT] or tecla[pygame.K_a]:
            jugador.hitbox.move_ip(-jugador.VELOCIDAD,0)
    elif tecla[pygame.K_RIGHT] or tecla[pygame.K_d]:
            jugador.hitbox.move_ip(jugador.VELOCIDAD,0)
    elif tecla[pygame.K_UP] or tecla[pygame.K_w]:
            jugador.hitbox.move_ip(0,-jugador.VELOCIDAD)
    elif tecla[pygame.K_DOWN] or tecla[pygame.K_s]:
            jugador.hitbox.move_ip(0,jugador.VELOCIDAD)
    pass

class NPC:
    def __init__(self,textura,x,y,escalax,escalay):
        self.estado="DERECHA"
        self.textura_inicial=textura
        self.textura=pygame.transform.scale(textura,(escalax,escalay))
        self.hitbox=self.textura.get_rect()
        self.hitbox.center=(x,y)
        if self.estado=="IZQUIERDA":
            self.textura_inicial=pygame.transform.flip(textura, True, False)
            


#no es una clase pero no conviene hacer otro docx separado 
def display_texto(pan,ancho,alto,texto):
    fuente=pygame.font.SysFont("Consolas",36,bold=True)
    #primero la cajita del txto
    ancho_caja=int(ancho*2)
    alto_caja=int(alto*0.30)
    caja_rect=pygame.Rect(0,0,ancho_caja,alto_caja)
    caja_rect.center=(ancho+160,alto)
    pygame.draw.rect(pan, AZUL_MARINO, caja_rect, border_radius=8)
    pygame.draw.rect(pan, TURQUESA, caja_rect, width=3, border_radius=8)
    #dibujamos el txto 
    txto=fuente.render(texto,True,BLANCO)
    pan.blit(txto,(caja_rect.x+100,caja_rect.y+45))

def display_2_opciones(pan,ancho,alto1,alto2,texto1,texto2):
    fuente=pygame.font.Font(None,36)
     #cajita 1
    ancho_caja=int(ancho)
    alto_caja=int(alto1*0.15)
    caja_rect_1=pygame.Rect(0,0,ancho_caja,alto_caja)
    caja_rect_1.center=(ancho+160,alto1)
    pygame.draw.rect(pan, AZUL_MARINO, caja_rect_1, border_radius=8)
    pygame.draw.rect(pan, TURQUESA, caja_rect_1, width=3, border_radius=8)
    #texto cajita1
    txto1=fuente.render(texto1,True,BLANCO)
    pan.blit(txto1,(caja_rect_1.x+100,caja_rect_1.y+45))
    #cajita2
    ancho_caja=int(ancho)
    alto_caja=int(alto2*0.15)
    caja_rect_2=pygame.Rect(0,0,ancho_caja,alto_caja)
    caja_rect_2.center=(ancho+160,alto2)
    pygame.draw.rect(pan, AZUL_MARINO, caja_rect_2, border_radius=8)
    pygame.draw.rect(pan, TURQUESA, caja_rect_2, width=3, border_radius=8)
    #texto cajita2
    txto2=fuente.render(texto2,True,BLANCO)
    pan.blit(txto2,(caja_rect_2.x//2,caja_rect_2.y//1))


def cambio_texto(pan,f,frect,j,jrect):
    pan.blit(f,frect)
    pan.blit(j,jrect)
        