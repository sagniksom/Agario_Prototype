#########################################
# Programmer: Alex Karner
# Date: 06.15.2016
# File Name: Quadrants.py
# Description: Below are the classes for the server quadrants.
#########################################

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

