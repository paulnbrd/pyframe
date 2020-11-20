import pygame, os, sys, pyframe, math, random, time
from collections.abc import Sequence
import numpy as np
import sys,io

tmp = sys.stdout
sys.stdout = io.StringIO()
import pymunk
sys.stdout = tmp

pygame.init()
pygame.font.init()
pygame.mixer.init()

__all__ = [
    "Particle",
    "ParticleEmitter",
    "IntervalEmitter",
    "Graph",
    "Button",
    "Reflection"
]

class Particle:
    def __init__(
            # Voir ParticleEmitter 123:7 pour signification des arguments
            self,
            x,
            y,
            surface,
            stay_in_window=False,
            radius=2,
            gravity=4,
            color=(255, 0, 0),
            start_velocity=1,
            velocity_randomness=0.1,
            air_resistance=0.999,
            elasticity=0.750,
            colliders=None,
            lifetime=0,
            reduce_radius_over_time=False,
            reduce_each=None,
            angle_borne_haute=math.pi * 2,
            angle_borne_basse=0,
            image=None,
            image_base_scale=1,
            image_blur=1
    ):
        if colliders is None:
            colliders = []
        self.x, self.y = x, y
        self.surface = surface
        self.stay_in_window = stay_in_window
        self.radius = radius
        self.base_radius = radius
        self.color = color
        self.velocity = random.uniform(start_velocity - velocity_randomness, start_velocity + velocity_randomness)
        self.air_resistance = air_resistance
        self.elasticity = elasticity
        self.colliders = colliders
        self.lifetime = random.randint(lifetime - 150, lifetime + 150)
        self.lifetime_elapsed = 0
        self.reduce_radius_over_time = reduce_radius_over_time
        self.reduce_each = reduce_each
        self.image = image
        self.image_base_scale = image_base_scale
        self.image_blur = image_blur
        if self.image is not None:
            self.image = pygame.image.load(self.image).convert_alpha()
            self.image = pygame.transform.scale(self.image, (
                int(self.image.get_width() * self.image_base_scale),
                int(self.image.get_height() * self.image_base_scale)))
            self.image_base_width = self.image.get_width()
            self.image_base_height = self.image.get_height()
            self.image = pyframe.functions.blur_surf(self.image, self.image_blur)

        self.gravity = (math.pi, gravity)
        self.angle = random.uniform(angle_borne_basse, angle_borne_haute)

    def __str__(self):

        return "<PyFrame Particle x=" + str(self.x) + " y=" + str(self.y) + " velocity=" + str(self.velocity) + ">"

    def scale_image_to_radius(self, image):
        surf = pygame.transform.smoothscale(image, (
            int(int(self.image_base_width * self.radius) / 100), int(int(self.image_base_height * self.radius) / 100)))
        # facteur = 2
        # rapport = ( 255*(self.radius/self.base_radius)**facteur)/255**facteur
        # alpha =  255*rapport*255
        # alpha = 255
        # print(alpha)
        # surf.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        return surf

    def render(self):
        if self.alive():
            if self.image is None:
                pygame.draw.circle(self.surface, self.color, (int(self.x), int(self.y)), self.radius)
            else:
                self.image = self.scale_image_to_radius(self.image)
                center = self.image.get_rect().center
                self.surface.blit(self.image, (int(self.x - center[0]), int(self.y - center[1])))

    def bounce(self):
        """
        Attention, cette fonction est buggée, ne pas trop utiliser pour faire rebondir en bas d'une surface
        """
        width, height = self.surface.get_size()
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
        elif self.y < self.radius:  # Pareil
            self.y = 2 * self.radius - self.y
            self.angle = math.pi - self.angle
            self.velocity *= self.elasticity

    def update(self, tick=0):
        """
        Permet de mettre à jour la position et la vitesse de la particule
        :param tick: Le temps écoulé depuis le dernier appel à cette fonction
        :return: Retourne la nouvelle valeur x et y de la particule
        """
        if self.velocity != 0:
            self.angle, self.velocity = pyframe.functions.add_vectors((self.angle, self.velocity),
                                                                      (self.gravity[0], self.gravity[1] * tick))

        if self.stay_in_window:
            self.bounce()

        # self.velocity *= self.air_resistance # Compliqué avec tick

        if self.lifetime > 0:
            self.lifetime_elapsed += tick
            if self.reduce_radius_over_time and self.reduce_each is not None:
                try:
                    self.radius = self.base_radius / round(self.lifetime_elapsed / self.reduce_each)
                except ZeroDivisionError:
                    pass

        self.x += math.sin(self.angle) * self.velocity * tick
        self.y -= math.cos(self.angle) * self.velocity * tick
        return self.x, self.y

    def alive(self):
        if self.lifetime < self.lifetime_elapsed:
            return False
        return True


class ParticleEmitter:
    """
    Un objet qui permet de générer un certain nombre de particule
    """

    def __init__(
            self,
            nb,  # Nombre de particules
            x,  # Pos x
            y,  # Pos y
            surface,  # Surface ou rendre la particule
            stay_in_window=False,  # Reste dans la fenêtre ? (Expérimental)
            radius=2,
            gravity=0.001,
            color=(255, 0, 0),
            start_velocity=0.7,
            velocity_randomness=0.5,
            air_resistance=0.999,
            elasticity=0.750,
            colliders=None,
            lifetime=0,
            reduce_radius_over_time=False,
            reduce_each=None,
            angle_borne_haute=math.pi * 2,
            angle_borne_basse=0,
            image=None,
            image_base_scale=1,
            image_blur=1
    ):
        self.nb = nb
        self.particles = []

        self.x, self.y = x, y
        self.surface = surface
        self.stay_in_window = stay_in_window
        self.radius = radius
        self.gravity = gravity
        self.color = color
        self.velocity = start_velocity
        self.velocity_randomness = velocity_randomness
        self.air_resistance = air_resistance
        self.elasticity = elasticity
        self.colliders = colliders
        self.lifetime = lifetime
        self.reduce_radius_over_time = reduce_radius_over_time
        self.reduce_each = reduce_each
        self.angle_borne_haute = angle_borne_haute
        self.angle_borne_basse = angle_borne_basse
        self.image = image
        self.image_base_scale = image_base_scale
        self.blur = image_blur

    def new_particle(self):
        return Particle(
            x=self.x,
            y=self.y,
            surface=self.surface,
            stay_in_window=self.stay_in_window,
            radius=self.radius,
            gravity=self.gravity,
            color=self.color,
            start_velocity=self.velocity,
            velocity_randomness=self.velocity_randomness,
            air_resistance=self.air_resistance,
            elasticity=self.elasticity,
            colliders=self.colliders,
            lifetime=self.lifetime,
            reduce_radius_over_time=self.reduce_radius_over_time,
            reduce_each=self.reduce_each,
            angle_borne_haute=self.angle_borne_haute,
            angle_borne_basse=self.angle_borne_basse,
            image=self.image,
            image_base_scale=self.image_base_scale,
            image_blur=self.blur
        )

    def generate(self):
        for i in range(self.nb):
            self.particles.append(self.new_particle())

    def update(self, tick):
        for p in self.particles:
            p.update(tick)
            if not p.alive():
                self.particles.remove(p)
                del p

    def render(self):
        for p in self.particles:
            p.render()


class IntervalEmitter:
    """
    Un objet qui permet de générer un certain nombre de particule
    """

    def __init__(
            self,
            nb_init: int,  # Nombre de particules
            interval: int,
            x: int,  # Pos x
            y: int,  # Pos y
            surface: pygame.surface.Surface,  # Surface ou rendre la particule
            stay_in_window: bool = False,  # Reste dans la fenêtre ? (Expérimental)
            radius: int = 2,
            gravity: float = 0.001,
            color: tuple = (255, 0, 0),
            start_velocity: float = 0.7,
            velocity_randomness: float = 0.5,
            air_resistance: float = 0.999,
            elasticity: float = 0.750,
            colliders: Sequence[list, None] = None,
            lifetime: int = 0,
            reduce_radius_over_time: bool = False,
            reduce_each: Sequence[None, int] = None,
            angle_borne_haute: float = math.pi * 2,
            angle_borne_basse: float = 0,
            image: Sequence[pygame.surface.Surface, None] = None,
            image_base_scale: float = 1,
            image_blur: float = 1
    ) -> None:
        self.nb = nb_init
        self.particles = []

        self.x, self.y = x, y
        self.surface = surface
        self.stay_in_window = stay_in_window
        self.radius = radius
        self.gravity = gravity
        self.color = color
        self.velocity = start_velocity
        self.velocity_randomness = velocity_randomness
        self.air_resistance = air_resistance
        self.elasticity = elasticity
        self.colliders = colliders
        self.lifetime = lifetime
        self.reduce_radius_over_time = reduce_radius_over_time
        self.reduce_each = reduce_each
        self.angle_borne_haute = angle_borne_haute
        self.angle_borne_basse = angle_borne_basse
        self.image = image
        self.image_base_scale = image_base_scale
        self.blur = image_blur

        self.interval = interval
        self.last_add = 0

    def new_particle(self) -> Particle:
        return Particle(
            x=self.x,
            y=self.y,
            surface=self.surface,
            stay_in_window=self.stay_in_window,
            radius=self.radius,
            gravity=self.gravity,
            color=self.color,
            start_velocity=self.velocity,
            velocity_randomness=self.velocity_randomness,
            air_resistance=self.air_resistance,
            elasticity=self.elasticity,
            colliders=self.colliders,
            lifetime=self.lifetime,
            reduce_radius_over_time=self.reduce_radius_over_time,
            reduce_each=self.reduce_each,
            angle_borne_haute=self.angle_borne_haute,
            angle_borne_basse=self.angle_borne_basse,
            image=self.image,
            image_base_scale=self.image_base_scale,
            image_blur=self.blur
        )

    def generate(self) -> None:
        for i in range(self.nb):
            self.particles.append(self.new_particle())

    def update(self, tick) -> None:
        for p in self.particles:
            p.update(tick)
            if not p.alive():
                self.particles.remove(p)
                del p

        self.last_add += tick
        while self.last_add > self.interval:
            self.particles.append(self.new_particle())
            self.last_add -= self.interval

    def render(self) -> None:
        for p in self.particles:
            p.render()


"""
   _____ _____            _____  _    _  _____ 
  / ____|  __ \     /\   |  __ \| |  | |/ ____|
 | |  __| |__) |   /  \  | |__) | |__| | (___  
 | | |_ |  _  /   / /\ \ |  ___/|  __  |\___ \ 
 | |__| | | \ \  / ____ \| |    | |  | |____) |
  \_____|_|  \_\/_/    \_\_|    |_|  |_|\_____/        

    Graphs
"""


# TODO : Optimiser
# TODO : Changer le texte dans l'exemple __main__.py : il est noté que la classe n'est pas optimisée
class Graph:
    """
        Permet de créer des graphiques
        avec pygame
    """

    def __init__(self,
                 size: tuple = (500, 200),
                 font: pygame.font.Font = pygame.font.SysFont("Arial", 18),
                 max_values: int = 1000,
                 titre: str = "",
                 fill_with = None
                 ) -> None:
        """
            Permet de tracer un graphique (voir Graph.get_surface())
            :param size: La taille du graphique
            :param font: La police d'écriture du graphique
            :param max_values: Le nombre maximum de valeurs
            :param fill_with: La valeur de base, le tableau de valeur sera rempli avec cette valeur
        """
        self.surface = pygame.surface.Surface(size)
        self.font = font
        self.titre = titre

        self.max_values = max_values
        self.values = []
        if fill_with is not None :
            for i in range(self.max_values) :
                self.values.append(fill_with)

    def polish_values(self,nb:int = None) :
        if len(self.values) > 3 :
            if nb is None :
                for i in range(1,len(self.values)-1) :
                    self.values[i] = (self.values[i-1]+self.values[i+1])/2
            else :
                for i in range(len(self.values)-1-nb,len(self.values)-1) :
                    self.values[i] = (self.values[i-1]+self.values[i+1])/2
    def polish_last_value(self) :
        if len(self.values) > 3 :
            self.values[ len(self.values)-2 ] = (self.values[len(self.values)-3]+self.values[len(self.values)-1])/2

    def get_surface(self, size:tuple[int,int]=None,auto_render:bool = False) -> pygame.surface.Surface:
        if auto_render : self.render()
        if size is None:
            size = self.surface.get_size()
        surf = pygame.transform.scale(self.surface, size)
        return surf

    def add_value(self, new_value) -> None:
        """
            Ajoute une nouvelle valeur à la liste des valeurs
        """
        assert type(new_value) is int or float
        self.values.append(new_value)
        while len(self.values) > self.max_values:
            self.values.pop(0)

    def render(self) -> None:
        self.surface.fill((0, 0, 0))

        borne_haute = pyframe.functions.get_biggest(self.values)
        # borne_haute += borne_haute * 0.1
        borne_basse = pyframe.functions.get_smallest(self.values)
        # borne_basse += borne_basse * 0.1
        borne_haute -= borne_basse

        points = []
        h = self.surface.get_height()

        for v in self.values:
            try:
                rapport = (v - borne_basse) / borne_haute
                points.append(h - rapport * h)
            except ZeroDivisionError:
                pass

        pygame.draw.line(self.surface, (255, 255, 255), (0, 0), (0, self.surface.get_height()))
        pygame.draw.line(self.surface, (255, 255, 255), (0, self.surface.get_height() - 1),
                         (self.surface.get_width(), self.surface.get_height() - 1))
        texte_borne_haute = self.font.render(str(round(borne_haute + borne_basse)), True, (255, 255, 255))
        self.surface.blit(texte_borne_haute, (2, 0))
        texte_borne_basse = self.font.render(str(round(borne_basse)), True, (255, 255, 255))
        self.surface.blit(texte_borne_basse, (2, h - texte_borne_basse.get_height()))
        titre = self.font.render(str(self.titre), True, (255, 255, 255))
        self.surface.blit(titre, (self.surface.get_width() - titre.get_width(), 0))

        w = self.surface.get_width()
        if len(points) > 1:
            espace = w / (len(points) - 1)
            for p in range(len(points) - 1):
                try:
                    pygame.draw.line(
                        self.surface,
                        (255, 0, 0),
                        (espace * p, points[p]),
                        (espace * (p + 1), points[p + 1])
                    )
                except:
                    pass
        elif len(points) == 1:
            pygame.draw.circle(
                self.surface,
                (255, 0, 0),
                (0, points[0]),
                2
            )


"""
  ____  _    _ _______ _______ ____  _   _  _____ 
 |  _ \| |  | |__   __|__   __/ __ \| \ | |/ ____|
 | |_) | |  | |  | |     | | | |  | |  \| | (___  
 |  _ <| |  | |  | |     | | | |  | | . ` |\___ \ 
 | |_) | |__| |  | |     | | | |__| | |\  |____) |
 |____/ \____/   |_|     |_|  \____/|_| \_|_____/ 
                                                  
    Buttons                               
"""


class Button(pygame.sprite.Sprite):
    """
        (C'est un pygame.sprite.Sprite parce que ce peut être utile)
    """

    def __init__(
            self,
            text: str = "", # Le texte affiché sur le bouton
            font:pygame.font.Font = pygame.font.SysFont("Arial",18),
            padding:int = 5,
            color: tuple[int,int,int] = (0,0,0), # La couleur du texte sur le bouton
            background_color: tuple[int,int,int] = (255,255,255), # La couleur de fond
            border_color: tuple[int,int,int] = (0,0,0), # Couleur de la bordure
            border_size:int = 2, # Largeur (en px) de la bordure
            hover_color: tuple[int,int,int] = (255,255,255), # La couleur du texte au survol
            hover_background_color: tuple[int,int,int] = (0,0,0), # La couleur de fond au survol
            hover_border_color: tuple[int,int,int] = (255,255,255), # La couleur de la bordure au survol
            state:str = "normal",
            surface: pygame.surface.Surface = None,
            position: tuple[int,int] = None
    ) -> None:
        """
            Créé un nouveau bouton, qui peut être intégré n'importe où ou presque
        :param text: Le texte affiché sur le bouton
        :param font: La police d'écriture avec laquelle rendre le texte
        :param padding: Comme en CSS, la distance (en px) entre le cadre intérieur et le texte (la bordure du texte)
        :param color: La couleur (format rgb) du texte lorsque le bouton est en state "normal"
        :param background_color: La couleur (format rgb) du fond du bouton lorsque le bouton est en state "normal"
        :param border_color: La couleur (format rgb) de la bordure
        :param border_size: La taille de la bordure (en px)
        :param hover_color: La couleur (format rgb) du texte lorsque le bouton est en state "hovered"
        :param hover_background_color: La couleur (format rgb) de fond du bouton lorsque le bouton est en state "hovered"
        :param hover_border_color: La couleur (format rgb) de la bordure lorsque le bouton est en state "hovered"
        :param state: La state de base du bouton (attention à la méthode "render" qui met à jour automatiquement l'état du bouton si la valeur de son argument "change_states" est laissé à True)
        :param surface: La surface sur laquelle rendre le bouton (optionnel, on peut passer par Button.surface après avoir appellé Button.update() pour obtenir la surface du bouton. Attention, si cet argument n'est pas renseigné, les méthodes "Button.is_clicked" et "Button.render" ne seront pas disponibles (soulèveront une exception RuntimeError).
        :param position: Argument obligatoire si surface est renseigné. La position à laquelle blit le bouton sur la surface. Soulève une exception RuntimeError si cet argument est renseigné mais pas surface. Argument ignoré si surface n'est pas renseigné.
        """
        super(Button, self).__init__()
        self.text = text
        self.font = font
        self.padding = padding
        self.color = color
        self.background_color = background_color
        self.border_color = border_color
        self.border_size = border_size
        self.hover_color = hover_color
        self.hover_background_color = hover_background_color
        self.hover_border_color = hover_border_color
        self.state = state

        self.rerender_text() # Calculer les surfaces des textes

        if surface is None :
            self.can_render = False
            self.regenerate_surface()
        elif position is not None :
            self.position = position
            self.can_render = True
            self.regenerate_surface()
            self.surface_blit = surface
        else :
            raise RuntimeError("Position requise si vous spécifiez la surface")

        ##>
        self.last_call_clicked = False
    def rerender_text(self) -> None :
        self.rendered_text = self.font.render( str(self.text),True,self.color )
        self.rendered_text_hover = self.font.render( str(self.text),True,self.hover_color )
    def regenerate_surface(self) :
        w = self.padding * 2 + self.border_size * 2 + self.rendered_text.get_width()
        h = self.padding * 2 + self.border_size * 2 + self.rendered_text.get_height()
        self.surface = pygame.surface.Surface((w, h))

    def update(self) -> pygame.surface.Surface :
        if self.state == "normal" :
            self.surface.fill( self.border_color )
            pygame.draw.rect( self.surface,self.background_color,(self.border_size,self.border_size,self.surface.get_width()-self.border_size*2,self.surface.get_height()-self.border_size*2) )
            self.surface.blit( self.rendered_text,(self.border_size+self.padding,self.border_size+self.padding) )

        elif self.state == "hovered" :
            self.surface.fill( self.hover_border_color )
            pygame.draw.rect( self.surface,self.hover_background_color,(self.border_size,self.border_size,self.surface.get_width()-self.border_size*2,self.surface.get_height()-self.border_size*2) )
            self.surface.blit(self.rendered_text_hover, (self.border_size + self.padding, self.border_size + self.padding))

        else :
            raise RuntimeError("État du bouton \"{}\" inconnu.".format(self.state))

        if self.can_render :
            self.rect = self.surface.get_rect()
            self.rect[0],self.rect[1] = self.position
        return self.surface

    def is_clicked(self,precomputed_pos:tuple[int,int] = None,mouse_clicked:bool = None,exceptions:bool = True) -> bool :
        """
        Retourne si le bouton est cliqué ou pas
        :param precomputed_pos: Si pygame.mouse.get_pos() à déjà été appelé, mettre son retour ici (inutile d'appeller deux fois la même fonction)
        :param mouse_clicked: Si pygame.mouse.get_pressed() à déjà été appelée, mettre ce que la fonction a retournée ici (inutile d'appeller deux fois la même fonction)
        :return: True or False, respectivement cliqué et pas cliqué
        """
        if not self.can_render :
            raise RuntimeError("Veuillez spécifier une surface sur laquelle rendre le bouton à son initialisation avec l'argument \"surface\" (et une position)")
        if not hasattr(self,"rect") :
            if exceptions :
                raise RuntimeError("Vous devez update le bouton avant d'appeller cette fonction")
            else :
                return False
        if precomputed_pos is not None :
            pos = precomputed_pos
        else :
            pos = pygame.mouse.get_pos()
        if mouse_clicked is None :
            mouse_clicked = pygame.mouse.get_pressed()

        if self.last_call_clicked and not mouse_clicked[0] :
            self.last_call_clicked = False

        if self.rect.collidepoint( pos ) and mouse_clicked[0] and not self.last_call_clicked :
            self.last_call_clicked = True
            return True
        else :
            return False

    def update_state(self) :
        mouse_pos = pygame.mouse.get_pos()  # Récupérer la position de la souris
        if hasattr(self, "rect"):  # (Il faut que le bouton est déjà été update) Si le bouton a l'attribut rect
            if self.rect.collidepoint(mouse_pos):  # Alors si la souris est dans le rectangle rendu
                self.state = "hovered"  # Définir l'état comme "survolé"
            else:  # Sinon
                self.state = "normal"  # Définir l'état comme normal

    def render(self,call_update = True,change_states = True) :
        """
        Permet de render le bouton sur la pygame.surface.Surface de self.surface !
        :param call_update: La fonction doit update le bouton avant de le render ?
        :param change_states: (Inutile si call_update = False) La fonction doit-elle changer l'état du bouton automatiquement ?
        """
        if not self.can_render : # Si aucune surface donnée ( self.can_render définie à l'__init__ de cet objet)
            # Soulever une erreur
            raise RuntimeError("Veuillez spécifier une surface sur laquelle rendre le bouton à son initialisation avec l'argument \"surface\" (et une position)")

        # Si call_update c-à-d que la fonction doit update le bouton avant de le render
        if call_update :
            # Alors
            # Si la fonction doit changer les états automatiquement
            if change_states :
                self.update_state()

            self.update() # Update le bouton
        ##>
        self.surface_blit.blit(self.surface,self.position) # Blit le bouton sur la surface donnée


class Reflection:
    def __init__(
            self,
            sprite: pygame.sprite.Sprite = pygame.sprite.Sprite(),
            blur: float = 5
    ) -> None:
        try:
            assert isinstance(sprite, pygame.sprite.Sprite)
        except AssertionError:
            raise pyframe.exception.ArgumentError("Le sprite n'est pas un pygame.sprite.Sprite")
        try:
            assert hasattr(sprite, "image")
        except AssertionError:
            raise pyframe.exception.ArgumentError("Le sprite n'a pas d'attribut image")
        self.sprite = sprite
        self.reflection = pyframe.functions.blur_surf(self.sprite.image, blur)
        self.reflection = pygame.transform.flip(self.reflection, False, True)

    def get_image(self) -> pygame.surface.Surface:
        return self.reflection