from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import random
from time import time
import numpy as np

width, height = 1200, 690

cam_angle = math.pi/2
cam_radius = 800
cam_height = 800
camera_pos = (cam_radius * math.cos(cam_angle), cam_radius * math.sin(cam_angle), cam_height)
look_at = (0, 0, 0)
fovY = 90

t1 = time()

GRID_LENGTH = 50

controls = {'fw': False,
            'bw': False,
            'l': False,
            'r': False}

game_state = {'over': False,
              'cam': 'fpv'}

def delT():                           # needs to be implemented later
    global t1
    t2 = time()
    dt = t2 - t1
    t1 = t2
    return dt

# def setupCamera():                    # only first person cam
#     global width, height, camera_pos, look_at, player
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     gluPerspective(fovY, width/height, 1.0, 3000)
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()
    
#     rad = math.radians(player.angle + 90)
#     cx = player.x  # Fixed camera position at player's x
#     cy = player.y
#     cz = player.z + 160  # Fixed height above player
#     lx = cx - math.cos(rad) * 200  # Rotate look-at point
#     ly = cy - math.sin(rad) * 200
#     lz = cz - 60  # Maintain downward tilt
#     gluLookAt(cx, cy, cz, lx, ly, lz, 0, 0, 1)


# apatoto kept third person view for testing purpose
lx_last = 0
ly_last = 0
lz_last = 0
def setupCamera():
    global width, height, camera_pos, game_state, look_at, player, lx_last, ly_last, lz_last
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, width/height, 1.0, 3000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if game_state['cam'] == 'tpv':
        cx, cy, cz = camera_pos
        gluLookAt(cx, cy, cz, 0, 0, 0, 0, 0, 1)
    
    if game_state['cam'] == 'fpv':
        rad = math.radians(player.angle + 90)
        cx = player.x  # Fixed camera position at player's x
        cy = player.y
        cz = player.z + 200  # Fixed height above player
        lx = cx - math.cos(rad) * 200  # Rotate look-at point
        ly = cy - math.sin(rad) * 200
        lz = cz - 60  # Maintain downward tilt
        gluLookAt(cx, cy, cz, lx, ly, lz, 0, 0, 1)

    
def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18): # type: ignore
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

# mapping the grid
# 0 - black, 1 - wall, 2 - free space

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

def drawMap():
    global GRID_LENGTH, map, player
    grid_mid = GRID_LENGTH/2

    for i in range(len(player.active_blocks)):
        for j in range(len(player.active_blocks)):
            if player.active_blocks[i][j]:
                if map[i][j] == 1:      # for wall use this as reference, for testing call drawWall() in here
                    x = (i - len(map)//2) * GRID_LENGTH
                    y = (j - len(map)//2) * GRID_LENGTH

                    glBegin(GL_QUADS)
                    if player.active_blocks[i][j] == 1:
                        glColor3f(0.05, 0.05, 0.05) 
                    if player.active_blocks[i][j] == 2:
                        glColor3f(*colorFunc(x+25, y-25, 1, 1, 1))
                    glVertex3f(x + GRID_LENGTH, y, 0)
                    glVertex3f(x, y, 0)
                    glVertex3f(x, y - GRID_LENGTH, 0)
                    glVertex3f(x + GRID_LENGTH, y - GRID_LENGTH, 0)
                    glEnd()

                    # glPointSize(5)
                    # glBegin(GL_POINTS)
                    # glColor3f(0, 1, 0)
                    # glVertex3f(x+25, y-25, 0) # center point of the block
                    # dglEnd()


                elif map[i][j] == 2:    # for free space use this as reference, for testing call drawBlock() in here
                    x = (i - len(map)//2) * GRID_LENGTH
                    y = (j - len(map)//2) * GRID_LENGTH

                    glBegin(GL_QUADS)
                    if player.active_blocks[i][j] == 1:
                        glColor3f(0.05, 0.05*0, 0.05*0) 
                    if player.active_blocks[i][j] == 2:
                        glColor3f(*colorFunc(x+25, y-25, 1, 0, 0))
                    glVertex3f(x + GRID_LENGTH, y, 0)
                    glVertex3f(x, y, 0)
                    glVertex3f(x, y - GRID_LENGTH, 0)
                    glVertex3f(x + GRID_LENGTH, y - GRID_LENGTH, 0)
                    glEnd()

def drawBlock():
    pass

def drawWall(i, j):
    global GRID_LENGTH, map 
    x = (i - len(map)//2) * GRID_LENGTH
    y = (j - len(map)//2) * GRID_LENGTH
    
    glPushMatrix()
    glTranslatef(x + 25, y - 25, 80)
    glScalef(1, 1, 4)
    glColor3f(.2,.2,.2)
    # if player.active_blocks[i][j] == 1:
    #     glColor3f(0.05, 0.05, 0.05) 
    # if player.active_blocks[i][j] == 2:
    #     glColor3f(*colorFunc(x+25, y-25, 1, 1, 1))
    glutSolidCube(50)
    glPopMatrix()


sin_table = [math.sin(math.radians(a)) for a in range(360)]
cos_table = [math.cos(math.radians(a)) for a in range(360)]
class Player:
    global GRID_LENGTH, wall_coords
    def __init__(self):
        self.angle = 0
        self.x = -100
        self.y = 50
        self.z = 0
        self.speed = 80
        self.view_range = 600
        self.active_blocks = np.zeros((len(map), len(map)), dtype=np.float32)
        self.activeBlocks()
    
    def rotateLeft(self, dt, ang=40):
        self.angle += ang * dt
        self.activeBlocks()

    def rotateRight(self, dt, ang=40):
        self.angle -= ang * dt
        self.activeBlocks()

    def goForward(self, dt):
        rad = math.radians(self.angle-90)
        next_x = self.x + math.cos(rad) * self.speed * dt
        next_y = self.y + math.sin(rad) * self.speed * dt

        next_i = int((next_x) // GRID_LENGTH + len(map)//2)
        next_j = int((next_y) // GRID_LENGTH + len(map)//2) + 1

        next_i_offset_plus = int((next_x + 25) // GRID_LENGTH + len(map)//2)
        next_j_offset_plus = int((next_y + 25) // GRID_LENGTH + len(map)//2) + 1
        next_i_offset_minus = int((next_x - 25) // GRID_LENGTH + len(map)//2)
        next_j_offset_minus = int((next_y - 25) // GRID_LENGTH + len(map)//2) + 1

        collision_x = False
        collision_y = False

        if map[next_i_offset_plus][next_j] == 1 or map[next_i_offset_minus][next_j] == 1: collision_x = True
        if map[next_i][next_j_offset_plus] == 1 or map[next_i][next_j_offset_minus] == 1: collision_y = True

        if not collision_x: self.x = next_x
        if not collision_y: self.y = next_y
        # print(self.x, self.y)
        self.activeBlocks()

    def goBackward(self, dt):
        rad = math.radians(self.angle-90)
        next_x = self.x - math.cos(rad) * self.speed * dt
        next_y = self.y - math.sin(rad) * self.speed * dt

        next_i = int((next_x) // GRID_LENGTH + len(map)//2)
        next_j = int((next_y) // GRID_LENGTH + len(map)//2) + 1

        next_i_offset_plus = int((next_x + 25) // GRID_LENGTH + len(map)//2)
        next_j_offset_plus = int((next_y + 25) // GRID_LENGTH + len(map)//2) + 1
        next_i_offset_minus = int((next_x - 25) // GRID_LENGTH + len(map)//2)
        next_j_offset_minus = int((next_y - 25) // GRID_LENGTH + len(map)//2) + 1

        collision_x = False
        collision_y = False

        if map[next_i_offset_plus][next_j] == 1 or map[next_i_offset_minus][next_j] == 1: collision_x = True
        if map[next_i][next_j_offset_plus] == 1 or map[next_i][next_j_offset_minus] == 1: collision_y = True

        if not collision_x: self.x = next_x
        if not collision_y: self.y = next_y
        self.activeBlocks()

    def activeBlocks(self, max_blocks=50, cone_angle=45, cone_range=15):
        """
        0 - not rendered
        1 - rendered but not in range
        2 - rendered and in range
        """
        n = len(map)
        self.active_blocks = np.zeros((len(map), len(map)), dtype=np.float32)

        px, py = int(self.x), int(self.y)
        p_angle = (self.angle-45) % 360
        pxi, pyi = int(px//GRID_LENGTH + n//2), int(py//GRID_LENGTH + n//2)

        # around blocks
        self.active_blocks[max(pxi-17,0):min(pxi+18,n), max(pyi-17,0):min(pyi+18,n)] = 1

        # cone blocks
        cone_blocks = findConeBlocks(pxi, pyi, p_angle)
        # print(cone_blocks)
        for i, j in cone_blocks:
            if 0 <= i < n and 0 <= j < n:
                self.active_blocks[i, j] = 2
            
view_angle = 60
def colorFunc(x, y, r, g, b):
    global player
    vx, vy = x-player.x, y-player.y
    dist = math.sqrt(vx**2 + vy**2)

    if dist == 0:
        bright = 1
    else:
        vx, vy = vx/dist, vy/dist

        dx = sin_table[int(player.angle%360)]
        dy = -cos_table[int(player.angle%360)]
        dlen = math.sqrt(dx**2 + dy**2)
        dx, dy = dx/dlen, dy/dlen

        dot = vx*dx + vy*dy

        angle_fac = max(0, (dot - cos_table[view_angle]) / (1 - cos_table[view_angle]))
        dist_fac = max(1, 1 - (dist / view_range))

        bright = 0.05 + 0.95 * angle_fac * dist_fac
    return bright*r, bright*g, bright*b

view_range=15
view_angle=60
view_range_sq = view_range * view_range

def findConeBlocks(x, y, dir_angle):
    global view_range, view_angle, view_range_sq
    blockij = set()
    rad = math.radians(dir_angle-45)
    fx = math.cos(rad)
    fy = math.sin(rad)

    half_view_angle = math.radians(view_angle / 2)

    for dx in range(-view_range, view_range+1):
        for dy in range(-view_range, view_range+1):
            if not(dx) and not(dy):
                blockij.add((x, y))
                continue

            vx, vy = dx, dy
            dist_sq = vx*vx + vy*vy
            if dist_sq > view_range_sq:
                continue

            dist = math.sqrt(dist_sq)
            vx, vy = vx/dist, vy/dist
            dot = fx*vx + fy*vy
            angle = math.acos(max(-1, min(1, dot)))

            if angle <= half_view_angle:
                steps = int(dist)
                sight_hit_wall = False
                for b in range(1, steps+1):
                    bx = int(x + vx * b)
                    by = int(y + vy * b)
                    if map[bx][by] == 1 and 0 <= bx < len(map) and 0 <= by < len(map):
                        sight_hit_wall = True
                        break
                if not(sight_hit_wall):
                    blockij.add((x+dx, y+dy))
                
    return blockij

player = Player()

def drawCube(w, h,d, color):
    glPushMatrix()
    glScalef(w, h, d)
    glColor3f(*color)
    glutSolidCube(1.0)
    glPopMatrix()
    
def drawPlayer(p):
    global game_state
    glPushMatrix()
    
    # Apply player transform
    if game_state['over']:
        glRotatef(90, 0, 1, 0)  # Tilt if game over
    glTranslatef(p.x, p.y, p.z+50)
    glRotatef(p.angle, 0, 0, 1)

    
    glScalef(40, 40, 40)

    #torso
    glPushMatrix()
    glTranslatef(0, 0, 1)
    drawCube(1.0, 0.5, 1.5, (0.0, 0.4, 0.2)) 
    glPopMatrix()

    #head
    glPushMatrix()
    glTranslatef(0, 0, 2.4)
    drawCube(0.8, 0.8, 0.8, (1.0, 0.8, 0.6))  
    glPopMatrix()
    #eyes
    glPushMatrix()
    glTranslatef(0, -0.45, 2.5)  

    
    glPushMatrix()
    glTranslatef(-0.2, 0, 0)  
    drawCube(0.15, 0.05, 0.05, (0,0,0))  
    glPopMatrix()

    
    glPushMatrix()
    glTranslatef(0.2, 0, 0)  
    drawCube(0.15, 0.05, 0.05, (0,0,0))
    glPopMatrix()

    glPopMatrix()
    #hair remove if its unnecessary
    glPushMatrix()
    glTranslatef(0, 0, 2.9)  
    glScalef(1.0, 1.0, 0.3)  
    drawCube(0.75, 0.75, 0.75, (0.0, 0.0, 0.0)) 
    glPopMatrix()

    #rightarm
    glPushMatrix()
    glTranslatef(-0.65, 0, 1.9)
    glRotatef(-80, 1, 0, 0)           
    glRotatef(10, 0, 1, 0)    

    drawCube(0.4, 0.4, 1.4, (1.0, 0.8, 0.6))  
    #weapon
    glPushMatrix()
    glTranslatef(0, -0.1, -1.5)           
    glRotatef(10, 0, 1, 0)            
    glColor3f(0.3, 0.3, 0.3)           
    gluCylinder(gluNewQuadric(), 0.05, 0.1, 0.8, 8, 2)
    glPopMatrix()

    glPopMatrix()

    #leftarm
    glPushMatrix()
    glTranslatef(0.65, 0, 1.9)
    glRotatef(30, 1, 0, 0) 
    drawCube(0.4, 0.4, 1.4, (1.0, 0.8, 0.6))
    
    
    glPushMatrix()
    glTranslatef(0, 0, 0.2)        
    glRotatef(-10, 0, 0, 1)        
    glColor3f(0.5, 0.25, 0.1)     
    gluCylinder(gluNewQuadric(), 0.1, 0.1, 1.2, 8, 8)  #torch 

    #fire
    glTranslatef(0, 0, 1.2)      
    glColor3f(1.0, 0.5, 0.0)       
    glutSolidCube(0.4)

    glPopMatrix() 
    glPopMatrix()  

    #legs
    glPushMatrix()
    glTranslatef(-0.35, 0, -0.4)
    drawCube(0.4, 0.4, 1.4, (0.2, 0.1, 0.6)) #right
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0.4, 0, -0.4)
    drawCube(0.4, 0.4, 1.4, (0.2, 0.1, 0.6))
    glPopMatrix()

    glPopMatrix()

def draw_creature(x, y, z):
    global player
    glPushMatrix()
    ang = math.degrees(math.atan2(player.y - y, player.x - x)) + 90
    glTranslatef(x, y, z)
    glRotatef(ang, 0, 0, 1)
    glScalef(1.3, 1.3, 1.3)
    

    glPushMatrix()
    glTranslatef(0, 0, 90) 
    glScalef(30, 20, 60)   
    glColor3f(0.1, 0.1, 0.1)  
    glutSolidCube(1)
    glPopMatrix()
    
    # Head
    glPushMatrix()
    glTranslatef(0, 0, 135)  
    glScalef(25, 25, 25)     
    glColor3f(0.15, 0.15, 0.15)  
    glutSolidCube(1)
    glPopMatrix()
    
    # Left eye
    glPushMatrix()
    glTranslatef(-8, -15, 135) 
    glScalef(4, 2, 4)
    glColor3f(1.0, 0.0, 0.0) 
    glutSolidCube(1.0)
    glPopMatrix()
    
    # Right eye  
    glPushMatrix()
    glTranslatef(8, -15, 135)   
    glScalef(4, 2, 4)
    glColor3f(1.0, 0.0, 0.0)   #
    glutSolidCube(1.0)
    glPopMatrix()
    
    # Left arm
    glPushMatrix()
    glTranslatef(-20, 0, 80)    
    glScalef(8, 8, 70)          
    glColor3f(0.1, 0.1, 0.1)
    glutSolidCube(1.0)
    glPopMatrix()
    
    # Right arm
    glPushMatrix()
    glTranslatef(20, 0, 80)   
    glScalef(8, 8, 70)        
    glColor3f(0.1, 0.1, 0.1)
    glutSolidCube(1.0)
    glPopMatrix()
    
    # Left leg
    glPushMatrix()
    glTranslatef(-8, 0, 30)     
    glScalef(8, 8, 60)          
    glColor3f(0.1, 0.1, 0.1)
    glutSolidCube(1.0)
    glPopMatrix()
    
    # Right leg
    glPushMatrix()
    glTranslatef(8, 0, 30)     
    glScalef(8, 8, 60)          
    glColor3f(0.1, 0.1, 0.1)
    glutSolidCube(1.0)
    glPopMatrix()
    
    glPopMatrix()
def specialKeyListener(key, x, y):
    global camera_pos, cam_angle, cam_radius, cam_height
    x, y, z = camera_pos

    if game_state['cam'] == 'tpv':
        if key == GLUT_KEY_UP: cam_height = min(cam_height+10, 1320)
        if key == GLUT_KEY_DOWN: cam_height = max(cam_height-10, 400)
        if key == GLUT_KEY_LEFT: cam_angle -= 0.01
        if key == GLUT_KEY_RIGHT: cam_angle += 0.01

    x = cam_radius * math.cos(cam_angle)
    y = cam_radius * math.sin(cam_angle)
    z = cam_height

    camera_pos = (x, y, z)

def keyboardListener(key, x, y):
    global game_state, player
    if not(game_state['over']):
        if key == b'w': controls['fw'] = True
        if key == b's': controls['bw'] = True
        if key == b'a': controls['l'] = True
        if key == b'd': controls['r'] = True
    
    if key == b'c':
        if game_state['cam'] == 'fpv': game_state['cam'] = 'tpv'
        else: game_state['cam'] = 'fpv'

def keyboardUpListener(key, x, y):
    global game_state, player
    if not(game_state['over']):
        if key == b'w': controls['fw'] = False
        if key == b's': controls['bw'] = False
        if key == b'a': controls['l'] = False
        if key == b'd': controls['r'] = False
    

def mouseListener(button, state, x, y):
    global camera_pos, cam_radius, cam_angle, cam_height, player
    if state == GLUT_DOWN:
        if button == GLUT_LEFT_BUTTON:
            pass

def idle():
    global game_state, player
    dt = delT()

    # controls
    if controls['fw']: player.goForward(dt)
    if controls['bw']: player.goBackward(dt)
    if controls['l']: player.rotateLeft(dt)
    if controls['r']: player.rotateRight(dt)

    pass
        
    glutPostRedisplay()

def showScreen():
    global width, height, player
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, width, height)  # Set viewport size

    setupCamera()  # Configure camera perspective

    #grid()
    
    drawPlayer(player)
    drawMap()
    drawWall()
    draw_creature()        
    glutSwapBuffers()

def main():
    global width, height
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutKeyboardUpFunc(keyboardUpListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically
    
    glEnable(GL_DEPTH_TEST) # enable depth
    glutMainLoop()

if __name__ == "__main__":
    main()



