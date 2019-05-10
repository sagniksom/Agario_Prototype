import pygame
import random
class Virus(object):
    def __init__(self,surface,playfieldWidth,playfieldHeight):
        """(object),(int),(int) ---> (None)
        Construtor Method for Viruses. 
        """
        self.x = random.randint(25,playfieldWidth)
        self.y = random.randint(25,playfieldHeight)
        self.mass = 100.111
        self.color = (173,255,47)
        self.borderColor = (34,139,34)
        self.surface = surface
    
    def render(self,camera):
        """(object) ---> (None)
        Construtor Method for Viruses. 
        """ 
        x = int(self.x*camera.zoom+camera.x)
        y = int(self.y*camera.zoom+camera.y)
        pygame.draw.circle(self.surface,self.color,(x,y),int(self.mass/3*camera.zoom), 0)
        pygame.draw.circle(self.surface,self.borderColor,(x,y),int(self.mass/3*camera.zoom),5)
        
    def update(self,camera):
        """(object) ---> (None)
        Updates Viruses.
        """
        self.render(camera)
