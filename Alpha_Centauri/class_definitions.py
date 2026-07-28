import pygame

class Jugador:
    def __init__(self,textura,x,y):
        self.textura=textura
        self.hitbox=self.textura.get_rect()
        self.hitbox.center=(x,y)

class Objetos_clickeables:
    click=False
    def __init__(self,x,y):
        self.textura=self.textura
        self.hitbox=self.textura.get_rect()
        self.hitbox.center=(x,y)
    def descripcion(self,texto):
        self.texto=texto

        