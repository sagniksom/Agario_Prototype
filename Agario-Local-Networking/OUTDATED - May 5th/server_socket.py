#########################################
# Programmer: Mr. G
# Date: 03.06.2015
# File Name: server_socket.py
# Description: This program opens a network socket, receives data and prints it
#               It works with the corresponding client_socket.py program.
#               The programs are to be executed on the same computer, first the server.
#########################################
from socket import *
import threading
import Queue
import time

PORT = 3000                             # arbitrary non-privileged port
BUFFER_SIZE = 1024                      # maximum amount of data that can be received at once

socket = socket(AF_INET, SOCK_DGRAM)
socket.setsockopt(SOL_SOCKET, SO_BROADCAST,1)
socket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
socket.bind(('', PORT))                 # sets "PORT" as the port that will be used for communication


class Recieve (threading.Thread):
    def __init__(self,q,socket,buffer_size):
        threading.Thread.__init__(self)
        self.q = q
        self.addr = False
        self.buffer_size = buffer_size
        self.socket = socket
        
    def run (self):
        while True:
            self.m, self.ip = self.socket.recvfrom(self.buffer_size)
            self.q.put([self.ip, self.m])
                
class Send (threading.Thread):
    def __init__(self,q,socket):
        threading.Thread.__init__(self)
        self.q = q
        self.socket = socket
        
    def run (self):
        while True:
            self.socket.sendto(sent_data,('<broadcast>', PORT))
            print 'SERVER: Sent Data: '+sent_data
            time.sleep(0.1)

sent_data = '1,2,3,4,5,6,7,8'

print 'SERVER: Setting up Queues...'
recieving_q = Queue.Queue(10)
sending_q = Queue.Queue(10)
print 'SERVER: Queues setup.'

print 'SERVER: Starting sending thread...'
sending = Send(sending_q,socket)
sending.start()
print 'SERVER: Started sending thread.'

print 'SERVER: Starting recieving thread...'
recieving = Recieve(recieving_q,socket,BUFFER_SIZE)
recieving.start()
print 'SERVER: Started recieving thread.'


while True:
    if recieving.q.empty() == False:
        client_ip, message = recieving.q.get()
        if client_ip != ('192.168.1.38',3000):
            print 'SERVER: Recieved '+str(message)+' from '+str(client_ip)

conn.close()                            # always close the connection socket; otherwise the process will stay active
