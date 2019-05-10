import socket
import threading
import thread
import Queue
import pygame
import encrypt

##Initialization
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = socket.gethostname()
print host
port = 3000
buffer_size = 1024
connections = []

server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind((host,port))
server_socket.listen(5) #Allows 5 connections

## Classes
class Client(threading.Thread):
    def __init__(self,socket,address):
        """This class is used to hold all information for all the clients that join the server
        Example: ip, name, coordinates """
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.recieving_queue = Queue.Queue(10)
        self.sending_queue = Queue.Queue(10)
        self.send = Send(self.socket,self.address,self.sending_queue)
        self.send.start()
        self.recv = Recieve(self.socket,self.address,self.recieving_queue)
        self.recv.start()
        self.x = False
        self.y = False
        self.m = False
        self.start()

    def run(self):
        while True:
            if self.recieving_queue.empty() == False:
                data = self.recieving_queue.get()
                self.x,self.y,self.m = encrypt.server_decode(data)

class Send(threading.Thread):
    def __init__(self,socket,address,queue):
        threading.Thread.__init__(self)
        self.socket = socket
        self.queue = queue
        self.address = address
        self.running = True
        
    def run(self):  
        while self.running:
            if self.queue.empty() == False:
                send_data = self.queue.get()
                try:
                    self.socket.sendall(send_data)
                except:
                    print "Cannot send data to: "+self.address[0]
                    self.socket.close()
                    print "Ended Connection with "+self.address[0]
                    self.running = False

class Recieve(threading.Thread):
    def __init__(self,socket,address,queue):
        threading.Thread.__init__(self)
        self.socket = socket
        self.queue = queue
        self.address = address
        self.running = True
        
    def run(self):
        while self.running:
            if self.queue.full() == False:
                try:
                    recieved_data = self.socket.recv(1024)
                    packets = recieved_data[1:].split('*')
                except:
                    print "Cannot receive data from: "+self.address[0]
                    self.socket.close()
                    print "Ended Connection with "+self.address[0]
                    self.running = False
                for packet in packets:
                   self.queue.put(packet)

## Functions
def client_communication():
    while True:
        clients_info = encrypt.server_encode(connections)
        if clients_info != '*':
            for client in connections:
                if client.sending_queue.full() == False:
                    client.sending_queue.put(clients_info)
                if client.send.running == False or client.recv.running == False:
                    connections.remove(client)
        pygame.time.wait(30)


## Main program 
thread.start_new_thread(client_communication,())

while True:
    print 'Waiting for Client...'
    client_socket,client_address = server_socket.accept()       #accepts new clients and...
    print "SERVER: Connection from: "+client_address[0]
    connections.append(Client(client_socket,client_address))    #adds them to connections list


            
