import pygame

#colores
NEGRO=(0,0,0)
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
        