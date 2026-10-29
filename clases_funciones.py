import pygame
import random
from config import *

class Boton:
    def __init__(self, x, y, ancho, alto, color_normal, color_hover, texto="", fuente=None):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.texto = texto
        self.fuente = fuente

    def dibujar(self, superficie):
        mouse_pos = pygame.mouse.get_pos()
        color = self.color_hover if self.rect.collidepoint(mouse_pos) else self.color_normal
        pygame.draw.rect(superficie, color, self.rect, border_radius=8)
        if self.texto and self.fuente:
            txt_superficie = self.fuente.render(self.texto, True, (255, 255, 255))
            txt_rect = txt_superficie.get_rect(center=self.rect.center)
            superficie.blit(txt_superficie, txt_rect)

    def presionado(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                return True
        return False

class EfectoEstrellas:
    def __init__(self, cantidad=100):
        self.estrellas = [[random.randint(0, ANCHO_PANTALLA), random.randint(0, ALTO_PANTALLA), random.randint(1, 3)] for _ in range(cantidad)]

    def actualizar_y_dibujar(self, superficie):
        for est in self.estrellas:
            est[0] -= est[2]
            if est[0] < 0:
                est[0] = ANCHO_PANTALLA
                est[1] = random.randint(0, ALTO_PANTALLA)
            pygame.draw.circle(superficie, (255, 255, 255), (int(est[0]), int(est[1])), est[2])