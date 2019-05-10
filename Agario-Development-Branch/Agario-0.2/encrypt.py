
def server_decode(string):
    "Input: 'x,y,m'"
    lst = string.split(',')
    return int(lst[0]),int(lst[1]),int(lst[2])

def server_encode(clients):
    clients_info =[]
    for client in clients:
        if client.x != False and client.y != False and client.m != False:
            clients_info.append(str(client.x)+','+str(client.y)+','+str(client.m))
    formatted_clients_info = '/'.join(clients_info)
    return '*'+formatted_clients_info


def client_decode(string):
    "Input: 'x,y,m/x,y,m'"
    lst = string.split('/')
    formatted_lst = []
    for client in lst:
        formatted_lst.append(client.split(','))
        for i in range(len(formatted_lst[-1])):
            formatted_lst[-1][i] = int(formatted_lst[-1][i])
    return formatted_lst

def client_encode(player_x,player_y,player_mass):
    "Input: [x,y,m]"   
    return '*'+str(player_x)+','+str(player_y)+','+str(player_mass)
