#########################################
# Programmer: Alex Karner
# Date: 06.15.2016
# File Name: Client_Classes.py
# Description: Below is the send and receive classes of the client.
#########################################
import threading


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
