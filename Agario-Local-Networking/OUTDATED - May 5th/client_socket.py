#########################################
# Programmer: Mr. G
# Date: 03.06.2015
# File Name: client_socket.py
# Description: This program connects to an open network socket, inputs data and sends it.
#               It works with the corresponding server_socket.py program.
#               The programs are to be executed on the same computer, first the server.
#########################################
from socket import *
import threading
import Queue

PORT = 3000                             # arbitrary non-privileged port, same as on the server
BUFFER_SIZE = 1024                      # maximum amount of data that can be received at once
IP = '192.168.1.38'

socket = socket(AF_INET, SOCK_DGRAM)
socket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
socket.bind(('',PORT))

computer_number = '2'
running = True

class Recieve (threading.Thread):
    def __init__(self,q,socket,buffer_size):
        threading.Thread.__init__(self)
        self.q = q
        self.buffer_size = buffer_size
        self.socket = socket
        
    def run (self):
        while True:
            print 'Recieving Thread waiting for data...'
            self.m = str(self.socket.recvfrom(self.buffer_size)[0])
            if not self.q.full():
                self.q.put(self.m)

    
class Send (threading.Thread):
    def __init__(self,q,socket):
        threading.Thread.__init__(self)
        self.q = q
        self.socket = socket
        
    def run(self): 
        while True:
            while not self.q.empty():
                data = self.q.get()
                print 'sending: '+data
                socket.sendto(data,('192.168.1.38',PORT))

#____________________________Main Program_________________________________________________
print 'CLIENT '+computer_number+': Setting up Queues...'
recieving_q = Queue.Queue(10)
sending_q = Queue.Queue(10)
print 'CLIENT '+computer_number+': Queues setup.'

print 'CLIENT '+computer_number+': Starting recieving thread...'
recieving = Recieve(recieving_q,socket,BUFFER_SIZE)
recieving.start()
print 'CLIENT '+computer_number+': Started recieving thread.'

print 'CLIENT '+computer_number+': Starting sending thread...'
sending = Send(sending_q,socket)
sending.start()
print 'CLIENT '+computer_number+': Started sending thread.'


while True:
    if recieving.q.empty() == False:
        string_from_queue = recieving.q.get()
        print 'CLIENT '+computer_number+': Recieved '+string_from_queue
        list_from_queue = string_from_queue.split(',')
        print list_from_queue
        list_from_queue[int(computer_number)-1] = '5'
        packed_string = ','.join(list_from_queue)
        sending.q.put(packed_string)

