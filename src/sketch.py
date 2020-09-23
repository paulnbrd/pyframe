import pygame, random, time, pyframe
pygame.font.init()
pygame.init()
WIN_WIDTH = 750
WIN_HEIGHT = 500
WIN_RUN = True
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
RENDER_EACH_FRAME = []
pyframe.base.GLOBAL_WIN = WIN
pyframe.base.set_framerate(60)
pygame.display.set_caption("PyFrame Exemple")


# Définition des variables
menu = 1
def new_particle() :
    return pyframe.base.ParticleSystem(
    x = pyframe.base.LAST_MOUSE_POS[0]-1,
    y = pyframe.base.LAST_MOUSE_POS[1]-1,
    number_of_particles = 100,
    particle_radius=2,
    start_velocity = 0.2,
    gravity = 0,
    air_resistance = 0.999,
    elasticity = 0.750,
    lifetime = 50 # Temps de vie
    )
def click_effect() :
    global menu
    if menu == 1 :
        RENDER_EACH_FRAME.append(new_particle())
    elif menu == 2 :
        RENDER_EACH_FRAME.append(new_particle())
    return 0
def menu_2(bouton) :
    global menu
    click_effect()
    menu = 2
def menu_1(bouton) :
    global menu
    click_effect()
    menu = 1
bouton_du_menu_1 = pyframe.base.Button(WIN_WIDTH/2,WIN_HEIGHT/2-50,"Menu 2",command = menu_2,background_color = (244,127,48),text_color=(255,255,255),vertical_centering=True,horizontal_centering=True)
bouton_du_menu_2 = pyframe.base.Button(WIN_WIDTH/2,WIN_HEIGHT/2+50,"Menu 1",command = menu_1,background_color = (248, 194, 145),text_color=(12, 36, 97),vertical_centering=True,horizontal_centering=True)

menu_1_display = pyframe.base.Display([bouton_du_menu_1])
menu_2_display = pyframe.base.Display([bouton_du_menu_2])

#####

while WIN_RUN :
    pyframe.base.clear_screen()
    pyframe.base.events_loop()
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            WIN_RUN = False

    if menu == 1 :
        menu_1_display.render()
        menu_1_display.move()
    elif menu == 2 :
        menu_2_display.render()
        menu_2_display.move()

    for sprite in RENDER_EACH_FRAME :
        if type(sprite) is pyframe.base.ParticleSystem :
            sprite.render()
            sprite.move()

    text = pyframe.base.render_text(WIN_WIDTH,WIN_HEIGHT,str(menu) + "-" +str(round(pyframe.CLOCK.get_fps())),blit_to_window=False)
    WIN.blit(text,(WIN_WIDTH-text.get_width(),WIN_HEIGHT-text.get_height()))
    pygame.display.flip()

pygame.quit()