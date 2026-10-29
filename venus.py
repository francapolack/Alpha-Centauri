# venus.py
import pygame

class NivelVenus:
    def __init__(self, assets, animaciones, factor_escala, alto_mapa):
        self.assets = assets
        self.animaciones = animaciones
        self.factor_escala = factor_escala
        self.alto_mapa = alto_mapa
        
        self.destino_pendiente = None 
        
        self.fondo_original = (
            assets.get("planeta_venus") or 
            assets.get("planeta venus") or 
            assets.get("venus")
        )
        
        # Posición inicial del jugador más abajo (sobre el suelo)
        self.x_jugador = 200
        self.y_jugador = 520
        self.direccion = "derecha"
        self.contador_pasos = 0
        
        self.img_alien_grande = assets.get("alien")
        
        # Objetos colocados en la zona del suelo
        self.objetos = [
            {
                "id": "alien",
                "nombre": "Criatura de Venus",
                "x": 650,
                "y": 480,
                "ancho": 90,
                "alto": 110,
                "img": assets.get("minialien"),
                "tipo": "trivia",
                "pregunta": "¿Cuál es la temperatura aproximada en la superficie de Venus?",
                "opciones": ["A) 100°C", "B) 460°C", "C) 800°C"],
                "respuesta_correcta": 1, # Opción B
                "estado_trivia": "preguntando"
            },
            {
                "id": "terminal",
                "nombre": "Terminal de Datos",
                "x": 380,
                "y": 510,
                "ancho": 60,
                "alto": 60,
                "img": None, # Cuadrado interactivo con pista
                "tipo": "simple",
                "mensaje": "REGISTRO TÉCNICO: La atmósfera densa retiene tanto calor que el plomo se fundiría fácilmente aquí."
            }
        ]
        
        self.objeto_activo = None
        self.mensaje_actual = ""
        self.mostrar_mensaje = False

    def manejar_eventos(self, event, pos_mouse, sonido_click):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.destino_pendiente = "finalizar"
            elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                if self.mostrar_mensaje:
                    if self.objeto_activo and self.objeto_activo["tipo"] == "trivia" and self.objeto_activo["estado_trivia"] in ["correcto", "incorrecto"]:
                        self.mostrar_mensaje = False
                        self.objeto_activo = None
                    elif not self.objeto_activo or self.objeto_activo["tipo"] == "simple":
                        self.mostrar_mensaje = False
                        self.objeto_activo = None
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_a, pygame.K_b, pygame.K_c]:
                if self.mostrar_mensaje and self.objeto_activo and self.objeto_activo["tipo"] == "trivia":
                    seleccion = -1
                    if event.key in [pygame.K_1, pygame.K_a]: seleccion = 0
                    elif event.key in [pygame.K_2, pygame.K_b]: seleccion = 1
                    elif event.key in [pygame.K_3, pygame.K_c]: seleccion = 2
                    
                    if seleccion != -1:
                        if sonido_click: sonido_click.play()
                        if seleccion == self.objeto_activo["respuesta_correcta"]:
                            self.objeto_activo["estado_trivia"] = "correcto"
                            self.mensaje_actual = "Alien: ¡EXCELLENT! Correcto. Tienes el pase libre."
                        else:
                            self.objeto_activo["estado_trivia"] = "incorrecto"
                            self.mensaje_actual = "Alien: Incorrecto humano. Revisa la terminal y prueba de nuevo."
            elif event.key == pygame.K_e:
                self.verificar_interaccion(sonido_click)
                
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.mostrar_mensaje:
                if self.objeto_activo and self.objeto_activo["tipo"] == "trivia" and self.objeto_activo["estado_trivia"] in ["correcto", "incorrecto"]:
                    self.mostrar_mensaje = False
                    self.objeto_activo = None
                elif not self.objeto_activo or self.objeto_activo["tipo"] == "simple":
                    self.mostrar_mensaje = False
                    self.objeto_activo = None
            else:
                for obj in self.objetos:
                    rect_obj = pygame.Rect(obj["x"], obj["y"], obj["ancho"], obj["alto"])
                    if rect_obj.collidepoint(pos_mouse):
                        dist = ((self.x_jugador - obj["x"])**2 + (self.y_jugador - obj["y"])**2)**0.5
                        if dist < 180:
                            if sonido_click: sonido_click.play()
                            self.objeto_activo = obj
                            if obj["tipo"] == "trivia":
                                obj["estado_trivia"] = "preguntando"
                                self.mensaje_actual = obj["pregunta"]
                            else:
                                self.mensaje_actual = obj["mensaje"]
                            self.mostrar_mensaje = True

    def verificar_interaccion(self, sonido_click):
        for obj in self.objetos:
            dist = ((self.x_jugador - obj["x"])**2 + (self.y_jugador - obj["y"])**2)**0.5
            if dist < 150:
                if sonido_click: sonido_click.play()
                self.objeto_activo = obj
                if obj["tipo"] == "trivia":
                    obj["estado_trivia"] = "preguntando"
                    self.mensaje_actual = obj["pregunta"]
                else:
                    self.mensaje_actual = obj["mensaje"]
                self.mostrar_mensaje = True
                return

    def actualizar(self, keys, w, h):
        if self.mostrar_mensaje:
            return

        esta_moviendose = False
        vel = 5

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

        # Delimitamos el movimiento en la zona del suelo de la pantalla
        self.x_jugador = max(20, min(self.x_jugador, w - 80))
        self.y_jugador = max(420, min(self.y_jugador, h - 90))

    def dibujar(self, pantalla, pos_mouse):
        w, h = pantalla.get_size()

        # Renderizar fondo
        if self.fondo_original:
            fondo_escalado = pygame.transform.smoothscale(self.fondo_original, (w, h))
            pantalla.blit(fondo_escalado, (0, 0))
        else:
            pantalla.fill((120, 50, 20))

        # Renderizar Objetos e Indicadores
        fuente_ui = pygame.font.SysFont("Consolas", 14, bold=True)
        for obj in self.objetos:
            if obj["img"]:
                img_obj = pygame.transform.smoothscale(obj["img"], (obj["ancho"], obj["alto"]))
                pantalla.blit(img_obj, (obj["x"], obj["y"]))
            else:
                # Dibujar terminal / objeto interactivo con mejor diseño
                pygame.draw.rect(pantalla, (230, 90, 40), (obj["x"], obj["y"], obj["ancho"], obj["alto"]), border_radius=6)
                pygame.draw.rect(pantalla, (255, 200, 100), (obj["x"], obj["y"], obj["ancho"], obj["alto"]), width=2, border_radius=6)

            dist = ((self.x_jugador - obj["x"])**2 + (self.y_jugador - obj["y"])**2)**0.5
            if dist < 150:
                txt_prompt = fuente_ui.render(f"[ E ] {obj['nombre']}", True, (255, 255, 100))
                pantalla.blit(txt_prompt, (obj["x"] - 10, obj["y"] - 25))

        # Renderizar Jugador
        img_adelante = self.animaciones["adelante"]
        img_atras = self.animaciones["atras"]
        img_adelante_espejo = self.animaciones["adelante_espejo"]
        img_atras_espejo = self.animaciones["atras_espejo"]
        img_derecha_1 = self.animaciones["derecha_1"]
        img_derecha_2 = self.animaciones["derecha_2"]
        img_izquierda_1 = self.animaciones["izquierda_1"]
        img_izquierda_2 = self.animaciones["izquierda_2"]

        if self.direccion == "adelante":
            img_actual = img_adelante_espejo if (self.contador_pasos // 10) % 2 == 0 else img_adelante
        elif self.direccion == "atras":
            img_actual = img_atras_espejo if (self.contador_pasos // 10) % 2 == 0 else img_atras
        elif self.direccion == "derecha":
            img_actual = img_derecha_1 if (self.contador_pasos // 10) % 2 == 0 else img_derecha_2
        elif self.direccion == "izquierda":
            img_actual = img_izquierda_1 if (self.contador_pasos // 10) % 2 == 0 else img_izquierda_2

        pantalla.blit(img_actual, (self.x_jugador, self.y_jugador))

        # Dibujar Alien Grande corregido (sin espejar al revés para que mire hacia la izquierda) y bien apoyado abajo
        if self.mostrar_mensaje and self.objeto_activo and self.objeto_activo["id"] == "alien":
            if self.img_alien_grande:
                alt_al = int(h * 0.55)
                anc_al = int(self.img_alien_grande.get_width() * (alt_al / self.img_alien_grande.get_height()))
                alien_scaled = pygame.transform.smoothscale(self.img_alien_grande, (anc_al, alt_al))
                # Quitamos el flip para que mire hacia el centro/izquierda correctamente
                alien_rect = alien_scaled.get_rect(bottomright=(w - 40, h - 145))
                pantalla.blit(alien_scaled, alien_rect)
                
                fuente_tag = pygame.font.SysFont("Consolas", 16, bold=True)
                tag_txt = fuente_tag.render("CRIATURA DE VENUS", True, (255, 200, 100))
                pantalla.blit(tag_txt, (alien_rect.centerx - 60, alien_rect.top - 25))

        # Cuadro de diálogo y Trivia con mejor espaciado vertical
        if self.mostrar_mensaje:
            caja = pygame.Rect(30, h - 165, w - 60, 145)
            pygame.draw.rect(pantalla, (15, 15, 35), caja, border_radius=10)
            pygame.draw.rect(pantalla, (255, 140, 0), caja, width=3, border_radius=10)
            
            fuente_msg = pygame.font.SysFont("Consolas", 15, bold=True)
            render_msg = fuente_msg.render(self.mensaje_actual, True, (255, 255, 255))
            pantalla.blit(render_msg, (caja.x + 25, caja.y + 18))
            
            if self.objeto_activo and self.objeto_activo["tipo"] == "trivia" and self.objeto_activo["estado_trivia"] == "preguntando":
                fuente_opt = pygame.font.SysFont("Consolas", 15, bold=True)
                for i, opcion in enumerate(self.objeto_activo["opciones"]):
                    txt_opt = fuente_opt.render(f"[{i+1}] {opcion}", True, (100, 240, 255))
                    pantalla.blit(txt_opt, (caja.x + 35, caja.y + 48 + (i * 26)))
                
                fuente_sub = pygame.font.SysFont("Consolas", 12)
                render_sub = fuente_sub.render("Presioná [ 1 ], [ 2 ] o [ 3 ] para responder", True, (180, 180, 190))
                pantalla.blit(render_sub, (caja.right - 320, caja.bottom - 25))
            else:
                fuente_sub = pygame.font.SysFont("Consolas", 12)
                render_sub = fuente_sub.render("[ Presioná ENTER o Click para continuar | ESC para volver ]", True, (180, 180, 190))
                pantalla.blit(render_sub, (caja.right - 420, caja.bottom - 25))

