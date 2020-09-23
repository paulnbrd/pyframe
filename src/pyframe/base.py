import os, pygame, random, sys, math, pyframe

pygame.font.init()  # Initialiser les polices d'écritures
GLOBAL_WIN = False  # La fenetre de rendu par défaut
GLOBAL_FONT = pygame.font.SysFont("Arial", 30)  # La police d'écriture par défaut
BACKGROUND_COLOR = (0, 0, 0)  # La couleur de fond par défaut
PRIMARY_COLOR = (213, 63, 60)  # La couleur principale par défaut
LAST_MOUSE_POS = False
LAST_KEYS_PRESSED = False
LAST_MOUSE_STATES = False

DEBUG = True

FPS = 60  # Les FPS par défaut
DELTA_TIME_DIVIDER = 1  # Constante, permet de changer la vitesse des objets
CLOCK = pygame.time.Clock()  # La clock pygame
TIME_SPEED = 1  # La vitesse du temps, peut-être arrangée pour faire du slow-motion
ELAPSED = CLOCK.tick(FPS)
DELTA_TIME = ELAPSED / DELTA_TIME_DIVIDER * TIME_SPEED  # Le calcul du delta time

MOVE_BINDS = []  # Les binds des mouvements sont stockés ici
HITBOXES = []
BUTTONS = []  # Les boutons sont stockés ici
SPRITES = []  # Les sprites sont stockés ici
PARTICLES_availableDirections = ["up", "down", "right", "left", "all"]  # Direction de particules autorisées
PARTICLES_directionsAngle = {"up": (-90, 0), "down": (0, 90), "right": (-45, 45), "left": (45, -45)}
PARTICLES_EMITTERS = []

# Les indexs pygame des touches
AZERTY_KEY_INDEXES = {
    "a": 113,
    "b": 98,
    "c": 99,
    "d": 100,
    "e": 101,
    "f": 102,
    "g": 103,
    "h": 104,
    "i": 105,
    "j": 106,
    "k": 107,
    "l": 108,
    "m": 59,
    "n": 110,
    "o": 111,
    "p": 112,
    "q": 97,
    "r": 114,
    "s": 115,
    "t": 116,
    "u": 117,
    "v": 118,
    "w": 122,
    "x": 120,
    "y": 121,
    "z": 119
}

local_dir = os.path.dirname(__file__)  # Le chemin vers le script éxecuté


#############################################
############# =<|= Classes =|>= #############
#############################################

class Hitbox:
    """
        Voici une classe de boîte de collision.
        Qui permet de correctement simuler les...
        collisions.
        Chaque objet, pour pouvoir interagir avec
        le monde doit avoir une boîte de collision.
    """

    def __init__(self, x, y, width, height, window=False, centered_hitbox=False):
        global HITBOXES
        if window == False:
            # Si aucune fenêtre n'est fournie,
            # Définir la fenêtre de rendue comme celle globale
            self.window = GLOBAL_WIN
        else:  # Sinon
            self.window = window  # Définir la fenêtre comme celle fournie
        self.x = x  # Position x
        self.y = y  # Position y
        self.width = width  # Largeur
        self.height = height  # Longueur
        self.centered_hitbox = centered_hitbox  # La boîte de collision est centrée sur les positions x et y ?
        HITBOXES.append(self)

    def debug_render(self, color=(0, 0, 255)):  # Faire un rendu dans self.window pour le débug
        # Dessiner un rectangle à la position de la hitbox
        pyframe.utils.drawRect(self.window, self.x - self.width / 2, self.y - self.height / 2, self.width, self.height,
                               color)

    def do_hitboxes_overlap(self, hitbox):  # Est-ce que cette boîte de collision en chevauche une autre ?
        if self.x > hitbox.x + hitbox.width or hitbox.x > self.x + self.width:  # Si une est à gauche de l'autre
            return False  # Renvoyer Faux !
        elif self.y > hitbox.y + hitbox.height or hitbox.y > self.y + self.height:  # Sinon si une est au dessus de l'autre
            return False  # Retourner Faux !
        else:  # Sinon
            return True  # Retourner Vrai !


class Particle:
    """
        La classe de particule !
    """

    def __init__(self, x, y, start_velocity, radius=2, gravity=4, air_resistance=0.999, elasticity=0.750,
                 colors=[[255, 0, 0], [100, 0, 0]], window=GLOBAL_WIN, random_values=False, random_ceil=0.01,
                 image=False, lifetime=0, stay_in_window=True):
        self.x = x  # La position x
        self.base_x = x  # La position x (save pour reset)
        self.y = y  # La position y
        self.base_y = y  # La position y (save pour reset)
        self.gravity = gravity = (math.pi, gravity)  # Le vecteur de gravité

        self.random_values = random_values  # Est-ce-que il y a des valeurs aléatoires
        self.random_ceil = random_ceil  # La limite d'intervalle de valeurs aléatoires

        self.lifetime = lifetime  # La durée de vie
        self.lifetime_elapsed = 0  # Le temps écoulé depuis sa création (si move() n'est pas appelé, ne bouge pas)

        if image != False:  # Si il y une image
            self.image = image  # Définir l'image
        else:
            self.image = False  # Sinon, pas d'image

        self.air_resistance = air_resistance  # La résistance à l'air
        self.elasticity = elasticity  # Le ralentissement quand tu touche un mur

        if window == False:  # La window de render
            self.window = GLOBAL_WIN
        else:
            self.window = window
        self.radius = radius  # Le rayon de la particule

        self.velocity = start_velocity  # La vélocité de départ
        self.base_velocity = start_velocity  # La vélocité de départ (save pour reset)
        self.angle = random.uniform(0, math.pi * 2)  # Un angle aléatoire (en radians)
        self.base_angle = self.angle  # La save de l'angle

        self.velocity_ceil = 0.15  # Seuil de l'arrêt de la particule
        self.stay_in_window = stay_in_window  # La particule ne peut pas partir de la fenêtre

        # Couleur aléatoire
        if colors[0][0] > colors[1][0]:
            temp = colors[0][0]
            colors[0][0] = colors[1][0]
            colors[1][0] = temp
        if colors[0][1] > colors[1][1]:
            temp = colors[0][1]
            colors[0][1] = colors[1][1]
            colors[1][1] = temp
        if colors[0][2] > colors[1][2]:
            temp = colors[0][2]
            colors[0][2] = colors[1][2]
            colors[1][2] = temp
        self.color = (
            random.randint(colors[0][0], colors[1][0]),
            random.randint(colors[0][1], colors[1][1]),
            random.randint(colors[0][2], colors[1][2])
        )

    def reset(self):  # Reset de la particule, comme si elle venait de spawner
        self.x = self.base_x  # La position x
        self.y = self.base_y  # La position y
        self.lifetime_elapsed = 0  # Temps en vie = 0
        self.velocity = self.base_velocity  # Vélocité de base
        self.angle = self.base_angle  # Angle de base

    def render(self):  # La fonction de render
        if self.image == False:  # Si ce n'est pas une image
            pygame.draw.circle(self.window, self.color, (int(self.x), int(self.y)),
                               self.radius)  # Dessiner un cercle (la particule)
        else:  # Si c'est une image
            self.window.blit(self.image, (self.x, self.y))  # Blit l'image

    def move(self):  # Fonction de mouvements
        if self.velocity != 0:  # Si la vélocité n'est pas égale à 0
            (self.angle, self.velocity) = pyframe.utils.addVectors((self.angle, self.velocity), (
                self.gravity[0], self.gravity[1] * DELTA_TIME / 1000))  # Ajouter à la vélocité et l'angle la gravité

        width, height = pygame.display.get_surface().get_size()  # Prendre la taille de l'écran
        if self.stay_in_window:
            if self.x > width - self.radius:
                self.x = 2 * (width - self.radius) - self.x  # Faire rebondir
                self.angle = - self.angle  # Changer de direction
                self.velocity *= self.elasticity  # Perte de vitesse quand ça touche un mur
            elif self.x < self.radius:  # Pareil
                self.x = 2 * self.radius - self.x
                self.angle = - self.angle
                self.velocity *= self.elasticity
            if self.y > height - self.radius:  # Pareil
                self.y = 2 * (height - self.radius) - self.y
                self.angle = math.pi - self.angle
                self.velocity *= self.elasticity
                if self.velocity < self.velocity_ceil:
                    self.velocity = 0
            elif self.y < self.radius:  # Pareil
                self.y = 2 * self.radius - self.y
                self.angle = math.pi - self.angle
                self.velocity *= self.elasticity

        for hitbox in HITBOXES:  # Check si il y a une hitbox
            overlap = False
            if hitbox.x <= self.x + self.radius and hitbox.x + hitbox.width >= self.x + self.radius:
                overlap = True
            elif hitbox.y <= self.y + self.radius and hitbox.y + hitbox.height >= self.y + self.radius:
                overlap = True
            if overlap:
                pass  # Si ça se chevauche

        # Résistance à l'air, un peu de perte de vitesse (Plus la vitesse est grande, plus la particule perd de la vitesse)
        self.velocity *= self.air_resistance

        if self.lifetime > 0:
            self.lifetime_elapsed += ELAPSED  # Augmenter la durée depuis l'initialisation

        self.x += math.sin(self.angle) * self.velocity * DELTA_TIME  # Changer la position de la particule
        self.y -= math.cos(self.angle) * self.velocity * DELTA_TIME  # Changer la position de la particule


class ParticleSystem:
    """
        Voici un système de particules
        qui permet de gérer plein de
        particules en même temps !
    """

    def __init__(self, x, y, number_of_particles, start_velocity, particle_radius=10, gravity=0.002,
                 air_resistance=0.999, elasticity=0.750, colors=[[255, 0, 0], [200, 0, 0]], color=PRIMARY_COLOR,
                 window=GLOBAL_WIN, random_values=False, random_ceil=0.01, image_path=False, lifetime=0,
                 stay_in_window=True):
        self.x = x  # Position x
        self.y = y  # Position y
        self.number_of_particles = number_of_particles  # Nombre de particules à générer
        self.velocity = start_velocity  # La vélocité des particule (cf. Particle())
        self.color = color  # La couleur des particules (Les deux bornes)
        self.window = window  # La fenêtre de rendu
        if self.window == False:  # Si pas de fenêtre
            self.window = GLOBAL_WIN  # Fenêtre de rendu = fenêtre globale
        self.particle_radius = particle_radius  # Rayon des particules
        self.gravity = gravity  # Gravité
        self.air_resistance = air_resistance  # Résistance à l'air
        self.elasticity = elasticity  # Ralentissement quand touche un mur

        self.random_values = random_values  # Des valeurs aléatoires ?
        self.random_ceil = random_ceil  # Seuil des valeurs aléatoires

        self.lifetime = lifetime  # Durée de vie
        self.stay_in_window = stay_in_window  # Les particules restent dans la fenêtre

        if image_path != False:  # Si il y a une image
            try:
                self.image = pygame.image.load(local_dir + image_path).convert_alpha()  # Charger l'image
                self.image = pygame.transform.scale(self.image, (
                    self.particle_radius * 2, self.particle_radius * 2))  # Redimmensionner à la taille des particules
            except:  # Si il y a une erreur
                self.image = False  # Définir pas d'image
                if DEBUG:
                    print("[pyframe][alert] Could not load image " + str(image_path) + ". Using circle as placeholder")
        else:
            self.image = False  # Définir pas d'image

        self.particles = []  # Tableau des particules gérées
        for i in range(self.number_of_particles):  # Pour toutes les particules
            # Ajouter une particules avec ces attributs
            self.particles.append(
                Particle(self.x, self.y, self.velocity, radius=self.particle_radius, gravity=self.gravity,
                         air_resistance=self.air_resistance, elasticity=self.elasticity, window=self.window,
                         random_values=self.random_values, random_ceil=self.random_ceil, image=self.image,
                         lifetime=self.lifetime, stay_in_window=self.stay_in_window))

    def move(self):  # Déplacer
        for particle in self.particles:  # Pour toutes les particules
            particle.move()  # Move la particle
            if particle.lifetime > 0:  # Si le temps de vie visé est > 0
                if particle.lifetime_elapsed >= particle.lifetime:  # Si le temps de vie est dépassé
                    self.particles.remove(particle)  # Supprimer la particule du tableau
                    del particle  # Supprimer l'objet

    def render(self):  # Render
        for particle in self.particles:  # Pour toutes les particules
            particle.render()  # Rendre la particule

    def reset(self):  # Reset
        for particle in self.particles:  # Pour toutes les particules
            particle.reset()  # Reset la particule


#############################################
############# =<|= Buttons =|>= #############
#############################################


class Button:
    """
        Classe de bouton !
    """

    def __init__(self, x, y, text, command=False, width=False, height=False, horizontal_centering=False,
                 vertical_centering=False, background_color=(255, 0, 0), background_hover_color=(0, 255, 0), font=False,
                 fontsize=30, text_color=(0, 255, 0), background_image=False, image_scale_width=False,
                 image_scale_height=False):
        global BUTTONS
        BUTTONS.append(self)  # Ajouter à la liste des boutons soi-même
        self.x = x  # La position x
        self.y = y  # La position y
        self.width = width  # La longueur
        self.height = height  # La largeur

        if self.width != False and type(self.width) is not int:  # Si ce ne sont pas des int
            raise pyframe.ArgumentError("width must be integer", "width")
        if self.height != False and type(self.height) is not int:
            raise pyframe.ArgumentError("height must be integer", "height")

        self.text = text  # Le texte à afficher
        if background_image == False:  # Si il n'y a pas d'image de fond
            self.is_background_is_image = False
        else:
            if os.path.isfile(background_image):  # Si c'est une image qui existe
                self.is_background_is_image = True  # Alors c'est une image
                self.background_image = pygame.image.load(background_image).convert_alpha()  # Charger l'image

        self.command = command  # La commande a éxecuter en cas de clic
        self.horizontal_centering = horizontal_centering  # Aligner horizontalement
        self.vertical_centering = vertical_centering  # Aligner verticalement
        self.background_color = background_color  # Couleur de fond
        self.background_hover_color = background_hover_color  # Couleur de fond lorsque la souris passe au dessus
        self.text_color = text_color  # Couleur du texte
        self.background_image = background_image  # Image d'arrière plan
        self.image_scale_width = image_scale_width  # Redimmensionner l'image ?
        self.image_scale_height = image_scale_height  # Redimmensionner l'image ?
        self.font = font  # Police d'écriture
        self.fontsize = fontsize  # Taille de police

        self.pressed = False  # En train d'être pressé ?
        self.hovered = False  # En train d'être survolé par la souris ?
        self.rendered_last_frame = False  # Rendu la dernière frame ?

        if self.width != False and self.height != False:
            if self.font != False:
                self.text_rendered = pyframe.utils.render_text(self.x, self.y, self.text,
                                                               vertical_centering=self.vertical_centering,
                                                               horizontal_centering=self.horizontal_centering,
                                                               scale=True,
                                                               width=self.width, heigth=self.height, font=self.font,
                                                               fontsize=self.fontsize, color=self.text_color,
                                                               blit_to_window=False)
            else:
                self.text_rendered = pyframe.utils.render_text(self.x, self.y, self.text,
                                                               vertical_centering=self.vertical_centering,
                                                               horizontal_centering=self.horizontal_centering,
                                                               scale=True,
                                                               width=self.width, height=self.height,
                                                               color=self.text_color,
                                                               blit_to_window=False)
        else:
            if self.font != False:
                self.text_rendered = pyframe.utils.render_text(self.x, self.y, self.text,
                                                               vertical_centering=self.vertical_centering,
                                                               horizontal_centering=self.horizontal_centering,
                                                               font=self.font,
                                                               fontsize=self.fontsize, color=self.text_color,
                                                               blit_to_window=False)
            else:
                self.text_rendered = pyframe.utils.render_text(self.x, self.y, self.text,
                                                               vertical_centering=self.vertical_centering,
                                                               horizontal_centering=self.horizontal_centering,
                                                               color=self.text_color,
                                                               blit_to_window=False)
            self.width = self.text_rendered.get_width()
            self.height = self.text_rendered.get_height()

    def render(self):
        global LAST_MOUSE_POS, GLOBAL_WIN

        used_color = self.background_color
        if self.hovered:
            used_color = self.background_hover_color

        if self.horizontal_centering and self.vertical_centering:
            if self.width != False and self.height != False:
                pyframe.utils.drawRect(GLOBAL_WIN, self.x - self.width / 2, self.y - self.height / 2, self.width,
                                       self.height,
                                       color=used_color)
                GLOBAL_WIN.blit(self.text_rendered, (self.x - self.width / 2, self.y - self.height / 2))
            else:
                pyframe.utils.drawRect(GLOBAL_WIN, self.x - self.width / 2, self.y - self.height / 2,
                                       self.text_rendered.get_width(),
                                       self.text_rendered.get_height(), color=used_color)
                GLOBAL_WIN.blit(self.text_rendered, (self.x - self.width / 2, self.y - self.height / 2))
        elif self.vertical_centering and not self.horizontal_centering:
            if self.width != False and self.height != False:
                pyframe.utils.drawRect(GLOBAL_WIN, self.x, self.y - self.height / 2, self.width, self.height,
                                       color=used_color)
                GLOBAL_WIN.blit(self.text_rendered, (self.x, self.y - self.height / 2))
            else:
                pyframe.utils.drawRect(GLOBAL_WIN, self.x, self.y - self.height / 2, self.text_rendered.get_width(),
                                       self.text_rendered.get_height(), color=used_color)
                GLOBAL_WIN.blit(self.text_rendered, (self.x, self.y - self.height / 2))
        elif self.horizontal_centering and not self.vertical_centering:
            if self.width != False and self.height != False:
                pyframe.utils.drawRect(GLOBAL_WIN, self.x - self.width / 2, self.y, self.width, self.height,
                                       color=used_color)
                GLOBAL_WIN.blit(self.text_rendered, (self.x - self.width / 2, self.y))
            else:
                pyframe.utils.drawRect(GLOBAL_WIN, self.x - self.width / 2, self.y, self.text_rendered.get_width(),
                                       self.text_rendered.get_height(), color=used_color)
                GLOBAL_WIN.blit(self.text_rendered, (self.x - self.width / 2, self.y))
        else:
            if self.width != False and self.height != False:
                pyframe.utils.drawRect(GLOBAL_WIN, self.x, self.y, self.width, self.height, color=used_color)
                GLOBAL_WIN.blit(self.text_rendered, (self.x, self.y))
            else:
                pyframe.utils.drawRect(GLOBAL_WIN, self.x, self.y, self.text_rendered.get_width(),
                                       self.text_rendered.get_height(),
                                       color=used_color)
                GLOBAL_WIN.blit(self.text_rendered, (self.x, self.y))

        self.rendered_last_frame = True

    def is_clicked(self):
        global LAST_MOUSE_POS, LAST_KEYS_PRESSED, LAST_MOUSE_STATES

        if LAST_MOUSE_STATES[0] == 0:
            self.pressed = False

        if self.horizontal_centering and self.vertical_centering:
            if self.x - self.width / 2 <= LAST_MOUSE_POS[0] and self.x + self.width - self.width / 2 >= LAST_MOUSE_POS[
                0] and self.y - self.height / 2 <= LAST_MOUSE_POS[1] <= self.y + self.height - self.height / 2:
                self.hovered = True
                if LAST_MOUSE_STATES[0] == 1 and self.pressed == False:
                    self.pressed = True
                    return True
            else:
                self.hovered = False
            return False
        elif self.horizontal_centering and not self.vertical_centering:
            if self.x - self.width / 2 <= LAST_MOUSE_POS[0] and self.x + self.width - self.width / 2 >= LAST_MOUSE_POS[
                0] and self.y <= LAST_MOUSE_POS[1] <= self.y + self.height:
                self.hovered = True
                if LAST_MOUSE_STATES[0] == 1 and self.pressed == False:
                    self.pressed = True
                return True
            else:
                self.hovered = False
            return False
        elif self.vertical_centering and not self.horizontal_centering:
            if self.x <= LAST_MOUSE_POS[0] and self.x + self.width >= LAST_MOUSE_POS[0] and self.y - self.height / 2 <= \
                    LAST_MOUSE_POS[1] and self.y + self.height - self.height / 2 >= LAST_MOUSE_POS[1]:
                self.hovered = True
                if LAST_MOUSE_STATES[0] == 1 and self.pressed == False:
                    self.pressed = True
                return True
            else:
                self.hovered = False
            return False
        else:
            if self.x <= LAST_MOUSE_POS[0] and self.x + self.width >= LAST_MOUSE_POS[0] and self.y <= LAST_MOUSE_POS[
                1] and self.y + self.height >= LAST_MOUSE_POS[1]:
                self.hovered = True
                if LAST_MOUSE_STATES[0] == 1 and self.pressed == False:
                    self.pressed = True
                return True
            else:
                self.hovered = False
            return False
        return False


class ProgressBar:
    """
        Une classe de barre de progression :-)
    """

    def recompute_percentage(self):  # Recalculer le pourcentage
        self.percent = self.value / self.maximum * 100  # Redéfinition du pourcentage
        return self.percent  # Retourner la nouvelle valeur (en général, pas utile)

    def __init__(self, value, maximum, padding=0, progress_color=PRIMARY_COLOR, background_color=BACKGROUND_COLOR,
                 window=GLOBAL_WIN):
        """
            value (int) = Valeur de base
            maximum (int) = Valeur maximum de la barre
            padding (int) = Espace en px entre le bord de la barre de progression et la progression en elle-même, valeur par défaut à 0
            progress_bar (tuple) = Valeur rgb de couleur de la progression en elle-même, valeur par défaut à la valeur de la globale PRIMARY_COLOR,
                PRIMARY_COLOR pouvant être changé, la couleur restera la même que la valeur de PRIMARY_COLOR à l'initialisation de la barre de
                progression
            background_color (tuple) = Valeur rgb de couleur de la barre de progression, valeur par défaut à la valeur de la globale BACKGROUND_COLOR,
                BACKGROUND_COLOR pouvant être changé, la couleur restera la même que la valeur de BACKGROUND_COLOR à l'initialisation de la barre de
                progression
            window (pygame.Surface) = Fenêtre de rendu de la barre de progression, valeur par défaut à la valeur de la globale GLOBAL_WIN,
                GLOBAL_WIN pouvant être changé, la fenêtre de rendu restera la même que la valeur de GLOBAL_WIN à l'initialisation de la barre de
                progression
        """

        self.value = value;
        pyframe.utils.verify_arg_type(self.value, "value", int)
        self.maximum = maximum;
        pyframe.utils.verify_arg_type(self.maximum, "maximum", int)
        self.recompute_percentage();
        pyframe.utils.verify_arg_type(self.percent, "percent", int)
        self.recompute_percentage_on_render = True
        self.window = window;
        pyframe.utils.verify_arg_type(self.window, "window", pygame.Surface)
        self.background_color = background_color;
        pyframe.utils.verify_arg_type(self.background_color, "background_color", tuple)
        self.progress_color = progress_color;
        pyframe.utils.verify_arg_type(self.progress_color, "progress_color", tuple)
        self.padding = padding;
        pyframe.utils.verify_arg_type(self.padding, "padding", int)

    def render(self):
        if self.recompute_percentage_on_render:
            self.recompute_percentage()
        pyframe.utils.drawRect(self.window, self.x, self.y, self.width + self.padding * 2, self.height + self.padding * 2,
                 self.background_color)
        size = self.width / 100 * self.percent
        pyframe.utils.drawRect(self.window, self.x + self.padding, self.y + self.padding, size, self.height, self.progress_color)


#############################################
############# =<|= Display =|>= #############
#############################################

class Display:
    def __init__(self, sprites=[]):
        self.sprites = sprites

    def render(self):
        for sprite in self.sprites:
            if "render" in dir(sprite):
                sprite.render()

    def move(self):
        for sprite in self.sprites:
            if "move" in dir(sprite):
                sprite.move()


#############################################
############# =<|= Sprites =|>= #############
#############################################

class PyFrameSuperSprite:  # La classe de Lutin de base
    def render(self):  # Ajouter des choses ici si besoin au moment du render
        pass

    def remove_hitbox(self, hitboxObject):  # Retirer une hitbox
        if type(hitboxObject) is Hitbox:  # Si l'argument fourni est une hitbox
            self.hitboxes.remove(hitboxObject)  # Retirer à la liste des hitboxes la hitbox

    def add_hitbox(self, hitboxObject):  # Ajouter une hitbox
        if type(hitboxObject) is Hitbox:  # Si l'argument fourni est une hitbox
            self.hitboxes.append(hitboxObject)  # Ajouter à la liste des hitboxes la hitbox

    def move(self, direction, step=1):  # Déplacer le Lutin
        directions = ["up", "down", "right", "left", "stand"]  # Directions valides
        if direction in directions:  # Si la direction est une direction valide

            if direction == "up":  # Si c'est up

                self.y += step * DELTA_TIME  # Faire monter le Lutin
                for hitbox in self.hitboxes:  # Pour toutes les hitboxes
                    hitbox.y += step * DELTA_TIME  # Faire monter la hitbox

            elif direction == "down":  # Si c'est down

                self.y -= step * DELTA_TIME  # Faire descendre le Lutin
                for hitbox in self.hitboxes:  # Pour toutes les hitboxes
                    hitbox.y -= step * DELTA_TIME  # Faire monter la hitbox

            elif direction == "right":  # Si c'est right

                self.x += step * DELTA_TIME  # Bouger le Lutin à droite
                for hitbox in self.hitboxes:  # Pour toutes les hitboxes
                    hitbox.x += step * DELTA_TIME  # Faire monter la hitbox

            elif direction == "left":  # Si c'est left

                self.x -= step * DELTA_TIME  # Bouger le Lutin à gauche
                for hitbox in self.hitboxes:  # Pour toutes les hitboxes
                    hitbox.x -= step * DELTA_TIME  # Faire monter la hitbox

        else:  # Si ce n'est pas une direction valide
            raise pyframe.ArgumentError("Invalid direction", "direction")  # Lever une exception

    def bind(self, key, direction, step):  # Lier une touche à un mouvement
        found = False  # Est-ce que ce lien existe déjà
        for i in range(len(MOVE_BINDS)):  # Pour tous les liens
            if MOVE_BINDS[i].get("obj") == self and MOVE_BINDS[i].get("direction") == direction and MOVE_BINDS[i].get(
                    "key") == key:  # Si le lien existe
                found = True  # On à trouvé un lien !
                MOVE_BINDS[i] = {"key": key, "direction": direction, "step": step,
                                 "obj": self}  # Redéfinir le lien avec une nouvelle vitesse (step)
        if found == False:  # Si le lien n'est pas trouvé
            MOVE_BINDS.append({"key": key, "direction": direction, "step": step,
                               "obj": self})  # Créer un dictionnaire et l'ajouter à la listes de liens


class PyFrameRectSprite(PyFrameSuperSprite):  # Le Lutin de rectangle, avec les même méthodes que le SuperSprite
    def __init__(self, window, x, y, w, h, centered_rendering=False):
        """ Définition de toutes les variables """
        self.window = window
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.centered_rendering = centered_rendering
        self.hitboxes = []  # Pour stocker les hitboxes

    def render(self):  # Pour rendre le Lutin
        if self.centered_rendering:  # Pour un rendu centré
            pyframe.utils.drawRect(self.window, self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
        else:  # Pour un rendu non centré
            pyframe.utils.drawRect(self.window, self.x, self.y, self.width, self.height)

        super().render()  # Appeler le rendu du SuperSprite (À compléter si besoin)
