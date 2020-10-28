import pyframe, pygame, math

def add_vectors(v1, v2):  # v[0] = Angle, v[1] = length
    x = math.sin(v1[0]) * v1[1] + math.sin(v2[0]) * v2[1]
    y = math.cos(v1[0]) * v1[1] + math.cos(v2[0]) * v2[1]

    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return angle, length

def blur_surf(surface, amt):
    """
    Floutte une surface pygame (généralement une image)
    """
    if amt < 1.0:
        raise ValueError("L'agument 'amt' doit être plus grand que 1.0, la valeur était de %s"%amt)
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf

def get_smallest(l) :
    assert type(l) is list
    val = math.inf
    for i in l :
        if i < val :
            val = i
    return val if val != math.inf or math.inf in l else None
def get_biggest(l) :
    assert type(l) is list
    val = -math.inf
    for i in l :
        if i > val :
            val = i
    return val if val != -math.inf or -math.inf in l else None