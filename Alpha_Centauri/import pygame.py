import pygame


pygame.font.init()


font_list = pygame.font.get_fonts()

print(f"fuentes: {len(font_list)}")
print(font_list)
