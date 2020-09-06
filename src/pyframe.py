import os
import pygame
import random
import math

pygame.font.init() # Initialiser les polices d'écritures
GLOBAL_WIN = False # La fenetre de rendu par défaut
GLOBAL_FONT = pygame.font.SysFont("Arial", 30) # La police d'écriture par défaut
BACKGROUND_COLOR = (0,0,0) # La couleur de fond par défaut
PRIMARY_COLOR = (213,63,60) # La couleur principale par défaut

FPS = 60 # Les FPS par défaut
DELTA_TIME_DIVIDER = 1000 # Constante, permet de changer la vitesse des objets
CLOCK = pygame.time.Clock() # La clock pygame
TIME_SPEED = 1 # La vitesse du temps, peut-être arrangée pour faire du slow-motion
DELTA_TIME = CLOCK.tick(FPS)/DELTA_TIME_DIVIDER*TIME_SPEED # Le calcul du delta time

MOVE_BINDS = [] # Les binds des mouvements sont stockés ici
SPRITES = [] # Les sprites sont stockés ici

# Les indexs pygame des touches
AZERTY_KEY_INDEXES = {
    "a":113,
    "b":98,
    "c":99,
    "d":100,
    "e":101,
    "f":102,
    "g":103,
    "h":104,
    "i":105,
    "j":106,
    "k":107,
    "l":108,
    "m":59,
    "n":110,
    "o":111,
    "p":112,
    "q":97,
    "r":114,
    "s":115,
    "t":116,
    "u":117,
    "v":118,
    "w":122,
    "x":120,
    "y":121,
    "z":119
}

local_dir = os.path.dirname(__file__) # Le chemin vers le script éxecuté

# Handling exceptions
class Error(Exception): # La classe d'erreur de base
    pass

class WindowError(Error): # Erreur de fenêtre
    def __init__(self, message):
        self.message = message
class ArgumentError(Error): # Erreur d'argument
    def __init__(self, message, subject):
        self.message = message
        self.subject = subject




#############################################
############ =<|= Functions =|>= ############
#############################################

def set_framerate(framerate) : # Définit les fps
    global FPS,DELTA_TIME
    FPS = framerate # Redéfinit la globale FPS

def clear_screen(color = BACKGROUND_COLOR,window = False) : # "Efface" l'écran
    global GLOBAL_WIN
    if window == False : # Si l'argument window est laissé de base (pas de fenêtre fournie)
        if GLOBAL_WIN == False : # Si la fenêtre globale n'est pas définie
            raise ArgumentError("GLOBAL_WIN is not defined","GLOBAL_WIN") # Raise une erreur d'argument
        else :
            GLOBAL_WIN.fill(color) # Remplir l'écran de la couleur désirée
    else :
        window.fill((0,0,0)) # Remplir l'écran de noir, faute de mieux

def key_to_index(key) :
    """ Permet de transformer un caractère en son index pygame (le clavier AZERTY n'est pas celui utilisé par pygame) """
    return AZERTY_KEY_INDEXES.get(key)
    
def events_loop() :
    """
        Voici la boucle d'évenements qui doit être appellée
        à chaque itération de la mainloop de pygame
        à chaque frame quoi.
    """
    DELTA_TIME = CLOCK.tick(FPS)/DELTA_TIME_DIVIDER*TIME_SPEED # Redéfinition du delta time
    keys = pygame.key.get_pressed() # Récupérer les touches appuyés

    for bind in MOVE_BINDS : # Pour tous les binds
        if keys[bind.get("key")] : # Si la touche du bind est appuyée
            bind.get("obj").move(bind.get("direction"),bind.get("step")) # Déplacer l'objet

def drawRect(window,x,y,w,h,color = PRIMARY_COLOR) : # Dessiner un rectangle
    pygame.draw.rect(window,color,(x,y,w,h)) # La fonction de pygame

def render_text(x,y,text,color = PRIMARY_COLOR,vertical_centering = False,horizontal_centering = False,font = False,fontsize = 30,window = False) :
    # Écrit du texte sur la fenêtre
    global GLOBAL_FONT, GLOBAL_WIN
    if font != False : # Si la police d'écriture n'est pas définie
        if type(font) is str : # Si la police d'écriture est une chaîne de caractères
            font = pygame.font.SysFont(font, int(fontsize)) # Définir la police d'écriture
        else : # Sinon
            raise ArgumentError("Invalid font argument","font") # Lever une erreur d'argument

    else : # Sinon
        font = GLOBAL_FONT # La police d'écriture est égale à la police d'écriture globale
    
    if window != False : # Si l'argument window est changé de la valeur de base
        if type(window) is pygame.Surface : # Si la window est un pygame.Surface (Une surface pygame,qui est probablement une fenêtre)
            window = window # Ne rien changer
        else :
            raise ArgumentError("Invalid window argument","window") # Lever une erreur d'argument
    else : # Sinon
        window = GLOBAL_WIN # La fenêtre de rendue est définie à la fenêtre globale
    text = font.render(text, False, color) # Rendre le texte
    window.blit(text,(x,y)) # Le coller dans la fenêtre

#############################################
############# =<|= Classes =|>= #############
#############################################

class Hitbox :
    """
        Voici une classe de boîte de collision.
        Qui permet de correctement simuler les...
        collisions.
        Chaque objet, pour pouvoir interagir avec
        le monde doit avoir une boîte de collision.
    """
    def __init__(self,x,y,width,height,window = False,centered_hitbox = False) :
        if window == False :
            # Si aucune fenêtre n'est fournie,
            # Définir la fenêtre de rendue comme celle globale
            self.window = GLOBAL_WIN
        else : # Sinon
            self.window = window # Définir la fenêtre comme celle fournie
        self.x = x # Position x
        self.y = y # Position y
        self.width = width # Largeur
        self.height = height # Longueur
        self.centered_hitbox = centered_hitbox # La boîte de collision est centrée sur les positions x et y ?

    def debug_render(self,color = (0,0,255)) : # Faire un rendu dans self.window pour le débug
        # Dessiner un rectangle à la position de la hitbox
        drawRect(self.window,self.x-self.width/2,self.y-self.height/2,self.width,self.height,color)

    def do_hitboxes_overlap(self,hitbox) : # Est-ce que cette boîte de collision en chevauche une autre ?
        if self.x > hitbox.x+hitbox.width or hitbox.x > self.x+self.width : # Si une est à gauche de l'autre
            return False # Renvoyer Faux !
        elif self.y > hitbox.y+hitbox.height or hitbox.y > self.y+self.height : # Sinon si une est au dessus de l'autre
            return False # Retourner Faux !
        else : # Sinon
            return True # Retourner Vrai !



PARTICLES_availableDirections = ["up","down","right","left","all"] # Direction de particules autorisées
PARTICLES_directionsAngle = {"up":(-90,0),"down":(0,90),"right":(-45,45),"left":(45,-45)}

def addVectors(v1, v2): # v[0] = Angle, v[1] = length
    x = math.sin(v1[0]) * v1[1] + math.sin(v2[0]) * v2[1]
    y = math.cos(v1[0]) * v1[1] + math.cos(v2[0]) * v2[1]

    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return (angle, length)

class Particle :
    def __init__(self,x,y,start_velocity, radius = 2, gravity = 0.002,air_resistance = 0.999,elasticity = 0.750, colors = [[255,0,0],[100,0,0]] ,window = GLOBAL_WIN) :
        self.x = x
        self.y = y
        self.window = window
        self.gravity = gravity = (math.pi, gravity)

        self.air_resistance = air_resistance
        self.elasticity = elasticity

        if self.window == False :
            self.window = GLOBAL_WIN
        self.radius = radius

        self.velocity = start_velocity
        self.angle = random.uniform(0, math.pi*2)

        if colors[0][0] > colors[1][0] :
            temp = colors[0][0]
            colors[0][0] = colors[1][0]
            colors[1][0] = temp
        if colors[0][1] > colors[1][1] :
            temp = colors[0][1]
            colors[0][1] = colors[1][1]
            colors[1][1] = temp
        if colors[0][2] > colors[1][2] :
            temp = colors[0][2]
            colors[0][2] = colors[1][2]
            colors[1][2] = temp
        self.color = (
            random.randint(colors[0][0],colors[1][0]),
            random.randint(colors[0][1],colors[1][1]),
            random.randint(colors[0][2],colors[1][2])
        )
    def render(self) :
        pygame.draw.circle(self.window,self.color,(int(self.x),int(self.y)),self.radius)
    def move(self) :
        (self.angle, self.velocity) = addVectors((self.angle, self.velocity), self.gravity)

        self.x += math.sin(self.angle) * self.velocity * DELTA_TIME
        self.y -= math.cos(self.angle) * self.velocity * DELTA_TIME

        width, height = pygame.display.get_surface().get_size()
        if self.x > width - self.radius:
            self.x = 2 * (width - self.radius) - self.x
            self.angle = - self.angle
            self.velocity *= self.elasticity # Perte de vitesse quand ça touche un mur
        elif self.x < self.radius:
            self.x = 2 * self.radius - self.x
            self.angle = - self.angle
            self.velocity *= self.elasticity
        if self.y > height - self.radius:
            self.y = 2 * (height - self.radius) - self.y
            self.angle = math.pi - self.angle
            self.velocity *= self.elasticity
        elif self.y < self.radius:
            self.y = 2 * self.radius - self.y
            self.angle = math.pi - self.angle
            self.velocity *= self.elasticity

        self.velocity *= self.air_resistance # Résistance à l'air, un peu de perte de vitesse (Plus la vitesse est grande, plus la particule perd de la vitesse)

class ParticleSystem :
    def __init__(self,x,y,number_of_particles,start_velocity,particle_radius = 10, gravity = 0.002,air_resistance = 0.999,elasticity = 0.750,colors = [[255,0,0],[200,0,0]],color = PRIMARY_COLOR,window = GLOBAL_WIN) :
        self.x = x
        self.y = y
        self.number_of_particles = number_of_particles
        self.velocity = start_velocity
        self.color = color
        self.window = window
        if self.window == False :
            self.window = GLOBAL_WIN
        self.particle_radius = particle_radius
        self.gravity = gravity
        self.air_resistance = air_resistance
        self.elasticity = elasticity

        self.particles = []
        for i in range(self.number_of_particles) :
            self.particles.append(Particle(self.x,self.y,self.velocity,radius = self.particle_radius,gravity = self.gravity,air_resistance = self.air_resistance,elasticity = self.elasticity,window = self.window))
    def move(self): 
        for particle in self.particles :
            particle.move()
    def render(self): 
        for particle in self.particles :
            particle.render()


#############################################
############# =<|= Sprites =|>= #############
#############################################

class PyFrameSuperSprite : # La classe de Lutin de base
    def render(self) : # Ajouter des choses ici si besoin au moment du render
        pass

    def remove_hitbox(self,hitboxObject) : # Retirer une hitbox
        if type(hitboxObject) is Hitbox : # Si l'argument fourni est une hitbox
            self.hitboxes.remove(hitboxObject) # Retirer à la liste des hitboxes la hitbox

    def add_hitbox(self,hitboxObject) : # Ajouter une hitbox
        if type(hitboxObject) is Hitbox : # Si l'argument fourni est une hitbox
            self.hitboxes.append(hitboxObject) # Ajouter à la liste des hitboxes la hitbox

    def move(self,direction,step = 1) : # Déplacer le Lutin
        directions = ["up","down","right","left","stand"] # Directions valides
        if direction in directions : # Si la direction est une direction valide

            if direction == "up" : # Si c'est up

                self.y += step*DELTA_TIME # Faire monter le Lutin
                for hitbox in self.hitboxes : # Pour toutes les hitboxes
                    hitbox.y += step*DELTA_TIME # Faire monter la hitbox

            elif direction == "down" : # Si c'est down

                self.y -= step*DELTA_TIME # Faire descendre le Lutin
                for hitbox in self.hitboxes : # Pour toutes les hitboxes
                    hitbox.y -= step*DELTA_TIME # Faire monter la hitbox

            elif direction == "right" : # Si c'est right

                self.x += step*DELTA_TIME # Bouger le Lutin à droite
                for hitbox in self.hitboxes : # Pour toutes les hitboxes
                    hitbox.x += step*DELTA_TIME # Faire monter la hitbox
                    
            elif direction == "left" : # Si c'est left

                self.x -= step*DELTA_TIME # Bouger le Lutin à gauche
                for hitbox in self.hitboxes : # Pour toutes les hitboxes
                    hitbox.x -= step*DELTA_TIME # Faire monter la hitbox

        else : # Si ce n'est pas une direction valide
            raise ArgumentError("Invalid direction","direction") # Lever une exception

    def bind(self,key,direction,step) : # Lier une touche à un mouvement
        found = False # Est-ce que ce lien existe déjà
        for i in range(len(MOVE_BINDS)) : # Pour tous les liens
            if MOVE_BINDS[i].get("obj") == self and MOVE_BINDS[i].get("direction") == direction and MOVE_BINDS[i].get("key") == key : # Si le lien existe
                found = True # On à trouvé un lien !
                MOVE_BINDS[i] = {"key":key,"direction":direction,"step":step,"obj":self} # Redéfinir le lien avec une nouvelle vitesse (step)
        if found == False : # Si le lien n'est pas trouvé
            MOVE_BINDS.append({"key":key,"direction":direction,"step":step,"obj":self}) # Créer un dictionnaire et l'ajouter à la listes de liens

class PyFrameRectSprite(PyFrameSuperSprite) : # Le Lutin de rectangle, avec les même méthodes que le SuperSprite
    def __init__(self,window,x,y,w,h,centered_rendering = False) :
        """ Définition de toutes les variables """
        self.window = window
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.centered_rendering = centered_rendering
        self.hitboxes = [] # Pour stocker les hitboxes
    def render(self) : # Pour rendre le Lutin
        if self.centered_rendering : # Pour un rendu centré
            drawRect(self.window,self.x-self.width/2,self.y-self.height/2,self.width,self.height)
        else : # Pour un rendu non centré
            drawRect(self.window,self.x,self.y,self.width,self.height)

        super().render() # Appeler le rendu du SuperSprite (À compléter si besoin)