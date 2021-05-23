from pygame.gfxdraw import aapolygon, filled_polygon
from math import sqrt

def toInt(pt: tuple):
    """
    Converts a tuple of two floats to integers
    """
    return (int(pt[0]), int(pt[1]))

def drawArrow(window, x: int, y: int, length: float, direction: tuple, width: int = 2, color: tuple =(255,0,0)):
    """
    Draw an arrow at the given location (x, y) using pygame.gfxdraw.aapolygon and pygame.gfxdraw.filled_polygon
    direction is a tuple/list (x0, y0) representing a mathematical vector pointing in the direction the arrow should point
    """
    
    direction_magnitude = sqrt(direction[0]**2 + direction[1]**2)
    if (direction_magnitude == 0):
        return

    # scale down the length of arrow
    length *= 0.7

    unit_direction = (direction[0] / direction_magnitude, direction[1] / direction_magnitude)

    p1 = (x + (unit_direction[1] * width/2), y - (unit_direction[0] * width /2))
    p2 = (x - (unit_direction[1] * width/2), y + (unit_direction[0] * width /2))

    p3 = (p1[0] + (unit_direction[0] * length), p1[1] + (unit_direction[1] * length))
    p4 = (p2[0] + (unit_direction[0] * length), p2[1] + (unit_direction[1] * length))

    p5 = (p3[0] + (unit_direction[1] * length / 7), p3[1] - (unit_direction[0] * length / 7))
    p6 = (p4[0] - (unit_direction[1] * length / 7), p4[1] + (unit_direction[0] * length / 7)) 

    p7 = (x + (unit_direction[0] * length * 1.3), y + (unit_direction[1] * length * 1.2))

    pt_list = [toInt(pt) for pt in [p1, p2, p4, p6, p7, p5, p3]]
    aapolygon(window, pt_list, color)
    filled_polygon(window, pt_list, color)
