import os
import pygame

pygame.font.init()
SPRITE_RECT = "rect"
GLOBAL_WIN = False
GLOBAL_FONT = pygame.font.SysFont("Arial", 30)

FPS = 60
DELTA_TIME_DIVIDER = 100
CLOCK = pygame.time.Clock()
TIME_SPEED = 1
DELTA_TIME = CLOCK.tick(FPS)/DELTA_TIME_DIVIDER*TIME_SPEED

MOVE_BINDS = []
SPRITES = []

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

local_dir = os.path.dirname(__file__)

# Handling exceptions
class Error(Exception):
    pass

class WindowError(Error):
    def __init__(self, message):
        self.message = message




#############################################
############ =<|= Functions =|>= ############
#############################################

def set_framerate(framerate) :
    global FPS,DELTA_TIME
    FPS = framerate
    DELTA_TIME = CLOCK.tick(FPS)/DELTA_TIME_DIVIDER*TIME_SPEED

def clear_screen(color = (0,0,0),window = False) :
    global GLOBAL_WIN
    if window == False :
        if GLOBAL_WIN == False :
            raise WindowError("GLOBAL_WIN is not defined")
        else :
            GLOBAL_WIN.fill(color)
    else :
        window.fill((0,0,0))

def key_to_index(key) :
    """ Permet de transformer un caractère en son index pygame (le clavier AZERTY n'est pas celui utilisé par pygame) """
    return AZERTY_KEY_INDEXES.get(key)
    
def events_loop() :
    DELTA_TIME = CLOCK.tick(FPS)/DELTA_TIME_DIVIDER*TIME_SPEED
    keys = pygame.key.get_pressed()
    #for i in range(len(keys)) :
    #    if keys[i] == 1 :
    #        print(str(i) + " => "+str(keys[i]))
    for bind in MOVE_BINDS :
        if keys[bind.get("key")] :
            bind.get("obj").move(bind.get("direction"),bind.get("step"))

def drawRect(window,x,y,w,h) :
    pygame.draw.rect(window,(255,0,0),(x,y,w,h))

def render_text(window,x,y,text,color,centered = False,font = False,fontsize = 30) :
    global GLOBAL_FONT
    if font != False :
        if type(font) is str :
            font = pygame.font.SysFont(font, fontsize)
        else :
            raise WindowError("Invalid font argument")
    else :
        font = GLOBAL_FONT
    text = font.render(text, False, color)
    window.blit(text,(x,y))

#############################################
############# =<|= Classes =|>= #############
#############################################

class PyFrameSuperSprite :
    def __init__(self,window) :
        self.window = window
    def render(self) :
        pass

    def move(self,direction,step = 1) :
        directions = ["up","down","right","left","stand"]
        if direction in directions :
            if direction == "up" :
                self.y += step*DELTA_TIME
            elif direction == "down" :
                self.y -= step*DELTA_TIME
            elif direction == "right" :
                self.x += step*DELTA_TIME
            elif direction == "left" :
                self.x -= step*DELTA_TIME
        else :
            raise WindowError("Invalid direction")

    def bind(self,key,direction,step) :
        found = False
        for i in range(len(MOVE_BINDS)) :
            if MOVE_BINDS[i].get("obj") == self and MOVE_BINDS[i].get("direction") == direction and MOVE_BINDS[i].get("key") == key  :
                found = True
                MOVE_BINDS[i] = {"key":key,"direction":direction,"step":step,"obj":self}
                print("found")
        if found == False :
            MOVE_BINDS.append({"key":key,"direction":direction,"step":step,"obj":self})

class PyFrameRectSprite(PyFrameSuperSprite) :
    def __init__(self,window,x,y,w,h,centered_rendering = False) :
        self.window = window
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.centered_rendering = centered_rendering
    def render(self) :
        if self.centered_rendering :
            drawRect(self.window,self.x-self.width/2,self.y-self.height/2,self.width,self.height)
        else :
            drawRect(self.window,self.x,self.y,self.width,self.height)

        super().render()