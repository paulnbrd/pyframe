import pygame, pyframe, random, time
pygame.font.init()
pygame.init()
WIN_WIDTH = 750
WIN_HEIGHT = 500
WIN_RUN = True
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pyframe.GLOBAL_WIN = WIN
pyframe.set_framerate(60)
pygame.display.set_caption("PyFrame Exemple")


# Définition des variables
clicked = False
def new_particle() :
    return pyframe.ParticleSystem(
    x = WIN_WIDTH/2,
    y = WIN_HEIGHT/2,
    number_of_particles = 100,
    particle_radius=2,
    start_velocity = 1,
    gravity = 0.05,
    air_resistance = 0.999,
    elasticity = 0.750,
    lifetime = 10000 # Temps de vie
    )
particule = new_particle()

def print_salut(bouton) :
    global particule, clicked
    clicked = True
    my_screen.sprites.append(new_particle())
    return 0
bouton = pyframe.Button(2,2,"Reset les particules",command = print_salut,background_color = (244,127,48),text_color=(255,255,255))

my_screen = pyframe.Display([bouton,particule])

#####

while WIN_RUN :
    pyframe.clear_screen()
    pyframe.events_loop()
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            WIN_RUN = False

    bouton.is_clicked()

    my_screen.render()
    if not clicked :
        pyframe.render_text(2,50,"Clique sur le bouton au dessus")
    my_screen.move()

    for sprite in my_screen.sprites : # Retirer les systèmes de particules qui ne bougent plus
        if type(sprite) is pyframe.ParticleSystem :
            if len(sprite.particles) == 0 :
                my_screen.sprites.remove(sprite)
                del sprite

    pygame.display.flip()

pygame.quit()