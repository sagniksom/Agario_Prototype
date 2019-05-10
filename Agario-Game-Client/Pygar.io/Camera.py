import pygame
class Camera:

    def __init__(self, screenWidth, screenHeight):
        """ (int), (int) ---> (None)
        This is a descriptor method for the class Camera
        """
        self.x = 0
        self.y = 0
        self.Xspeed = 0
        self.Xspeed = 0
        self.width = screenWidth
        self.height = screenHeight
        self.zoom = 10.0

    def centre(self,player,screenWidth,screenHeight):
        """ (object),(int),(int) ---> (None)
        Centres the player on the screen
        """
        self.x = (screenWidth/2)-(player.x*self.zoom)
        self.y = (screenHeight/2)-(player.y*self.zoom)
            
