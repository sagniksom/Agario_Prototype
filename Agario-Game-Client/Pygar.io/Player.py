import pygame
import random
from Food_Blobs import *
from Additional_Functions import *
from labels_and_text import *
import Food
pygame.mixer.init()

class Player:
    def __init__(self,surface,screenHeight,screenWidth,playfieldWidth,playfieldHeight,name = "Unamed Cell",x=None,y=None,):
        """ (object),(int),(int),(int),(int),(string),(int),(int) ---> (None)
        This portion of the Player class assigns basic constants and variables to the player object. Everytime a new player
        object is created, it is created following this template.
        """
        self.x = random.randint(25,screenWidth - 25)
        self.y = random.randint(25,screenHeight - 25)
        self.mass = 16
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.name = name
        self.surface = surface
        self.Xspeed = 0
        self.Yspeed = 0
        self.screenHeight, self.screenWidth = screenHeight, screenWidth
        self.playfieldWidth, self.playfieldHeight  = playfieldWidth, playfieldHeight
        self.cameraValue = (self.mass/3)+3
        self.label = myfont.render(self.name,1,(0,0,0))
        self.label_offset = self.label.get_width()   
        self.font_size = 3
        self.veloctiy = 11
        
    def move(self):
        """ (None) ---> (None)
        This Function is responsible for the movement of player objects, with their direction dependent upon the mouses position 
        relative to the player object and their speed dependent upon the player's mass 
        """
        # Bases Speed On Current Player Mass
        if self.mass <= 164:
            self.velocity = 11
        if self.mass >= 165 and self.mass <= 312:
            self.velocity = 10        
        if self.mass >= 313 and self.mass <= 460:
            self.velocity = 9 
        if self.mass >= 461 and self.mass <= 608:
            self.velocity = 8       
        if self.mass >= 609 and self.mass <= 756:
            self.velocity = 7           
        if self.mass >= 757 and self.mass <= 904:
            self.velocity = 6        
        if self.mass >= 905 and self.mass <= 1052:
            self.velocity = 5
        if self.mass >= 1053:
            self.velocity = 4  
      
        mouseX,mouseY = pygame.mouse.get_pos()
        angle = math.atan2(mouseY-self.screenHeight/2,mouseX-self.screenWidth/2)*180/math.pi
        
        self.Xspeed = int((self.velocity*math.cos(angle*math.pi/180))) 
        self.Yspeed = int((self.velocity*math.sin(angle*math.pi/180)))    
        self.x += self.Xspeed
        self.y += self.Yspeed

        if self.x < self.mass/3:
            self.x = self.mass/3
        elif self.x > (self.playfieldWidth-(self.mass/3)):
            self.x = (self.playfieldWidth-(self.mass/3)) 
            
        if self.y < self.mass/3:
            self.y = self.mass/3 
        elif self.y > (self.playfieldHeight-(self.mass/3)):
            self.y = (self.playfieldHeight-(self.mass/3))  
        
    def collision_detection(self, item_list, item_value, required_mass, camera):
        """ (list),(int),(int),(object) ---> (None)
        This function identifies collisions between a variety of different objects and the player, and is maniputable in order to set
        indentifiers that allow the player object to comprehend what it is collidiing with and how to react
        """
        for item in item_list:
            if distance(self.x,self.y,item.x,item.y) <= self.mass/3 and self.mass > required_mass:
                item_list.remove(item)
                if self.mass <=800:
                    self.mass += item_value
                    pygame.mixer.Sound("Eat.wav").play()
                    self.cameraValue += 10*float(item_value)/self.mass
                elif self.mass > 800 and self.mass <= 1200:
                    self.mass += item_value
                    pygame.mixer.Sound("Eat.wav").play()
                    self.cameraValue += 30*float(item_value)/self.mass
                elif self.mass > 1150 and self.mass <= 1300:
                    self.mass += item_value
                    pygame.mixer.Sound("Eat.wav").play()
                    self.cameraValue += 55*float(item_value)/self.mass
                elif self.mass > 1300 and self.mass <= 1450:
                    self.mass += item_value
                    pygame.mixer.Sound("Eat.wav").play()
                    self.cameraValue += 65*float(item_value)/self.mass 
                elif self.mass > 1450 and self.mass <= 1600:
                    self.mass += item_value
                    pygame.mixer.Sound("Eat.wav").play()
                    self.cameraValue += 85*float(item_value)/self.mass 
                elif self.mass > 1600 and self.mass < 2000:
                    self.mass += item_value
                    pygame.mixer.Sound("Eat.wav").play()
                    self.cameraValue += 120*float(item_value)/self.mass
                elif self.mass >= 2000:
                    self.mass += item_value
                    pygame.mixer.Sound("Eat.wav").play()
                    self.cameraValue = self.cameraValue
                if item_value == 1:
                    Food.spawn_food(item_list,1,self.surface,self.playfieldWidth,self.playfieldHeight)
                elif item_value == 100.111:
                    self.explode(camera,item_list)
                    pygame.mixer.explode_sound.play()
                    
    def feed(self,food_blob_list,camera):
        """ (list),(object) ---> (None)
        This function checks whether the player objects mass is at or above a certain value, and if it is the function creates a food blob 
        and appends it to the food blob list for later updating and rendering. The function also subtracts 16 mass from the player object
        to make it seem as though the player object is actually shooting off a piece of itself
        """
        if self.mass >= 36:
            food_blob = food_blobs(self.surface,self.playfieldWidth,self.playfieldHeight,self.x,self.y,self.mass,camera,self.color)
            food_blob_list.append(food_blob)
            self.mass = self.mass-16
            self.cameraValue -= 5*float(16)/self.mass
            pygame.mixer.Sound("Shoot.wav").play()
        else:
            pass

    def explode(self,camera,viruses,food_blob_list):
        """ (object),(list),(list) ---> (None)
        Makes the player explode into food blobs.
        """
         for item in viruses:
            if distance(self.x,self.y,item.x,item.y) <= self.mass/3 + (100/6) and self.mass >= 100:
                segments = points_on_circumfrence(self.mass/3,7)
                angles = [(2*math.pi/7*x)*(self.mass/3) for x in xrange(0,8)]
                mass_lossed = (self.mass/10)
                pygame.mixer.Sound("Explosion.wav").play()
                for i in range(8):
                    x,y = segments[i]
                    x += self.x
                    y += self.y
                    food_blob = food_blobs(self.surface,self.playfieldWidth,self.playfieldHeight,x,y,self.mass,camera,self.color)
                    food_blob.angle = angles[i]
                    food_blob_list.append(food_blob)
                    self.mass -= mass_lossed
                    self.cameraValue -= 10*float(16)/self.mass
                    
    def massLoss(self):
        """ (None) ---> (None)
        This function has the player object lose a percentage of of its mass every time it is run, with the percentage dependant upon the
        mass of the player object. (i.e. The higher the mass of the player; the higher the percentage of mass lossed)
        """
        if self.mass >= 250 and self.mass <= 750:
            self.mass *= 0.9999
        elif self.mass > 750 and self.mass <=1000:
            self.mass *= 0.99985
        elif self.mass > 1000 and self.mass <= 1100:
            self.mass *= 0.999825
        elif self.mass > 1000 and self.mass <= 1100:
            self.mass *= 0.99981     
        elif self.mass > 1100 and self.mass <= 1200:
            self.mass *= 0.99977 
        elif self.mass > 1200:
            self.mass *= 0.9997             
        elif self.mass > 2000:
            self.mass = 2000
        else:
            pass
        pass
    
    def render(self,camera):
        """ (object) ---> (None)
        This function is resposible for rendering the player object on screen at the correct position, as well as consistently 
        rendering the players over the player object
        """
        x = int(self.x*camera.zoom+camera.x)
        y = int(self.y*camera.zoom+camera.y)
        pygame.draw.circle(self.surface,self.color,(x,y),int(self.mass/3*camera.zoom), 0)
        myfont = pygame.font.SysFont("monospace",int(self.font_size))
        self.label = myfont.render(self.name,1,(0,0,0))
        self.label_offset = self.label.get_width()
        self.surface.blit(self.label, (int(self.x*camera.zoom+camera.x) - (self.label_offset/2),int(self.y*camera.zoom+camera.y)))        

    def update(self,food_list,food_blob_list,viruses,camera,screenWidth,screenHeight):
        """ (list),(list),(list),(object),(int),(int) ---> (None)
        This function is responsible for sequentially running through all of the other functions 
        necessary to update as well as operate the player object
        """
        self.massLoss()
        self.move()
        self.collision_detection(food_list,1,1,camera)
        self.collision_detection(food_blob_list,12,16,camera)
        self.explode(camera,viruses,food_blob_list)
        self.render(camera)
        self.font_size = self.mass/11
        if self.font_size > 42:
            self.font_size = 42
