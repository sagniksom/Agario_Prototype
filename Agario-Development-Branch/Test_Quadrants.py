import pygame
import random
pygame.init()

class Quadrants():
    def __init__(self,rows,coloums,quad_length):
        self.rows = rows
        self.coloums = coloums
        self.quad_length = quad_length
        self.quadrants = []
        
        for i in range(self.rows):
            self.quadrants.append([])
            for e in range(self.coloums):
                quadrant_x = i*self.quad_length
                quadrant_y = e*self.quad_length
                self.quadrants[i].append(Quadrant([],quadrant_x,quadrant_y))

    def add_item(self,item):
        for coloum in self.quadrants:
            for quadrant in coloum:
                if quadrant.check(item) == (0,0):
                    quadrant.items.append(item)
                    break

    def update(self,quad_row,quad_coloum,item_ID,item_updated_x,item_updated_y,item_updated_m):
        item_index = self.quadrants[quad_row][quad_coloum].find(item_ID)
        
        self.quadrants[quad_row][quad_coloum].items[item_index].update(item_updated_x,item_updated_y,item_updated_m)
        row_change,coloum_change = self.quadrants[quad_row][quad_coloum].check(self.quadrants[quad_row][quad_coloum].items[item_index])
        if row_change != 0 or coloum_change != 0: 
            self.quadrants[quad_row][quad_coloum].items[item_index].quad_row = quad_row+row_change
            self.quadrants[quad_row][quad_coloum].items[item_index].quad_coloum = quad_coloum+coloum_change
            self.quadrants[quad_row+row_change][quad_coloum+coloum_change].items.append(self.quadrants[quad_row][quad_coloum].items[item_index])
            del self.quadrants[quad_row][quad_coloum].items[item_index]
        
        
    def draw(self,surface,scale,offset_x,offset_y):
        for coloum in self.quadrants:
            for quadrant in coloum:
                for item in quadrant.items:
                    if item.ID == 1:
                        visable_quadrants = item.camera.check_visable_quadrants()
                        for quadrant in visable_quadrants:
                            self.quadrants[quadrant[0]][quadrant[1]].draw(surface,scale,offset_x,offset_y)

class Quadrant():
    def __init__(self,items,x,y):
        self.items = items
        self.x = x
        self.y = y

    def check(self,item):
        if self.x > item.x: 
            if self.y > item.y:
                return -1,-1
            elif self.y + quad_length < item.y:
                return -1,1
            else:
                return -1,0

        elif self.x + quad_length < item.x:
            if self.y > item.y:
                return 1,-1
            elif self.y + quad_length < item.y:
                return 1,1
            else:
                return 1,0

        elif self.y > item.y:
            return 0,-1
        elif self.y+quad_length < item.y:
            return 0,1
        else:
            return 0,0    

    def find(self,item_ID):
        for i in range(len(self.items)):
            if self.items[i].ID == item_ID:
                return i

    def draw(self,surface,scale,offset_x,offset_y):
        for item in self.items:
            item.draw(surface,scale,offset_x,offset_y)
        pygame.draw.rect(surface,(255,0,0),(int((self.x-offset_x)*scale),int((self.y-offset_y)*scale),int(quad_length*scale),int(quad_length*scale)),2)

class Client():
    def __init__(self,x,y,m,ID):
        self.quad_row = 0
        self.quad_coloum = 0
        self.x = x
        self.y = y
        self.m = m
        self.ID = ID
        self.camera = Camera(self.x,self.y,90,90)

    def update(self,x,y,m):
        self.x = x
        self.y = y
        self.m = m
        self.camera.x = self.x
        self.camera.y = self.y

    def draw(self,surface, scale,offset_x,offset_y):
        pygame.draw.circle(surface,(0,0,0),(int((self.x-offset_x)*scale),int((self.y-offset_y)*scale)),int(self.m/2*scale), 0)
        self.camera.draw(surface,scale,offset_x,offset_y)

class Food():
    def __init__(self,x,y,m,ID):
        self.quad_row = 0
        self.quad_coloum = 0
        self.x = x
        self.y = y
        self.m = m
        self.ID = ID

    def draw(self,surface, scale,offset_x,offset_y):
        pygame.draw.circle(surface,(0,0,0),(int((self.x-offset_x)*scale),int((self.y-offset_y)*scale)),int(self.m/2*scale), 0)

class Camera():
    def __init__(self,x,y,size_x,size_y):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y

    def check_visable_quadrants(self):
        visable_quadrants = []
        left_camera = self.x - self.size_x/2
        right_camera = self.x + self.size_x/2
        top_camera = self.y - self.size_y/2
        bottom_camera = self.y + self.size_y/2
        for coloum in range(number_of_quad_rows):
            for row in range(number_of_quad_coloums):
                left_quad = quad_length*coloum
                right_quad = quad_length*coloum + quad_length
                top_quad = quad_length*row
                bottom_quad = quad_length*row + quad_length
    
                if ((bottom_quad > top_camera and bottom_quad < bottom_camera) or (top_quad > top_camera and top_quad < bottom_camera)) and ((right_quad > left_camera and right_quad < right_camera) or (left_quad < right_camera and left_quad > left_camera)):
                    visable_quadrants.append([coloum,row])
                elif ((top_camera < bottom_quad and top_camera > top_quad) or (bottom_camera < bottom_quad and bottom_camera > top_quad)) and ((right_camera < right_quad  and right_camera > left_quad) or (left_camera < right_quad and left_camera > left_quad)):
                    visable_quadrants.append([coloum,row])

        return visable_quadrants
        
    def draw(self,surface, scale,offset_x,offset_y):
        pygame.draw.rect(surface,(0,0,255),(int((self.x-self.size_x/2-offset_x)*scale),int((self.y-self.size_y/2-offset_y)*scale),int(self.size_x*scale),int(self.size_y*scale)),2)

            
WHITE = (255,255,255)
screen_width = 900
screen_height = 900
screen=pygame.display.set_mode((screen_width,screen_height))
quad_length = 100
number_of_quad_rows = screen_width/quad_length
number_of_quad_coloums = screen_height/quad_length
inPlay = True

all_quadrants = Quadrants(number_of_quad_rows,number_of_quad_coloums,quad_length)
food_list = []
for i in range(1000):
    all_quadrants.add_item(Food(random.randint(0,screen_width),random.randint(0,screen_height),15,i+2))


player_x = 10
player_y = 10
player_mass = 10

client = Client(player_x,player_y,player_mass,1)
all_quadrants.add_item(client)

def redraw_screen():
    screen.fill(WHITE)
    all_quadrants.draw(screen,float(screen_width)/float(client.camera.size_x),client.camera.x-client.camera.size_x/2,client.camera.y-client.camera.size_y/2)
    pygame.display.update()
    
while inPlay:

    pygame.event.get()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x = player_x - 5
    if keys[pygame.K_RIGHT]:
        player_x = player_x + 5
    if keys[pygame.K_UP]:
        player_y = player_y - 5
    if keys[pygame.K_DOWN]:
        player_y = player_y + 5
    if keys[pygame.K_KP_PLUS]:
        client.camera.size_x = client.camera.size_x + 10
        client.camera.size_y = client.camera.size_y + 10
    if keys[pygame.K_KP_MINUS]:
        client.camera.size_x = client.camera.size_x - 10
        client.camera.size_y = client.camera.size_y - 10
    
    all_quadrants.update(client.quad_row,client.quad_coloum,1,player_x,player_y,player_mass)
    

    redraw_screen()
    pygame.time.wait(30)
