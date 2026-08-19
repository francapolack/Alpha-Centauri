import pygame
import os
import sys
import random
from pyvidplayer2 import Video 
from clases_funciones import aplicar_filtro_oscuro,cargar_img_mapa, os_join

def main():
    pygame.init()
    pygame.mixer.init()

    #CONSTANTES
    ANCHO_PANTALLA = 1000
    ALTO_PANTALLA = 600
    ALTO_MAPA_ASTRO = 58 
    screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.RESIZABLE)
    pygame.display.set_caption("Alpha Centauri")
    
    clock = pygame.time.Clock()
    carpeta_actual = os.path.dirname(__file__)

    # 2. AUDIO
    fondo_musica=os_join(carpeta_actual,"musica_menu.mp3")
    if os_join:
        pygame.mixer.music.load(fondo_musica)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    
    ruta_click = os.path.join(carpeta_actual, "click.wav")
    sonio_click = None
    if os.path.exists(ruta_click):
        try:
            sonio_click = pygame.mixer.Sound(ruta_click)
        except Exception as e:
            print(f"Advertencia: No se pudo cargar 'click.wav' ({e}). El juego continuará sin sonido de clic.")

    # 3. VIDEO DE MENÚ
    ruta_video_menu = Video(os.path.join(carpeta_actual,"videomenu.mp4"),no_audio=True)
    video_menu = None
    if os.path.exists(ruta_video_menu):
        try:
            video_menu = Video(ruta_video_menu, audio=False)
        except TypeError:
            video_menu = Video(ruta_video_menu)
            video_menu.mute()

    # 4. CARGA DE ASSETS GRÁFICOS
    assets = {}
    nombres_archivos = {
        "fondointro": "fondointro.png",
        "titulo": "titulomenu.png",
        "jugar": "botoninicio.png",
        "salir": "botonsalir.png",
        "astronauta": "astronautito.png",
        "rene": "rene.png",
        "pasillo": "habitaciones.png",
        "pasillo_abierto": "sinpuertas.png", # <- Imagen con las puertas abiertas
        "asteroide": "asteroide.png",
        "controles": "controles.png"
    }
    
    for clave, archivo in nombres_archivos.items():
        ruta = os.path.join(carpeta_actual, "imagenes", archivo)
        if os.path.exists(ruta):
            assets[clave] = pygame.image.load(ruta).convert_alpha()
        else:
            assets[clave] = None

    # 4B. ANIMACIONES DEL ASTRONAUTA
     

    img_adelante = cargar_img_mapa(carpeta_actual,"camina adelante.png",ALTO_MAPA_ASTRO)
    img_atras = cargar_img_mapa(carpeta_actual,"camina atras.png",ALTO_MAPA_ASTRO)
    img_adelante_espejo = pygame.transform.flip(img_adelante, True, False)
    img_atras_espejo = pygame.transform.flip(img_atras, True, False)
    
    img_derecha_1 = cargar_img_mapa("caminapataadelante.png")
    ANCHO_LATERAL_FIJO = img_derecha_1.get_width()
    img_derecha_2 = cargar_img_mapa("caminapataatras.png", ancho_fijo=ANCHO_LATERAL_FIJO)
    
    img_izquierda_1 = pygame.transform.flip(img_derecha_1, True, False)
    img_izquierda_2 = pygame.transform.flip(img_derecha_2, True, False)

    # ESCALADO DEL MAPA MUNDO (Para la cámara)
    FACTOR_ESCALA_MAPA = 1.6
    
    mapa_actual_base = assets["pasillo"] if assets["pasillo"] else pygame.Surface((1200, 800))
    ANCHO_MUNDO = int(mapa_actual_base.get_width() * FACTOR_ESCALA_MAPA)
    ALTO_MUNDO = int(mapa_actual_base.get_height() * FACTOR_ESCALA_MAPA)

    # Coordenadas globales en el mapa del juego
    x_jugador = int(ANCHO_MUNDO * 0.08)
    y_jugador = int(ALTO_MUNDO * 0.52)
    velocidad_jugador = 3.5  
    direccion_jugador = "derecha"
    contador_pasos = 0

    # Posición de René dentro de la habitación superior central (frente a la ventana/puertas abiertas)
    x_rene_mapa = int(ANCHO_MUNDO * 0.53)
    y_rene_mapa = int(ALTO_MUNDO * 0.23)
    mostrar_dialogo_rene = False

    # Variables de cámara
    camara_x = 0
    camara_y = 0

    # Estados
    estado_actual = "menu"
    fase_narrativa = 1  
    opacidad_astronauta = 0
    opacidad_rene = 0   
    nombre_jugador = ""
    
    texto_prologo = "Que pasó?... donde estan mis compañeros de tripulación?"
    texto_rene = "" 
    caracteres_vistos = 0
    conteo_frames = 0
    boton_demo_rect = pygame.Rect(0, 0, 0, 0)
    
    # Temporizador Alarma
    alfa_alarma = 0
    incremento_alarma = 4

    mision_completada = False
    mostrar_cartel_exito = False
    frames_cartel = 0

    # Minijuego
    asteroides = []  
    particulas_fuego = []  
    estrellas_fondo = []   
    
    for _ in range(80):
        estrellas_fondo.append({
            'x': random.randint(0, 1200),
            'y': random.randint(0, 800),
            'vel': random.uniform(0.5, 3.0),
            'tam': random.randint(1, 3)
        })

    asteroides_destruidos = 0
    max_asteroides_mision = 10
    temporizador_spawn = 0

    while True:
        W_ACTUAL, H_ACTUAL = screen.get_size()
        pos_mouse = pygame.mouse.get_pos()
        esta_moviendose = False
        
        texto_rene_completo = "René: ¡Amigo! Porfin te despertaste de esa 'mini siesta', andá al panel de navegación"

        # Cámara seguidora
        camara_x = x_jugador - W_ACTUAL // 2
        camara_y = y_jugador - H_ACTUAL // 2
        camara_x = max(0, min(camara_x, ANCHO_MUNDO - W_ACTUAL))
        camara_y = max(0, min(camara_y, ALTO_MUNDO - H_ACTUAL))

        # Zona de interactuación con la consola de misión
        zona_mision = pygame.Rect(
            int(ANCHO_MUNDO * 0.77), 
            int(ALTO_MUNDO * 0.16), 
            int(ANCHO_MUNDO * 0.15), 
            int(ALTO_MUNDO * 0.22)
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if video_menu: video_menu.close()
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if video_menu: video_menu.close()
                    pygame.quit()
                    sys.exit()

                if estado_actual == "cinematica":
                    if fase_narrativa == 1:
                        if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                            if sonio_click: sonio_click.play()
                            fase_narrativa = 2
                    
                    elif fase_narrativa == 2:
                        if event.key == pygame.K_BACKSPACE:
                            nombre_jugador = nombre_jugador[:-1]
                        elif event.key == pygame.K_RETURN and nombre_jugador.strip() != "":
                            if sonio_click: sonio_click.play()
                            fase_narrativa = 3
                            caracteres_vistos = 0 
                            conteo_frames = 0
                        elif event.unicode.isalnum() and len(nombre_jugador) < 14:
                            nombre_jugador += event.unicode
                            if sonio_click: sonio_click.play()
                            
                    elif fase_narrativa == 3:
                        if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                            if sonio_click: sonio_click.play()
                            fase_narrativa = 4
                            caracteres_vistos = 0
                            conteo_frames = 0

                    elif fase_narrativa == 4:
                        if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                            if sonio_click: sonio_click.play()
                            if caracteres_vistos < len(texto_rene_completo):
                                caracteres_vistos = len(texto_rene_completo)
                            else:
                                estado_actual = "controles"

                elif estado_actual == "controles":
                    if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        if sonio_click: sonio_click.play()
                        estado_actual = "exploracion"

                elif estado_actual == "exploracion" and mision_completada:
                    # Interactuar con René mediante 'E'
                    if event.key == pygame.K_e:
                        dist_rene = ((x_jugador - x_rene_mapa)**2 + (y_jugador - y_rene_mapa)**2)**0.5
                        if dist_rene < 100:
                            mostrar_dialogo_rene = not mostrar_dialogo_rene

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if estado_actual == "menu":
                    if assets["jugar"] and jugar_rect.collidepoint(pos_mouse):
                        if sonio_click: sonio_click.play()
                        if video_menu: video_menu.close()
                        estado_actual = "cinematica"
                        fase_narrativa = 1
                        caracteres_vistos = 0
                        conteo_frames = 0
                        
                    if assets["salir"] and salir_rect.collidepoint(pos_mouse):
                        if sonio_click: sonio_click.play()
                        if video_menu: video_menu.close()
                        pygame.time.wait(300)
                        pygame.quit()
                        sys.exit()

                elif estado_actual == "cinematica" and fase_narrativa == 4:
                    if caracteres_vistos < len(texto_rene_completo):
                        if sonio_click: sonio_click.play()
                        caracteres_vistos = len(texto_rene_completo)
                    elif boton_demo_rect.collidepoint(pos_mouse):
                        if sonio_click: sonio_click.play()
                        estado_actual = "controles"

                elif estado_actual == "controles":
                    if sonio_click: sonio_click.play()
                    estado_actual = "exploracion"

                elif estado_actual == "minijuego_asteroides":
                    for asteroide in asteroides[:]:
                        if asteroide['rect'].collidepoint(pos_mouse):
                            for _ in range(12):
                                particulas_fuego.append({
                                    'x': asteroide['rect'].centerx,
                                    'y': asteroide['rect'].centery,
                                    'vel_x': random.uniform(-4, 4),
                                    'vel_y': random.uniform(-4, 4),
                                    'radio': random.randint(4, 8),
                                    'vida': 25,
                                    'color': random.choice([(255, 200, 50), (255, 80, 20), (100, 100, 100)])
                                })
                            asteroides.remove(asteroide)
                            asteroides_destruidos += 1
                            if sonio_click: sonio_click.play()
                            break

        if estado_actual == "exploracion":
            keys = pygame.key.get_pressed()
            ancho_actual_astro = img_adelante.get_width() if direccion_jugador in ["adelante", "atras"] else ANCHO_LATERAL_FIJO

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                x_jugador -= velocidad_jugador
                direccion_jugador = "izquierda"
                esta_moviendose = True
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                x_jugador += velocidad_jugador
                direccion_jugador = "derecha"
                esta_moviendose = True

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                y_jugador -= velocidad_jugador
                direccion_jugador = "atras"
                esta_moviendose = True
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                y_jugador += velocidad_jugador
                direccion_jugador = "adelante"
                esta_moviendose = True

            if esta_moviendose:
                contador_pasos += 1
            else:
                contador_pasos = 0

            # --- SISTEMA DINÁMICO DE COLISIONES DE PAREDES ---
            Y_MIN_PASILLO = int(ALTO_MUNDO * 0.44)  
            Y_MAX_PASILLO = int(ALTO_MUNDO * 0.54)  

            if not mision_completada:
                # Puertas Cerradas: El jugador no puede salir del pasillo central
                X_ENTRADA_HAB3 = int(ANCHO_MUNDO * 0.74) 
                if x_jugador < X_ENTRADA_HAB3:
                    if y_jugador < Y_MIN_PASILLO: y_jugador = Y_MIN_PASILLO
                    if y_jugador > Y_MAX_PASILLO: y_jugador = Y_MAX_PASILLO
                else:
                    if y_jugador < int(ALTO_MUNDO * 0.12): y_jugador = int(ALTO_MUNDO * 0.12)
                    if y_jugador > Y_MAX_PASILLO: y_jugador = Y_MAX_PASILLO
                    if y_jugador < Y_MIN_PASILLO:
                        if x_jugador < int(ANCHO_MUNDO * 0.70): x_jugador = int(ANCHO_MUNDO * 0.70)
                        if x_jugador > int(ANCHO_MUNDO * 0.93) - ancho_actual_astro: x_jugador = int(ANCHO_MUNDO * 0.93) - ancho_actual_astro
            else:
                # PUERTAS ABIERTAS: Se extienden las fronteras para acceder a las habitaciones superiores e inferiores
                puerta_superior_x = (int(ANCHO_MUNDO * 0.45), int(ANCHO_MUNDO * 0.58))
                puerta_inferior_x = (int(ANCHO_MUNDO * 0.44), int(ANCHO_MUNDO * 0.55))

                # Límite Superior: Permite subida solo por la puerta abierta hacia la sala de René
                if y_jugador < Y_MIN_PASILLO:
                    if x_jugador >= puerta_superior_x[0] and x_jugador <= puerta_superior_x[1]:
                        if y_jugador < int(ALTO_MUNDO * 0.18):
                            y_jugador = int(ALTO_MUNDO * 0.18)
                    else:
                        y_jugador = Y_MIN_PASILLO

                # Límite Inferior: Permite bajada solo por el umbral inferior
                if y_jugador > Y_MAX_PASILLO:
                    if x_jugador >= puerta_inferior_x[0] and x_jugador <= puerta_inferior_x[1]:
                        if y_jugador > int(ALTO_MUNDO * 0.78):
                            y_jugador = int(ALTO_MUNDO * 0.78)
                    else:
                        y_jugador = Y_MAX_PASILLO

            # Paredes de contención laterales del mapa
            if x_jugador < int(ANCHO_MUNDO * 0.04): x_jugador = int(ANCHO_MUNDO * 0.04)
            if x_jugador > int(ANCHO_MUNDO * 0.94) - ancho_actual_astro: x_jugador = int(ANCHO_MUNDO * 0.94) - ancho_actual_astro

            hitbox_final = pygame.Rect(x_jugador, y_jugador, ancho_actual_astro, ALTO_MAPA_ASTRO)
            if hitbox_final.colliderect(zona_mision) and not mision_completada:
                estado_actual = "minijuego_asteroides"
                asteroides_destruidos = 0
                asteroides.clear()
                particulas_fuego.clear()

        elif estado_actual == "minijuego_asteroides":
            temporizador_spawn += 1
            if temporizador_spawn >= 30 and (asteroides_destruidos + len(asteroides)) < max_asteroides_mision:
                temporizador_spawn = 0
                tam_ast = random.randint(40, 65)
                pos_x = random.randint(50, W_ACTUAL - 50)
                rect_ast = pygame.Rect(pos_x, -50, tam_ast, tam_ast)
                asteroides.append({
                    'rect': rect_ast,
                    'vel_y': random.uniform(3.0, 5.5),
                    'vel_x': random.uniform(-0.8, 0.8),
                    'rotacion': 0,
                    'vel_rotacion': random.uniform(-3, 3)
                })

            for asteroide in asteroides[:]:
                asteroide['rect'].y += asteroide['vel_y']
                asteroide['rect'].x += asteroide['vel_x']
                asteroide['rotacion'] += asteroide['vel_rotacion']

                particulas_fuego.append({
                    'x': asteroide['rect'].centerx + random.randint(-8, 8),
                    'y': asteroide['rect'].top + 10,
                    'vel_x': random.uniform(-0.5, 0.5),
                    'vel_y': -random.uniform(1.0, 2.5),
                    'radio': random.randint(3, 7),
                    'vida': random.randint(15, 25),
                    'color': random.choice([(255, 120, 20), (255, 200, 40), (80, 80, 80)])
                })

                if asteroide['rect'].y > H_ACTUAL + 50:
                    asteroides.remove(asteroide)

            for p in particulas_fuego[:]:
                p['x'] += p['vel_x']
                p['y'] += p['vel_y']
                p['vida'] -= 1
                p['radio'] = max(1, p['radio'] - 0.2)
                if p['vida'] <= 0:
                    particulas_fuego.remove(p)

            for est in estrellas_fondo:
                est['y'] += est['vel']
                if est['y'] > H_ACTUAL:
                    est['y'] = 0
                    est['x'] = random.randint(0, W_ACTUAL)

            if asteroides_destruidos >= max_asteroides_mision:
                mision_completada = True
                mostrar_cartel_exito = True
                frames_cartel = 0
                estado_actual = "exploracion"
                x_jugador = int(ANCHO_MUNDO * 0.80)
                y_jugador = int(ALTO_MUNDO * 0.52)
                import Mercurio
                Mercurio.main()

        if estado_actual == "menu" and video_menu:
            video_menu.update()
            if not video_menu.active:
                video_menu.restart()

        screen.fill((10, 10, 15))

        # --- RENDERING ---

        if estado_actual == "menu":
            if video_menu and video_menu.active:
                frame_superficie = video_menu.frame_surf
                if frame_superficie:
                    frame_escalado = pygame.transform.smoothscale(frame_superficie, (W_ACTUAL, H_ACTUAL))
                    screen.blit(frame_escalado, (0, 0))
            else:
                screen.fill((20, 20, 40))

            if assets["titulo"]:
                anc_t = int(W_ACTUAL * 0.36)
                alt_t = int(assets["titulo"].get_height() * (anc_t / assets["titulo"].get_width()))
                titulo_render = pygame.transform.smoothscale(assets["titulo"], (anc_t, alt_t))
                titulo_rect = titulo_render.get_rect(center=(int(W_ACTUAL * 0.22), int(H_ACTUAL * 0.21)))
                screen.blit(titulo_render, titulo_rect)

            if assets["jugar"]:
                anc_b = int(W_ACTUAL * 0.33)
                alt_b = int(assets["jugar"].get_height() * (anc_b / assets["jugar"].get_width()))
                jugar_rect = pygame.Rect(0, 0, anc_b, alt_b)
                jugar_rect.center = (int(W_ACTUAL * 0.22), int(H_ACTUAL * 0.57))
                if jugar_rect.collidepoint(pos_mouse):
                    jugar_h = pygame.transform.smoothscale(assets["jugar"], (int(anc_b * 1.12), int(alt_b * 1.12)))
                    screen.blit(jugar_h, jugar_h.get_rect(center=jugar_rect.center))
                else:
                    jugar_n = pygame.transform.smoothscale(assets["jugar"], (anc_b, alt_b))
                    screen.blit(jugar_n, jugar_rect)

            if assets["salir"]:
                anc_s = int(W_ACTUAL * 0.17)
                alt_s = int(assets["salir"].get_height() * (anc_s / assets["salir"].get_width()))
                salir_rect = pygame.Rect(0, 0, anc_s, alt_s)
                salir_rect.center = (int(W_ACTUAL * 0.22), int(H_ACTUAL * 0.70))
                if salir_rect.collidepoint(pos_mouse):
                    salir_h = pygame.transform.smoothscale(assets["salir"], (int(anc_s * 1.12), int(alt_s * 1.12)))
                    screen.blit(salir_h, salir_h.get_rect(center=salir_rect.center))
                else:
                    salir_n = pygame.transform.smoothscale(assets["salir"], (anc_s, alt_s))
                    screen.blit(salir_n, salir_rect)

        elif estado_actual == "cinematica":
            if assets["fondointro"]:
                fondo_intro = pygame.transform.smoothscale(assets["fondointro"], (W_ACTUAL, H_ACTUAL))
                capa_oscura = pygame.Surface((W_ACTUAL, H_ACTUAL))
                capa_oscura.fill((0, 0, 0))
                capa_oscura.set_alpha(140) 
                screen.blit(fondo_intro, (0, 0))
                screen.blit(capa_oscura, (0, 0))
            
            fuente_dialogo = pygame.font.SysFont("Consolas", 21, bold=True)
            fuente_sistema = pygame.font.SysFont("Consolas", 15)
            fuente_nombre_tag = pygame.font.SysFont("Arial", 22, bold=True)

            if assets["astronauta"]:
                if opacidad_astronauta < 255: opacidad_astronauta += 3
                if fase_narrativa == 4:
                    astro_base = aplicar_filtro_oscuro(assets["astronauta"], opacidad_astronauta)
                else:
                    astro_base = assets["astronauta"].copy()
                    astro_base.set_alpha(opacidad_astronauta)
                
                alt_astro = int(H_ACTUAL * 0.75) 
                anc_astro = int(assets["astronauta"].get_width() * (alt_astro / assets["astronauta"].get_height()))
                astro_scaled = pygame.transform.smoothscale(astro_base, (anc_astro, alt_astro))
                astro_rect = astro_scaled.get_rect(bottomleft=(W_ACTUAL * -0.15, H_ACTUAL - int(H_ACTUAL * 0.15)))
                screen.blit(astro_scaled, astro_rect)

            if fase_narrativa == 4 and assets["rene"]:
                if opacidad_rene < 255: opacidad_rene += 4
                rene_base = assets["rene"].copy()
                rene_base.set_alpha(opacidad_rene)
                
                alt_rene = int(H_ACTUAL * 0.70)
                anc_rene = int(assets["rene"].get_width() * (alt_rene / assets["rene"].get_height()))
                rene_scaled = pygame.transform.smoothscale(rene_base, (anc_rene, alt_rene))
                rene_rect = rene_scaled.get_rect(bottomright=(W_ACTUAL * 0.86, H_ACTUAL - int(H_ACTUAL * 0.15)))
                screen.blit(rene_scaled, rene_rect)

            ancho_caja = int(W_ACTUAL * 0.90)
            alto_caja = int(H_ACTUAL * 0.22)
            caja_rect = pygame.Rect(0, 0, ancho_caja, alto_caja)
            caja_rect.center = (W_ACTUAL // 2, H_ACTUAL - int(H_ACTUAL * 0.14))
            
            pygame.draw.rect(screen, (20, 20, 35), caja_rect, border_radius=8)
            pygame.draw.rect(screen, (0, 200, 220), caja_rect, width=3, border_radius=8)

            if fase_narrativa == 1:
                conteo_frames += 1
                if conteo_frames % 3 == 0 and caracteres_vistos < len(texto_prologo):
                    caracteres_vistos += 1
                texto_actual = texto_prologo[:caracteres_vistos]
                render_txt = fuente_dialogo.render(texto_actual, True, (240, 240, 255))
                screen.blit(render_txt, (caja_rect.x + 25, caja_rect.y + 35))
                
                if caracteres_vistos == len(texto_prologo):
                    render_ayuda = fuente_sistema.render("[ Presioná ENTER para continuar ]", True, (100, 220, 220))
                    screen.blit(render_ayuda, (caja_rect.right - 280, caja_rect.bottom - 25))

            elif fase_narrativa == 2:
                render_pregunta = fuente_dialogo.render("SISTEMA: Ingrese credencial de Tripulante :", True, (255, 220, 120))
                screen.blit(render_pregunta, (caja_rect.x + 25, caja_rect.y + 30))
                render_nombre = fuente_dialogo.render(f"> {nombre_jugador}_", True, (0, 255, 200))
                screen.blit(render_nombre, (caja_rect.x + 25, caja_rect.y + 65))
                
                render_ayuda = fuente_sistema.render("[ Escribí tu nombre y presioná ENTER ]", True, (130, 130, 140))
                screen.blit(render_ayuda, (caja_rect.right - 320, caja_rect.bottom - 25))

            elif fase_narrativa == 3:
                texto_contexto = f"Comandante {nombre_jugador}: CONAE informa que perdimos contacto con la base Tierra hace 4hs."
                conteo_frames += 1
                if conteo_frames % 3 == 0 and caracteres_vistos < len(texto_contexto):
                    caracteres_vistos += 1
                texto_actual = texto_contexto[:caracteres_vistos]
                render_txt = fuente_dialogo.render(texto_actual, True, (240, 240, 255))
                screen.blit(render_txt, (caja_rect.x + 25, caja_rect.y + 35))
                
                tag_nombre = fuente_nombre_tag.render(nombre_jugador, True, (255, 230, 100))
                tag_rect = tag_nombre.get_rect(centerx=astro_rect.centerx, bottom=astro_rect.top + 45)
                tag_sombra = fuente_nombre_tag.render(nombre_jugador, True, (0, 0, 0))
                screen.blit(tag_sombra, (tag_rect.x + 2, tag_rect.y + 2))
                screen.blit(tag_nombre, tag_rect)

                if caracteres_vistos == len(texto_contexto):
                    render_ayuda = fuente_sistema.render("[ Presioná ENTER para reunir a la tripulación ]", True, (255, 100, 100))
                    screen.blit(render_ayuda, (caja_rect.right - 420, caja_rect.bottom - 25))

            elif fase_narrativa == 4:
                conteo_frames += 1
                if conteo_frames % 3 == 0 and caracteres_vistos < len(texto_rene_completo):
                    caracteres_vistos += 1
                texto_actual = texto_rene_completo[:caracteres_vistos]
                render_txt = fuente_dialogo.render(texto_actual, True, (240, 240, 255))
                screen.blit(render_txt, (caja_rect.x + 25, caja_rect.y + 35))
                
                tag_nombre = fuente_nombre_tag.render(nombre_jugador, True, (130, 120, 70))
                tag_rect = tag_nombre.get_rect(centerx=astro_rect.centerx, bottom=astro_rect.top + 45)
                screen.blit(tag_nombre, tag_rect)

                if assets["rene"]:
                    tag_rene = fuente_nombre_tag.render("RENÉ", True, (0, 200, 255))
                    tag_rene_rect = tag_rene.get_rect(centerx=rene_rect.centerx, bottom=rene_rect.top - 4)
                    tag_rene_sombra = fuente_nombre_tag.render("RENÉ", True, (0, 0, 0))
                    screen.blit(tag_rene_sombra, (tag_rene_rect.x + 2, tag_rene_rect.y + 2))
                    screen.blit(tag_rene, tag_rene_rect)

                if caracteres_vistos < len(texto_rene_completo):
                    render_ayuda = fuente_sistema.render("[ Click o ENTER para saltear texto ]", True, (0, 180, 180))
                    screen.blit(render_ayuda, (caja_rect.right - 290, caja_rect.bottom - 25))
                else:
                    ancho_btn = 180
                    alto_btn = 40
                    boton_demo_rect = pygame.Rect(0, 0, ancho_btn, alto_btn)
                    boton_demo_rect.bottomright = (caja_rect.right - 25, caja_rect.bottom - 20)
                    
                    color_btn = (0, 230, 150) if boton_demo_rect.collidepoint(pos_mouse) else (0, 160, 100)
                    pygame.draw.rect(screen, color_btn, boton_demo_rect, border_radius=5)
                    
                    fuente_btn = pygame.font.SysFont("Arial", 16, bold=True)
                    txt_btn = fuente_btn.render("CONTINUAR", True, (255, 255, 255))
                    txt_btn_rect = txt_btn.get_rect(center=boton_demo_rect.center)
                    screen.blit(txt_btn, txt_btn_rect)

        elif estado_actual == "controles":
            if assets["controles"]:
                img_ctrl = pygame.transform.smoothscale(assets["controles"], (W_ACTUAL, H_ACTUAL))
                screen.blit(img_ctrl, (0, 0))
            else:
                screen.fill((15, 15, 25))
                panel = pygame.Rect(int(W_ACTUAL * 0.1), int(H_ACTUAL * 0.1), int(W_ACTUAL * 0.8), int(H_ACTUAL * 0.8))
                pygame.draw.rect(screen, (25, 30, 45), panel, border_radius=12)
                pygame.draw.rect(screen, (0, 220, 200), panel, width=3, border_radius=12)

                fuente_tit = pygame.font.SysFont("Consolas", 24, bold=True)
                fuente_body = pygame.font.SysFont("Consolas", 18)
                fuente_sub = pygame.font.SysFont("Consolas", 14)

                txt_t = fuente_tit.render("TUTORIAL DE CONTROL DEL JUGADOR", True, (0, 255, 200))
                screen.blit(txt_t, txt_t.get_rect(center=(W_ACTUAL // 2, panel.y + 40)))

                txt_m1 = fuente_body.render("MOVER PERSONAJE: [W, A, S, D] / [FLECHAS]", True, (255, 255, 255))
                txt_m2 = fuente_body.render("ACCIONAR / DESTRUIR ASTEROIDES: [CLIC IZQUIERDO]", True, (255, 255, 255))
                txt_m3 = fuente_body.render("INTERACTUAR CON TRIPULANTE: [ TECLA E ]", True, (255, 255, 255))

                screen.blit(txt_m1, (panel.x + 40, panel.y + 110))
                screen.blit(txt_m2, (panel.x + 40, panel.y + 160))
                screen.blit(txt_m3, (panel.x + 40, panel.y + 210))

                txt_cont = fuente_sub.render("PRESIONA ESPACIO / ENTER O CLICK PARA EMPEZAR A JUGAR", True, (0, 220, 200))
                screen.blit(txt_cont, txt_cont.get_rect(center=(W_ACTUAL // 2, panel.bottom - 40)))

        elif estado_actual == "exploracion":
            # REEMPLAZO GARANTIZADO DE MAPA TRAS COMPLETAR LA MISIÓN
            if mision_completada and assets["pasillo_abierto"]:
                img_mapa_usar = assets["pasillo_abierto"]
            else:
                img_mapa_usar = assets["pasillo"]
            
            if img_mapa_usar:
                mapa_escalado = pygame.transform.smoothscale(img_mapa_usar, (ANCHO_MUNDO, ALTO_MUNDO))
                screen.blit(mapa_escalado, (-camara_x, -camara_y))
            else:
                screen.fill((40, 40, 60))

            if not mision_completada:
                alfa_alarma += incremento_alarma
                if alfa_alarma >= 110 or alfa_alarma <= 0:
                    incremento_alarma *= -1  
                
                superficie_alarma = pygame.Surface((zona_mision.width, zona_mision.height), pygame.SRCALPHA)
                superficie_alarma.fill((240, 0, 0, max(0, alfa_alarma)))
                screen.blit(superficie_alarma, (zona_mision.x - camara_x, zona_mision.y - camara_y))
                
                pygame.draw.rect(screen, (255, 50, 50), (zona_mision.x - camara_x, zona_mision.y - camara_y, zona_mision.width, zona_mision.height), width=2)
                
                if alfa_alarma > 35:
                    fuente_alerta = pygame.font.SysFont("Consolas", 11, bold=True)
                    txt_alerta = fuente_alerta.render("¡FALLA DETECTADA!", True, (255, 255, 255))
                    txt_alerta_rect = txt_alerta.get_rect(center=(zona_mision.centerx - camara_x, zona_mision.centery - camara_y))
                    screen.blit(txt_alerta, txt_alerta_rect)

            # Dibujado de René en la habitación de las ventanas (frente a la sala central)
            if mision_completada and assets["rene"]:
                alt_rene_m = int(ALTO_MAPA_ASTRO * 1.05)
                anc_rene_m = int(assets["rene"].get_width() * (alt_rene_m / assets["rene"].get_height()))
                rene_mapa_img = pygame.transform.smoothscale(assets["rene"], (anc_rene_m, alt_rene_m))
                screen.blit(rene_mapa_img, (x_rene_mapa - camara_x, y_rene_mapa - camara_y))

                dist_rene = ((x_jugador - x_rene_mapa)**2 + (y_jugador - y_rene_mapa)**2)**0.5
                if dist_rene < 100:
                    fuente_int = pygame.font.SysFont("Consolas", 13, bold=True)
                    txt_int = fuente_int.render("[ Presioná E ]", True, (0, 255, 200))
                    screen.blit(txt_int, (x_rene_mapa - camara_x - 10, y_rene_mapa - camara_y - 20))

            # Animación de pasos
            if direccion_jugador == "adelante":
                img_actual = img_adelante if (contador_pasos // 16) % 2 == 0 else img_adelante_espejo
            elif direccion_jugador == "atras":
                img_actual = img_atras if (contador_pasos // 16) % 2 == 0 else img_atras_espejo
            elif direccion_jugador == "derecha":
                img_actual = img_derecha_1 if (contador_pasos // 14) % 2 == 0 else img_derecha_2
            elif direccion_jugador == "izquierda":
                img_actual = img_izquierda_1 if (contador_pasos // 14) % 2 == 0 else img_izquierda_2

            screen.blit(img_actual, (x_jugador - camara_x, y_jugador - camara_y))

            # Cartel de diálogo interactivo con René
            if mostrar_dialogo_rene:
                caja_r = pygame.Rect(W_ACTUAL // 2 - 250, H_ACTUAL - 120, 500, 80)
                pygame.draw.rect(screen, (15, 25, 40), caja_r, border_radius=8)
                pygame.draw.rect(screen, (0, 200, 255), caja_r, width=2, border_radius=8)
                
                f_rene = pygame.font.SysFont("Consolas", 14, bold=True)
                t1 = f_rene.render("René: ¡Bien hecho comandante! Las puertas ya están desbloqueadas.", True, (255, 255, 255))
                t2 = f_rene.render("Podemos explorar el resto de la nave ahora.", True, (200, 240, 255))
                screen.blit(t1, (caja_r.x + 15, caja_r.y + 20))
                screen.blit(t2, (caja_r.x + 15, caja_r.y + 45))

            if mostrar_cartel_exito:
                frames_cartel += 1
                if frames_cartel < 180:  
                    caja_exito = pygame.Rect(0, 0, 460, 80)
                    caja_exito.center = (W_ACTUAL // 2, 80)
                    pygame.draw.rect(screen, (10, 40, 25), caja_exito, border_radius=6)
                    pygame.draw.rect(screen, (0, 255, 120), caja_exito, width=2, border_radius=6)
                    
                    fuente_exito = pygame.font.SysFont("Consolas", 15, bold=True)
                    txt1 = fuente_exito.render("¡SISTEMAS ESTABILIZADOS!", True, (0, 255, 150))
                    txt2 = fuente_exito.render("Las puertas de seguridad han sido desbloqueadas.", True, (230, 255, 240))
                    
                    screen.blit(txt1, txt1.get_rect(centerx=caja_exito.centerx, top=caja_exito.y + 18))
                    screen.blit(txt2, txt2.get_rect(centerx=caja_exito.centerx, top=caja_exito.y + 42))
                else:
                    mostrar_cartel_exito = False

        elif estado_actual == "minijuego_asteroides":
            screen.fill((5, 5, 20))

            for est in estrellas_fondo:
                brillo = random.randint(180, 255)
                pygame.draw.circle(screen, (brillo, brillo, brillo), (int(est['x']), int(est['y'])), int(est['tam']))

            for p in particulas_fuego:
                pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), int(p['radio']))

            for asteroide in asteroides:
                ancho_ast = asteroide['rect'].width
                alto_ast = asteroide['rect'].height

                if assets["asteroide"]:
                    img_escalada = pygame.transform.smoothscale(assets["asteroide"], (ancho_ast, alto_ast))
                    img_rotada = pygame.transform.rotate(img_escalada, asteroide['rotacion'])
                    rect_rotado = img_rotada.get_rect(center=asteroide['rect'].center)
                    screen.blit(img_rotada, rect_rotado)
                else:
                    centro_x = asteroide['rect'].centerx
                    centro_y = asteroide['rect'].centery
                    pygame.draw.circle(screen, (130, 80, 50), (centro_x, centro_y), ancho_ast // 2)
                    pygame.draw.circle(screen, (200, 120, 60), (centro_x, centro_y), ancho_ast // 2, width=3)

            pygame.draw.rect(screen, (0, 255, 150), (10, 10, W_ACTUAL-20, H_ACTUAL-20), width=3)

            fuente_mision = pygame.font.SysFont("Consolas", 24, bold=True)
            txt_mision = fuente_mision.render(f"DESTRUÍDOS: {asteroides_destruidos} / {max_asteroides_mision}", True, (255, 255, 255))
            screen.blit(txt_mision, (30, 30))

            pygame.draw.circle(screen, (0, 255, 255), pos_mouse, 15, width=2)
            pygame.draw.line(screen, (0, 255, 255), (pos_mouse[0] - 22, pos_mouse[1]), (pos_mouse[0] + 22, pos_mouse[1]), 2)
            pygame.draw.line(screen, (0, 255, 255), (pos_mouse[0], pos_mouse[1] - 22), (pos_mouse[0], pos_mouse[1] + 22), 2)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
