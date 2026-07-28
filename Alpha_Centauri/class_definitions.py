import pygame

class Jugador:
    def __init__(self,textura,x,y):
        self.textura=textura
        self.hitbox=self.textura.get_rect()
        self.hitbox.center=(x,y)

class Objetos_clickeables:
    click=False
    def __init__(self,textura,x,y):
        self.textura=textura
        self.hitbox=self.textura.get_rect()
        self.hitbox.center=(x,y)

        