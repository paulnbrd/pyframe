"""

This example show the basic usage of graphs (pyframe.Graph)
Note that the graph are for now not very well optimized.
On my PC :
    average of 1100 fps when graph is hidden
    average of 400 fps when graph is shown

Press F1 to show/hide the graph

"""

import pygame,pyframe,sys,os # Importing modules


size = (500,500) # Window size

#########################################

pygame.init()
pygame.font.init()
fenetre = pygame.display.set_mode( size )
pygame.display.set_caption("pyframe.Graph example")
icon = pygame.image.load(  pyframe.constants.local_dir+"..\\images\\logo-PyFrame.png" )
pygame.display.set_icon( icon )

done = False
#########################################

# Example de bouton

bouton = pyframe.classes.Button(
    text = "Clique ici pour afficher une grille",
    surface = fenetre,
    position = (100,100)
)
clock = pygame.time.Clock()
click = False
graph = pyframe.classes.Graph(
    size = size,
    titre = "FPS",
    fill_with = 0
)
graph.polish_values()
font = pygame.font.SysFont("Arial",18)
graph_show = True
#########################################
while not done :
    fenetre.fill( (0,0,0) )

    fps = clock.get_fps()
    graph.add_value(fps)
    graph.polish_values(50) # Plish the last 50 values
    if graph_show :
        fenetre.blit( graph.get_surface(auto_render=True),(0,0) )

    text = font.render("Press F1 to hide/show the graph",True,(255,255,255))
    fenetre.blit( text,(size[0]-text.get_width(),size[1]-text.get_height()) )

#########################################
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_F1 :
                graph_show = not graph_show
    pygame.display.flip()
    clock.tick(0)

#########################################
pygame.quit()