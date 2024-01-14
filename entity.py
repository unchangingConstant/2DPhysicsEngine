#Will handle logic for handling sprites (circles for now) in my little simulation
from abc import ABC, abstractmethod
import colorGradient as CG
import numpy as np
import collisionHandler as ch

class EntityInterface(ABC):

    @abstractmethod

    def __init__():
        #Duh
        pass
    
    @abstractmethod

    def force():
        pass
    
    @abstractmethod

    def tick():
        pass

class Player(EntityInterface):

    RIGHT = np.array([1, 0])
    LEFT = np.array([-1, 0])
    DOWN = np.array([0, 1])
    UP = np.array([0, -1])

    def __init__(self, initPos, walkSpeed, dexterity, elasticity):

        self.position = np.array([initPos[0], initPos[1]])
        self.priorPosition = np.array([initPos[0], initPos[1]])
        self.velocity = np.array([0, 0])

        self.walkSpeed = walkSpeed
        self.dex = dexterity

        self.elasticity = elasticity
    
    def force(self, vector, magnitude):

        self.velocity = self.velocity + (ch.normalize(vector) * magnitude)

    def tick(self):
        
        self.priorPosition = self.position
        self.position = self.position + self.velocity

