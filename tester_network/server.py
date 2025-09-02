import json
import socket

player_states = {}

format = "utf-8"
server_port = 8000
disconnect_msg = "disconnect"

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

# Bind to address
server.bind(server_addr)
print(f"UDP Server listening on {server_ip}:{server_port}\n")

while True:
    # Receive message from client
    data, client_addr = server.recvfrom(1024)   # max 1024 bytes
    message = data.decode(format)

    if client_addr not in player_states:
        player_states[client_addr[0]] = {'x': None,
                                      'y': None}
        print(message)
        server.sendto("LAN connection successful.".encode(format), client_addr)
    else:
        update = json.loads(message)
        player_states[client_addr]['x'] = update['x']
        player_states[client_addr]['y'] = update['y']
        print(player_states)

    #if message == disconnect_msg:
    #    print(f"Client {client_addr} disconnected.")
    #    server.sendto("Goodbye.".encode(format), client_addr)
    #else:
    #    print(f"From {client_addr}: {message}")
    #    server.sendto("Message received.".encode(format), client_addr)
