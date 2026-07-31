import pygame

class Jugador:
    VELOCIDAD=1
    def __init__(self,textura,x,y):
        self.textura_inicial=textura
        self.textura=pygame.transform.scale(self.textura_inicial,(60,60))
        self.hitbox=self.textura.get_rect()
        self.hitbox.center=(x,y)
        
        

class Agarrables:
    AGARRADO=False
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.velocidad=1
        self.tamanio=90

#no es una clase pero no conviene hacer otro docx separado 
def display_texto(pan,ancho,alto,texto):
    fuente=pygame.font.SysFont("Consolas",36,bold=True)
    #primero la cajita del txto
    ancho_caja=int(ancho*0.90)
    alto_caja=int(alto*0.22)
    caja_rect=pygame.Rect(0,0,ancho_caja,alto_caja)
    caja_rect.center=(ancho//2,alto-int(alto*0.14))
    pygame.draw.rect(pan, (20, 20, 35), caja_rect, border_radius=8)
    pygame.draw.rect(pan, (0, 200, 220), caja_rect, width=3, border_radius=8)
    #dibujamos el txto 
    txto=fuente.render(texto,True,(240,240,255))
    pan.blit(txto,(caja_rect.x+25,caja_rect.y+35))

        