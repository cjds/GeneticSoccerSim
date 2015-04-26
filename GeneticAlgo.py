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
from NavUtils import getObstacleAvoidance, getTeamNearestAvoidance, getRestrictionField, distBetween
class  GeneticAlgo(object):
    '''
    classdocs

    The genetic algorithm works as follows

    The algorithm will play multiple games and try to decide what to do if it is in certain conditions

    The condition will be based on the following tuple (teamAreas[], enemyAreas[], ballPosition,goalPosition)

    The grid will be split into a 4x4 grid which each grid cell defining an area

    The basic steps that the algorithm can take at any point will be as follows (these will form the base genes)
        1. Kick ball to team Mate 
        2. Kick ball ahead of self slightly (i.e. dribble)
        3. Run to other sector (randomly determined)
        4. Kick ball toward goal

    The genome of the algorithm will be encoded in the following way
        At each possible combination of the Tuple there will be a random gene which will define how the agent acts in that situation

    Fitness Function 
        The fitness function will be the feedback the bot gets on every move whether his move was correct or not.
        The players will be given a rating based on 
            1. How many passes were made successfully
            2. How long they kept the ball
            3. How many shots they made scored
            4. How m
            5. How many goal were scored against them

    

    Bias. 
        1 Agent will be biased to tend to run forwards (as an attacker) 
        1 Agent will be biased to tend to run backwards in situations (as an attacker)



    '''


    def __init__(self):      
        pass
    
    def takeStep(self, myTeam=[], enemyTeam=[], balls=[], obstacles=[],goals=[]):

        actions = []
        actions.append(Kick(balls[0], [1, 0, 0], 100))        
        deltaPos = np.array([1, 0, 0])
        # avoidMovement = getObstacleAvoidance(obstacles)
        avoidEnemyMovement = getTeamNearestAvoidance(enemyTeam)
        avoidTeamMovement = getTeamNearestAvoidance(myTeam)
        # fenceAvoidMovement = getRestrictionField(obstacles[1], 200)
        movement = balls[0].position
        goalDirection=goals[0]
        #Move the Y position to the center
        #goalDirection[0]=goalDirection[0]+50;
        deltaRot = getYPRFromVector(0.5* goalDirection + 1.5 * movement + 1.5 * avoidTeamMovement + 1.5 * avoidEnemyMovement)
        #deltaRot = getYPRFromVector(movement)
        return deltaPos, deltaRot, actions

    def baseActionPass(self, agentToPassTo):

    def baseActionShoot(self, goalObstacle):

    def baseActionDribble(self,direction):

    def baseActionRun(self, position):

    def updateFitness():

    def writeBrain(self,file):

    def readBrain(self,file):
        
class Gene(object):

    def __init__(self,teamAreas,enemyAreas,ballPosition,goalPosition):
        self.teamAreas=teamAreas
        self.enemyAreas=enemyAreas
        self.ballPosition=ballPosition
        self.goalPosition=goalPosition


        