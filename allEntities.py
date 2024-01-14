#This will store all the sprites I wanna use
from entity import *
from environment import *

david = Player((250, 200), .9)
floor = Surface((0, 400), (1000, 400), 'floor')
wall1 = Surface((500, 200), (500, 300), 'wall1')
wall2 = Surface((250, 200), (250, 300), 'wall2')

bound1 = Surface((0, 0), (500, 0), 'bound1')
bound2 = Surface((500, 0), (500, 500), 'bound2')
bound3 = Surface((500, 500), (0, 500), 'bound3')
bound4 = Surface((0, 500), (0, 0), 'bound4')

diagonalWall = Surface((250, 500), (500, 250), 'diagonalWall')