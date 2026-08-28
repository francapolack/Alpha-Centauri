# venus.py
import pygame
import random

class NivelVenus:
    def __init__(self, assets, animaciones, factor_escala, alto_astro):
        self.assets = assets
        self.animaciones = animaciones
        self.FACTOR_ESCALA = factor_escala
        self.ALTO_ASTRO = alto_astro

        # Configuración de mapa
        self.mapa_base = assets.get("planeta_venus")
        if self.mapa_base is None:
            self.mapa_base = pygame.Surface((1200, 800))
            self.mapa_base.fill((180, 100, 30))

        self.ANCHO_MUNDO = int(self.mapa_base.get_width() * self.FACTOR_ESCALA)
        self.ALTO_MUNDO = int(self.mapa_base.get_height() * self.FACTOR_ESCALA)

        # Posición inicial del astronauta en el suelo
        self.x_jugador = int(self.ANCHO_MUNDO * 0.10)
        self.y_jugador = int(self.ALTO_MUNDO * 0.75)
        self.direccion = "derecha"
        self.contador_pasos = 0

        # Posición del Alien en Venus
        self.x_alien = int(self.ANCHO_MUNDO * 0.82)
        self.y_alien = int(self.ALTO_MUNDO * 0.70)

        # Definición de los 5 Objetos Científicos en el Terreno
        self.objetos = [
            {
                "rect": pygame.Rect(int(self.ANCHO_MUNDO * 0.22), int(self.ALTO_MUNDO * 0.76), 45, 45),
                "nombre": "Sonda Destruida",
                "dato": "1. Venus es el planeta más caliente (~465°C) por su efecto invernadero extremo.",
                "visto": False
            },
            {
                "rect": pygame.Rect(int(self.ANCHO_MUNDO * 0.38), int(self.ALTO_MUNDO * 0.72), 45, 45),
                "nombre": "Cristal de Ácido",
                "dato": "2. Las densas nubes venusianas están compuestas de ácido sulfúrico.",
                "visto": False
            },
            {
                "rect": pygame.Rect(int(self.ANCHO_MUNDO * 0.52), int(self.ALTO_MUNDO * 0.78), 45, 45),
                "nombre": "Barómetro Piezométrico",
                "dato": "3. La presión en la superficie de Venus es 90 veces superior a la de la Tierra.",
                "visto": False
            },
            {
                "rect": pygame.Rect(int(self.ANCHO_MUNDO * 0.66), int(self.ALTO_MUNDO * 0.74), 45, 45),
                "nombre": "Reloj de Rotación",
                "dato": "4. Un día en Venus (243 días terrestres) dura más tiempo que su año (225 días).",
                "visto": False
            },
            {
                "rect": pygame.Rect(int(self.ANCHO_MUNDO * 0.75), int(self.ALTO_MUNDO * 0.78), 45, 45),
                "nombre": "Brújula Invertida",
                "dato": "5. Venus posee rotación retrógrada: gira en sentido opuesto a la mayoría de planetas.",
                "visto": False
            }
        ]

        self.objeto_activo = None

        # Banco de 5 Preguntas basadas en los 5 objetos
        self.preguntas = [
            {
                "pregunta": "¿Cuál es la causa del calor extremo (~465°C) en Venus?",
                "opciones": ["Su cercanía directa al Sol", "Efecto invernadero extremo", "Volcanes de plasma ininterrumpidos"],
                "correcta": 1
            },
            {
                "pregunta": "¿De qué están compuestas principalmente sus densas nubes?",
                "opciones": ["Ácido sulfúrico", "Dióxido de carbono líquido", "Vapor de agua hirviendo"],
                "correcta": 0
            },
            {
                "pregunta": "¿Cómo es la presión atmosférica venusiana respecto a la Tierra?",
                "opciones": ["10 veces menor", "50 veces mayor", "90 veces mayor"],
                "correcta": 2
            },
            {
                "pregunta": "¿Qué relación existe entre la duración de un día y un año en Venus?",
                "opciones": ["Un día dura más que un año", "Un día dura 12 horas", "Tienen exactamente la misma duración"],
                "correcta": 0
            },
            {
                "pregunta": "¿En qué sentido realiza Venus su movimiento de rotación?",
                "opciones": ["No gira sobre su eje", "En sentido opuesto a la mayoría (retrógrada)", "De norte a sur"],
                "correcta": 1
            }
        ]

        # Estados internos: 'exploracion', 'cinematica', 'trivia', 'completado'
        self.subestado = "exploracion"
        self.pregunta_actual = 0
        self.puntaje = 0

        # Control de transición
        self.transicion_activa = False
        self.transicion_alfa = 0
        self.transicion_modo = "ninguno"
        self.destino_pendiente = None

        # Texto cinemático
        self.texto_intro_alien = "Zylor: ¡Bienvenido a Venus, viajero! Demuestra que aprendiste sobre nuestro planeta."
        self.caracteres_vistos = 0
        self.conteo_frames = 0

    def manejar_eventos(self, event, pos_mouse, sonido_click):
        if self.subestado == "exploracion" and not self.transicion_activa:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Clic en objeto interactivo
                camara_x, camara_y = self.obtener_camara(pos_mouse[0], pos_mouse[1])
                pos_mundo = (pos_mouse[0] + camara_x, pos_mouse[1] + camara_y)
                
                for obj in self.objetos:
                    if obj["rect"].collidepoint(pos_mundo):
                        if sonido_click: sonido_click.play()
                        self.objeto_activo = obj
                        obj["visto"] = True
                        return

                if self.objeto_activo:
                    self.objeto_activo = None

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                # Interactuar con el Alien al presionar 'E'
                dist_alien = ((self.x_jugador - self.x_alien)**2 + (self.y_jugador - self.y_alien)**2)**0.5
                if dist_alien < 110:
                    self.iniciar_transicion("cinematica")

        elif self.subestado == "cinematica" and not self.transicion_activa:
            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]:
                if self.caracteres_vistos < len(self.texto_intro_alien):
                    self.caracteres_vistos = len(self.texto_intro_alien)
                else:
                    if sonido_click: sonido_click.play()
                    self.subestado = "trivia"
                    self.pregunta_actual = 0
                    self.puntaje = 0

        elif self.subestado == "trivia":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                idx_opcion = self.obtener_opcion_cliqueada(pos_mouse)
                if idx_opcion is not None:
                    if sonido_click: sonido_click.play()
                    if idx_opcion == self.preguntas[self.pregunta_actual]["correcta"]:
                        self.puntaje += 1

                    self.pregunta_actual += 1
                    if self.pregunta_actual >= len(self.preguntas):
                        self.subestado = "completado"

        elif self.subestado == "completado":
            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]:
                if sonido_click: sonido_click.play()
                self.iniciar_transicion("finalizar")

    def actualizar(self, keys, w_pantalla, h_pantalla):
        # Actualización del fundido a negro
        if self.transicion_activa:
            if self.transicion_modo == "out":
                self.transicion_alfa += 14
                if self.transicion_alfa >= 255:
                    self.transicion_alfa = 255
                    self.subestado = self.destino_pendiente
                    self.transicion_modo = "in"
                    self.caracteres_vistos = 0
            elif self.transicion_modo == "in":
                self.transicion_alfa -= 14
                if self.transicion_alfa <= 0:
                    self.transicion_alfa = 0
                    self.transicion_activa = False

        # Movimiento de exploración en el terreno de Venus
        if self.subestado == "exploracion" and not self.transicion_activa:
            esta_moviendose = False
            vel = 4

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.x_jugador -= vel
                self.direccion = "izquierda"
                esta_moviendose = True
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.x_jugador += vel
                self.direccion = "derecha"
                esta_moviendose = True

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.y_jugador -= vel
                self.direccion = "atras"
                esta_moviendose = True
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.y_jugador += vel
                self.direccion = "adelante"
                esta_moviendose = True

            if esta_moviendose:
                self.contador_pasos += 1
            else:
                self.contador_pasos = 0

            # Restricciones de movimiento en la franja del suelo
            min_y = int(self.ALTO_MUNDO * 0.65)
            max_y = int(self.ALTO_MUNDO * 0.88)
            self.x_jugador = max(0, min(self.x_jugador, self.ANCHO_MUNDO - 40))
            self.y_jugador = max(min_y, min(self.y_jugador, max_y))

    def iniciar_transicion(self, destino):
        self.transicion_activa = True
        self.transicion_alfa = 0
        self.transicion_modo = "out"
        self.destino_pendiente = destino

    def obtener_camara(self, w_act, h_act):
        camara_x = self.x_jugador - w_act // 2
        camara_y = self.y_jugador - h_act // 2
        camara_x = max(0, min(camara_x, self.ANCHO_MUNDO - w_act))
        camara_y = max(0, min(camara_y, self.ALTO_MUNDO - h_act))
        return camara_x, camara_y

    def dibujar(self, screen, pos_mouse):
        W_ACT, H_ACT = screen.get_size()
        camara_x, camara_y = self.obtener_camara(W_ACT, H_ACT)

        # 1. Dibujar escenario
        mapa_escalado = pygame.transform.smoothscale(self.mapa_base, (self.ANCHO_MUNDO, self.ALTO_MUNDO))
        screen.blit(mapa_escalado, (-camara_x, -camara_y))

        # 2. Dibujar 5 objetos científicos en el mundo y actualizar cursor si hay hover
        hay_hover = False
        pos_mundo_mouse = (pos_mouse[0] + camara_x, pos_mouse[1] + camara_y)

        for i, obj in enumerate(self.objetos):
            r = obj["rect"]
            r_pantalla = pygame.Rect(r.x - camara_x, r.y - camara_y, r.width, r.height)
            
            color_base = (0, 220, 255) if obj["visto"] else (255, 200, 50)
            pygame.draw.rect(screen, color_base, r_pantalla, border_radius=6)
            pygame.draw.rect(screen, (255, 255, 255), r_pantalla, width=2, border_radius=6)

            # Icono numerado en el objeto
            fuente_num = pygame.font.SysFont("Consolas", 16, bold=True)
            txt_num = fuente_num.render(str(i + 1), True, (10, 10, 20))
            screen.blit(txt_num, txt_num.get_rect(center=r_pantalla.center))

            if r_pantalla.collidepoint(pos_mouse):
                hay_hover = True

        # 3. Dibujar Alien en el terreno
        r_alien_pantalla = pygame.Rect(self.x_alien - camara_x, self.y_alien - camara_y, 50, 70)
        if self.assets.get("minialien"):
            img_alien = pygame.transform.smoothscale(self.assets["minialien"], (50, 70))
            screen.blit(img_alien, r_alien_pantalla)
        else:
            pygame.draw.ellipse(screen, (80, 220, 100), r_alien_pantalla)
            pygame.draw.circle(screen, (255, 255, 255), (r_alien_pantalla.centerx - 8, r_alien_pantalla.y + 20), 5)
            pygame.draw.circle(screen, (255, 255, 255), (r_alien_pantalla.centerx + 8, r_alien_pantalla.y + 20), 5)

        if r_alien_pantalla.collidepoint(pos_mouse):
            hay_hover = True

        # Aplicar el cambio de cursor según si pasa por encima de un objeto interactivo
        if hay_hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Indicador para interactuar con el alien
        dist_alien = ((self.x_jugador - self.x_alien)**2 + (self.y_jugador - self.y_alien)**2)**0.5
        if dist_alien < 110 and self.subestado == "exploracion":
            fuente_e = pygame.font.SysFont("Consolas", 14, bold=True)
            txt_e = fuente_e.render("[Presioná E para hablar con Zylor]", True, (255, 255, 255))
            screen.blit(txt_e, (self.x_alien - camara_x - 40, self.y_alien - camara_y - 25))

        # 4. Dibujar Jugador
        img_adelante = self.animaciones["adelante"]
        img_atras = self.animaciones["atras"]
        img_adelante_e = self.animaciones["adelante_espejo"]
        img_atras_e = self.animaciones["atras_espejo"]
        img_der1 = self.animaciones["derecha_1"]
        img_der2 = self.animaciones["derecha_2"]
        img_izq1 = self.animaciones["izquierda_1"]
        img_izq2 = self.animaciones["izquierda_2"]

        if self.direccion == "adelante":
            img_actual = img_adelante if (self.contador_pasos // 14) % 2 == 0 else img_adelante_e
        elif self.direccion == "atras":
            img_actual = img_atras if (self.contador_pasos // 14) % 2 == 0 else img_atras_e
        elif self.direccion == "derecha":
            img_actual = img_der1 if (self.contador_pasos // 14) % 2 == 0 else img_der2
        elif self.direccion == "izquierda":
            img_actual = img_izq1 if (self.contador_pasos // 14) % 2 == 0 else img_izq2

        screen.blit(img_actual, (self.x_jugador - camara_x, self.y_jugador - camara_y))

        # Popup emergente al inspeccionar un objeto
        if self.objeto_activo and self.subestado == "exploracion":
            caja_pop = pygame.Rect(0, 0, int(W_ACT * 0.70), 90)
            caja_pop.center = (W_ACT // 2, H_ACT - 70)
            pygame.draw.rect(screen, (20, 25, 40), caja_pop, border_radius=8)
            pygame.draw.rect(screen, (0, 220, 255), caja_pop, width=2, border_radius=8)

            f_tit = pygame.font.SysFont("Consolas", 15, bold=True)
            f_body = pygame.font.SysFont("Consolas", 13)

            t_tit = f_tit.render(f"REGISTRO CIENTÍFICO: {self.objeto_activo['nombre']}", True, (255, 200, 50))
            t_body = f_body.render(self.objeto_activo["dato"], True, (240, 240, 255))

            screen.blit(t_tit, (caja_pop.x + 20, caja_pop.y + 15))
            screen.blit(t_body, (caja_pop.x + 20, caja_pop.y + 48))

        # 5. Interfaz de Cinemática / Diálogo con Zylor
        if self.subestado == "cinematica":
            self.dibujar_cinematica_alien(screen, W_ACT, H_ACT)

        # 6. Interfaz de Cuestionario (Trivia de 5 Preguntas)
        elif self.subestado == "trivia":
            self.dibujar_trivia(screen, W_ACT, H_ACT, pos_mouse)

        # 7. Interfaz de Resultado Final
        elif self.subestado == "completado":
            self.dibujar_resultado(screen, W_ACT, H_ACT)

        # Capa de Fundido
        if self.transicion_activa or self.transicion_alfa > 0:
            surf_fade = pygame.Surface((W_ACT, H_ACT), pygame.SRCALPHA)
            surf_fade.fill((0, 0, 0, self.transicion_alfa))
            screen.blit(surf_fade, (0, 0))

    def dibujar_cinematica_alien(self, screen, W_ACT, H_ACT):
        capa_oscura = pygame.Surface((W_ACT, H_ACT))
        capa_oscura.fill((0, 0, 0))
        capa_oscura.set_alpha(150)
        screen.blit(capa_oscura, (0, 0))

        # Retrato de Zylor (Alien)
        if self.assets.get("alien"):
            img_a = pygame.transform.smoothscale(self.assets["alien"], (int(W_ACT * 0.25), int(H_ACT * 0.60)))
            screen.blit(img_a, (W_ACT * 0.68, H_ACT * 0.25))
        else:
            pygame.draw.ellipse(screen, (80, 220, 100), (int(W_ACT * 0.70), int(H_ACT * 0.30), 180, 240))

        caja = pygame.Rect(int(W_ACT * 0.05), int(H_ACT * 0.68), int(W_ACT * 0.90), int(H_ACT * 0.24))
        pygame.draw.rect(screen, (20, 20, 35), caja, border_radius=8)
        pygame.draw.rect(screen, (80, 220, 100), caja, width=3, border_radius=8)

        f_txt = pygame.font.SysFont("Consolas", 18, bold=True)
        self.conteo_frames += 1
        if self.conteo_frames % 2 == 0 and self.caracteres_vistos < len(self.texto_intro_alien):
            self.caracteres_vistos += 1

        t_render = f_txt.render(self.texto_intro_alien[:self.caracteres_vistos], True, (255, 255, 255))
        screen.blit(t_render, (caja.x + 25, caja.y + 35))

        f_sub = pygame.font.SysFont("Consolas", 13)
        t_sub = f_sub.render("[ Clic o ENTER para empezar la Trivia ]", True, (80, 220, 100))
        screen.blit(t_sub, (caja.right - 320, caja.bottom - 25))

    def dibujar_trivia(self, screen, W_ACT, H_ACT, pos_mouse):
        panel = pygame.Rect(int(W_ACT * 0.10), int(H_ACT * 0.10), int(W_ACT * 0.80), int(H_ACT * 0.80))
        pygame.draw.rect(screen, (25, 28, 45), panel, border_radius=12)
        pygame.draw.rect(screen, (0, 220, 200), panel, width=3, border_radius=12)

        p = self.preguntas[self.pregunta_actual]

        f_tit = pygame.font.SysFont("Consolas", 18, bold=True)
        t_tit = f_tit.render(f"EVALUACIÓN DE VENUS - PREGUNTA {self.pregunta_actual + 1} DE 5", True, (255, 200, 50))
        screen.blit(t_tit, (panel.x + 30, panel.y + 30))

        f_preg = pygame.font.SysFont("Consolas", 16)
        t_preg = f_preg.render(p["pregunta"], True, (255, 255, 255))
        screen.blit(t_preg, (panel.x + 30, panel.y + 80))

        for i, opc in enumerate(p["opciones"]):
            r_opc = self.obtener_rect_opcion(panel, i)
            es_hover = r_opc.collidepoint(pos_mouse)

            color_bg = (40, 60, 90) if es_hover else (30, 35, 55)
            color_borde = (0, 255, 200) if es_hover else (100, 110, 130)

            pygame.draw.rect(screen, color_bg, r_opc, border_radius=6)
            pygame.draw.rect(screen, color_borde, r_opc, width=2, border_radius=6)

            txt_o = f_preg.render(f"{chr(65+i)})  {opc}", True, (240, 240, 255))
            screen.blit(txt_o, (r_opc.x + 20, r_opc.y + 15))

    def obtener_rect_opcion(self, panel, idx):
        y_base = panel.y + 140 + idx * 65
        return pygame.Rect(panel.x + 30, y_base, panel.width - 60, 50)

    def obtener_opcion_cliqueada(self, pos_mouse):
        W_ACT, H_ACT = pygame.display.get_surface().get_size()
        panel = pygame.Rect(int(W_ACT * 0.10), int(H_ACT * 0.10), int(W_ACT * 0.80), int(H_ACT * 0.80))
        for i in range(3):
            if self.obtener_rect_opcion(panel, i).collidepoint(pos_mouse):
                return i
        return None

    def dibujar_resultado(self, screen, W_ACT, H_ACT):
        panel = pygame.Rect(int(W_ACT * 0.15), int(H_ACT * 0.20), int(W_ACT * 0.70), int(H_ACT * 0.60))
        pygame.draw.rect(screen, (20, 25, 40), panel, border_radius=12)
        pygame.draw.rect(screen, (0, 255, 150), panel, width=3, border_radius=12)

        f_t = pygame.font.SysFont("Consolas", 22, bold=True)
        f_b = pygame.font.SysFont("Consolas", 16)

        txt_t = f_t.render("¡MISIÓN EN VENUS COMPLETADA!", True, (0, 255, 150))
        txt_res = f_b.render(f"Respuestas Correctas: {self.puntaje} / 5", True, (255, 255, 255))

        msg_alien = "Zylor: ¡Increíble! Eres un verdadero aliado intergaláctico." if self.puntaje >= 3 else "Zylor: Has aprendido lo básico. Podemos continuar la expedición."
        txt_ali = f_b.render(msg_alien, True, (255, 220, 100))

        screen.blit(txt_t, txt_t.get_rect(centerx=panel.centerx, top=panel.y + 40))
        screen.blit(txt_res, txt_res.get_rect(centerx=panel.centerx, top=panel.y + 110))
        screen.blit(txt_ali, txt_ali.get_rect(centerx=panel.centerx, top=panel.y + 160))

        f_s = pygame.font.SysFont("Consolas", 13)
        txt_c = f_s.render("[ Presioná ENTER o hacé Clic para continuar ]", True, (150, 150, 160))
        screen.blit(txt_c, txt_c.get_rect(centerx=panel.centerx, bottom=panel.bottom - 25))