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
    	self.top=[top,top+left,0]
        self.bottom=[top+size,left+size,0]
    	pass


    def setPoints(self,uid=0,top=[],bottom=[]):
        self.uid=uid
        self.top=top
        self.bottom=bottom


    def getCenterPoint(self):
        return list(np.array(self.top) + np.array(self.bottom))


    def getIfPointIsInCell(self,point):
        point_in_cell=True
        if not (point[0]>self.top[0] and point[0]<self.bottom[0]):
            point_in_cell=False
        if not (point[1]>self.top[1] and point[0]<self.bottom[1]):
            point_in_cell=False
        return point_in_cell


