import json
import socket
import threading
import random


format = "utf-8"
server_port = 8000
connect_msg = 'connect'             # player must send this message to connect, implement this in player code
disconnect_msg = "disconnect"       # implement this too in player code
check_start_msg = "s"               # clients send this msg to check start
not_start_msg = 'wait'

player_states = {}

# Create UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Get LAN IP
def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        print("LMAO")
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

server_ip = get_lan_ip()
server_addr = (server_ip, server_port)
CONNECT_REPLY_MSG = f"You connected to {server_ip}"

# maps
def makeMap():
    map_outline = np.array([[2 for _ in range(102)] for _ in range(102)])
    map_outline[0, :] = 1
    map_outline[-1, :] = 1
    map_outline[:, 0] = 1
    map_outline[:, -1] = 1

    # section 1
    map_outline[20, :11] = 1
    map_outline[20:81, 10] = 1
    map_outline[80, 1:10] = 1
    map_outline[30, 11:21] = 1
    map_outline[21:80, 0:10] = 0

    # section 2
    map_outline[1:11, 10] = 1
    map_outline[10, 10:55] = 1
    map_outline[10:25, 54] = 1
    map_outline[24, 54:66] = 1
    map_outline[10:36, 65] = 1
    map_outline[10, 65:91] = 1
    map_outline[1:11, 90] = 1
    map_outline[11:31, 28] = 1
    map_outline[0:10, 11:90] = 0
    map_outline[10:24, 55:65] = 0

    # section 3
    map_outline[91:101, 10] = 1
    map_outline[91, 10:53] = 1
    map_outline[77:91, 52] = 1
    map_outline[77, 52:61] = 1
    map_outline[77:92, 60] = 1
    map_outline[91, 60:91] = 1
    map_outline[91:101, 90] = 1
    map_outline[71:91, 40] = 1
    map_outline[92:102, 11:90] = 0
    map_outline[78:92, 53:60] = 0

    # section 4
    map_outline[20, 90:101] = 1
    map_outline[20:81, 90] = 1
    map_outline[80, 90:101] = 1
    map_outline[35, 75:90] = 1
    map_outline[21:80, 91:102] = 0

    # section 5
    map_outline[40:76, 28] = 1
    map_outline[75, 20:29] = 1
    map_outline[57:76, 20] = 1
    map_outline[57, 20:28] = 1
    map_outline[58:75, 21:28] = 0

    # section 6
    map_outline[32:58, 40] = 1
    map_outline[57, 40:61] = 1
    map_outline[51:58, 60] = 1
    map_outline[50, 40:74] = 1
    map_outline[50:77, 73] = 1
    map_outline[51:57, 41:60] = 0

    # section 7
    map_outline[64, 40:61] = 1
    return map_outline

map = makeMap()

def genPwCoords():
    pw_coords = {
        'speed 1': [random.randint(1,100),random.randint(1,100)],
        'speed 2': [random.randint(1,100),random.randint(1,100)],
        'range 1': [random.randint(1,100),random.randint(1,100)],
        'range 2': [random.randint(1,100),random.randint(1,100)],
        'speed 1': [random.randint(1,100),random.randint(1,100)],
        'speed 2': [random.randint(1,100),random.randint(1,100)]}
    for i in pw_coords:
        if pw_coords[i]

# Bind to address
server.bind(server_addr)
print(f"UDP Server listening on {server_ip}:{server_port}\n")

def handleMessage(message, client_addr):
    player = client_addr[0]
    message = message.decode(format)

    print(message)

    # start logics
    if message == check_start_msg:
        if len(player_states) == 4:
            # listing the players in a str and send
            players = []
            for player in player_states:
                players.append(player)
            players = ' '.join(players)

            server.sendto(players.encode(format), client_addr)
        else:
            server.sendto(not_start_msg.encode(format), client_addr)

    elif message == connect_msg:
        player_states[player] = {'x': None,
                                 'y': None}
        server.sendto(CONNECT_REPLY_MSG.encode(format), client_addr)
        print(f"{player} has connected to LAN.")
        
    elif message == disconnect_msg:
        print("Connection terminated with", player)
        server.sendto("Disconnected.".encode(format), client_addr)
        return
    
    else:
        # updating
        update_recv = json.loads(message)
        # for key, val in player_states[player]:
        #     player_states[player][key] = update[key]
        player_states[player]['x'] = update_recv['x']
        player_states[player]['y'] = update_recv['y']

        # sending updates
        update_send = json.dumps(player_states)
        server.sendto(update_send.encode(format), client_addr)
        print(player_states)

while True:
    message, client_addr = server.recvfrom(1024)
    thread = threading.Thread(target=handleMessage, args=(message, client_addr))
    thread.start()