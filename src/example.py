import pygame
import pyframe
import time
import random

# PyGame Init
pygame.init()
pygame.font.init()

WIN_WIDTH = 750
WIN_HEIGHT = 500
WIN_RUN = True

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
# Init the pyframe generic window
pyframe.base.GLOBAL_WIN = WIN
# Set the fps
pyframe.utils.set_framerate(60)

pygame.display.set_caption("PyFrame Exemple") # Setting up the window title

# Example sprite

# This is a rect sprite, the very first sprite of pyframe.
# There's different method for each sprite.
exampleSprite = pyframe.base.PyFrameRectSprite(WIN,50,50,50,50,centered_rendering = True)

# Create an hitbox in the middle of the
# screen. Particle doesn't support hitbox
# bounce for now
middle_hitbox = pyframe.base.Hitbox(WIN_WIDTH/2-25,WIN_HEIGHT/2-25,50,50,centered_hitbox=True)

bouton = pyframe.base.Button(20,20,"Hello !",width = 35,height = 35) # Create a button with text "Hello !"

def return_new_particle_system() : # Return a brand new ParticleSystem
    return pyframe.base.ParticleSystem(
        x=random.randint(WIN_WIDTH-50,WIN_WIDTH+50)/2,
        y=random.randint(WIN_HEIGHT-50,WIN_HEIGHT+50)/2,
        number_of_particles=1000,
        start_velocity=0.3,
        particle_radius=5,
        gravity = 0,
        air_resistance=1,
        elasticity=1,
        random_values = True,
        random_ceil = 100,
        image_path = "\\images\\bubble.png",
        lifetime = 5000
        )

particule = return_new_particle_system()

myActivity = pyframe.base.Display([particule,bouton]) # Create an "Activity", like a screen, or a display

# pyframe.base.PyFrameSuperSprite.bind(key,direction,step) : Bind a key to a movement
#     key = The key to move the sprite,
#     direction = Direction of movement. Can be "up","down","right","left","stand".
#     step = Movement speed
#
# pyframe.base.key_to_index(key) : return the index of a certain key
# (AZERTY, see https://www.pygame.org/docs/ref/key.html#key-constants-label for all the keys and QWERTY characters)
#     key = The key. Can be any letter. Specials characters not implemented yet
exampleSprite.bind(key=pyframe.utils.key_to_index("d"),direction="right",step=1) # 100 is the pygame D key
exampleSprite.bind(key=pyframe.utils.key_to_index("q"),direction="left",step=1) # 97 is the pygame Q key

# key argument can also be the index directly
exampleSprite.bind(key=115,direction="up",step=1) # 115 is the pygame Z key
exampleSprite.bind(key=119,direction="down",step=1) # 119 is the pygame S key

# If you want to move manually a sprite, use the move function :
# pyframe.base.PyFrameSuperSprite.move(direction,step) : Move a sprite in one direction
#     direction =  Direction of movement. Can be "up","down","right","left","stand".
#     step = Movement length
# exampleSprite.move(direction="right",step=25)
while WIN_RUN : # Mainloop
    # clear_screen(color,window) : Fill the screen with a certain color.
    #     color = A tuple to represent the color (e.g. : (255,0,0) for red). By default, it use the BACKGROUND_COLOR color
    #     window = If you want to clear a specific window. By default, it clear the GLOBAL_WIN window
    pyframe.utils.clear_screen()
    pyframe.utils.events_loop() # PyFrame function to handle binds and timings

    ####
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            WIN_RUN = False # To quit the loop if you click the close button
    ####


    #middle_hitbox.debug_render()

    myActivity.render()
    myActivity.move()


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
    pyframe.utils.render_text(10,10,str(round(pyframe.base.CLOCK.get_fps()))+" FPS",(0,255,0),window=WIN)

    # pyframe.base.PyFrameRectSprite.render() : Render a sprite on his window
    # exampleSprite.render()

    # Update the pygame display
    pygame.display.flip()
