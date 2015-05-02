'''
(c) 2015 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see the LICENSE.txt file included with this software for more information

authors: Carl Saladnha (csladanha3@gatech.edu)
'''

from Agent import Agent
from Ball import Ball
from Obstacle import Obstacle
from LinearAlegebraUtils import *
import numpy as np
from Action import Stun, Kick
from GridCell import GridCell
from NavUtils import getObstacleAvoidance, getTeamNearestAvoidance, getRestrictionField
from DatabaseAccess import DatabaseAccess, Gene, Individual
import random

class  GeneticAlgo(object):
    '''
    classdocs

    The genetic algorithm works as follows

    The algorithm will play multiple games and try to decide what to do if it is in certain states

    The state will be based on the following tuple (teamAreas[], enemyAreas[], ballPosition)

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
            1. How many shots they made scored
            2. How many goal were scored against them
            3. How long they stay in possession

    '''


    def __init__(self,individual_brain):      
        self.brain=individual_brain
        
    
    def takeStep(self, myTeam=[], enemyTeam=[], balls=[], obstacles=[],goals=[],gridCells=[],agent=-1):

		#distance to ball
		distance=np.sqrt(balls[0].position[0]*balls[0].position[0] + balls[0].position[1]*balls[0].position[1])
		if distance< 30:
			self.brain.inPossession(True)
		else:
			self.brain.inPossession(False)

		return self.chooseBaseAction(myTeam,enemyTeam,balls,obstacles,goals,gridCells,agent)




    def chooseBaseAction(self, myTeam=[], enemyTeam=[], balls=[], obstacles=[],goals=[],gridCells=[],agent=-1):
        team_area=[self.convertToGridCell(x,gridCells) for x in myTeam]
        enemy_area=[self.convertToGridCell(x,gridCells) for x in enemyTeam]
        ballPosition=self.convertToGridCell(balls[0],gridCells)

        #add some noise

    	moveType, extraInformation= self.brain.match_expression(team_area,enemy_area,ballPosition)
    	
    	if moveType == -1:
    		moveType=random.randint(0,3)
    		if moveType==0:
    			extraInformation=random.randint(0,3)
    		else:
    			extraInformation=random.randint(0,25)
    			if extraInformation>15:
    				extraInformation=-1
    		self.brain.randomMoveMade()

        if moveType == 0:
           return self.baseActionPass(extraInformation, myTeam, enemyTeam, balls, obstacles,goals,gridCells,agent)
        elif moveType == 1:
           return self.baseActionShoot(myTeam, enemyTeam, balls, obstacles,goals,gridCells,agent)
        elif moveType == 2:
           return self.baseActionDribble(extraInformation,myTeam, enemyTeam, balls, obstacles,goals,gridCells,agent)
        elif moveType == 3:	
           return self.baseActionRun(extraInformation,myTeam, enemyTeam, balls, obstacles,goals,gridCells,agent)



    ##This will take in numbres an return the appropriate grid cell to which it belongs
    def convertToGridCell(self,position,gridCells):
        for i in range(0,16):
			if gridCells[i].getIfPointIsInCell(position.position):
				return gridCells[i].uid
        #if you cannot find which cell it is check it noisily. Cause of the problems with building egocentric co-ordinates
        
        for noise in range(1,20):
        	
	        for i in range(0,16):
				#if noise ==1:
				#	print str(map(int,gridCells[i].top))+" "+str(map(int,gridCells[i].bottom))+" "+str(map(int,position.position))
				if gridCells[i].getIfPointIsInCellNoisy(position.position,noise):
					return gridCells[i].uid        
        #if all else fails return a random number
        #raw_input('Enter a file name: ')
        #print -1
        return random.randint(0,15)


    def baseActionPass(self, agentToPassTo, myTeam=[], enemyTeam=[], balls=[], obstacles=[],goals=[],gridCells=[],agent=-1):
		actions=[]
		angle=[0,0,0]
		deltaRot=[0,0,0]
		distance=0
		for agent in myTeam:
			if(agent.uid==agentToPassTo):
				angle= getYPRFromVector(normalize(agent.position))
				distance=distBetween(balls[0].position,agent.position)
		actions.append(Kick(balls[0],angle,distance/2))
		deltaPos = np.array([1, 0, 0])
		movement = normalize(balls[0].position)
		deltaPos =movement
		return deltaPos,deltaRot,actions

    def baseActionShoot(self, myTeam=[], enemyTeam=[], balls=[], obstacles=[],goals=[],gridCells=[],agent=-1):
		actions=[]
		deltaPos = np.array([1, 0, 0])
		deltaRot = [0,0,0]
		actions.append(Kick(balls[0],goals[0].position,100))
		if(distBetween(balls[0].position,[0,0,0]>20)):
			movement = normalize(balls[0].position)
		else:
			movement = normalize(goals[0].position)
		deltaPos=movement
		return deltaPos,deltaRot,actions

    def baseActionDribble(self,gridIndex,myTeam=[], enemyTeam=[], balls=[], obstacles=[],goals=[],gridCells=[],agent=0):
		actions=[]
		deltaPos=[1,0,0]
		deltaRot=[0,0,0]
		uid=agent.uid
		if(gridIndex==-1):
			actions.append(Kick(balls[0],np.array([1,0,0]),10))
			deltaPos = np.array([1, 0, 0])
			movement1 = balls[0].position
			movement2 = goals[0].position
			deltaPos = normalize( movement1 + movement2)
		else:
			for i in range(0,16):
				if(gridCells[i].uid==gridIndex):
					movement= normalize(gridCells[i].getCenterPoint())
			deltaPos=movement
			actions.append(Kick(balls[0],deltaRot,10))

		return deltaPos,deltaRot,actions

    def baseActionRun(self, gridIndex, myTeam=[], enemyTeam=[], balls=[], obstacles=[],goals=[],gridCells=[],agent=-1):
        # if position is -1 go toward the ball
		actions=[]
		deltaPos=[1,0,0]
		deltaRot=[0,0,0]
		if(gridIndex==-1):

			deltaPos = normalize(balls[0].position)
			#movement =normalize(balls[0].position)
			
			#deltaRot = getYPRFromVector(movement)
		else:
			for i in range(0,16):
				if(gridCells[i].uid==gridIndex):
					movement= normalize(gridCells[i].getCenterPoint())
				#print str(map(int,gridl.lCells[gridIndex].magicTop))+"  "+ str(map(int,gridCells[gridIndex].magicBottom))+" "+str(agent.isEastToWest)
			#deltaRot = getYPRFromVector(5*movement)-agent.rotation
			deltaPos = movement
			
		return deltaPos,deltaRot,actions

    def updateFitness():
    	pass

    def writeBrain(self):
    	pass

    def readBrain(self,file):
    	pass
        