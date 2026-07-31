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



        