from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import json
from time import time
import socket

format = "utf-8"
server_port = 8000
connect_msg = "connect"
disconnect_msg = "disconnect"
check_start_msg = "s"               # clients send this msg to check start
not_start_msg = 'wait'

last_sent = time()

start = False
player_states = {}

# Create UDP socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# get own ip addr
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
ip_addr = get_lan_ip()

# Ask user for server IP
server_ip = input("Enter server IP: ")
server_addr = (server_ip, server_port)


# send connect_msg to introduce to server
def sendConnect():
    client.sendto(connect_msg.encode(format), server_addr)
    data, _ = client.recvfrom(1024)
    print(f"Server: {data.decode(format)}\n")

sendConnect()

def sendCheckStart():
    global start, ip_addr, player_states
    client.sendto(check_start_msg.encode(format), server_addr)
    data, _ = client.recvfrom(1024)
    data = data.decode(format)

    # setting player states and starting game
    if data != not_start_msg:
        start = True
        data = data.split()
        for player in data:
            if player != ip_addr:
                player_states[player]['x'] = None
                player_states[player]['y'] = None

# sends and recieves updates from server and updates state
# include powerups updates here too later
def sendrecvUpdate():
    global p
    # sending update of own
    update_send = {'x': p.x, 
                   'y': p.y}
    update_send = json.dumps(update_send)
    client.sendto(update_send.encode(format), server_addr)

    # receiving updates
    update_recv, _ = client.recvfrom(1024)
    update_recv = json.loads(update_recv)

    # exclude own update and update others state
    for player, info in update_recv.items():
        if player != ip_addr:
            player_states[player]['x'] = info['x']
            player_states[player]['y'] = info['y']


# send a msg to server and recieve a reply
def send(msg):
    client.sendto(msg.encode(format), server_addr)
    data, _ = client.recvfrom(1024)
    print(f"From server: {data.decode(format)}\n")

def sendInterval():
    global last_sent
    if time() >= last_sent + 5: # todo: change this to last_sent+0.05
        last_sent = time()
        return True

class Point:
    def __init__(self):
        self.x = 100
        self.y = 100

p = Point()

def draw_points(p):
    glColor3f(1.0, 1.0, 0.0)
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(p.x, p.y) #jekhane show korbe pixel
    glEnd()


def keyboard(key, x, y):
    global p
    if key == b'w': p.y += 10
    if key == b's': p.y -= 10
    if key == b'a': p.x -= 10
    if key == b'd': p.x += 10

    glutPostRedisplay()

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    global p
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    #call the draw methods here
    draw_points(p)
    glutSwapBuffers()

def idle():
    global p
    if sendInterval():
        sendrecvUpdate()
    glutPostRedisplay()

while not(start):
    if sendInterval():
        sendCheckStart()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
glutDisplayFunc(showScreen)
glutIdleFunc(idle)
glutKeyboardFunc(keyboard)

glutMainLoop()