#########################################
# Programmer: Alex Karner
# Date: 06.15.2016
# File Name: Quadrants.py
# Description: Below are the encrpyt functions for the client.
#########################################

def decode(string):
    "Input: 'x,y,m/x,y,m'"
    lst = string.split('/')
    formatted_lst = []
    for client in lst:
        formatted_lst.append(client.split(','))
        for i in range(len(formatted_lst[-1])):
            formatted_lst[-1][i] = int(formatted_lst[-1][i])
    return formatted_lst

def encode(player_x,player_y,player_mass):
    "Input: [x,y,m]"   
    return '*'+str(player_x)+','+str(player_y)+','+str(player_mass)
