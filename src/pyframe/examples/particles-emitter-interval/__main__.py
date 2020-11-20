import pyframe,pygame,sys,os


size = pyframe.functions.get_screen_size() # Function to get screen size

# But for this example, we will take a size of 500x500
size = (500,500)


if size == False : # If the function returned False (not found)
    print("Unable to get screen size")
    sys.exit(0)

# Init pygame
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial",18)

# Screen init
screen = pygame.display.set_mode(size)
pygame.display.set_caption("pyframe.IntervalEmitter example")
icon = pygame.image.load(  pyframe.constants.local_dir+"..\\images\\logo-PyFrame.png" )
pygame.display.set_icon( icon )


#
# IntervalEmitter > Emit particle every "interval" ms
#
emitter = pyframe.classes.IntervalEmitter(
    surface = screen, # The surface to blit onto (pygame.surface.Surface)
    interval = 15, # every 15 ms
    nb_init=0, # Particle at initialisation
    x = round(size[0] / 2), # Middle of the screen
    y=round(size[1] / 2),  # Middle of the screen
    color = (255,0,0), # Default color is (255,0,0). The color is used to create circles of this color for the particles
    image = pyframe.constants.local_dir+"..\\images\\fire.png", # The path to the image (overwrite the colo argument)
    radius = 50, # Base radius of the particle
    image_base_scale = 2.5, # The scale of the image, if needed (default : 1)
    image_blur = 7, # The blur factor of the image (no scale)
    start_velocity = 0.01, # The velocity of the particle
    velocity_randomness = 0.01, # The range of the velocity (between start_velocity-velocity_randomness and start_velocity+velocity_randomness)
    gravity = -0.0001, # Gravity applied to the particle
    lifetime = 750, # Lifetime of a particle
    reduce_each = 100 # Reduce radius each x ms
)

# MAINLOOP
done = False
fps = 60
blocked_fps = False
while not done :
    screen.fill( (255,255,255) ) # Fill the screen
    # If fps blocked or not
    if not blocked_fps :
        elapsed = clock.tick(fps) # Tick clock
    else :
        elapsed = clock.tick(10) # To see the difference between smooth and not smooth : the result is the same

    # > Update and render an emitter

    # The tick arg is how many ms elapsed since last frame.
    # Each velocity and gravity calculation are multiplied by this number.
    # This way, the gravity and velocity will be applied regardless of the number of fps
    # For example :
    #   A particle lifts as much if there is 10 fps or 100 fps.
    #   It's just smoother at 100 fps
    #   ( When the example is running, try to press F1 and see : 10fps or 60, the particle's speed is the same )
    emitter.update(tick=elapsed)

    # Blit the particles to the surface
    emitter.render()


    # Display the fps
    text = font.render( str(round(clock.get_fps())),True,(0,0,0) )
    screen.blit( text,(0,0) )
    h = text.get_height()
    text = font.render( "Press F1",True,(0,0,0) )
    screen.blit( text,(0,h) )

    # Handle events
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN :
            if event.key == pygame.K_F1 :
                blocked_fps = not blocked_fps # Change the value to its inverse
    # Update display
    pygame.display.flip()