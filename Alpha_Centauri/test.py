# Source - https://stackoverflow.com/a/43642354
# Posted by skrx
# Retrieved 2026-08-27, License - CC BY-SA 3.0

import sys
import pygame as pg
from clases_funciones import planeta_info
def screenfill(screen):
    screen.fill((255,0,0))
def main():
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    
    font = pg.font.Font(None, 30)
    text_surface = font.render('text button', True, pg.Color('steelblue3'))
    # Use this rect for collision detection with the mouse pos.
    button_rect = text_surface.get_rect(topleft=(200, 200))
    text_2=font.render('click!',True,pg.Color('steelblue3'))
    txt2_rect=text_2.get_rect(topleft=(200,200))

    done = False
    screen.fill((40, 60, 70))
    screen.blit(text_surface, button_rect)
    while not done:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Use event.pos or pg.mouse.get_pos().
                    if button_rect.collidepoint(event.pos):
                        screenfill(screen)
                        print("clicked")
                        
                    if txt2_rect.collidepoint(event.pos):
                        screen.fill((255,0,0))

        planeta_info(screen,"info de mercurio blah blah blah","Mercurio",(pg.Color("azure3")))


        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()
