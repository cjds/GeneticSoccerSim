'''
(c) 2015 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see the LICENSE.txt file included with this software for more information

authors: Arindam Bose (arindam.1993@gmail.com), Tucker Balch (trbalch@gmail.com)
'''

import numpy as np

class Obstacle(object):
    '''
    classdocs
    '''


    def __init__(self, position, radius):
        '''
        Constructor
        '''
        self.position = position
        self.radius = radius
        
    def draw(self, subplot):
        #draw a sphere of specified size at specified position
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)

        x = self.radius * np.outer(np.cos(u), np.sin(v)) + self.position[0]
        y = self.radius * np.outer(np.sin(u), np.sin(v)) + self.position[1]
        z = self.radius * np.outer(np.ones(np.size(u)), np.cos(v)) + self.position[2]
        subplot.plot_surface(x, y, z,  rstride=4, cstride=4, linewidth = 0, color='#ffff00')


# a goal obstacle is a special obstacle which is basically a goal
class GoalObstacle(object):

    def __init__(self,position,height,width):
        self.position=position
        self.height=height
        self.width=width

    def draw(self,subplot):
        u=np.linspace(self.position[1],self.position[1]+self.width,50)
        v=np.linspace(self.position[0],self.position[0]+1,50)
        z=np.linspace(self.position[2],self.position[2]+self.height,50)
        X, Y = np.meshgrid(u, z) 
        subplot.plot_wireframe(v, X, Y,  rstride=4, cstride=4,color='#ffff00')