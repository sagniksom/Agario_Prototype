#########################################
# Programmer: Alex Karner
# Date: 06.15.2016
# File Name: Client_Classes.py
# Description: Below is the Client class and send and recieve for the server.
#########################################
import threading
import Queue
from Encrpytion_Functions import *

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
                self.x,self.y,self.m = decode(data)

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
