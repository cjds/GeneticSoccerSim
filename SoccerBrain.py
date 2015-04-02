'''
(c) 2015 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see the LICENSE.txt file included with this software for more information

authors: Carl Saladnha (csladanha3@gatech.edu)
'''

from Agent import Agent
from Ball import Ball
from Obstacle import Obstacle
from LinearAlegebraUtils import getYPRFromVector
import numpy as np
from Action import Stun, Kick
from NavUtils import getObstacleAvoidance, getTeamNearestAvoidance, getRestrictionField
class  SoccerBrain(object):
    '''
    classdocs
    '''


    def __init__(self):      
        pass
    
    def takeStep(self, myTeam=[], enemyTeam=[], balls=[], obstacles=[],goals=[]):

        actions = []
        actions.append(Kick(balls[0], [1, 0, 0], 100))        
        deltaPos = np.array([1, 0, 0])
        # avoidMovement = getObstacleAvoidance(obstacles)
        # avoidEnemyMovement = getTeamNearestAvoidance(enemyTeam)
        # fenceAvoidMovement = getRestrictionField(obstacles[1], 200)
        movement = balls[0].position
        goalDirection=goals[0]
        goalDirection[0]=goalDirection[0]
        #Move the Y position to the center
        #goalDirection[0]=goalDirection[0]+50;
        deltaRot = getYPRFromVector(1.5* goalDirection + 1.5 * movement)
        #deltaRot = getYPRFromVector(movement)
        return deltaPos, deltaRot, actions
        

        