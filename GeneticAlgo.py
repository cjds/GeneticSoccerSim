'''
(c) 2015 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see the LICENSE.txt file included with this software for more information

authors: Carl Saladnha (csladanha3@gatech.edu)
'''

from Agent import Agent
from Ball import Ball
from Obstacle import Obstacle
from LinearAlegebraUtils import getYPRFromVector,distBetween
import numpy as np
from Action import Stun, Kick
from GridCell import GridCell
from NavUtils import getObstacleAvoidance, getTeamNearestAvoidance, getRestrictionField
class  GeneticAlgo(object):
    '''
    classdocs

    The genetic algorithm works as follows

    The algorithm will play multiple games and try to decide what to do if it is in certain conditions

    The condition will be based on the following tuple (teamAreas[], enemyAreas[], ballPosition,goalPosition)

    The grid will be split into a 4x4 grid which each grid cell defining an area
    
    Lets define some stuff 
    The grid is assumedd to be 160x160 (this is specified in Simulator.py)
    GridCell 
    # 		Top 	Left	Bottom 	Right 
    0		0		0		40		40
    1		0    	0		40		40
    2		0		0		40		40
    3		0		0		40		40
    4		40		40		80		80
    5		40		40		80		80
    6		40		40		80		80
    7		40		40		80		80
    8		80		80		120		120
    9		80		80		120		120
    10		80		80		120		120
    11		80		80		120		120
    12		120		120		160		160
    13		120		120		160		160
    14		120		120		160		160
    15		120		120		160		160


    The basic steps that the algorithm can take at any point will be as follows (these will form the base genes)
        1. Kick ball to team Mate 
        The method has to specify the team mate to which the ball will be passed to 
        
        2. Kick ball ahead of self slightly (i.e. dribble)
        This dribble action will dribble the ball toward the goal. The agent will move toward the goal and the ball avoiding 
        the enemie and kicking the ball 

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
            4. How many goal were scored against them

    Bias. 
        1 Agent will be biased to tend to run forwards (as an attacker) 
        1 Agent will be biased to tend to run backwards in situations (as an attacker)

    '''


    def __init__(self):      
        pass
    
    def takeStep(self, myTeam=[], enemyTeam=[], balls=[], obstacles=[],goals=[],gridCells=[],uid=-1):
		if(uid==0):
			return self.baseActionShoot(13,myTeam, enemyTeam, balls, obstacles,goals,gridCells,uid)
		else:
			return self.baseActionRun(0,myTeam, enemyTeam, balls, obstacles,goals,gridCells,uid)
        # actions = []
        # actions.append(Kick(balls[0], [1, 0, 0], 100))        
        # deltaPos = np.array([1, 0, 0])
        # # avoidMovement = getObstacleAvoidance(obstacles)
        # #avoidEnemyMovement = getTeamNearestAvoidance(enemyTeam)
        # avoidTeamMovement = getTeamNearestAvoidance(myTeam)
        # # fenceAvoidMovement = getRestrictionField(obstacles[1], 200)
        # movement = balls[0].position
        # goalDirection=goals[0]
        # #Move the Y position to the center
        # #goalDirection[0]=goalDirection[0]+50;
        # deltaRot = getYPRFromVector(0.5* goalDirection + 1.5 * movement + 1.5 * avoidTeamMovement + 1.5 * avoidEnemyMovement)
        # #deltaRot = getYPRFromVector(movement)
        # return deltaPos, deltaRot, actions,ui

    def chooseBaseAction(self):
    	pass

    def baseActionPass(self, agentToPassTo, myTeam=[], enemyTeam=[], balls=[], obstacles=[],goals=[],gridCells=[],uid=-1):
		actions=[]
		angle=[0,0,0]
		distance=0
		for agent in myTeam:
			if(agent.uid==agentToPassTo):
				angle= getYPRFromVector(agent.position)
				distance=distBetween(balls[0].position,agent.position)
		actions.append(Kick(balls[0],angle,distance/2))
		deltaPos = np.array([1, 0, 0])
		movement = balls[0].position
		deltaRot = getYPRFromVector(movement)
		return deltaPos,deltaRot,actions



    def baseActionShoot(self, goalObstacle, myTeam=[], enemyTeam=[], balls=[], obstacles=[],goals=[],gridCells=[],uid=-1):
		actions=[]
		deltaPos = np.array([1, 0, 0])
		actions.append(Kick(balls[0],-goals[0].position,100))
		if(distBetween(balls[0].position,[0,0,0]>5)):
			movement = balls[0].position
		else:
			movement = goals[0].position
		deltaRot = getYPRFromVector(movement)
		return deltaPos,deltaRot,actions


    def baseActionDribble(self,direction,position,myTeam=[], enemyTeam=[], balls=[], obstacles=[],goals=[]):
		actions=[]
		actions.append(Kick(balls[0],np.array([1,0,0]),10))
		deltaPos = np.array([1, 0, 0])
		movement1 = balls[0].position
		movement2 = goals[0].position
		deltaRot = getYPRFromVector(1.5* movement1 + 1.5* movement2)
		return deltaPos,deltaRot,actions

    def baseActionRun(self, position, myTeam=[], enemyTeam=[], balls=[], obstacles=[],goals=[],gridCells=[],uid=-1):
        # if position is -1 go toward the ball
		actions=[]
		deltaPos=[1,0,0]
		deltaRot=[0,0,0]
		if(position==-1):
			deltaPos = np.array([1, 0, 0])
			movement = balls[0].position
			deltaRot = getYPRFromVector(movement)
		else:
			movement= gridCells[position].getCenterPoint()
			deltaRot = getYPRFromVector(movement)

		return deltaPos,deltaRot,actions

    def updateFitness():
    	pass

    def writeBrain(self,file):
    	pass

    def readBrain(self,file):
    	pass
        
class Gene(object):

    def __init__(self,teamAreas,enemyAreas,ballPosition,goalPosition):
        self.teamAreas=teamAreas
        self.enemyAreas=enemyAreas
        self.ballPosition=ballPosition
        self.goalPosition=goalPosition


        