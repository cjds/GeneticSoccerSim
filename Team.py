'''
(c) 2015 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see the LICENSE.txt file included with this software for more information

authors: Arindam Bose (arindam.1993@gmail.com), Tucker Balch (trbalch@gmail.com)
'''


class Team(object):
    '''
    classdocs
    '''


    def __init__(self, name, color,goal):
        '''
        Constructor
        '''
        self.name = name
        self.color = color
        self.goal=goal
        self.fitness=0
        if goal.position[0]<0:
            self.isEastToWest=True;
        else:
            self.isEastToWest=False;

