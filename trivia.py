import pygame

class TriviaPantalla:
    def __init__(self):
        # Generación de avatares seguros mediante superficies (puedes cambiarlos por pygame.image.load)
        self.alien_img = pygame.Surface((100, 100))
        self.alien_img.fill((50, 200, 50)) # Alien verde
        
        self.usuario_img = pygame.Surface((100, 100))
        self.usuario_img.fill((50, 150, 255)) # Usuario azul

        # Banco de preguntas asociadas a los hallazgos de Venus
        self.preguntas = [
            {
                "pregunta": "¿Qué indica el análisis del termómetro crítico sobre Venus?",
                "opciones": ["Altas temperaturas extremas", "Bajas temperaturas bajo cero", "Clima templado y estable"],
                "correcta": 0
            },
            {
                "pregunta": "¿Qué tipo de muestra contiene el tubo atmosférico?",
                "opciones": ["Agua líquida pura", "Gases de efecto invernadero y ácido", "Minerales magnéticos puros"],
                "correcta": 1
            },
            {
                "pregunta": "¿Qué particularidad tiene la rama de flora analizada?",
                "opciones": ["Posee estructuras de cristal defensivas", "Es idéntica a los árboles terrestres", "Es una planta carnívora gigante"],
                "correcta": 0
            }
        ]
        
        self.indice_actual = 0
        self.puntaje = 0
        self.respondido = False
        self.seleccion_usuario = None
        self.terminado = False
        self.botones_opciones = []

    def dibujar(self, pantalla):
        w, h = pantalla.get_size()
        pantalla.fill((25, 25, 40)) # Fondo estilo panel de juego
        
        # Dibujar personajes a los costados
        pantalla.blit(self.alien_img, (60, 220))
        txt_al = pygame.font.SysFont("Consolas", 16, bold=True).render("Alien de Venus", True, (255, 255, 255))
        pantalla.blit(txt_al, (50, 330))

        pantalla.blit(self.usuario_img, (w - 160, 220))
        txt_us = pygame.font.SysFont("Consolas", 16, bold=True).render("Tripulante", True, (255, 255, 255))
        pantalla.blit(txt_us, (w - 160, 330))
        
        fuente = pygame.font.SysFont("Consolas", 20, bold=True)
        
        if not self.terminado:
            p_actual = self.preguntas[self.indice_actual]
            
            # Caja de Pregunta (Arriba al centro)
            rect_preg = pygame.Rect(w//2 - 350, 70, 700, 80)
            pygame.draw.rect(pantalla, (20, 80, 130), rect_preg, border_radius=12)
            pygame.draw.rect(pantalla, (0, 200, 255), rect_preg, width=3, border_radius=12)
            
            # Texto ajustado de la pregunta
            txt_p = fuente.render(p_actual["pregunta"], True, (255, 255, 255))
            pantalla.blit(txt_p, (rect_preg.x + 25, rect_preg.y + 28))
            
            # Opciones de respuesta abajo
            self.botones_opciones = []
            for i, opcion in enumerate(p_actual["opciones"]):
                rect_op = pygame.Rect(w//2 - 300, 180 + (i * 90), 600, 70)
                
                # Colores dinámicos (Verde si es correcta, Rojo si se equivocó)
                color_fondo = (45, 45, 65)
                if self.respondido:
                    if i == p_actual["correcta"]:
                        color_fondo = (0, 160, 0) # Verde éxito
                    elif i == self.seleccion_usuario:
                        color_fondo = (180, 0, 0) # Rojo error
                
                pygame.draw.rect(pantalla, color_fondo, rect_op, border_radius=10)
                pygame.draw.rect(pantalla, (200, 200, 200), rect_op, width=2, border_radius=10)
                
                txt_o = fuente.render(opcion, True, (255, 255, 255))
                pantalla.blit(txt_o, (rect_op.x + 25, rect_op.y + 22))
                
                self.botones_opciones.append((rect_op, i))
                
            if self.respondido:
                txt_sig = pygame.font.SysFont("Consolas", 18, bold=True).render("Hacé clic en cualquier lado para continuar...", True, (255, 255, 0))
                pantalla.blit(txt_sig, (w//2 - txt_sig.get_width()//2, 530))
        else:
            # Pantalla final de la trivia
            txt_fin = pygame.font.SysFont("Consolas", 28, bold=True).render(f"¡Trivia finalizada! Aciertos: {self.puntaje}/{len(self.preguntas)}", True, (255, 255, 255))
            txt_salir = pygame.font.SysFont("Consolas", 20).render("Hacé clic para volver al planeta.", True, (180, 180, 220))
            
            pantalla.blit(txt_fin, (w//2 - txt_fin.get_width()//2, h//2 - 30))
            pantalla.blit(txt_salir, (w//2 - txt_salir.get_width()//2, h//2 + 20))

    def manejar_clic(self, pos):
        if self.terminado:
            return True # Devuelve True para cerrar la trivia y volver a Venus
            
        if self.respondido:
            # Pasa a la siguiente pregunta después de haber respondido la anterior
            self.respondido = False
            self.indice_actual += 1
            if self.indice_actual >= len(self.preguntas):
                self.terminado = True
            return False

        # Verificar clics en las opciones
        for rect, i in self.botones_opciones:
            if rect.collidepoint(pos):
                self.seleccion_usuario = i
                self.respondido = True
                if i == self.preguntas[self.indice_actual]["correcta"]:
                    self.puntaje += 1
        return False