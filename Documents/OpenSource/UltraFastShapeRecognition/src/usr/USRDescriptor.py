'''
Created on Jul 2, 2010
Calculates Ultrafast shape descriptors for proteins.
@author: ed
'''
import os, sys, math, operator
from Mol2Reader import *

class Point():
    def __init__(self,x=0,y=0,z=0):
        '''
        Represents a three dimensional point in space.
        '''
        self.xCoordinate = x
        self.yCoordinate = y
        self.zCoordinate = z

class AtomIndexAndDistance():
    def __init__(self,index,distance):
        '''
        Simple object to represent atom id and Euclidean distance
        (glorified dictionary).
        '''
        self.index = index
        self.distance = distance
    
class USR():
    def __init__(self):
        '''
        USR descriptor constructor.
        '''
        pass
    def CalculateCentroid(self,aMolecule):
        '''
        Calculates the centroid of the molecule.
        '''
        centroid = Point()
        summedX = 0.0
        summedY = 0.0
        summedZ = 0.0
        atomsInMolecule = len(aMolecule.getAtoms())
        for i in range(len(aMolecule.getAtoms())):
            summedX = summedX+float(aMolecule.getAtom(i).getXCoordinate())
            summedY = summedY+float(aMolecule.getAtom(i).getYCoordinate())
            summedZ = summedZ+float(aMolecule.getAtom(i).getZCoordinate()) 
           
        if atomsInMolecule == 0 or summedX == 0:
            centroid.xCoordinate = 0
        if atomsInMolecule == 0 or  summedY == 0:
            centroid.yCoordinate = 0
        if atomsInMolecule == 0 or summedZ == 0:
            centroid.zCoordinate = 0
        else:
            centroid.xCoordinate = summedX/atomsInMolecule
            centroid.yCoordinate = summedY/atomsInMolecule
            centroid.zCoordinate = summedZ/atomsInMolecule
        return centroid

    def ClosestAndFurthestAtomToCentroid(self,aMolecule):
        '''
        Returns the index of the atoms closest and furthest from the centroid atom.
        '''
        centroid = self.CalculateCentroid(aMolecule)
        atomIndexWithDistance=[]
        closestAndFurthestAtom=[]
        for i in range(len(aMolecule.getAtoms())):
            dist = self.EuclideanDistanceMeasure(aMolecule,centroid,i)
            result = AtomIndexAndDistance(i,dist)
            atomIndexWithDistance.append(result)
        atomIndexWithDistance.sort(key = operator.attrgetter('distance'))
        closestAndFurthestAtom.append(atomIndexWithDistance[0])
        closestAndFurthestAtom.append(atomIndexWithDistance[len(atomIndexWithDistance)-1])
        return closestAndFurthestAtom

    def FurthestAtomFromFurthestAtom(self,aMolecule,furthestAtom):
        '''
        Returns atom furthest from furthest atom.
        '''
        atomIndexWithDistance=[]
        furthestAtomIndex = furthestAtom.index
        x = float(aMolecule.getAtom(furthestAtomIndex).getXCoordinate())
        y = float(aMolecule.getAtom(furthestAtomIndex).getYCoordinate())
        z = float(aMolecule.getAtom(furthestAtomIndex).getZCoordinate())
    
        def Distance():
            for i in range(len(aMolecule.getAtoms())):
                xvalue = math.pow(float(aMolecule.getAtom(i).getXCoordinate()) -x,2)
                yvalue = math.pow(float(aMolecule.getAtom(i).getYCoordinate())-y,2)
                zvalue = math.pow(float(aMolecule.getAtom(i).getZCoordinate())-z,2)
                distance = math.sqrt(xvalue+yvalue+zvalue)
                result = AtomIndexAndDistance(i,distance)
                atomIndexWithDistance.append(result)
            atomIndexWithDistance.sort(key = operator.attrgetter('distance'))
            return atomIndexWithDistance
        atomsWithDistance = Distance()
        furthestFromFurthestAtomIndex = atomsWithDistance[len(atomsWithDistance)-1].index
        return furthestFromFurthestAtomIndex

    def EuclideanDistanceMeasure(self,aMolecule,b,i):
        '''
        Calculates Euclidean distance between atoms.
        '''
        xvalue = math.pow((float(aMolecule.getAtom(i).getXCoordinate()))-float(b.xCoordinate),2)
        yvalue = math.pow((float(aMolecule.getAtom(i).getYCoordinate()))-float(b.yCoordinate),2)
        zvalue = math.pow((float(aMolecule.getAtom(i).getZCoordinate()))-float(b.zCoordinate),2)
        distance = math.sqrt((xvalue+yvalue+zvalue))
        return distance

    def MomentToCentroid(self,momentId,aMolecule,centroidPoint):
        '''
        Calculates the nth moment to the centroid.
        '''
        def MeanFromCentroid():
            distance = 0
            for i in range(len(aMolecule.getAtoms())):
                       xval = math.pow(math.fabs(float(aMolecule.getAtom(i).getXCoordinate())-centroidPoint.xCoordinate),2)
                       yval = math.pow(math.fabs(float(aMolecule.getAtom(i).getYCoordinate())-centroidPoint.yCoordinate),2)
                       zval = math.pow(math.fabs(float(aMolecule.getAtom(i).getZCoordinate())-centroidPoint.zCoordinate),2)
                       dist =  math.sqrt(xval+yval+zval)
                       distance = distance+dist
            mean = distance/len(aMolecule.getAtoms())
            return mean
        if momentId == 1:
            meanValue = MeanFromCentroid()
            return meanValue
    
        if momentId == 2:
            summedDistance = 0
            meanDistanceToCentroid = MeanFromCentroid()
            for i in  range(len(aMolecule.getAtoms())):
                xval = math.pow(math.fabs(float(aMolecule.getAtom(i).getXCoordinate())-centroidPoint.xCoordinate),2)
                yval = math.pow(math.fabs(float(aMolecule.getAtom(i).getYCoordinate())-centroidPoint.yCoordinate),2)
                zval = math.pow(math.fabs(float(aMolecule.getAtom(i).getZCoordinate())-centroidPoint.zCoordinate),2)
                dist =  math.sqrt(xval+yval+zval)
                summedDistance = summedDistance+math.pow((dist-meanDistanceToCentroid),2)
            variance = summedDistance/len(aMolecule.getAtoms())
            return variance
    
        if momentId == 3:
            summedDistance = 0
            numeratorSum =  0
            denominatorSum =  0
            meanDistanceToCentroid = MeanFromCentroid()
            for i in  range(len(aMolecule.getAtoms())):
                xval = math.pow(math.fabs(float(aMolecule.getAtom(i).getXCoordinate())-centroidPoint.xCoordinate),2)
                yval = math.pow(math.fabs(float(aMolecule.getAtom(i).getYCoordinate())-centroidPoint.yCoordinate),2)
                zval = math.pow(math.fabs(float(aMolecule.getAtom(i).getZCoordinate())-centroidPoint.zCoordinate),2)
                dist =  math.sqrt(xval+yval+zval)
                numeratorSum = numeratorSum+math.pow(math.fabs((dist-meanDistanceToCentroid)),3)
                denominatorSum = denominatorSum+math.pow(math.fabs((dist-meanDistanceToCentroid)),2)
            numerator = numeratorSum/len(aMolecule.getAtoms())
            denominator = math.pow(denominatorSum/len(aMolecule.getAtoms()),1.5)
            skewness = numerator/denominator
            return skewness

    def MomentToX(self,MomentId,aMolecule,atomIndexValue):
        '''
        Calculate moment from specified point.
        '''
        def MeanFromPoint():
            distance = 0
            for i in range(len(aMolecule.getAtoms())):
                xval = math.pow(math.fabs(float(aMolecule.getAtom(i).getXCoordinate())-float(aMolecule.getAtom(atomIndexValue).getXCoordinate())),2)
                yval = math.pow(math.fabs(float(aMolecule.getAtom(i).getYCoordinate())-float(aMolecule.getAtom(atomIndexValue).getYCoordinate())),2)
                zval = math.pow(math.fabs(float(aMolecule.getAtom(i).getZCoordinate())-float(aMolecule.getAtom(atomIndexValue).getZCoordinate())),2)
                dist =  math.sqrt(xval+yval+zval)
                distance = distance+dist
            mean = distance/len(aMolecule.getAtoms())
            return mean
        if MomentId == 1:
            meanValue = MeanFromPoint()
            return meanValue
    
        if MomentId == 2:
            summedDistance = 0
            meanDistance = MeanFromPoint()
            for i in  range(len(aMolecule.getAtoms())):
                xval = math.pow(math.fabs(float(aMolecule.getAtom(i).getXCoordinate())-float(aMolecule.getAtom(atomIndexValue).getXCoordinate())),2)
                yval = math.pow(math.fabs(float(aMolecule.getAtom(i).getYCoordinate())-float(aMolecule.getAtom(atomIndexValue).getYCoordinate())),2)
                zval = math.pow(math.fabs(float(aMolecule.getAtom(i).getZCoordinate())-float(aMolecule.getAtom(atomIndexValue).getZCoordinate())),2)
                dist =  math.sqrt(xval+yval+zval)
                summedDistance = summedDistance+math.pow((dist-meanDistance),2)
            variance = summedDistance/len(aMolecule.getAtoms())
            return variance

        if MomentId == 3:
            summedDistance = 0
            numeratorSum =  0
            denominatorSum =  0
            meanDistance = MeanFromPoint()
            for i in range(len(aMolecule.getAtoms())):
                xval = math.pow(math.fabs(float(aMolecule.getAtom(i).getXCoordinate())-float(aMolecule.getAtom(atomIndexValue).getXCoordinate())),2)
                yval = math.pow(math.fabs(float(aMolecule.getAtom(i).getYCoordinate())-float(aMolecule.getAtom(atomIndexValue).getYCoordinate())),2)
                zval = math.pow(math.fabs(float(aMolecule.getAtom(i).getZCoordinate())-float(aMolecule.getAtom(atomIndexValue).getZCoordinate())),2)
                dist =  math.sqrt(xval+yval+zval)
                numeratorSum = numeratorSum+math.pow(math.fabs((dist-meanDistance)),3)
                denominatorSum = denominatorSum+math.pow(math.fabs((dist-meanDistance)),2)
            numerator = numeratorSum/len(aMolecule.getAtoms())
            denominator = math.pow(denominatorSum/len(aMolecule.getAtoms()),1.5)
            skewness = numerator/denominator
            return skewness

def getUSRDescriptor(aMolecule):
    '''
    Calculates USR descriptor.
    '''
    usrDescriptor = []
    usr = USR()
    centroidPoint = usr.CalculateCentroid(aMolecule)
    euclideanDistance = usr.EuclideanDistanceMeasure(aMolecule,centroidPoint,0)
    v = usr.ClosestAndFurthestAtomToCentroid(aMolecule)
    ffaIndex = usr.FurthestAtomFromFurthestAtom(aMolecule,v[1])
    #From centroid
    meanFromCentroid = usr.MomentToCentroid(1,aMolecule,centroidPoint)
    varianceFromCentroid = usr.MomentToCentroid(2,aMolecule,centroidPoint)
    skewnessFromCentroid = usr.MomentToCentroid(3,aMolecule,centroidPoint)
    #From closest atom
    m1CA = usr.MomentToX(1,aMolecule,v[0].index)
    m2CA = usr.MomentToX(2,aMolecule,v[0].index)
    m3CA = usr.MomentToX(3,aMolecule,v[0].index)
    #FurthestAtom
    m1FA = usr.MomentToX(1,aMolecule,v[1].index)
    m2FA = usr.MomentToX(2,aMolecule,v[1].index)
    m3FA = usr.MomentToX(3,aMolecule,v[1].index)
    #Furthest to Furthest atom
    m1FFA = usr.MomentToX(1,aMolecule,ffaIndex)
    m2FFA = usr.MomentToX(2,aMolecule,ffaIndex)
    m3FFA = usr.MomentToX(3,aMolecule,ffaIndex)
    usrDescriptor.append(meanFromCentroid)
    usrDescriptor.append(varianceFromCentroid)
    usrDescriptor.append(skewnessFromCentroid)
    usrDescriptor.append(m1CA)
    usrDescriptor.append(m2CA)
    usrDescriptor.append(m3CA)
    usrDescriptor.append(m1FA)
    usrDescriptor.append(m2FA)
    usrDescriptor.append(m3FA)
    usrDescriptor.append(m1FFA)
    usrDescriptor.append(m2FFA)
    usrDescriptor.append(m3FFA)
    return usrDescriptor

def writeResultsToFile(outputFile,molecules):
    '''
    Writes USR descriptors to a file.
    '''
    outputFileResults = open(outputFile,'w')
    def formatDescriptor(descriptorValue):
        aDescriptor = str(descriptorValue).replace('[', '')
        formattedDescriptor = aDescriptor.replace(']','')
        return formattedDescriptor
    
    for i in range(len(molecules)):
        descriptor = getUSRDescriptor(molecules[i])
        descriptorProcessed = formatDescriptor(descriptor)
        outputFileResults.write(descriptorProcessed+"\n")
        
if __name__ == "__main__":
    mol2data = Mol2Reader(sys.argv[1])
    molecules = mol2data.readInMolecules()
    writeResultsToFile(sys.argv[2],molecules)
    