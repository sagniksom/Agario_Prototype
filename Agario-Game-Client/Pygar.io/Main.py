import pygame
import random
import math
from Player import *
from Food import *
from Food_Blobs import *
from Additional_Functions import *
from Camera import *
from labels_and_text import *
from Segment import *
from Virus import *
pygame.init()

name = raw_input("Please Name Your Blob:")
screenWidth, screenHeight = pygame.display.Info().current_w, pygame.display.Info().current_h
playfieldWidth, playfieldHeight = 3000,3000
screen=pygame.display.set_mode((screenWidth,screenHeight), pygame.FULLSCREEN,32)
player = Player(screen,screenHeight,screenWidth,playfieldWidth,playfieldHeight,name)
camera = Camera(screenWidth,screenHeight)
food_list = []
food_blob_list = []
segments = []
viruses = [Virus(screen,playfieldWidth,playfieldHeight) for i in range(25)]
spawn_food(food_list,500,screen,playfieldHeight,playfieldWidth)
pygame.key.set_repeat(1,2000)
WHITE = (255,255,255)
inPlay = True
clock = pygame.time.Clock() 

while inPlay:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
            if event.key == pygame.K_SPACE:   
                player.feed(food_blob_list,camera)
            if event.key == pygame.K_LSHIFT and segments == [] and player.mass >= 32:   
                split(segments,screen,playfieldWidth,playfieldHeight,player,camera)
                pygame.mixer.Sound("Split.wav").play()

    camera.zoom = 1/(0.03*player.cameraValue) + 0.3
    camera.centre(player,screenWidth, screenHeight)

    
    screen.fill(WHITE)
    drawGrid(screen,playfieldWidth,playfieldHeight,camera)
    
    #Render Food Blobs
    for item in food_blob_list:
        item.update(camera)
        
    #Render Food Items
    for item in food_list:
        item.render(camera)
        
    #Render And Update Segments
    for segment in segments:
        segment.update(screen,player,segments,viruses,food_list,food_blob_list,1,12,1,16,camera,screenWidth,screenHeight)
        segment.duration += 1
        
    #Render And Render Player
    player.update(food_list,food_blob_list,viruses,camera,screenWidth,screenHeight)

    #Render And Update Viruses
    for virus in viruses:
        virus.update(camera)

    #Render Score Label
    render_score_label(screenWidth,screenHeight,player.mass,screen)
    pygame.display.update()
    clock.tick(30)
    
pygame.quit()
