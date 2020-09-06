import pygame
import pyframe
import time

pygame.init()
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 500
WIN_RUN = True

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
# Init the pyframe generic window
pyframe.GLOBAL_WIN = WIN
# Set the fps
pyframe.set_framerate(60)

pygame.display.set_caption("PyFrame Exemple")

# Create a new Sprite


# Example sprite
# Rect sprite... Not very useful
exempleSprite = pyframe.PyFrameRectSprite(WIN,50,50,50,50,centered_rendering = True) # This is a rect sprite
exempleSprite.bind(key=pyframe.key_to_index("d"),direction="right",step=1) # 100 is the pygame D key
exempleSprite.bind(key=pyframe.key_to_index("q"),direction="left",step=1) # 97 is the pygame Q key
exempleSprite.bind(key=115,direction="up",step=1) # 115 is the pygame Z key
exempleSprite.bind(key=119,direction="down",step=1) # 119 is the pygame S key


while WIN_RUN :
    pyframe.events_loop()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            WIN_RUN = False

    pyframe.clear_screen()

    # USES OF PYFRAME
    pyframe.render_text(WIN,10,10,str(round(pyframe.CLOCK.get_fps())),(0,255,0))

    # Example function
    exempleSprite.render()

    pygame.display.flip()
