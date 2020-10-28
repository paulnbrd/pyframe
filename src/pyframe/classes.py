import pygame, os, sys, pyframe, math, random, time
pygame.init()
pygame.font.init()
pygame.mixer.init()

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
            nb_init,  # Nombre de particules
            interval,
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

        self.last_add += tick
        while self.last_add > self.interval:
            self.particles.append(self.new_particle())
            self.last_add -= self.interval

    def render(self):
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

class Graph :
    """
        Permet de créer des graphiques
        avec pygame
    """
    def __init__(self,
                 size = (500,200),
                 font = pygame.font.SysFont("Arial",18),
                 max_values = 1000,
                 titre = ""
    ) :
        """
            Permet de tracer un graphique (voir Graph.get_surface())
            :param size: La taille du graphique
            :param font: La police d'écriture du graphique
            :param max_values: Le nombre maximum de valeurs
        """
        self.surface = pygame.surface.Surface( size )
        self.font = font
        self.titre = titre

        self.max_values = max_values
        self.values = []
    def get_surface(self,size = None ) :
        if size is None :
            size = self.surface.get_size()
        surf = pygame.transform.scale( self.surface,size )
        return surf
    def add_value(self,new_value) :
        """
            Ajoute une nouvelle valeur à la liste des valeurs
        """
        assert type(new_value) is int or float
        self.values.append( new_value )
        if len(self.values) > self.max_values :
            self.values.pop( 0 )
    def render(self) :
        self.surface.fill( (0,0,0) )

        borne_haute = pyframe.functions.get_biggest( self.values )
        # borne_haute += borne_haute * 0.1
        borne_basse = pyframe.functions.get_smallest( self.values )
        # borne_basse += borne_basse * 0.1
        borne_haute -= borne_basse

        points = []
        h = self.surface.get_height()

        for v in self.values :
            try :
                rapport = (v-borne_basse)/borne_haute
                points.append( h-rapport*h )
            except ZeroDivisionError :
                pass

        pygame.draw.line(self.surface,(255,255,255),(0,0),(0,self.surface.get_height()))
        pygame.draw.line(self.surface,(255,255,255),(0,self.surface.get_height()-1),(self.surface.get_width(),self.surface.get_height()-1))
        texte_borne_haute = self.font.render( str(round(borne_haute+borne_basse)),True,(255,255,255) )
        self.surface.blit( texte_borne_haute,(2,0) )
        texte_borne_basse = self.font.render(str(round(borne_basse)), True, (255, 255, 255))
        self.surface.blit(texte_borne_basse, (2, h-texte_borne_basse.get_height()))
        titre = self.font.render(str(self.titre), True, (255, 255, 255))
        self.surface.blit( titre,(self.surface.get_width()-titre.get_width(),0) )

        w = self.surface.get_width()
        if len(points) > 1 :
            espace = w / (len(points)-1)
            for p in range(len(points)-1) :
                try :
                    pygame.draw.line(
                        self.surface,
                        (255,0,0),
                        (espace*p, points[p] ),
                        (espace*(p+1), points[p+1])
                    )
                except :
                    pass
        elif len(points) == 1 :
            pygame.draw.circle(
                self.surface,
                (255,0,0),
                (0,points[0]),
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

class Button ( pygame.sprite.Sprite ) :
    """
        (C'est un pygame.sprite.Sprite parce que ce peut être utile)
    """
    def __init__(
            self,
            text
    ) :
        super(Button, self).__init__()
        self.text = text