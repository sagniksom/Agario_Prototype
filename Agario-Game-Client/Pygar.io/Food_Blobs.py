import pygame
from Additional_Functions import *

class food_blobs:
    def __init__(self, surface, playfieldWidth, playfieldHeight, player_X, player_Y,player_mass, camera, player_color):     
        """ (object),(int),(int),(int),(int),(int),(float),(object),(tuple) ---> (None)
        This class assigns basic constants and variables for food that is shot out of player objects. Everytime a player shoots out a food
        blob it creates a new object using this class as a template.
        """
        self.color = player_color
        self.surface = surface
        self.acceleration = 0.65
        self.velocity = 25
        self.mouseX, self.mouseY = pygame.mouse.get_pos()
        self.playfieldWidth, self.playfieldHeight = playfieldWidth, playfieldHeight
        self.angle = get_angle(self.mouseX,self.mouseY,int(player_X*camera.zoom+camera.x),int(player_Y*camera.zoom+camera.y))
        self.points_on_circumfrence = points_on_circumfrence(player_mass/3)
        self.Xspeed = int((self.velocity*math.cos(self.angle*math.pi/180))) 
        self.Yspeed = int((self.velocity*math.sin((self.angle + 180)*math.pi/180))) 
        self.x,self.y = self.points_on_circumfrence[int(self.angle)-1]
        self.x,self.y = int(player_X + self.x),int(player_Y - self.y)
        
    def move(self):
        """ (None) ---> (None)
        This Function is responsible for the movement of food blobs that have shot from players
        """
        self.x += self.Xspeed
        self.y += self.Yspeed        
        self.velocity = self.velocity * 0.965
        self.Xspeed = int((self.velocity*math.cos(self.angle*math.pi/180))) 
        self.Yspeed = int((self.velocity*math.sin((self.angle + 180)*math.pi/180))) 
        if self.x < 12:
            self.x = 12
        elif self.x > (self.playfieldWidth -(12)):
            self.x = (self.playfieldWidth -(12)) 
            
        if self.y < 12:
            self.y = 12 
        elif self.y > (self.playfieldHeight -(12)):
            self.y = (self.playfieldHeight -(12))        
        
    def render(self,camera):
        """ (object) ---> (None)
        This function is resposible for rendering food blobs on the screen
        """
        pygame.draw.circle(self.surface,self.color,(int(self.x*camera.zoom+camera.x),int(self.y*camera.zoom+camera.y)),int(camera.zoom*8))

    def update(self,camera):
        """ (object) ---> (None)
        This function is responsible for sequentially running through all of the other functions 
        necessary to update and move the food blob objects.
        """
        self.render(camera)
        self.move()
