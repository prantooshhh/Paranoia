from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import random
from time import time

width, height = 1200, 690

cam_angle = math.pi/2
cam_radius = 800
cam_height = 800
camera_pos = (cam_radius * math.cos(cam_angle), cam_radius * math.sin(cam_angle), cam_height)
look_at = (0, 0, 0)
fovY = 90

t1 = time()

GRID_LENGTH = 150

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
        cz = player.z + 160  # Fixed height above player
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

# 4 rectangles of a block
def gridBlock(x, y):
    global GRID_LENGTH
    glBegin(GL_QUADS)

    glColor3f(1, 1, 1)
    
    glVertex3f(GRID_LENGTH+x, 0+y, 0)
    glVertex3f(0+x, 0+y, 0)
    glVertex3f(0+x, -GRID_LENGTH+y, 0)
    glVertex3f(GRID_LENGTH+x, -GRID_LENGTH+y, 0)

    glVertex3f(0+x, 0+y, 0)
    glVertex3f(-GRID_LENGTH+x, 0+y, 0)
    glVertex3f(-GRID_LENGTH+x, GRID_LENGTH+y, 0)
    glVertex3f(0+x, GRID_LENGTH+y, 0)

    glColor3f(0.7, 0.5, 0.95)

    glVertex3f(0+x, -GRID_LENGTH+y, 0)
    glVertex3f(-GRID_LENGTH+x, -GRID_LENGTH+y, 0)
    glVertex3f(-GRID_LENGTH+x, 0+y, 0)
    glVertex3f(0+x, 0+y, 0)

    glVertex3f(GRID_LENGTH+x, 0+y, 0)
    glVertex3f(0+x, 0+y, 0)
    glVertex3f(0+x, GRID_LENGTH+y, 0)
    glVertex3f(GRID_LENGTH+x, GRID_LENGTH+y, 0)

    glEnd()

# a block of grid iterated in a loop to replicate
def grid():
    grid_size = 1200

    for i in range(-grid_size//2, grid_size//2+1, 300):
        for j in range(-grid_size//2, grid_size//2+1, 300):
            gridBlock(i,j)

    gridBorders(grid_size)

# borders of grid
def gridBorders(size):
    size += 300
    border_size = 125
    glBegin(GL_QUADS)

    glColor3f(0,1,1)
    glVertex3f(size/2, -size/2, border_size)
    glVertex3f(-size/2, -size/2, border_size)
    glVertex3f(-size/2, -size/2, 0)
    glVertex3f(size/2, -size/2, 0)

    glColor3f(0,0,1)
    glVertex3f(-size/2, -size/2, border_size)
    glVertex3f(-size/2, size/2, border_size)
    glVertex3f(-size/2, size/2, 0)
    glVertex3f(-size/2, -size/2, 0)

    glColor3f(0,1,0)
    glVertex3f(size/2, -size/2, border_size)
    glVertex3f(size/2, size/2, border_size)
    glVertex3f(size/2, size/2, 0)
    glVertex3f(size/2, -size/2, 0)

    glColor3f(1,1,1)
    glVertex3f(size/2, size/2, border_size)
    glVertex3f(-size/2, size/2, border_size)
    glVertex3f(-size/2, size/2, 0)
    glVertex3f(size/2, size/2, 0)

    glEnd()

class Player:
    global GRID_LENGTH
    def __init__(self):
        self.angle = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.speed = 80
    
    def rotateLeft(self, dt, ang=40):
        self.angle += ang * dt

    def rotateRight(self, dt, ang=40):
        self.angle -= ang * dt

    def goForward(self, dt):
        if -680 <= self.x <= 680 and -680 <= self.y <= 680:
            rad = math.radians(self.angle-90)
            self.x += math.cos(rad) * self.speed * dt
            self.y += math.sin(rad) * self.speed * dt
            if self.x > 680: self.x = 680
            if self.x < -680: self.x = -680
            if self.y > 680: self.y = 680
            if self.y < -680: self.y = -680

    def goBackward(self, dt):
        if -680 <= self.x <= 680 and -680 <= self.y <= 680:
            rad = math.radians(self.angle-90)
            self.x -= math.cos(rad) * self.speed * dt
            self.y -= math.sin(rad) * self.speed * dt
            if self.x > 680: self.x = 680
            if self.x < -680: self.x = -680
            if self.y > 680: self.y = 680
            if self.y < -680: self.y = -680

player = Player()

def drawPlayer(p):
    global game_state
    glPushMatrix()
    if game_state['over']: glRotatef(90, 0, 1, 0)
    glTranslatef(p.x, p.y, p.z)
    glRotatef(p.angle, 0, 0, 1)

    # legs
    glPushMatrix()

    glColor3f(0,0,1)
    glRotatef(0, 0,0,1)
    glTranslatef(-14, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 12, 40, 5, 5)# parameters are: quadric, base radius, top radius, height, slices, stacks

    glTranslatef(28, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 12, 40, 5, 5)

    glPopMatrix()

    # body
    glPushMatrix()

    glColor3f(0.2,0.3,0.2)
    glTranslatef(0, 0, 70)
    glScalef(1.65, 0.75, 2)
    glutSolidCube(30)

    glPopMatrix()

    # hands
    glPushMatrix()

    glColor3f(1,.86,.68)
    glTranslatef(-15, -10, 92)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 7, 6, 50, 10, 4)
    
    glPopMatrix()

    glPushMatrix()

    glTranslatef(15, -10, 92)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 7, 6, 50, 10, 4)

    glPopMatrix()

    # gun
    glPushMatrix()

    glColor3f(.41,.41,.41)
    glTranslatef(0, -10, 90)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 8, 5, 60, 10, 4)

    glPopMatrix()

    # head
    glPushMatrix()

    glColor3f(0,0,0)
    glTranslatef(0, 0, 120)
    gluSphere(gluNewQuadric(), 20, 10, 10)  # parameters are: quadric, radius, slices, stacks

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

    grid()
    drawPlayer(player)

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