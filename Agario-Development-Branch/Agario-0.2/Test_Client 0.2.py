import socket
import threading
import thread
import Queue
import pygame
import encrypt

pygame.init()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('Server-PC', 3000)
print 'Connecting to server...'
client_socket.connect(server_address)
print 'Connected to server :)'

class Send(threading.Thread):
    def __init__(self,sock,queue):
        threading.Thread.__init__(self)
        self.sock = sock
        self.queue = queue
        self.running = True
        
    def run(self):
        while self.running:
            if self.queue.empty() == False:
                send_data = self.queue.get()
                try:
                    self.sock.sendall(send_data)
                except:
                    print "Cannot send data to server"
                    self.sock.close()
                    print "Ended Connection with server"
                    self.running = False

class Recieve(threading.Thread):
    def __init__(self,sock,queue):
        threading.Thread.__init__(self)
        self.sock = sock
        self.queue = queue
        self.running = True
        
    def run(self):
        while self.running:
            if self.queue.full() == False:
                try:
                    recieved_data = self.sock.recv(1024)
                except:
                    print "Cannot receive data from server"
                    self.sock.close()
                    print "Ended Connection with server"
                    self.running = False
                packets = recieved_data[1:].split('*')
                for packet in packets:
                    self.queue.put(packet)

print 'CLIENT: Setting up Queues...'
recieving_queue = Queue.Queue(10)
sending_queue = Queue.Queue(10)
print 'CLIENT: Queues setup.'

print 'CLIENT: Starting recieving thread...'
recieving = Recieve(client_socket,recieving_queue)
recieving.start()
print 'CLIENT: Started recieving thread.'

print 'CLIENT: Starting sending thread...'
sending = Send(client_socket,sending_queue)
sending.start()
print 'CLIENT: Started sending thread.'


WHITE = (255,255,255)
screenWidth = 900
screenHeight = 900
screen=pygame.display.set_mode((screenWidth,screenHeight))
player_x = 10
player_y = 10
player_mass = 50
inPlay = True
all_players_info = []

def redraw_screen():
    screen.fill(WHITE)
    for player in all_players_info:
        pygame.draw.circle(screen,(0,0,0),(player[0],player[1]),player[2]/2, 0)
    pygame.display.update()

def get_players_info():
    global all_players_info
    while inPlay:
        if recieving_queue.empty() == False:
            data = recieving_queue.get()
            all_players_info = encrypt.client_decode(data)

thread.start_new_thread(get_players_info,())


while inPlay:
    moved = False

    pygame.event.get()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x = player_x - 5
        moved = True
    if keys[pygame.K_RIGHT]:
        player_x = player_x + 5
        moved = True
    if keys[pygame.K_UP]:
        player_y = player_y - 5
        moved = True
    if keys[pygame.K_DOWN]:
        player_y = player_y + 5
        moved = True
    if keys[pygame.K_ESCAPE]:
        inPlay = False
        
##    if moved == True:
    if recieving.running == False or sending.running == False:
        inPlay = False
        
    sending_queue.put(encrypt.client_encode(player_x,player_y,player_mass))
    redraw_screen()
    pygame.time.wait(30)
    

sending.running = False
sending.sock.close()
recieving.running = False
recieving.sock.close()
pygame.quit()
