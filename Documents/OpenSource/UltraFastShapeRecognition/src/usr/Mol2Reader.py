'''
Created on Jul 2, 2010
Simple class to read in Mol2 file.
@author: ed
'''
import os, sys

class Atom():
    def __init__(self,index,atomType,xCoordinate,yCoordinate,zCoordinate,sybylAtomType):
        '''
        Simple atom class constructor to contain information on the atom index, type, coordinates and Sybyl atom type.
        '''
        self.index = index
        self.atomType = atomType
        self.x = xCoordinate
        self.y = yCoordinate
        self.z = zCoordinate
        self.sybylAtomType = sybylAtomType
    
    def getXCoordinate(self):
        '''
        Returns X coordinate.
        '''
        return self.x
    
    def getYCoordinate(self):
        '''
        Returns Y coordinate.
        '''
        return self.y
    
    def getZCoordinate(self):
        '''
        Returns Z coordinate.
        '''
        return self.z
    
class Molecule():
    def __init__(self):
        '''
        Defines a molecule.
        '''
        self.index = 0
        self.atoms = []
        self.totalAtoms = 0
        self.totalBonds = 0
        
    def addAtom(self, atom):
        '''
        Adds an atom to the molecule.
        '''
        self.atoms.append(atom)
    
    def getAtom(self, i):
        '''
        Returns atom at specified index.
        '''
        return self.atoms[i]
    
    def getAtoms(self):
        '''
        Returns all atoms.
        '''
        return self.atoms

class Mol2Reader():
    def __init__(self,fileName):
        '''
        Mol2 file reader.
        '''
        self.file = fileName
        self.molecules = []
    
    def readInMolecules(self):
        '''
        Reads in all molecules in a .mol2 file.
        '''
        mol2file = open(self.file,'r')
        fileData = mol2file.readlines()
        moleculeIndex = 0
        atomStartIndex = 0
        moleculeCounter = -1
        atomsInMolecule = 0
        counterToAtom = 0
        for i in range(len(fileData)):
            splitData = str(fileData[i]).split()
            if fileData[i][0:17] == "@<TRIPOS>MOLECULE":
                mol = Molecule()
                counterToAtom = 0
                self.molecules.append(mol)
                moleculeIndex = i
                moleculeCounter = moleculeCounter+1
                print "Molecule Number: "+str(moleculeCounter)
            counterToAtom = counterToAtom+1
            if counterToAtom == 3:
                mol.totalAtoms = splitData[0]
                mol.totalBonds = splitData[1]
            stopAtomAddition = 9+int(self.molecules[moleculeCounter].totalAtoms)   
            if (counterToAtom >=9) and (counterToAtom < stopAtomAddition):
                atom = Atom(int(splitData[0]),splitData[1],float(splitData[2]),float(splitData[3]),float(splitData[4]),splitData[5]) 
                self.molecules[moleculeCounter].addAtom(atom)
        return self.molecules               