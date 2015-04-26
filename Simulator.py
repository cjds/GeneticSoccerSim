'''
(c) 2015 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see the LICENSE.txt file included with this software for more information

authors: Arindam Bose (arindam.1993@gmail.com), Tucker Balch (trbalch@gmail.com)
'''


import numpy as np
import matplotlib.pyplot as plt
from numpy import *
from World import *
from Agent import Agent, RestrictedAgent
from Obstacle import *
from pylab import *
from Ball import Ball
from LinearAlegebraUtils import distBetween
from PreyBrain import PreyBrain
from PredatorBrain import PredatorBrain
from SoccerBrain import SoccerBrain
from Team import Team
from SimTime import SimTime
from StatsTracker import StatsTracker



#Called once for initialization
'''
Usage guidelines:
1. Define globals required for the simulation in the __init__ constructor, here we define a bunch of waypoints for the ball
2. Initialize the globals in the setup() method. 
'''

class Simulator(object):
    def __init__(self, world, simTime, fps, imageDirName):
        self.world = world
        self.simTime = simTime
        self.fps = fps
        self.imageDirName = imageDirName
        self.currWP = 0
        self.scoreTeam1=0
        self.scoreTeam2=0
        self.finalScore=5
        self.teamSize=4
        self.ballInitialPosition=array([0,0,-150])
        self.teamPosition= [array([-50,50,-150]),array([-50,-50,-150]),array([-100,100,-150]),array([-100,-100,-150]),array([50,50,-150]),array([50,-50,-150]),array([100,100,-150]),array([100,-100,-150])]
        #self.ballWPs = [array([50.0, -100.0, 0.0]), array([0.0, 100.0, -70.0]), array([50.0, 20.0, 100.0]),array([-30.0, 50.0, -100.0]), array([80.0, -50.0, 50.0]), array([80.0, -50.0, -50.0]), array([-65.0, 20.0, 50.0]), array([-50.0, 20.0, -60.0])]

    def setup(self):    
        #setup directory to save the images
        try:
            os.mkdir(self.imageDirName)
        except:
            print self.imageDirName + " subdirectory already exists. OK."

  
         #define teams which the agents can be a part of
        predator = Team("Predator", '#ff99ff',GoalObstacle([-150,-50,-150],50,100))
        prey = Team("Prey", '#ffcc99',GoalObstacle([150,-50,-150],50,100))
        #Defining a couple of agents 

        self.world.teams=[predator,prey]

        #initialize Team 1
        for i in range(0,self.teamSize):
            brain = SoccerBrain()
            agent = Agent(predator,  self.teamPosition[i], array([0,0,0]),brain, 5, 5, 5)
            self.world.addAgent(agent)

        #initialize Team 2
        for i in range(0, self.teamSize):
            brain = SoccerBrain()
            agent = Agent(prey, self.teamPosition[i+self.teamSize],array([0,0,0]), brain, 5, 5, 5)
            self.world.addAgent(agent)

        ball=Ball (self.ballInitialPosition)
        ball.isDynamic = True
        self.world.addBall(ball)
  
        #define a bunch of obstacles
        #ob1Pos = array([-50,-50,-50])
        #ob1 = Obstacle(ob1Pos, 30)
         
        #ob2Pos = array([80,-50,-50])
        #ob2 = Obstacle(ob2Pos, 20)

        # originRef = Obstacle(array([0.1, 0.1, 0.1]), 10)
         
        #add obstacles to the world
        # self.world.addObstacle(ob1)
        # self.world.addObstacle(originRef)
        
        
#called at a fixed 30fps always
    def fixedLoop(self):
        for agent in self.world.agents:
            agent.moveAgent(self.world)

        for ball in self.world.balls:  
            #BALL IS IN GOAL       
            if ball.position[0] <= -world.width +0.5 and ball.position[1]>-50 and ball.position[1]<50:
                #team 1 scored
                self.scoreTeam1=self.scoreTeam1+1
                #reset everything
                ball.resetBall(self.ballInitialPosition)
                for i in range(0, self.teamSize*2):
                    self.world.agents[i].position=self.teamPosition[i]
            if ball.position[0] >= world.width -0.5 and ball.position[1]>-50 and ball.position[1]<50:
                self.scoreTeam2=self.scoreTeam2+1
                ball.resetBall(self.ballInitialPosition)
                for i in range(0, self.teamSize*2):
                    self.world.agents[i].position=self.teamPosition[i]
            ball.updatePhysics(self.world)                

    
#Called at specifed fps
    def loop(self, ax):       
        self.world.draw(ax)
       
                
    def run(self):
        #Run setup once
        self.setup()
        
        #Setup loop
        timeStep = 1/double(30)
        frameProb = double(self.fps) / 30
        currTime = double(0)
        SimTime.fixedDeltaTime = timeStep
        SimTime.deltaTime = double(1/ self.fps)
        drawIndex = 0
        physicsIndex = 0
        while(currTime < self.simTime and self.scoreTeam1<5 and self.scoreTeam1<5 ):
            self.fixedLoop()
            SimTime.time = currTime
            currProb = double(drawIndex)/double(physicsIndex+1)
            if currProb < frameProb:
                self.drawFrame(drawIndex)  
                drawIndex+=1
            physicsIndex+=1
            currTime+=double(timeStep)

     
        print "Physics ran for "+str(physicsIndex)+" steps"
        print "Drawing ran for "+str(drawIndex)+" steps"
        print "Agents were stunned for"+str(StatsTracker.stunTimeDict)
            
    def drawFrame(self, loopIndex):
        fig = plt.figure(figsize=(16,12))
        ax = fig.add_subplot(111, projection='3d') 
        ax.view_init(elev = 30)
        ax.set_xlabel(self.world.teams[0].name +'  '+str(self.scoreTeam1) + ' - ' + str(self.scoreTeam2)+'  '+self.world.teams[1].name )
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")    
        fname = self.imageDirName + '/' + str(int(100000000+loopIndex)) + '.png' # name the file 
        self.loop(ax)
        plt.gca().set_ylim(ax.get_ylim()[::-1])
        savefig(fname, format='png', bbox_inches='tight')
        print 'Written Frame No.'+ str(loopIndex)+' to '+ fname
        plt.close()


#Simulation runs here
#set the size of the world
world = World(150, 150)
#specify which world to simulate, total simulation time, and frammerate for video
sim = Simulator(world, 200, 1, "images1")
#run the simulation
sim.run()

'''
To create a video using the image sequence, execute the following command in command line.
>ffmpeg -framerate 30 -i "1%08d.png" -r 30 outPut.mp4
                    ^                    ^
                Framerate mtached with simulator
Make sure to set your current working directory to /images and have ffmpeg in your path.
'''

    