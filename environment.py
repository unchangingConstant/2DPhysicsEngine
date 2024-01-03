#Handles all logic for the environment 
from abc import ABC, abstractmethod
import numpy as np

class Surface():

    def __init__(self, edge1, edge2, tag):
    
        self.edge1 = np.array([edge1[0], edge1[1]])
        self.edge2 = np.array([edge2[0], edge2[1]])

        self.tag = tag

