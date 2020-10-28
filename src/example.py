import pyframe,pygame

pygame.init()
pygame.font.init()
fenetre = pygame.display.set_mode( (1360,768),pygame.FULLSCREEN )
r = pygame.display.set_caption( "PyFrame Example" )

emitters = []
for i in range(1) :
    emitter = pyframe.classes.IntervalEmitter(
        nb_init = 0,
        interval=2,
        x = (1360/20)*i*2+25,
        y = 450,
        gravity = -0.0002,
        start_velocity = 0.01,
        velocity_randomness = 0.01,
        color = (230, 126, 34),
        surface = fenetre,
        radius=25,
        lifetime = 700,
        reduce_radius_over_time = True,
        reduce_each = 350,
        image = pyframe.constants.local_dir+"images\\fire.png",
        image_base_scale = 5,
        image_blur = 20
    )
    emitter.generate()
    emitters.append(emitter)

graph = pyframe.classes.Graph(titre="Nombre d'images par seconde",size=(1360/2,200))
graph_particle = pyframe.classes.Graph(titre="Nombre de particules affichées",size=(1360/2,200))

done = False
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial",18)

fps_blocking = False
graph_on = True


def nb_particles() :
    nb = 0
    for e in emitters :
        nb += len(e.particles)
    return nb

while not done :
    if not fps_blocking :
        e = clock.tick(0)
    else :
        e = clock.tick(60)

    fenetre.fill( (0,0,0) )
    for emitter in emitters :
        emitter.update(e)
        emitter.render()

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            done = True
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_F5 :
                fps_blocking = not fps_blocking
            elif event.key == pygame.K_F1 :
                graph_on = False
            elif event.key == pygame.K_F2 :
                graph_on = True
    fps = int(clock.get_fps())
    graph.add_value( fps )
    graph.render()
    if graph_on :
        fenetre.blit( graph.get_surface( ),(0,0) )
    graph_particle.add_value( nb_particles() )
    graph_particle.render()
    if graph_on :
        fenetre.blit( graph_particle.get_surface( ),(graph.surface.get_width(),0) )

    pygame.display.flip()

pygame.quit()