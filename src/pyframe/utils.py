import pyframe, pygame, math, random

#############################################
############ =<|= Functions =|>= ############
#############################################

def set_framerate(framerate):  # Définit les fps
    pyframe.base.FPS = framerate  # Redéfinit la globale FPS


def clear_screen(color=pyframe.base.BACKGROUND_COLOR, window=False):  # "Efface" l'écran
    if window == False:  # Si l'argument window est laissé de base (pas de fenêtre fournie)
        if pyframe.base.GLOBAL_WIN == False:  # Si la fenêtre globale n'est pas définie
            raise pyframe.ArgumentError("GLOBAL_WIN is not defined", "GLOBAL_WIN")  # Raise une erreur d'argument
        else:
            pyframe.base.GLOBAL_WIN.fill(color)  # Remplir l'écran de la couleur désirée
    else:
        window.fill((0, 0, 0))  # Remplir l'écran de noir, faute de mieux


def key_to_index(key):
    """ Permet de transformer un caractère en son index pygame (le clavier AZERTY n'est pas celui utilisé par pygame) """
    return pyframe.base.AZERTY_KEY_INDEXES.get(key)


def events_loop():
    """
        Voici la boucle d'évenements qui doit être appellée
        à chaque itération de la mainloop de pygame
        à chaque frame quoi. Après un clear de l'écran,
        car des render peuvent y être fait
    """
    pyframe.base.ELAPSED = pyframe.base.CLOCK.tick(pyframe.base.FPS)
    pyframe.base.DELTA_TIME = pyframe.base.ELAPSED / pyframe.base.DELTA_TIME_DIVIDER * pyframe.base.TIME_SPEED  # Le calcul du delta time
    keys = pygame.key.get_pressed()  # Récupérer les touches appuyés
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    pyframe.base.LAST_MOUSE_POS = (mouse_pos_x, mouse_pos_y)
    pyframe.base.LAST_KEYS_PRESSED = keys
    pyframe.base.LAST_MOUSE_STATES = mouse_pressed

    for bind in pyframe.base.MOVE_BINDS:  # Pour tous les binds
        if keys[bind.get("key")]:  # Si la touche du bind est appuyée
            bind.get("obj").move(bind.get("direction"), bind.get("step"))  # Déplacer l'objet

    for emitter in pyframe.base.PARTICLES_EMITTERS:
        emitter.particle_system.move()
        emitter.particle_system.render()

    for bouton in pyframe.base.BUTTONS:
        if bouton.command != False:
            if bouton.is_clicked() and bouton.rendered_last_frame:
                bouton.command(bouton)

        bouton.rendered_last_frame = False


def drawRect(window, x, y, w, h, color=pyframe.base.PRIMARY_COLOR):  # Dessiner un rectangle
    pygame.draw.rect(window, color, (x, y, w, h))  # La fonction de pygame


def render_text(x, y, text, color=pyframe.base.PRIMARY_COLOR, vertical_centering=False, horizontal_centering=False, font=False,
                fontsize=30, window=False, scale=False, width=False, height=False, blit_to_window=True):
    # Écrit du texte sur la fenêtre
    if font != False:  # Si la police d'écriture n'est pas définie
        if type(font) is str:  # Si la police d'écriture est une chaîne de caractères
            font = pygame.font.SysFont(font, int(fontsize))  # Définir la police d'écriture
        else:  # Sinon
            raise pyframe.ArgumentError("Invalid font argument", "font")  # Lever une erreur d'argument

    else:  # Sinon
        font = pyframe.base.GLOBAL_FONT  # La police d'écriture est égale à la police d'écriture globale

    if window != False:  # Si l'argument window est changé de la valeur de base
        if type(window) is pygame.Surface:  # Si la window est un pygame.Surface (Une surface pygame,qui est probablement une fenêtre)
            window = window  # Ne rien changer
        else:
            raise pyframe.ArgumentError("Invalid window argument", "window")  # Lever une erreur d'argument
    else:  # Sinon
        window = pyframe.base.GLOBAL_WIN  # La fenêtre de rendue est définie à la fenêtre globale
    text = font.render(text, False, color)  # Rendre le texte

    if scale:
        if width != False and height != False:
            text = pygame.transform.scale(text, (width, height))
        else:
            raise pyframe.ArgumentError("Scale need width and height arguments", "width,height")

    if blit_to_window:
        window.blit(text, (x, y))  # Le coller dans la fenêtre

    return text


def addVectors(v1, v2):  # v[0] = Angle, v[1] = length
    x = math.sin(v1[0]) * v1[1] + math.sin(v2[0]) * v2[1]
    y = math.cos(v1[0]) * v1[1] + math.cos(v2[0]) * v2[1]

    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return angle, length


def verify_arg_type(var, varname, type, auto_raise=True):
    if type(var) is type:
        return True
    else:
        if auto_raise:
            raise pyframe.ArgumentError(varname, "Invalid var type")
        return False