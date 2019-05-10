#########################################
# Programmer: Steven Kovacs-Snider
# Date: 06.02.2016
# File Name: Food.py
# Description: This class contains all imformation and functions pertanent too the food objects within Pygar.io  
#########################################

import random
import pygame

class Food:
    def __init__(self,surface,screenHeight,screenWidth):
        """ (object),(int),(int) ---> (None)
        This function assigns basic constants and variables too any and all food objects
        """
        self.x = random.randint(25,screenWidth-25)
        self.y = random.randint(25,screenHeight-25)
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.surface = surface     
             
    def render(self,camera):
        """ (object) --> (None) 
        Draws food on the screen
        """
        pygame.draw.circle(self.surface,self.color,(int(self.x*camera.zoom+camera.x),int(self.y*camera.zoom+camera.y)),int(camera.zoom*4))
            
def spawn_food(food_list,num_of_food_elements,surface,screenHeight,screenWidth):
    """ (list),(int),(object),(int),(int) --> (list)
    Creates and appends food objects to the defined list, a number of times preditermined by the coder
    """
    for element in range(num_of_food_elements):
        food = Food(surface,screenHeight,screenWidth)
        food_list.append(food)
