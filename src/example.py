import pygame
import pyframe
import time

pygame.init()
pygame.font.init()

WIN_WIDTH = 750
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

# This is a rect sprite, the very first sprite of pyframe.
# There's different method for each sprite.
exampleSprite = pyframe.PyFrameRectSprite(WIN,50,50,50,50,centered_rendering = True)

particule = pyframe.ParticleSystem(
    x=250,
    y=250,
    number_of_particles=100,
    start_velocity=1,
    particle_radius=5,
    gravity = 0,
    air_resistance=1,
    elasticity=1
    )

# pyframe.PyFrameSuperSprite.bind(key,direction,step) : Bind a key to a movement
#     key = The key to move the sprite,
#     direction = Direction of movement. Can be "up","down","right","left","stand".
#     step = Movement speed
#
# pyframe.key_to_index(key) : return the index of a certain key
# (AZERTY, see https://www.pygame.org/docs/ref/key.html#key-constants-label for all the keys and QWERTY characters)
#     key = The key. Can be any letter. Specials characters not implemented yet
exampleSprite.bind(key=pyframe.key_to_index("d"),direction="right",step=1) # 100 is the pygame D key
exampleSprite.bind(key=pyframe.key_to_index("q"),direction="left",step=1) # 97 is the pygame Q key

# key argument can also be the index directly
exampleSprite.bind(key=115,direction="up",step=1) # 115 is the pygame Z key
exampleSprite.bind(key=119,direction="down",step=1) # 119 is the pygame S key

# If you want to move manually a sprite, use the move function :
# pyframe.PyFrameSuperSprite.move(direction,step) : Move a sprite in one direction
#     direction =  Direction of movement. Can be "up","down","right","left","stand".
#     step = Movement length
# exampleSprite.move(direction="right",step=25)

while WIN_RUN : # Mainloop
    pyframe.events_loop() # PyFrame function to handle binds and timings
    
    ####
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            WIN_RUN = False # To quit the loop if you click the close button
    ####


    # clear_screen(color,window) : Fill the screen with a certain color.
    #     color = A tuple to represent the color (e.g. : (255,0,0) for red). By default, it use the BACKGROUND_COLOR color
    #     window = If you want to clear a specific window. By default, it clear the GLOBAL_WIN window
    pyframe.clear_screen()

    particule.move()
    particule.render()

    # render_text(x,y,text,color,vertical_centering,horizontal_centering,font,fontsize,window) : Render a text on a window
    #     x = The x position of the text
    #     y = The y position of the text
    #     text = ...
    #     color = A tuple to represent the color (e.g. : (255,0,0) for red). By default, it use the PRIMARY_COLOR color
    #     vertical_centering = Boolean that say if the text need to be centered vertically
    #     horizontal_centering = Boolean that say if the text need to be centered horizontally
    #     font = A pygame.font font used to render the text. By default, it use the GLOBAL_FONT font
    #     fontsize = Font size if argument font is defined. If this argument is not present, it use the value 30
    #     window = Window to render the text. By default, the text is rendered on GLOBAL_WIN window
    pyframe.render_text(10,10,str(round(pyframe.CLOCK.get_fps()))+" FPS",(0,255,0),window=WIN)

    # pyframe.PyFrameRectSprite.render() : Render a sprite on his window
    # exampleSprite.render()

    # Update the pygame display
    pygame.display.flip()
