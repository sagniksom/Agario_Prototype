from Food_Blobs import *
from Additional_Functions import *
from labels_and_text import *
class Segment(food_blobs):
    def __init__(self, surface, playfieldWidth, playfieldHeight, player, camera):
        """(object),(int),(int),(object),(object) ---> (None)
        This is a constructor method for the segment class
        """
        food_blobs.__init__(self, surface, playfieldWidth, playfieldHeight, player.x, player.y,player.mass, camera, player.color)
        self.mass = player.mass/2
        self.duration = 0

    def collision_detection(self, item_list, item_value, required_mass, camera):
        """(list),(int),(int),(object) ---> (None)
        Detects collision with things.
        """
        for item in item_list:
            if distance(self.x,self.y,item.x,item.y) <= self.mass/3 and self.mass > required_mass:
                item_list.remove(item)
                self.mass += 120*float(item_value)/self.mass
                pygame.mixer.Sound("Eat.wav").play() 
                
    def fuse(self,player,segments,screenWidth,screenHeight,camera):
        """(object),(list),(int),(int),(object) ---> (None)
        Fuses the Player and the segment
        """
        if int(self.velocity) <= 4:
            if distance(player.x,player.y,self.x,self.y) >= self.mass/4 + player.mass/3:
                angle = math.atan2((player.y*camera.zoom + camera.y)-(self.y*camera.zoom + camera.y),(player.x*camera.zoom + camera.x)-(self.x*camera.zoom + camera.x))*180/math.pi                
                self.x += int((player.velocity*math.cos(angle*math.pi/180))) 
                self.y += int((player.velocity*math.sin(angle*math.pi/180)))
        
        if self.duration >= 400:
            player.mass += self.mass
            segments.remove(self)
            pygame.mixer.Sound("Merge.wav").play()

    def explode(self,camera,viruses,food_blob_list):
        """(object),(list),(list) ---> (None)
        Makes the segment explode when it collides with a virus.
        """
        for item in viruses:
            if distance(self.x,self.y,item.x,item.y) <= self.mass/3 and self.mass >= 100:
                food_blob_size = (self.mass*0.7)/8
                segments = points_on_circumfrence(self.mass/3,7)
                angles = [(2*math.pi/7*x)*(self.mass/3) for x in xrange(0,8)]
                pygame.mixer.Sound("Explosion.wav").play()
                for i in range(8):
                    x,y = segments[i]
                    x += self.x
                    y += self.y
                    food_blob = food_blobs(self.surface,self.playfieldWidth,self.playfieldHeight,x,y,self.mass,camera,self.color)
                    food_blob.angle = angles[i]
                    food_blob_list.append(food_blob)
                    self.mass = self.mass-food_blob_size
    
    def render(self,camera):
        """(object) ---> (None)
        Draws the segment
        """
        pygame.draw.circle(self.surface,self.color,(int(self.x*camera.zoom+camera.x),int(self.y*camera.zoom+camera.y)),int(camera.zoom*self.mass/3),0)

    def update(self,surface,player,segments,viruses,item_list, item_list_2, item_value,item_value_2, required_mass,required_mass_2, camera,screenWidth,screenHeight):
        """(object),(object),(list),(list),(list),(list),(int),(int),(int),(int),(int),(int),(object) ---> (None)
        Updates the segment
        """
        self.render(camera)
        self.move()
        self.collision_detection(item_list, item_value, required_mass, camera)
        self.collision_detection(item_list_2, item_value_2, required_mass_2, camera)
        self.fuse(player,segments,screenWidth,screenHeight,camera)
        self.explode(camera,viruses,item_list_2)
        self.render_rejoin_timer(surface,screenWidth,screenHeight)

    def render_rejoin_timer(self,surface,screenWidth,screenHeight):
        """ (object),(int),(int)  ---> (None)
        Displays a timer in the top right corner of the screen counting down until the segments rejoin after splitting
        """
        x = (screenWidth / 40)*37
        y = screenHeight / 40
        timer_label = myfont.render("Rejoin: " + (str(100-int(self.duration/4))),1,(0,0,0))
        surface.blit(timer_label, (x,y))
        
def split(segments,surface,playfieldWidth,playfieldHeight,player,camera):
    """(list),(object),(int),(int),(object),(object) ---> (None)
    Splits the player into two.
    """
    segment = Segment(surface,playfieldWidth,playfieldHeight,player,camera)
    segments.append(segment)
    player.mass /= 2
