import os, pygame, random, sys, math

pygame.font.init() # Initialiser les polices d'écritures
GLOBAL_WIN = False # La fenetre de rendu par défaut
GLOBAL_FONT = pygame.font.SysFont("Arial", 30) # La police d'écriture par défaut
BACKGROUND_COLOR = (0,0,0) # La couleur de fond par défaut
PRIMARY_COLOR = (213,63,60) # La couleur principale par défaut
LAST_MOUSE_POS = False
LAST_KEYS_PRESSED = False
LAST_MOUSE_STATES = False

FPS = 60 # Les FPS par défaut
DELTA_TIME_DIVIDER = 1 # Constante, permet de changer la vitesse des objets
CLOCK = pygame.time.Clock() # La clock pygame
TIME_SPEED = 1 # La vitesse du temps, peut-être arrangée pour faire du slow-motion
ELAPSED = CLOCK.tick(FPS)
DELTA_TIME = ELAPSED/DELTA_TIME_DIVIDER*TIME_SPEED # Le calcul du delta time

MOVE_BINDS = [] # Les binds des mouvements sont stockés ici
HITBOXES = []
BUTTONS = [] # Les boutons sont stockés ici
SPRITES = [] # Les sprites sont stockés ici
PARTICLES_availableDirections = ["up","down","right","left","all"] # Direction de particules autorisées
PARTICLES_directionsAngle = {"up":(-90,0),"down":(0,90),"right":(-45,45),"left":(45,-45)}
PARTICLES_EMITTERS = []

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
    global DELTA_TIME,ELAPSED,LAST_KEYS_PRESSED,LAST_MOUSE_POS, LAST_MOUSE_STATES,BUTTONS
    """
        Voici la boucle d'évenements qui doit être appellée
        à chaque itération de la mainloop de pygame
        à chaque frame quoi. Après un clear de l'écran,
        car des render peuvent y être fait
    """
    ELAPSED = CLOCK.tick(FPS)
    DELTA_TIME = ELAPSED/DELTA_TIME_DIVIDER*TIME_SPEED # Le calcul du delta time
    keys = pygame.key.get_pressed() # Récupérer les touches appuyés
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    LAST_MOUSE_POS = (mouse_pos_x,mouse_pos_y)
    LAST_KEYS_PRESSED = keys
    LAST_MOUSE_STATES = mouse_pressed

    for bind in MOVE_BINDS : # Pour tous les binds
        if keys[bind.get("key")] : # Si la touche du bind est appuyée
            bind.get("obj").move(bind.get("direction"),bind.get("step")) # Déplacer l'objet

    for emitter in PARTICLES_EMITTERS :
        emitter.particle_system.move()
        emitter.particle_system.render()

    for bouton in BUTTONS :
        if bouton.command != False :
            if bouton.is_clicked() :
                bouton.command(bouton)

        bouton.rendered_last_frame = False

def drawRect(window,x,y,w,h,color = PRIMARY_COLOR) : # Dessiner un rectangle
    pygame.draw.rect(window,color,(x,y,w,h)) # La fonction de pygame

def render_text(x,y,text,color = PRIMARY_COLOR,vertical_centering = False,horizontal_centering = False,font = False,fontsize = 30,window = False,scale = False,width = False,height = False,blit_to_window = True) :
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

    if scale :
        if width != False and height != False :
            text = pygame.transform.scale(text,(width,height))
        else: 
            raise ArgumentError("Scale need width and height arguments","width,height")

    if blit_to_window :
        window.blit(text,(x,y)) # Le coller dans la fenêtre

    return text

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
        global HITBOXES
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
        HITBOXES.append(self)

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


def addVectors(v1, v2): # v[0] = Angle, v[1] = length
    x = math.sin(v1[0]) * v1[1] + math.sin(v2[0]) * v2[1]
    y = math.cos(v1[0]) * v1[1] + math.cos(v2[0]) * v2[1]

    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return (angle, length)

class Particle :
    def __init__(self,x,y,start_velocity, radius = 2, gravity = 0.002,air_resistance = 0.999,elasticity = 0.750, colors = [[255,0,0],[100,0,0]] ,window = GLOBAL_WIN,random_values = False,random_ceil=0.01, image = False, lifetime = 0) :
        self.x = x
        self.base_x = x
        self.y = y
        self.base_y = y
        self.window = window
        self.gravity = gravity = (math.pi, gravity)

        self.random_values = random_values
        self.random_ceil = random_ceil

        self.lifetime = lifetime
        self.lifetime_elapsed = 0

        if image != False :
            self.image = image
        else :
            self.image = False

        self.air_resistance = air_resistance
        self.elasticity = elasticity

        if self.window == False :
            self.window = GLOBAL_WIN
        self.radius = radius

        self.velocity = start_velocity
        self.base_velocity = start_velocity
        self.angle = random.uniform(0, math.pi*2)
        self.base_angle = self.angle

        self.velocity_ceil = 0.15

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
    def reset(self) :
        self.x = self.base_x
        self.y = self.base_y
        self.lifetime_elapsed = 0
        self.velocity = self.base_velocity
        self.angle = self.base_angle
    def render(self) :
        if self.image == False :
            pygame.draw.circle(self.window,self.color,(int(self.x),int(self.y)),self.radius)
        else :
            self.window.blit(self.image,(self.x,self.y))
    def move(self) :
        if self.velocity != 0 :
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
            if self.velocity < self.velocity_ceil :
                self.velocity = 0
        elif self.y < self.radius:
            self.y = 2 * self.radius - self.y
            self.angle = math.pi - self.angle
            self.velocity *= self.elasticity

        for hitbox in HITBOXES :
            overlap = False
            if hitbox.x <= self.x+self.radius and hitbox.x+hitbox.width >= self.x+self.radius :
                overlap = True
            elif hitbox.y <= self.y+self.radius and hitbox.y+hitbox.height >= self.y+self.radius :
                overlap = True
            if overlap :
                pass # Si ça se chevauche


        # Résistance à l'air, un peu de perte de vitesse (Plus la vitesse est grande, plus la particule perd de la vitesse)
        self.velocity *= self.air_resistance

        if self.lifetime > 0 :
            self.lifetime_elapsed += ELAPSED # Augmenter la durée depuis l'initialisation

class ParticleSystem :
    def __init__(self,x,y,number_of_particles,start_velocity,particle_radius = 10, gravity = 0.002,air_resistance = 0.999,elasticity = 0.750,colors = [[255,0,0],[200,0,0]],color = PRIMARY_COLOR,window = GLOBAL_WIN,random_values = False,random_ceil = 0.01,image_path = False,lifetime = 0) :
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

        self.random_values = random_values
        self.random_ceil = random_ceil

        self.lifetime = lifetime
        
        if image_path != False :
            try :
                self.image = pygame.image.load(local_dir+image_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.particle_radius*2, self.particle_radius*2))
            except :
                self.image = False
                print("[pyframe][alert] Could not load image "+str(image_path)+". Using circle as placeholder")
        else :
            self.image = False

        self.particles = []
        for i in range(self.number_of_particles) :
            self.particles.append(Particle(self.x,self.y,self.velocity,radius = self.particle_radius,gravity = self.gravity,air_resistance = self.air_resistance,elasticity = self.elasticity,window = self.window,random_values = self.random_values,random_ceil=self.random_ceil,image = self.image,lifetime=self.lifetime))
    def move(self): 
        for particle in self.particles :
            particle.move()
            if particle.lifetime > 0 :
                if particle.lifetime_elapsed >= particle.lifetime :
                    self.particles.remove(particle)
                    del particle
    def render(self): 
        for particle in self.particles :
            particle.render()
    def reset(self) :
        for particle in self.particles :
            particle.reset()



#############################################
############# =<|= Buttons =|>= #############
#############################################


class Button :
    def __init__(self,x,y,text,command = False,width = False, height = False,horizontal_centering = False,vertical_centering = False,background_color = (255,0,0),font = False,fontsize = 30,text_color = (0,255,0),background_image = False,image_scale_width = False,image_scale_height = False) :
        global BUTTONS
        BUTTONS.append(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        if self.width != False and type(self.width) is not int :
            raise ArgumentError("width must be integer","width")
        if self.height != False and type(self.heigth) is not int :
            raise ArgumentError("height must be integer","height")

        self.text = text
        if background_image == False :
            self.is_background_is_image = False
        else :
            if os.path.isfile(background_image) :
                self.is_background_is_image = True
                self.background_image = pygame.image.load(background_image).convert_alpha()

        self.command = command
        self.horizontal_centering = horizontal_centering
        self.vertical_centering = vertical_centering
        self.background_color = background_color
        self.text_color = text_color
        self.background_image = background_image
        self.image_scale_width = image_scale_width
        self.image_scale_height = image_scale_height
        self.font = font
        self.fontsize = fontsize

        self.pressed = True
        self.rendered_last_frame = False

        if self.width != False and self.height != False :
            if self.font != False :
                self.text_rendered = render_text(self.x,self.y,self.text,vertical_centering=self.vertical_centering,horizontal_centering=self.horizontal_centering,scale=True,width=self.width,heigth=self.height,font = self.font,fontsize = self.fontsize,color=self.text_color,blit_to_window = False)
            else :
                self.text_rendered = render_text(self.x,self.y,self.text,vertical_centering=self.vertical_centering,horizontal_centering=self.horizontal_centering,scale=True,width=self.width,heigth=self.height,color=self.text_color,blit_to_window = False)
        else :
            if self.font != False :
                self.text_rendered = render_text(self.x,self.y,self.text,vertical_centering=self.vertical_centering,horizontal_centering=self.horizontal_centering,font=self.font,fontsize=self.fontsize,color=self.text_color,blit_to_window = False)
            else :
                self.text_rendered = render_text(self.x,self.y,self.text,vertical_centering=self.vertical_centering,horizontal_centering=self.horizontal_centering,color=self.text_color,blit_to_window = False)
            self.width = self.text_rendered.get_width()
            self.height = self.text_rendered.get_height()

    def render(self) :
        global LAST_MOUSE_POS,GLOBAL_WIN


        if self.width != False and self.height != False :
            drawRect(GLOBAL_WIN,self.x,self.y,self.width,self.height,color=self.background_color)
            GLOBAL_WIN.blit(self.text_rendered,(self.x,self.y))
        else :
            drawRect(GLOBAL_WIN,self.x,self.y,self.text_rendered.get_width(),self.text_rendered.get_height(),color=self.background_color)
            GLOBAL_WIN.blit(self.text_rendered,(self.x,self.y))

        self.rendered_last_frame = True

    def is_clicked(self) :
        global LAST_MOUSE_POS,LAST_KEYS_PRESSED, LAST_MOUSE_STATES

        if LAST_MOUSE_STATES[0] == 0 :
            self.pressed = False

        if self.x <= LAST_MOUSE_POS[0] and self.x+self.width >= LAST_MOUSE_POS[0] and self.y <= LAST_MOUSE_POS[1] and self.y+self.height >= LAST_MOUSE_POS[1] and LAST_MOUSE_STATES[0] == 1 and self.pressed == False :
            self.pressed = True
            return True
        return False


#############################################
############# =<|= Display =|>= #############
#############################################

class Display :
    def __init__(self,sprites = []) :
        self.sprites = sprites
    def render(self) :
        for sprite in self.sprites :
            if "render" in dir(sprite) :
                sprite.render()
    def move(self) :
        for sprite in self.sprites :
            if "move" in dir(sprite) :
                sprite.move()

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