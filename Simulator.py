'''
Created on Jan 16, 2015

@author: Arindam
'''

import numpy as np
from numpy import *
from World import *
from Agent import Agent
from Obstacle import *
from pylab import *
import os
from Ball import Ball


#Called once for initialization
def setup():
    #setup directory to save the images
    global imageDirName;
    imageDirName = 'images'
    try:
        os.mkdir(imageDirName)
    except:
        print imageDirName + " subdirectory already exists. OK."
        
    #World Setup
    global simTime             #Simulation time
    simTime= 5        
    global fps                 #Frame rate(Frames per second)
    fps = 30  
    global world        
      
    worldWidth = 100           #Width of the World
    worldHeight = 100          #Height of the World
     
    world = World(worldWidth, worldHeight) #Initialize the world
    
    #Defining a couple of agents 
    ag1Pos = array([0, 0, 0])
    ag1Rot = array([0, 0, 0])
    agent1 = Agent("A", ag1Pos, ag1Rot, 10, 10)
    
    ag2Pos = array([0, 20, 0])
    ag2Rot = array([-30, 0, 120])
    agent2 = Agent("A", ag2Pos, ag2Rot, 10, 10)
    
    ag3Pos = array([70, 30, 50])
    ag3Rot = array([0, 0, 0])
    agent3 = Agent("B", ag3Pos, ag3Rot, 10, 10)
    
    ag4Pos = array([-80, 20, 60])
    ag4Rot = array([0, 0, 30])
    agent4 = Agent("B", ag4Pos, ag4Rot, 10, 10)
    
    #Add the agent to the world
    world.agents.append(agent1)
    world.agents.append(agent2)
    world.agents.append(agent3)
    world.agents.append(agent4)
    
    #define a bunch of obstacles
    ob1Pos = array([-50,-50,-50])
    ob1 = Obstacle(ob1Pos, 30)
    
    ob2Pos = array([80,-50,-50])
    ob2 = Obstacle(ob2Pos, 20)
    
    #add obstacles to the world
    world.obstacles.append(ob1);
    world.obstacles.append(ob2)
    
    #define a ball
    ball = Ball(array([100, -25, 30]))
    
    #add the ball to the world
    world.balls.append(ball)
    
#Called repeatedly to create the movie
def loop(loopIndex, imageDirName):
    world.draw(loopIndex, imageDirName)
    for agent in world.agents:
        agent.position+=agent.forward * 10 / fps #move em forward




#Simulation starts here
setup()
timeStep = double(0.0333333333333333)
currTime = double(0)
print timeStep
loopIndex = 0
while(currTime < simTime):
    loop(loopIndex, imageDirName)
    loopIndex+=1
    print currTime
    currTime+=double(timeStep)
    