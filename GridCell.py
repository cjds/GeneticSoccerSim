import numpy as np
class  GridCell(object):
    '''
    classdocs

    This is the GridCell that is used in the algorithms.

    methods

        getCenterPoint() returns the center point of the GridCell
        getIfPointIsInCell(array[2]) returns true or false if point is in the cell or not
    '''

    def __init__(self,uid=0, top=0,left=0,size=0):
        self.uid=uid
    	self.top=[top,left,-150]
        self.bottom=[top+size,left+size,-150]
    	pass


    def setPoints(self,uid=0,top=[],bottom=[],gridCell=None):
        self.uid=uid
        self.top=top
        self.bottom=bottom
        if not gridCell ==None:
            self.magicTop=gridCell.top
            self.magicBottom=gridCell.bottom


    def getCenterPoint(self):
        return list((np.array(self.top) + np.array(self.bottom))/2)


    def getIfPointIsInCell(self,point):
        point_in_cell=True
        if not (point[0]>=self.top[0] and point[0]<=self.bottom[0]):
            point_in_cell=False
        if not (point[1]>=self.top[1] and point[1]<=self.bottom[1]):
            point_in_cell=False
        return point_in_cell

    def getIfPointIsInCellNoisy(self,point,noiseSize):
        point_in_cell=True
        if not (point[0]>=self.top[0]-noiseSize and point[0]<=self.bottom[0]+noiseSize):
            point_in_cell=False
        if not (point[1]>=self.top[1]-noiseSize and point[1]<=self.bottom[1]+noiseSize):
            point_in_cell=False
        return point_in_cell


