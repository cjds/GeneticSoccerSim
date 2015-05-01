'''
(c) 2015 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see the LICENSE.txt file included with this software for more information

authors: Arindam Bose (arindam.1993@gmail.com), Tucker Balch (trbalch@gmail.com)

Genetic Algorithm Statistics

To get the output we need to track the stats of the genetic algorithm to maintain the population and judge the fitness

The statistics on which the fitness function is based that we will be judging will be
	1. Goal Difference
	2. Randomness (how many times the genetic algorithm makes a random choice)

Scoring nothing will lead to a very poor fitness

Statistics will be stored in the stats table in the database

'''

from numpy import *

class StatsTracker(object):
	stunTimeDict = dict()
