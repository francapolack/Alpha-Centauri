import pygame
from entidades import Asteroide

def ejecutar_minijuego(pantalla, imagen_asteroide, fondo):
    reloj = pygame.time.Clock()
    
    # Creamos 5 objetos asteroide reusando la Clase Asteroide
    lista_asteroides = [Asteroide(pantalla.get_width()) for _ in range(5)]
    asteroides_destruidos = 0
    objetivo = 10
    
    jugando = True
    while jugando:
        pantalla.blit(fondo, (0, 0))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False  # Cierra el juego
                
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_mouse = evento.pos
                for asteroide in lista_asteroides:
                    if asteroide.fue_cliqueado(pos_mouse):
                        asteroide.resetear()
                        asteroides_destruidos += 1

        # Actualizar y dibujar cada asteroide
        for asteroide in lista_asteroides:
            asteroide.actualizar(pantalla.get_height())
            pantalla.blit(imagen_asteroide, (asteroide.x, asteroide.y))

        # Evaluar condición de victoria
        if asteroides_destruidos >= objetivo:
            return True  # Misión completada con éxito

        pygame.display.flip()
        reloj.tick(60)