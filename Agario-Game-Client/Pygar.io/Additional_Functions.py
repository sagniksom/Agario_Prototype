import math
import pygame

def distance(x1,y1,x2,y2):
    """(int),(int),(int),(int) ---> (int)
    The method is used to find the distance between two sets of coordinates 
    """
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return distance

def get_angle(x1,y1,x2,y2):
    """(int),(int),(int),(int) ---> (int)
    The method is used to find the angle between two points relative to the horizontal axis 
    """
    hyp = distance(x1,y1,x2,y2)
    adj = x2-x1
    angle = 180 + (math.acos(adj/hyp))/(math.pi/180)
    if y2>y1:
        angle = 180 - (math.acos(adj/hyp))/(math.pi/180)
    return angle

def drawGrid(surface,playfieldWidth,playfieldHeight,camera):
    """(object),(int),(int),(object) ---> (none)
    This method is used to make a grid that is diplayed on your screen. The grid is not static but scales based off your camera
    and your position on the field.
    """
    GRIDSIZE = 50
    BLACK = (0,0,0)
    H_Start = 0
    H_End = playfieldWidth
    V_Start = 0
    V_End = playfieldHeight
    for i in range(H_Start,H_End+1,GRIDSIZE):
        pygame.draw.line(surface,BLACK,(i*camera.zoom+camera.x,V_Start + camera.y),(i*camera.zoom+camera.x,V_End*camera.zoom+camera.y),1)
    for i in range(V_Start,V_End+1,GRIDSIZE):
        pygame.draw.line(surface,BLACK,(H_Start + camera.x,i*camera.zoom+camera.y),(H_End*camera.zoom+camera.x,i*camera.zoom+camera.y),1)
        
def points_on_circumfrence(r,n=359):
    """(int)(int) ---> (list)
    This method creates a list of 360 sets of coordinates on the circumference of any given circle.
    """
    r += 12
    segment_list = [(math.cos(2*math.pi/n*x)*r,math.sin(2*math.pi/n*x)*r) for x in xrange(0,n+1)]
    return segment_list
