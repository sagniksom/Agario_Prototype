#########################################
# Programmer: Alex Karner
# Date: 06.15.2016
# File Name: Server_Encrpyt.py
# Description: Below is the server encrpytion functions.
#########################################

def decode(string):
    "Input: 'x,y,m'"
    lst = string.split(',')
    return int(lst[0]),int(lst[1]),int(lst[2])

def encode(clients):
    clients_info =[]
    for client in clients:
        if client.x != False and client.y != False and client.m != False:
            clients_info.append(str(client.x)+','+str(client.y)+','+str(client.m))
    formatted_clients_info = '/'.join(clients_info)
    return '*'+formatted_clients_info

