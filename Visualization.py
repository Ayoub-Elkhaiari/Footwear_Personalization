from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *



class Visualizer:
    def __init__(self, shoe_model):
        self.shoe_model = shoe_model

    def render(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutCreateWindow("Virtual Try-On")
        glEnable(GL_DEPTH_TEST)

        def display():
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            # Render the shoe model
            self.shoe_model.draw()
            glutSwapBuffers()

        glutDisplayFunc(display)
        glutMainLoop()