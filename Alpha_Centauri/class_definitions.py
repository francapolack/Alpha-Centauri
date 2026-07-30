import pygame

class Jugador:
    def __init__(self,textura,x,y):
        self.textura_inicial=textura
        self.textura=pygame.transform.scale(self.textura_inicial,(60,60))
        self.hitbox=self.textura.get_rect()
        self.hitbox.center=(x,y)
    def movimiento(self):
        VELOCIDAD=2
        tecla=pygame.key.get_pressed()
        if tecla[pygame.K_LEFT] or tecla[pygame.K_a]:
            self.hitbox.move_ip(-VELOCIDAD,0)
        elif tecla[pygame.K_RIGHT] or tecla[pygame.K_d]:
            self.hitbox.move_ip(VELOCIDAD,0)

class Agarrables:
    AGARRADO=False
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.velocidad=2
        self.tamanio=40



        