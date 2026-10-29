import pygame
import sys
from config import *

def ejecutar_nivel_mercurio(pantalla, reloj):
    fuente = pygame.font.SysFont("Arial", 30)
    fuente_titulo = pygame.font.SysFont("Arial", 40, bold=True)
    
    reloj_nivel = pygame.time.Clock()
    
    while True:
        pantalla.fill((40, 20, 10))
        
        titulo = fuente_titulo.render("Nivel: Mercurio - Superficie Solar", True, (255, 100, 50))
        instruccion = fuente.render("Presiona ESPACIO para completar misión o ESC para volver a la nave.", True, (200, 200, 200))
        
        pantalla.blit(titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, 150))
        pantalla.blit(instruccion, (ANCHO_PANTALLA // 2 - instruccion.get_width() // 2, 250))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "nave"
                if evento.key == pygame.K_SPACE:
                    return "nave"
                    
        pygame.display.flip()
        reloj_nivel.tick(FPS)