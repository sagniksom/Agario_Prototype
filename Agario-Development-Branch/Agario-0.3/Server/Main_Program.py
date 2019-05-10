#########################################
# Programmer: Alex Karner
# Date: 06.15.2016
# File Name: Server.py
# Description: Below is the main program of the server.
#########################################

import socket
import threading
import thread
import Queue
import pygame
from Quadrant_Classes import *
from Client_Classes import *
from Encrpytion_Functions import *


#################################################################################
#------------------------------Server Init--------------------------------------#
#################################################################################

##Network Variables

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = socket.gethostname()
port = 3000
print "IP: ",host
print "Port: ",port

buffer_size = 1024
connections = []

server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind((host,port))
server_socket.listen(8) #Allows 8 connections

##Game Variables

game_height = 900
game_width = 900
quad_length = 100
number_of_quad_rows = game_width/quad_length
number_of_quad_coloums = game_height/quad_length
all_quadrants = Quadrants(number_of_quad_rows,number_of_quad_coloums,quad_length)

#################################################################################
#----------------------------Sever Functions------------------------------------#
#################################################################################
def client_communication():
    while True:
        clients_info = encode(connections)
        if clients_info != '*':
            for client in connections:
                if client.sending_queue.full() == False:
                    client.sending_queue.put(clients_info)
                if client.send.running == False or client.recv.running == False:
                    connections.remove(client)
        pygame.time.wait(30)


#################################################################################
#----------------------------Sever Main Program---------------------------------#
#################################################################################
        
thread.start_new_thread(client_communication,())

while True:
    print 'Waiting for Client...'
    client_socket,client_address = server_socket.accept()       #accepts new clients and...
    print "SERVER: Connection from: "+client_address[0]
    connections.append(Client(client_socket,client_address))    #adds them to connections list


            
