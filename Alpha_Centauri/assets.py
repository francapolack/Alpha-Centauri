# assets.py
import pygame
import os

# =====================================================================
#  ACÁ PONÉR LOS NOMBRES EXACTOS DE IMÁGENES, VIDEOS Y AUDIOS 
# =====================================================================
NOMBRES_ARCHIVOS = {
    # Multimedia (Estos van en la carpeta principal o la que uses)
    "musica_menu": "musica_menu.mp3",
    "sonido_click": "click.wav",
    "video_menu": "videomenu.mp4", # Asume que está dentro de la carpeta "imagenes"

    # Imágenes de Menú y UI
    "fondointro": "fondointro.png",
    "titulo": "titulomenu.png",
    "jugar": "botoninicio.png",
    "salir": "botonsalir.png",
    "controles": "controles.png",
    
    # Personajes y Escenario
    "astronauta": "astronautito.png",
    "rene": "rene.png",
    "minirene": "minirene.PNG",
    "rogelio": "rogelio.png",
    "minicrogelio": "minicrogelio.PNG",
    "pasillo": "habitaciones.png",
    "pasillo_abierto": "pasillo_abierto.png",
    "asteroide": "asteroide.png",
    "alien": "alien.png",
    "minialien": "minialien.png",
    "planeta venus": "planeta venus.png",

    "colisiones": "colisiones.png",  # Imagen para depuración de colisiones
    "colisiones_abiertas": "colisiones_abiertas.png", 
    
    # Animaciones (Caminata)
    "camina_adelante": "camina adelante.png",
    "camina_atras": "camina atras.png",
    "camina_der_1": "caminapataadelante.png",
    "camina_der_2": "caminapataatras.png"
}
# =====================================================================

def cargar_imagenes():
    carpeta_actual = os.path.dirname(__file__)
    img_dict = {}
    
    # Imágenes estáticas
    claves_imagenes = [
        "fondointro", "titulo", "jugar", "salir", "astronauta", 
        "rene", "minirene", "rogelio", "minicrogelio", "alien", "minialien",
        "pasillo", "pasillo_abierto", "asteroide", "controles",
        "colisiones", "colisiones_abiertas"
    ]
    
    for clave in claves_imagenes:
        ruta = os.path.join(carpeta_actual, "imagenes", NOMBRES_ARCHIVOS[clave])
        if os.path.exists(ruta):
            img_dict[clave] = pygame.image.load(ruta).convert_alpha()
        else:
            img_dict[clave] = None
            
    return img_dict

def cargar_animaciones(alto_mapa):
    carpeta_actual = os.path.dirname(__file__)
    anims = {}
    
    def cargar_img_mapa(nombre_archivo, ancho_fijo=None):
        ruta = os.path.join(carpeta_actual, "imagenes", nombre_archivo)
        if os.path.exists(ruta):
            img = pygame.image.load(ruta).convert_alpha()
            ancho_final = ancho_fijo if ancho_fijo else int(img.get_width() * (alto_mapa / img.get_height()))
            return pygame.transform.scale(img, (ancho_final, alto_mapa))
        
        ancho_aux = ancho_fijo if ancho_fijo else 35
        surf = pygame.Surface((ancho_aux, alto_mapa))
        surf.fill((255, 0, 0))
        return surf

    anims["adelante"] = cargar_img_mapa(NOMBRES_ARCHIVOS["camina_adelante"])
    anims["atras"] = cargar_img_mapa(NOMBRES_ARCHIVOS["camina_atras"])
    anims["adelante_espejo"] = pygame.transform.flip(anims["adelante"], True, False)
    anims["atras_espejo"] = pygame.transform.flip(anims["atras"], True, False)
    
    anims["derecha_1"] = cargar_img_mapa(NOMBRES_ARCHIVOS["camina_der_1"])
    ancho_fijo = anims["derecha_1"].get_width()
    anims["derecha_2"] = cargar_img_mapa(NOMBRES_ARCHIVOS["camina_der_2"], ancho_fijo)
    
    anims["izquierda_1"] = pygame.transform.flip(anims["derecha_1"], True, False)
    anims["izquierda_2"] = pygame.transform.flip(anims["derecha_2"], True, False)
    
    anims["ancho_fijo_lateral"] = ancho_fijo
    
    return anims