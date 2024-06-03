#Will handle logic for handling sprites (circles for now) in my little simulation
from abc import ABC, abstractmethod
import colorGradient as CG
import numpy as np
from math import ceil

def round2DVector(vector):

    entry1 = round(vector[0], 5)
    entry2 = round(vector[1], 5)
    return np.array([entry1, entry2])

class EntityInterface(ABC):

    @abstractmethod

    def __init__():
        #Duh
        pass

class Player(EntityInterface):

    RIGHT = np.array([1, 0])
    LEFT = np.array([-1, 0])
    DOWN = np.array([0, 1])
    UP = np.array([0, -1])

    def __init__(self, initPos, elasticity):

        self._position = np.array([initPos[0], initPos[1]])
        self._priorPosition = np.array([initPos[0], initPos[1]])
        self._velocity = np.array([0, 0])

        self.elasticity = elasticity
    
    #Moving methods
    def move(self, moveVector):
        self._priorPosition = self._position
        self._position = self._position + moveVector

    #Position methods
    def getPosition(self):
        return self._position
    
    def modPosition(self, modVector):
        self._position = self._position + round2DVector(modVector)

    def setPosition(self, newPos):
        self._position = round2DVector(newPos)
    
    #PriorPosition methods
    def getPriorPosition(self):
        return self._priorPosition

    def modPriorPosition(self, modVector):
        self._priorPosition = self._priorPosition + round2DVector(modVector)

    def setPriorPosition(self, newPriorPos):
        self._priorPosition = round2DVector(newPriorPos)

    #Velocity methods
    def getVelocity(self):
        return self._velocity
    
    def modVelocity(self, modVector):
        self._velocity = self._velocity + round2DVector(modVector)

    def setVelocity(self, newVel):
        self._velocity = round2DVector(newVel)

